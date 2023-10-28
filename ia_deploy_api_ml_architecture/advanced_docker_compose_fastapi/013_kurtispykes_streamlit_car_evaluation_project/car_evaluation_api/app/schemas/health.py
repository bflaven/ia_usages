from pydantic import BaseModel

class Health(BaseModel):
    name: str
    api_version: str
    model_version: str