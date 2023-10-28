from fastapi import FastAPI, File, status
import redis
import os

# tags_metadata
tags_metadata = [
    {
        'name': 'healthcheck',
        'description': 'It basically sends a GET request to the route & hopes to get a "200"'
    },
    {
        'name': 'summary',
        'description': 'For the moment, a fake endpoint. It waits for the function and the summarization logic but it should enable to make a summary from a text.'
    },
    {
        'name': 'visit',
        'description': 'Just to make sure that redis is working'
    }
]


api = FastAPI(
    title="MamamIA",
    description="""Fake API made with FastAPI for basic deployment on Azure.""",
    openapi_tags=tags_metadata,
    version="1.0",
)


redis_server=os.getenv("REDIS_SERVER", default="localhost")
redis_pass=os.getenv("REDIS_PASS", default="")
print("REDIS_SERVER = {}".format(redis_server))
print("REDIS_PASS = {}".format(redis_pass))
r = redis.StrictRedis(host=redis_server, port=6379,
        password=redis_pass,charset="utf-8", decode_responses=True)

# home
@api.get("/", include_in_schema=False)
async def home():
    # return RedirectResponse("/docs")
    return {'fastapi test api': 'It is running'}
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

######################### Support Func #################################
@api.get("/summary/", tags=['summary'])
async def get_summary():
    return {"summary": "endpoint that call function summary come here"}


@api.get("/visit/", tags=['visit'])
async def get_visit():
    if r.exists('visits') == 1: 
        visits = r.get("visits")
        # print("Read {} visits".format(visits))
    else:
        visits = 0
    # print("Save {} visits".format(int(visits) +1))
    r.set("visits", int(visits)+1)
    return {"message": "Hello World, visits {}".format(str(visits))}
