#!/bin/bash
# sh create_files_for_fastapi_sql_app.sh

echo "1. Create sql_app directory and get in"
mkdir sql_app
cd ./sql_app

echo "2. Create files required in sql_app directory and start coding :)"
touch __init__.py
touch crud.py
touch main.py
touch database.py
touch models.py
touch schemas.py

echo "3. DONE for sql_app start the FastAPI"

