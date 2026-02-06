
# 001_mistral_ocr.md

## PROMPT_1 

As a Python and Mistral OCR, make this script work for local pdf as indicated

- path to pdf
```bash
source/_settings_wip.pdf
```

- SCRIPT_1
```python
from dotenv import load_dotenv
import datauri
import os


load_dotenv()
api_key = os.environ["MISTRAL_API_KEY"]
client = Mistral(api_key=api_key)



ocr_response = client.ocr.process(
  model="mistral-ocr-latest",
  document={
    "type": "document_url",
    "document_url": "https://arxiv.org/pdf/2501.00663",
  },
)
print(ocr_response)

```













