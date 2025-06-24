#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[env]
# Conda Environment
conda create --name prompt_management python=3.9.13
conda info --envs
source activate prompt_management
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n prompt_management


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt


pip install fastapi sqlmodel uvicorn jinja2 python-multipart
python -m pip install fastapi sqlmodel uvicorn jinja2 python-multipart

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/ia_managing_prompts/prompt-cms-two


# LAUNCH the file
uvicorn main:app --reload
uvicorn main:app --reload --reload-include="*.html" --reload-include="*.css"


"""


# Assume these are already defined elsewhere in your code
from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import Optional, List
import uuid
from datetime import datetime

# Database setup
DATABASE_URL = "sqlite:///prompts.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})



class Connector(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    llm_provider: str
    model: str

class Prompt(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    system: str
    user: str
    keywords: str  # Comma-separated
    connector_id: int = Field(foreign_key="connector.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})

SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Helper to extract variables
def extract_variables(text: str) -> list:
    import re
    return list(set(re.findall(r"\{\{(.*?)\}\}", text)))

# Home: Prompt Registry
@app.get("/")
def prompt_registry(request: Request, session: Session = Depends(get_session)):
    prompts = session.exec(select(Prompt)).all()
    connectors = session.exec(select(Connector)).all()
    return templates.TemplateResponse("registry.html", {
        "request": request,
        "prompts": prompts,
        "connectors": connectors
    })

# Create Prompt Form
@app.get("/prompts/create")
def create_prompt_form(request: Request, session: Session = Depends(get_session)):
    connectors = session.exec(select(Connector)).all()
    return templates.TemplateResponse("create_prompt.html", {
        "request": request,
        "connectors": connectors
    })

# Handle Prompt Edit
@app.get("/prompts/edit/{prompt_id}", response_class=HTMLResponse)
def edit_prompt_form(
    request: Request,
    prompt_id: str,
    session: Session = Depends(get_session)
):
    prompt = session.get(Prompt, prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    connectors = session.exec(select(Connector)).all()
    return templates.TemplateResponse(
        "edit_prompt.html",
        {
            "request": request,
            "prompt": prompt,
            "connectors": connectors
        }
    )

@app.post("/prompts/edit/{prompt_id}", response_class=HTMLResponse)
def edit_prompt_submit(
    request: Request,
    prompt_id: str,
    system: str = Form(...),
    user: str = Form(...),
    keywords: str = Form(...),
    connector_id: int = Form(...),
    session: Session = Depends(get_session)
):
    prompt = session.get(Prompt, prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    prompt.system = system
    prompt.user = user
    prompt.keywords = keywords
    prompt.connector_id = connector_id
    session.add(prompt)
    session.commit()
    return RedirectResponse(url="/", status_code=303)

# Handle Prompt Creation
@app.post("/prompts/create")
def create_prompt(
    request: Request,
    system: str = Form(...),
    user: str = Form(...),
    keywords: str = Form(...),
    connector_id: int = Form(...),
    session: Session = Depends(get_session)
):
    prompt = Prompt(system=system, user=user, keywords=keywords, connector_id=connector_id)
    session.add(prompt)
    session.commit()
    return RedirectResponse(url="/", status_code=303)

# Create Connector Form and Handler (for admin/initial setup)
@app.get("/connectors/create")
def create_connector_form(request: Request):
    return templates.TemplateResponse("create_connector.html", {"request": request})

@app.post("/connectors/create")
def create_connector(
    llm_provider: str = Form(...),
    model: str = Form(...),
    session: Session = Depends(get_session)
):
    connector = Connector(llm_provider=llm_provider, model=model)
    session.add(connector)
    session.commit()
    return RedirectResponse(url="/", status_code=303)


# handle connectors
# List connectors
@app.get("/connectors", response_class=HTMLResponse)
def list_connectors(request: Request, session: Session = Depends(get_session)):
    connectors = session.exec(select(Connector)).all()
    return templates.TemplateResponse(
        "connectors.html",
        {"request": request, "connectors": connectors}
    )

# Edit connector form
@app.get("/connectors/edit/{connector_id}", response_class=HTMLResponse)
def edit_connector_form(
    request: Request,
    connector_id: int,
    session: Session = Depends(get_session)
):
    connector = session.get(Connector, connector_id)
    if not connector:
        raise HTTPException(status_code=404, detail="Connector not found")
    return templates.TemplateResponse(
        "edit_connector.html",
        {"request": request, "connector": connector}
    )

# Edit connector submit
@app.post("/connectors/edit/{connector_id}", response_class=HTMLResponse)
def edit_connector_submit(
    request: Request,
    connector_id: int,
    llm_provider: str = Form(...),
    model: str = Form(...),
    session: Session = Depends(get_session)
):
    connector = session.get(Connector, connector_id)
    if not connector:
        raise HTTPException(status_code=404, detail="Connector not found")
    connector.llm_provider = llm_provider
    connector.model = model
    session.add(connector)
    session.commit()
    return RedirectResponse(url="/connectors", status_code=303)
    
