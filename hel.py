import pygame
import random
import numpy as np
import sys
from pygame.locals import *

# Initialize pygame
pygame.init()

# Constants
GRID_SIZE = 7
TILE_SIZE = 80
WINDOW_SIZE = GRID_SIZE * TILE_SIZE
FPS = 5  # Animation speed

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (100, 200, 100)  # Clean tile
RED = (255, 100, 100)    # Dirty tile
BLUE = (100, 100, 255)   # Vacuum cleaner
YELLOW = (200, 200, 100) # Visited tile
GRAY = (200, 200, 200)   # Status bar
PURPLE = (200, 100, 200) # Target tile

class SystematicVacuumAgent:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.grid = np.random.randint(0, 2, (GRID_SIZE, GRID_SIZE))  # 0=dirty, 1=clean
        self.position = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
        self.cleaned = 0
        self.total_steps = 0
        self.cleaning_steps = 0
        self.visited = set([self.position])
        self.unvisited = set((i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE)) - self.visited
        self.dirty_tiles = set((i,j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if self.grid[i][j] == 0)
        self.last_dirty_position = None
        self.font = pygame.font.SysFont('Arial', 20)
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 120))  # Increased height for more stats
        pygame.display.set_caption('Systematic Vacuum Agent')
        self.clock = pygame.time.Clock()
        
        # Track completion metrics
        self.steps_to_clean_all = None
        self.steps_to_visit_all = None
        self.all_cleaned = False
        self.all_visited = False
        
    def get_adjacent_tiles(self, position=None):
        x, y = position if position else self.position
        adjacent = []
        
        # Check 4 adjacent tiles (up, down, left, right)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                adjacent.append((nx, ny))
        
        return adjacent
    
    def find_closest_unvisited(self):
        if not self.unvisited:
            return None
            
        current_x, current_y = self.position
        return min(self.unvisited, key=lambda pos: abs(pos[0]-current_x) + abs(pos[1]-current_y))
    
    def plan_path_to_target(self, target):
        """Simple pathfinding using BFS to find shortest path"""
        if target == self.position:
            return []
            
        queue = [(self.position, [])]
        visited = set([self.position])
        
        while queue:
            (x, y), path = queue.pop(0)
            
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                    if (nx, ny) == target:
                        return path + [(nx, ny)]
                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append(((nx, ny), path + [(nx, ny)]))
        return None
    
    def execute_step(self):
        if not self.dirty_tiles and not self.unvisited:
            return False  # All done
            
        # First check current position
        x, y = self.position
        if self.grid[x][y] == 0:
            self.grid[x][y] = 1
            self.cleaned += 1
            self.dirty_tiles.remove((x, y))
            self.last_dirty_position = (x, y)
            self.cleaning_steps = self.total_steps
            
            # Check if all tiles are now clean
            if not self.dirty_tiles and not self.all_cleaned:
                self.steps_to_clean_all = self.total_steps + 1  # +1 because we count this step
                self.all_cleaned = True
            
            return True
            
        # Check adjacent dirty tiles
        adjacent = self.get_adjacent_tiles()
        dirty_adjacent = [pos for pos in adjacent if pos in self.dirty_tiles]
        
        if dirty_adjacent:
            next_pos = random.choice(dirty_adjacent)
            self.position = next_pos
            self.total_steps += 1
            
            if next_pos not in self.visited:
                self.visited.add(next_pos)
                self.unvisited.discard(next_pos)
                
                # Check if all tiles are now visited
                if not self.unvisited and not self.all_visited:
                    self.steps_to_visit_all = self.total_steps
                    self.all_visited = True
            
            return True
            
        # No adjacent dirty, find closest unvisited tile
        target = self.find_closest_unvisited()
        if target:
            path = self.plan_path_to_target(target)
            if path and len(path) > 0:
                next_pos = path[0]
                self.position = next_pos
                self.total_steps += 1
                
                if next_pos not in self.visited:
                    self.visited.add(next_pos)
                    self.unvisited.discard(next_pos)
                    
                    # Check if all tiles are now visited
                    if not self.unvisited and not self.all_visited:
                        self.steps_to_visit_all = self.total_steps
                        self.all_visited = True
                
                return True
                
        # If no unvisited left but still dirty tiles
        if self.dirty_tiles:
            target = next(iter(self.dirty_tiles))  # Get any dirty tile
            path = self.plan_path_to_target(target)
            if path and len(path) > 0:
                next_pos = path[0]
                self.position = next_pos
                self.total_steps += 1
                return True
                
        return False
    
    def draw_grid(self):
        self.screen.fill(WHITE)
        
        # Draw grid tiles
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                rect = pygame.Rect(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                
                if (i, j) == self.position:
                    color = BLUE
                elif self.grid[i][j] == 1:
                    color = GREEN if (i, j) in self.visited else WHITE
                else:
                    color = RED if (i, j) not in self.visited else YELLOW
                
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, BLACK, rect, 1)
        
        # Draw status
        status_rect = pygame.Rect(0, WINDOW_SIZE, WINDOW_SIZE, 100)
        pygame.draw.rect(self.screen, GRAY, status_rect)
        
        stats = [
            f"Total Steps: {self.total_steps}",
            f"Cleaned: {self.cleaned}/{len(self.dirty_tiles) + self.cleaned}",
            f"Visited: {len(self.visited)}/{GRID_SIZE*GRID_SIZE}",
        ]
        
        # Add completion metrics when available
        if self.steps_to_clean_all is not None:
            stats.append(f"Steps to clean all: {self.steps_to_clean_all}")
        if self.steps_to_visit_all is not None:
            stats.append(f"Steps to visit all: {self.steps_to_visit_all}")
        
        if not self.dirty_tiles and not self.unvisited:
            stats.append(f"Final Position: {self.position}")
            stats.append(f"Steps after last clean: {self.total_steps - self.cleaning_steps}")
        
        for i, stat in enumerate(stats):
            text = self.font.render(stat, True, BLACK)
            self.screen.blit(text, (10, WINDOW_SIZE + 10 + i * 20))
        
        pygame.display.flip()
    
    def run(self):
        running = True
        paused = False
        
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        paused = not paused
                    elif event.key == K_r:
                        self.reset()
            
            if not paused and (self.dirty_tiles or self.unvisited):
                self.execute_step()
            
            self.draw_grid()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    agent = SystematicVacuumAgent()
    agent.run()