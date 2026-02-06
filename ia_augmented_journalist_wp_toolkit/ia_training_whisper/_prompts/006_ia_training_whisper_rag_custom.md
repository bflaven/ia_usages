## PROMPT_1

As a python, can you write a python script for debugging that will load the files : `RFI_BR_thematicTags.py`, `RFI_CN_thematicTags.py`... to see if the file is OK, make the choice of file configurable and load the first keywords on the console. I want to be sure that the python files are well written.

```python
# NB OF TAGS: 2005
from typing import Literal
from pydantic import BaseModel
# RFI_SW_thematicTags
class BachSectionTag(BaseModel):
    label: Literal["1899 Hoffenheim", "AC Leopards", "AC Milan", "ADC Ikibiri", "ADF", "AFCON"]
```


I am using anaconda to manage the python environment. The name of the env is `whisper_train`


## OUTPUT_1




