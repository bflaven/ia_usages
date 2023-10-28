"""
[env]
# Conda Environment
conda create --name azure_fastapi python=3.9.13
conda info --envs
source activate azure_fastapi
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n azure_fastapi

# update conda
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_deploy_api_ml_architecture/fastapi_cheatsheet/

# launch the api
uvicorn main:app --reload

# get the docs
http://127.0.0.1:8000/docs


"""



from enum import Enum

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.status import HTTP_200_OK

from customized import fastapi_title, fastapi_description, fastapi_version, \
    fastapi_openapi_url, fastapi_docs_url, fastapi_redoc_url, \
    decorator_response_description, decorator_summary,decorator_tags, decorator_responses, decorator_operation_id, decorator_name


class Item(BaseModel):
    """This is an item"""
    my_str: str


app = FastAPI(title=fastapi_title,
              description=fastapi_description,
              version=fastapi_version,
              openapi_url=fastapi_openapi_url,
              docs_url=fastapi_docs_url,
              redoc_url=fastapi_redoc_url,
              )


class PathModel(str, Enum):
    enum1 = "you"
    enum2 = "love"
    enum3 = "enums"

# home
@app.get("/", include_in_schema=False)
async def home():
    # return RedirectResponse("/docs")
    return {'fastapi test app': 'It is running'}

@app.get("/get_endpoint_showing_path_params/{path_id}/{path_model}",
         status_code=HTTP_200_OK,
         response_description=decorator_response_description,
         summary=decorator_summary,
         # description=decorator_description,
         responses=decorator_responses,
         operation_id=decorator_operation_id,
         tags=decorator_tags,
         name=decorator_name,  # no idea what it does
         include_in_schema=True  # set to False and the endpoint disappears from documentation
         )
async def a_get_function(path_id: int, path_model: PathModel, query_str_no_default: str, query_int: int = 0):
    """
    Use either a docstring either description kwargs
    in the decorator, if both are set the decorator kwarg takes precedance
    """
    return path_id


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
