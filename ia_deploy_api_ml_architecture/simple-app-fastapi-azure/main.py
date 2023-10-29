#!/usr/bin/python
# -*- coding: utf-8 -*-
#
from fastapi import FastAPI, File, status
from fastapi.responses import RedirectResponse
# from fastapi.responses import StreamingResponse
# from fastapi.responses import FileResponse
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.exceptions import HTTPException
 
app = FastAPI()

# home
@app.get("/")
async def home():
    return RedirectResponse("/docs")

@app.get("/healthcheck")
async def perform_healthcheck():
    return {'Youtube Again and Again Test Again Azure FastAPI test api': 'It is running and it is OK.'}
    
    