
# pricing_mistral_chatgpt_4.md

## prompt

As an advanced programmer in Excel, create an Excel spreadsheet that generate a spreadsheet that allows you to make a LOW estimation and a HIGH estimation for the cost of using the following models: "mistral-small, mistral-medium, mistral-large, open-mistral-7b, open-mixtral-8x7b, open-mixtral-8x22b". Here is the precises variables, values and instructions.



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
Volume or Number of contents = 1,000, 50,000, 100,000...


4. Price per model


For model "mistral-small"
Input price = €1.85 per 1 Million tokens
Output price = €5.55 per 1 Million tokens

For model "mistral-medium
Input price = 2.5€ per 1 Million tokens
Output price = 7.5€ per 1 Million tokens


For model "mistral-large"
Input price = 7.3€ per 1 Million tokens
Output price = 22€ per 1 Million tokens


For model "open-mistral-7b"
Input price = 0.2€ per 1 Million tokens
Output price = 0.2€ per 1 Million tokens

For model "open-mixtral-8x7b" 
Input price = 0.65€ per 1 Million tokens
Output price = 0.65€ per 1 Million tokens

For model "open-mixtral-8x22b"
Input price = 1.9€ per 1 Million tokens
Output price = 5.6€ per 1 Million tokens




## ChatGPT

To create an Excel spreadsheet that meets the given requirements, you will need to incorporate drop-down menus for user selections and use formulas to calculate low and high estimations for costs based on the given input data.

Here is a step-by-step guide to create such an Excel spreadsheet:

### Step 1: Create the Drop-Down Menus
1. Open a new Excel spreadsheet.
2. Go to the `Data` tab and select `Data Validation`.
3. Choose `Data Validation` from the dropdown, then select `List`.
4. Create the `model_name` drop-down menu:
   - In the `Source` field, enter the following values (separated by commas):
     ```
     mistral-small, mistral-medium, mistral-large, open-mistral-7b, open-mixtral-8x7b, open-mixtral-8x22b
     ```
   - Click `OK`.
5. Similarly, create drop-down menus for other configurable variables:
   - `nb_words_item` with the following values: `500, 1000, 1500, 2000`
   - `volume_items` with the following values: `1000, 50000, 100000`
   - `multiplier_low` and `multiplier_high` with these values: `1.33, 1.5`

### Step 2: Create a Table for Model Prices
1. In a new section of the spreadsheet, create a table with the following structure:
   - `A1`: "Model Name"
   - `B1`: "Input Price (€/M tokens)"
   - `C1`: "Output Price (€/M tokens)"
2. Fill in the following data:
   - `A2`: "mistral-small"
   - `B2`: `1.85`
   - `C2`: `5.55`
   - `A3`: "mistral-medium"
   - `B3`: `2.5`
   - `C3`: `7.5`
   - `A4`: "mistral-large"
   - `B4`: `7.3`
   - `C4`: `22`
   - `A5`: "open-mistral-7b"
   - `B5`: `0.2`
   - `C5`: `0.2`
   - `A6`: "open-mixtral-8x7b"
   - `B6`: `0.65`
   - `C6`: `0.65`
   - `A7`: "open-mixtral-8x22b"
   - `B7`: `1.9`
   - `C7`: `5.6`

### Step 3: Create Formulas for Cost Calculation
1. In the main section of the spreadsheet, place the drop-down menus:
   - `A1`: "Model Name"
   - `B1`: The drop-down created for `model_name`
   - `A2`: "Number of Words per Item"
   - `B2`: The drop-down for `nb_words_item`
   - `A3`: "Volume of Items"
   - `B3`: The drop-down for `volume_items`
   - `A4`: "Coefficient LOW"
   - `B4`: The drop-down for `multiplier_low`
   - `A5`: "Coefficient HIGH"
   - `B5`: The drop-down for `multiplier_high`

2. Define a section to calculate the costs:
   - `D1`: "Low Estimation"
   - `E1`: "High Estimation"

3. Use the `XLOOKUP` or `VLOOKUP` function to find the input and output prices based on the selected model:
   - `D2`: Formula to get the `Input Price`:
     ```excel
     =XLOOKUP(B1, A2:A7, B2:B7)
     ```
   - `E2`: Formula to get the `Output Price`:
     ```excel
     =XLOOKUP(B1, A2:A7, C2:C7)
     ```

4. Calculate the number of tokens for low and high estimations:
   - `D3`: Number of tokens for low estimation:
     ```excel
     =B2 * B4
     ```
   - `E3`: Number of tokens for high estimation:
     ```excel
     =B2 * B5
     ```

5. Calculate the total tokens for the entire volume of items for low and high estimations:
   - `D4`: Total tokens for low estimation:
     ```excel
     =D3 * B3
     ```
   - `E4`: Total tokens for high estimation:
     ```excel
     =E3 * B3
     ```

6. Calculate the cost for input and output for low and high estimations:
   - `D5`: Input cost for low estimation:
     ```excel
     =D4 / 1000000 * D2
     ```
   - `E5`: Input cost for high estimation:
     ```excel
     =E4 / 1000000 * E2
     ```
   - `D6`: Output cost for low estimation:
     ```excel
     =D4 / 1000000 * E2
     ```
   - `E6`: Output cost for high estimation:
     ```excel
     =E4 / 1000000 * E2
     ```

7. Calculate the total cost for low and high estimations:
   - `D7`: Total cost for low estimation:
     ```excel
     =D5 + D6
     ```
   - `E7`: Total cost for high estimation:
     ```excel
     =E5 + E6
     ```

This guide should help you create a basic Excel spreadsheet for cost estimations based on different models and configurations. Modify as needed for additional customization and functionalities.

