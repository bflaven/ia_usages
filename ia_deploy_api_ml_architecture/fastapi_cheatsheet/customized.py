# FastAPI object customization
fastapi_title = "fastapi cheatsheet"
fastapi_description = "FastAPI cheatseheet helps you visualizse what part of python code corresponds to what part of swagger UI"
fastapi_version = "0.0.0"
fastapi_openapi_url = "/custom_openapi.json"
fastapi_docs_url = "/custom_docs"
fastapi_redoc_url = "/custom_redoc"

# decorator custom elements
decorator_response_description = "Custom 200 message"
decorator_summary = "Custom summary, if not used it will print the function name `a_get_function` capitalized with underscores switchd to spaces ie here A Get Function"

decorator_responses = {
    201: {
        "content": {"image/png": {}},
        "description": "Return the JSON item or an image.",
    }, }
decorator_operation_id = "Awesome_operation_id"
decorator_tags = ["Mytag1"]
decorator_name = "MyName"
