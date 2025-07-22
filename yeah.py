import pandas as pd

# Load Excel files
df1 = pd.read_excel('RatecardUP.xlsx')
df2 = pd.read_excel('Remaining cities for upload rate.xlsx')

# Find rows in df1 not in df2
diff1 = pd.concat([df1, df2, df2]).drop_duplicates(keep=False)

# Find rows in df2 not in df1
diff2 = pd.concat([df2, df1, df1]).drop_duplicates(keep=False)

# Optionally combine both differences
differences = pd.concat([diff1, diff2]).drop_duplicates()

# Output results
print("Rows in file1.xlsx but not in file2.xlsx:")
print(diff1)

print("\nRows in file2.xlsx but not in file1.xlsx:")
print(diff2)

# Save differences to Excel
differences.to_excel('differences.xlsx', index=False)
print("\nDifferences saved to differences.xlsx")
