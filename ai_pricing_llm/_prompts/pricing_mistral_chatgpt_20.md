
# pricing_mistral_chatgpt_20.md

## prompt_1
As an advanced programmer in Python, browse a directory named "output/", list all the files ending with ".xlsx". Each of the files contained multiple sheets, can you merge in single file maned %date_created_output_all where date_created is equal to creation_date = datetime.now().strftime("%Y-%m-%d"), preserve the names for all the sheets.


## ChatGPT_1


Certainly! You can achieve this task using the `pandas` library in Python. Below is a Python script that accomplishes what you described:

```python
import os
import pandas as pd
from datetime import datetime

# Get current date in the required format
date_created = datetime.now().strftime("%Y-%m-%d")
output_folder = "output/"
output_all_filename = f"{date_created}_output_all.xlsx"

# Find all .xlsx files in the output folder
xlsx_files = [file for file in os.listdir(output_folder) if file.endswith(".xlsx")]

# Check if there are any .xlsx files in the folder
if not xlsx_files:
    print("No .xlsx files found in the directory.")
else:
    # Create an empty DataFrame to store combined data
    combined_data = pd.DataFrame()

    # Iterate through each .xlsx file
    for file in xlsx_files:
        file_path = os.path.join(output_folder, file)
        # Read all sheets from the Excel file
        sheets = pd.read_excel(file_path, sheet_name=None)
        
        # Iterate through each sheet
        for sheet_name, df in sheets.items():
            # Add a column with the original filename for reference
            df['Original_Filename'] = file
            # Append the data from the current sheet to the combined DataFrame
            combined_data = combined_data.append(df, ignore_index=True)

    # Write the combined data to a new Excel file
    output_path = os.path.join(output_folder, output_all_filename)
    combined_data.to_excel(output_path, index=False)
    print(f"Combined data saved to {output_all_filename} in the output folder.")
```

Make sure to place this script in the same directory as your "output/" folder or provide the full path to the folder. This script will merge all sheets from all `.xlsx` files in the "output/" folder into a single Excel file named `%date_created_output_all.xlsx`, where `%date_created` is the current date in the format "YYYY-MM-DD". Each sheet will preserve its original name, and a new column called "Original_Filename" will be added to identify the source file.