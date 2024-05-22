
# pricing_mistral_chatgpt_1.md


## prompt

As an advanced programmer in Excel, create an Excel spreadsheet that allows you to make a LOW estimation and a HIGH estimation for the cost of using the following models: "mistral-small, mistral-medium, mistral-large". Here is the precises variables, values and instructions.

1. The models must be available in dropdown named "model_name".

2. The following variables must be configurable via a drop-down menu:
nb_words_item = Number of words per article
multiplier_low = Coef LOW number of tokens per article
multiplier_high = Coef HIGH number of tokens per article
price_input = Price of the input (input)
price_output = Price of output
volume_items = Volume or Number of contents


3. The values are as follows:
Number of words per content = 500, 1000, 1500, 2000
BAS coef number of tokens per item = 1.33
Coef HIGH number of tokens per item = 1.5
Input price = €1.85 per 1 Million tokens
Output price = €5.55 per 1 Million tokens
Volume or Number of contents = 1,000, 50,000, 100,000...



## ChatGPT
To create this Excel spreadsheet with the requested configuration, follow these steps:

### Step 1: Create the Dropdown for "model_name"
1. Open a new Excel spreadsheet.
2. Select a cell where you want the "model_name" dropdown (e.g., cell `A1`).
3. Go to the "Data" tab and select "Data Validation."
4. In the "Data Validation" dialog, select "List" in the "Allow" dropdown.
5. In the "Source" field, enter `mistral-small,mistral-medium,mistral-large`.
6. Click "OK."

### Step 2: Create Dropdowns for Configurable Variables
- For each variable, create a dropdown with the given values.

1. **Number of words per content**
   - In cell `A3`, enter "Words per content."
   - In cell `B3`, create a dropdown with the values: `500, 1000, 1500, 2000`.

2. **BAS coef number of tokens per item**
   - In cell `A4`, enter "Multiplier (Low)."
   - In cell `B4`, create a dropdown with the value `1.33`.

3. **Coef HIGH number of tokens per item**
   - In cell `A5`, enter "Multiplier (High)."
   - In cell `B5`, create a dropdown with the value `1.5`.

4. **Input price**
   - In cell `A6`, enter "Input price (per million tokens)."
   - In cell `B6`, enter `1.85` (as a default value).

5. **Output price**
   - In cell `A7`, enter "Output price (per million tokens)."
   - In cell `B7`, enter `5.55` (as a default value).

6. **Volume or Number of contents**
   - In cell `A8`, enter "Volume (Number of contents)."
   - In cell `B8`, create a dropdown with the values `1000, 50000, 100000`.

### Step 3: Calculate LOW and HIGH Costs
- Create formulas to calculate the cost estimates based on the configurable variables.

1. **Low Estimation Cost**
   - In cell `A10`, enter "Low Estimation."
   - In cell `B10`, use a formula to calculate the cost based on the following formula:
     ```
     =((B3 * B4) * B6 * B8) / 1e6
     ```

2. **High Estimation Cost**
   - In cell `A11`, enter "High Estimation."
   - In cell `B11`, use a similar formula to calculate the cost based on the higher coefficient:
     ```
     =((B3 * B5) * B7 * B8) / 1e6
     ```

### Summary
The above steps create a spreadsheet with a dropdown for model selection and configurable dropdowns for the key variables. It calculates a low and high estimation cost based on the formula provided. You can further refine it by adding more explanatory text, formatting, or additional features as needed.

## MISTRAL

Sure, I can guide you on how to create such an Excel spreadsheet. However, I can't create it for you as I'm a text-based AI and don't have the ability to interact with software. Here's a step-by-step guide:

1. **Creating the Dropdown for Model Names:**
   - Click on the cell where you want the dropdown list.
   - Go to the `Data` tab and click on `Data Validation`.
   - In the `Allow` dropdown, select `List`.
   - In the `Source` field, type `mistral-small, mistral-medium, mistral-large`.
   - Click `OK`.

2. **Creating Dropdowns for Variables:**
   - Repeat the above steps for each variable (`nb_words_item`, `multiplier_low`, `multiplier_high`, `price_input`, `price_output`, `volume_items`).
   - For `nb_words_item`, use `500, 1000, 1500, 2000` as the source.
   - For `multiplier_low`, use `1.33` as the source.
   - For `multiplier_high`, use `1.5` as the source.
   - For `price_input`, use `1.85` as the source.
   - For `price_output`, use `5.55` as the source.
   - For `volume_items`, use `1000, 50000, 100000` as the source.

3. **Calculating the Cost:**
   - You can use formulas to calculate the cost based on the selected values. For example, to calculate the LOW estimation, you could use a formula like this: `= (Selected_nb_words_item * Selected_multiplier_low * Selected_price_input / 1000000) * Selected_volume_items`.
   - Replace `Selected_nb_words_item`, `Selected_multiplier_low`, `Selected_price_input`, and `Selected_volume_items` with the actual cell references.
   - Similarly, create a formula for the HIGH estimation using `Selected_multiplier_high` and `Selected_price_output`.



