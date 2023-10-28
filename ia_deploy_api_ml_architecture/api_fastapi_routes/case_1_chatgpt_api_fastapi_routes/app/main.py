from fastapi import FastAPI
from api import user, item
from fastapi.responses import RedirectResponse

# tags_metadata
tags_metadata = [
    {
        'name': 'healthcheck',
        'description': 'It basically sends a GET request to the route & hopes to get a "200"'
    } 
    
]

app = FastAPI(
    title="TrattorIA",
    description="""EXAMPLE_1 Routes examples for FastAPI""",
    openapi_tags=tags_metadata,
    version="2.0",
    )


@app.get('/', include_in_schema=False)
def home():
    # return {"Welcome here - Benvenidos aqui - Добро пожаловать - Bienvenue ici"}
    return RedirectResponse(f"/docs")

@app.get('/healthcheck', tags=['healthcheck'])
def perform_healthcheck():
    '''
    It basically sends a GET request to the route & hopes to get a "200"
    response code. Failing to return a 200 response code just enables
    the GitHub Actions to rollback to the last version the project was
    found in a "working condition". It acts as a last line of defense in case something goes south.
    Additionally, it also returns a JSON response in the form of:
    {
        'healtcheck': 'Everything OK!'
    }
    '''
    return {'healthcheck': 'Everything OK!'}



app.include_router(user.router, prefix="/people", tags=["users"])
app.include_router(item.router, prefix="/cart", tags=["items"])



