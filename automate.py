import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import time
import os
from datetime import datetime
import logging
from dotenv import load_dotenv

# Load credentials from .env file
load_dotenv()
USERNAME = os.getenv("EXPOPRESS_USERNAME")
PASSWORD = os.getenv("EXPOPRESS_PASSWORD")

# Configuration
BASE_URL = "https://parcel.expoexpressnp.com"
LOGIN_URL = f"{BASE_URL}/"
FORM_URL =  f"{BASE_URL}/AdminDashboard/Neighbour/Create"
EXCEL_DATA_PATH = "Book1.xlsx"
EDGE_DRIVER_PATH = "C:\\Users\\Lenovo\\Downloads\\edgedriver_win64\\msedgedriver.exe"
OUTPUT_LOG = "submission_results.xlsx"
SCREENSHOT_DIR = "screenshots"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('submission.log'),
        logging.StreamHandler()
    ]
)

def setup_driver():
    """Configure and return Edge WebDriver"""
    edge_options = Options()
    edge_options.add_argument("--start-maximized")
    edge_options.add_argument("--disable-notifications")
    edge_options.add_argument("--disable-blink-features=AutomationControlled")
    
    service = Service(EDGE_DRIVER_PATH)
    driver = webdriver.Edge(service=service, options=edge_options)
    driver.implicitly_wait(5)
    return driver

def take_screenshot(driver, name):
    """Take screenshot and save to screenshots directory"""
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{SCREENSHOT_DIR}/{name}_{timestamp}.png"
    driver.save_screenshot(filename)
    return filename

def login(driver, max_attempts=3):
    """Handle login with retry logic"""
    for attempt in range(1, max_attempts + 1):
        try:
            driver.get(LOGIN_URL)
            
            # Wait for login elements
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "UserMail")))
            
            # Fill credentials
            driver.find_element(By.ID, "UserMail").send_keys(USERNAME)
            driver.find_element(By.ID, "UserPass").send_keys(PASSWORD)
            
            # Click login
            driver.find_element(By.ID, "LoginBtn").click()
            
            # Verify login success
            WebDriverWait(driver, 15).until(
                EC.url_contains("/Dashboard") or 
                EC.presence_of_element_located((By.CLASS_NAME, "dashboard")))
            logging.info("Login successful")
            return True
            
        except Exception as e:
            logging.warning(f"Login attempt {attempt} failed: {str(e)}")
            take_screenshot(driver, f"login_fail_attempt_{attempt}")
            if attempt < max_attempts:
                time.sleep(3)
                continue
            logging.error("Max login attempts reached")
            return False

def submit_neighbour_form(driver, record, attempt=1, max_attempts=3):
    """Submit neighborhood form with comprehensive error handling"""
    try:
        # Navigate to form
        driver.get(FORM_URL)
        
        # Wait for form elements
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "City")))
        
        # Select City
        city_select = Select(driver.find_element(By.ID, "City"))
        try:
            city_select.select_by_visible_text(record['City'])
        except:
            for option in city_select.options:
                if record['City'].lower() in option.text.lower():
                    option.click()
                    break
            else:
                raise ValueError(f"City '{record['City']}' not found")
        
        # Enter Neighbourhood
        neighbour_field = driver.find_element(By.ID, "Neighbour")
        neighbour_field.clear()
        neighbour_field.send_keys(record['Neighbourhood'])
        
        # Enter Address
        address_field = driver.find_element(By.ID, "search-input")
        address_field.clear()
        
        # Try different address formats
        address_formats = [
            f"{record['Neighbourhood']}, {record['City']}, Nepal",
            f"{record['Neighbourhood']}, {record['City']}",
            record['Neighbourhood']
        ]
        
        for addr_format in address_formats:
            address_field.send_keys(addr_format)
            time.sleep(2)
            try:
                driver.find_element(By.CSS_SELECTOR, ".pac-item").click()
                break
            except:
                address_field.clear()
                continue
        
        # Submit form
        submit_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btnSave")))
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", submit_button)
        
        # Verify submission
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-success")))
            return True
        except:
            # Check for error messages
            try:
                error_msg = driver.find_element(By.CSS_SELECTOR, ".alert-danger").text
                raise ValueError(f"Server error: {error_msg}")
            except:
                raise ValueError("No confirmation message received")
                
    except Exception as e:
        if attempt < max_attempts:
            logging.warning(f"Attempt {attempt} failed for {record['City']}. Retrying...")
            time.sleep(3)
            return submit_neighbour_form(driver, record, attempt+1, max_attempts)
        else:
            screenshot_path = take_screenshot(driver, f"error_{record['City']}")
            logging.error(f"Final attempt failed for {record['City']}: {str(e)}")
            logging.info(f"Screenshot saved to {screenshot_path}")
            return str(e)

def main():
    """Main execution flow"""
    driver = None
    try:
        # Initialize
        driver = setup_driver()
        
        # Login first
        if not login(driver):
            raise RuntimeError("Login failed. Check credentials and try again.")
        
        # Load data
        df = pd.read_excel(EXCEL_DATA_PATH)
        
        # Prepare results
        df['Submission_Status'] = "Pending"
        df['Error_Details'] = ""
        df['Attempts'] = 0
        df['Timestamp'] = ""
        
        # Process records
        for idx, record in df.iterrows():
            logging.info(f"\nProcessing {idx+1}/{len(df)}: {record['City']} - {record['Neighbourhood']}")
            
            start_time = datetime.now()
            result = submit_neighbour_form(driver, record)
            end_time = datetime.now()
            
            # Record results
            df.at[idx, 'Timestamp'] = start_time.strftime("%Y-%m-%d %H:%M:%S")
            df.at[idx, 'Attempts'] = 3 if result is True else (1 if isinstance(result, str) else 0)
            
            if result is True:
                df.at[idx, 'Submission_Status'] = "Success"
            else:
                df.at[idx, 'Submission_Status'] = "Failed"
                df.at[idx, 'Error_Details'] = result
            
            # Periodic save
            if (idx + 1) % 5 == 0:
                df.to_excel(OUTPUT_LOG, index=False)
                logging.info("Progress saved to output file")
            
            time.sleep(2)  # Polite delay
        
    except Exception as e:
        logging.critical(f"Fatal error: {str(e)}")
        if driver:
            take_screenshot(driver, "fatal_error")
    finally:
        # Final save and cleanup
        if 'df' in locals():
            df.to_excel(OUTPUT_LOG, index=False)
            logging.info("\nProcessing complete. Final results saved.")
            
            # Generate summary
            success = df[df['Submission_Status'] == 'Success']
            failed = df[df['Submission_Status'] == 'Failed']
            
            logging.info(f"\nSummary Statistics:")
            logging.info(f"Total records: {len(df)}")
            logging.info(f"Successfully submitted: {len(success)} ({len(success)/len(df)*100:.1f}%)")
            logging.info(f"Failed submissions: {len(failed)}")
            
            if not failed.empty:
                failed.to_excel("failed_submissions.xlsx", index=False)
                logging.info("Failed records saved to failed_submissions.xlsx")
        
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()