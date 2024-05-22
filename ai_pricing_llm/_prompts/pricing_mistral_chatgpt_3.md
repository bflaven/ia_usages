
# pricing_mistral_chatgpt_3.md

## prompt

As an advanced programmer in Office Scripts, create an Excel script that generate a spreadsheet that allows you to make a LOW estimation and a HIGH estimation for the cost of using the following models: "mistral-small, mistral-medium, mistral-large, open-mistral-7b, open-mixtral-8x7b, open-mixtral-8x22b". Here is the precises variables, values and instructions.



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

Creating an Office Script for Excel that generates a spreadsheet with dropdown menus for configuration and automatically calculates low and high cost estimations requires leveraging Office Scripts and Data Validation features in Excel. Here's a script that accomplishes that:

```javascript
function main(workbook: ExcelScript.Workbook) {
  const sheet = workbook.addWorksheet("Cost Estimation");

  // Step 1: Create the model dropdown
  const models = [
    "mistral-small",
    "mistral-medium",
    "mistral-large",
    "open-mistral-7b",
    "open-mixtral-8x7b",
    "open-mixtral-8x22b",
  ];

  sheet.getRange("A1").setValue("Select Model");
  const modelDropdown = sheet.getRange("B1");
  modelDropdown.setDataValidation({
    type: ExcelScript.DataValidationType.list,
    operator: ExcelScript.DataValidationOperator.between,
    formula1: `"${models.join(",")}"`,
    showDropDownArrow: true,
  });

  // Step 2: Create dropdowns for configurable variables
  const wordsPerArticleOptions = [500, 1000, 1500, 2000];
  const volumeItemsOptions = [1000, 50000, 100000];

  sheet.getRange("A2").setValue("Number of Words per Article");
  const wordsDropdown = sheet.getRange("B2");
  wordsDropdown.setDataValidation({
    type: ExcelScript.DataValidationType.list,
    operator: ExcelScript.DataValidationOperator.between,
    formula1: `"${wordsPerArticleOptions.join(",")}"`,
    showDropDownArrow: true,
  });

  sheet.getRange("A3").setValue("Volume (Number of Contents)");
  const volumeDropdown = sheet.getRange("B3");
  volumeDropdown.setDataValidation({
    type: ExcelScript.DataValidationType.list,
    operator: ExcelScript.DataValidationOperator.between,
    formula1: `"${volumeItemsOptions.join(",")}"`,
    showDropDownArrow: true,
  });

  // Constants for calculations
  const multiplierLow = 1.33;
  const multiplierHigh = 1.5;

  const modelPrices = {
    "mistral-small": { input: 1.85, output: 5.55 },
    "mistral-medium": { input: 2.5, output: 7.5 },
    "mistral-large": { input: 7.3, output: 22 },
    "open-mistral-7b": { input: 0.2, output: 0.2 },
    "open-mixtral-8x7b": { input: 0.65, output: 0.65 },
    "open-mixtral-8x22b": { input: 1.9, output: 5.6 },
  };

  // Step 3: Define cost calculations
  sheet.getRange("A5").setValue("Low Estimation (€)");
  sheet.getRange("A6").setValue("High Estimation (€)");

  const lowCostFormula = `
    =((B2 * ${multiplierLow}) * modelPrices[INDIRECT("B1")].input * B3) / 1_000_000
  `;
  
  const highCostFormula = `
    =((B2 * ${multiplierHigh}) * modelPrices[INDIRECT("B1")].output * B3) / 1_000_000
  `;

  sheet.getRange("B5").setFormula(lowCostFormula);
  sheet.getRange("B6").setFormula(highCostFormula);

  sheet.getRange("A1:A3").setFontBold(true);
  sheet.getRange("A5:A6").setFontBold(true);

  // Add a note about formulas and calculations
  sheet.getRange("A8").setValue(
    "Note: The estimations are based on the price of 1 million tokens for input/output. Prices vary depending on the model."
  );
}
```

### Usage Instructions

1. Open Excel Online or Excel with Office Scripts enabled.
2. Open the Automate tab and select "New Script".
3. Paste the above script into the script editor.
4. Click "Run" to generate the new worksheet with the dropdowns and calculations.
5. Test different configurations to ensure the cost estimations are calculated correctly.

This script creates a spreadsheet with dropdowns for model selection, the number of words, and volume of contents. It automatically calculates the low and high cost estimations based on the given model prices and multiplier coefficients.
## MISTRAL

Here's an Office Script that creates a spreadsheet with the specified dropdown menus, variables, and values. The script also calculates the LOW and HIGH estimations based on the selected values.

```javascript
function main(workbook: ExcelScript.Workbook) {
  let sheet = workbook.getActiveWorksheet();

  // Define data
  let models = ["mistral-small", "mistral-medium", "mistral-large", "open-mistral-7b", "open-mixtral-8x7b", "open-mixtral-8x22b"];
  let nb_words_item_options = [500, 1000, 1500, 2000];
  let volume_items_options = [1000, 50000, 100000];
  let prices = {
    "mistral-small": { input: 1.85, output: 5.55 },
    "mistral-medium": { input: 2.5, output: 7.5 },
    "mistral-large": { input: 7.3, output: 22 },
    "open-mistral-7b": { input: 0.2, output: 0.2 },
    "open-mixtral-8x7b": { input: 0.65, output: 0.65 },
    "open-mixtral-8x22b": { input: 1.9, output: 5.6 },
  };

  // Add headers
  let headers = ["Model", "Number of words per item", "LOW coef", "HIGH coef", "Input price", "Output price", "Volume", "LOW estimation", "HIGH estimation"];
  let headerRange = sheet.getRange("A1:I1");
  headerRange.setValues([headers]);

  // Add dropdown menus
  let modelDropdown = sheet.getRange("A2").addDataValidation();
  modelDropdown.setListValidation(models);

  let nb_words_itemDropdown = sheet.getRange("B2").addDataValidation();
  nb_words_itemDropdown.setListValidation(nb_words_item_options);

  let multiplier_low = 1.33;
  let multiplier_high = 1.5;
  sheet.getRange("C2").setValue(multiplier_low);
  sheet.getRange("D2").setValue(multiplier_high);

  let volume_itemsDropdown = sheet.getRange("G2").addDataValidation();
  volume_itemsDropdown.setListValidation(volume_items_options);

  // Calculate estimations
  sheet.getRange("H2").setFormula(`=IF(A2="", "", (B2 * C2 * G2 * VLOOKUP(A2, {'Model'!A:B}, 2, FALSE) + B2 * D2 * G2 * VLOOKUP(A2, {'Model'!C:D}, 2, FALSE)) / 1000000)`);
  sheet.getRange("I2").setFormula(`=IF(A2="", "", (B2 * C2 * G2 * VLOOKUP(A2, {'Model'!A:B}, 2, FALSE) * multiplier_high + B2 * D2 * G2 * VLOOKUP(A2, {'Model'!C:D}, 2, FALSE) * multiplier_high) / 1000000)`);

  // Helper table for prices
  let helperTableRange = sheet.getRange("A4:D10");
  helperTableRange.setValues([
    ["Model", "Input price", "Output price"],
    ...models.map((model) => [model, prices[model].input, prices[model].output]),
  ]);
  helperTableRange.getFormat().setColumnWidths([20, 20, 20]);
}
```

This script creates a spreadsheet with the specified dropdown menus and calculations. The LOW and HIGH estimations are calculated based on the selected values in the dropdown menus and the given prices for each model. The helper table containing the prices for each model is created on the same sheet, starting from cell A4.

## prompt

What is this language that work in excel ?

function main(workbook: ExcelScript.Workbook) {
    // Obtenir la cellule et la feuille de calcul actives.
    let selectedCell = workbook.getActiveCell();
    let selectedSheet = workbook.getActiveWorksheet();

    // Définis la couleur de remplissage sur jaune pour la cellule sélectionnée.
    selectedCell.getFormat().getFill().setColor("yellow");

    // TODO: écrivez du code ou utilisez le bouton Insérer une action ci-dessous.

}

The language you're using is called Office Scripts, a JavaScript-based language developed by Microsoft for Office applications. It's used to automate tasks in Excel on the web. The script you provided changes the fill color of the active cell to yellow in the active worksheet. Here's a brief explanation of the code:

1. `main(workbook: ExcelScript.Workbook)`: This is the main function that takes a workbook object as an argument.

2. `let selectedCell = workbook.getActiveCell();`: This line gets the currently active cell in the workbook.

3. `let selectedSheet = workbook.getActiveWorksheet();`: This line gets the currently active worksheet in the workbook.

4. `selectedCell.getFormat().getFill().setColor("yellow");`: This line changes the fill color of the active cell to yellow.

You can add more actions or functions according to your needs under the `TODO` comment. Office Scripts can be used to read, write, and format data in Excel, making it a powerful tool for automating tasks and improving productivity.

