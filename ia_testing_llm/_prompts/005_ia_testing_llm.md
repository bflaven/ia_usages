
# 005_ia_testing_llm.md



## PROMPT_1

As a Python expert, using langdetect, writes a script that parses all files with the extension 1.txt contained in each directory, then loads the content into the function "detect" and prints the result. You can use best practices in coding and leverage on Class or function to do so, as the directory can be extended with ne languages



```sh
articles/ar/1.txt
articles/br/1.txt
articles/cn/1.txt
articles/en/1.txt
articles/es/1.txt
articles/fa/1.txt
articles/ff/1.txt
articles/fr/1.txt
articles/ha/1.txt
articles/km/1.txt
articles/ma/1.txt
articles/pt/1.txt
articles/ro/1.txt
articles/ru/1.txt
articles/sw/1.txt
articles/uk/1.txt
articles/vi/1.txt
```



```python
from langdetect import detect, LangDetectException

result = detect("War doesn't show who's right, just who's left.")

print("\n--- RESULT")
print (result)

``` 




## MISTRAL_1


Certainly! Below is a Python script that parses all files with the extension `1.txt` contained in each directory, loads the content into the `detect` function from the `langdetect` library, and prints the result. This script uses best practices and leverages a class for better organization and extensibility.

```python
import os
from langdetect import detect, LangDetectException

class LanguageDetector:
    def __init__(self, base_directory):
        self.base_directory = base_directory

    def detect_language(self, text):
        try:
            return detect(text)
        except LangDetectException as e:
            return f"Error detecting language: {e}"

    def process_files(self):
        for root, dirs, files in os.walk(self.base_directory):
            for file in files:
                if file == '1.txt':
                    file_path = os.path.join(root, file)
                    self.process_file(file_path)

    def process_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            result = self.detect_language(content)
            print(f"File: {file_path}")
            print(f"Detected Language: {result}")
            print("---")

if __name__ == "__main__":
    base_directory = 'articles'
    detector = LanguageDetector(base_directory)
    detector.process_files()
```

### Explanation:

1. **Class Definition**:
   - `LanguageDetector`: A class that encapsulates the functionality for detecting languages in text files.

2. **Initialization**:
   - `__init__(self, base_directory)`: Initializes the class with the base directory where the files are located.

3. **Language Detection**:
   - `detect_language(self, text)`: A method that uses the `detect` function from `langdetect` to determine the language of the given text. It handles exceptions gracefully.

4. **File Processing**:
   - `process_files(self)`: A method that walks through the directory structure starting from the base directory and processes each file named `1.txt`.
   - `process_file(self, file_path)`: A method that reads the content of a file, detects its language, and prints the result.

5. **Main Execution**:
   - The script sets the base directory to `articles` and creates an instance of `LanguageDetector`. It then calls the `process_files` method to process all relevant files.

### Usage:
- Ensure that the `langdetect` library is installed (`pip install langdetect`).
- Place the script in the same directory as the `articles` folder or adjust the `base_directory` variable accordingly.
- Run the script, and it will print the detected language for each `1.txt` file found in the subdirectories.

This approach makes the script modular and easy to extend or modify in the future.