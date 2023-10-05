# fastapi_database

**Still exploring the FastAPI's capabilities to be use as a wrapper for data science API and expose NLP features as a RESTFUL microservice. But, this I have extended the scope and decide to interface an API's POC, leveraging on Spacy's NLP features, with a Sqlite or MySQL database through an ORM like SQLAlchemy or Peewee**

[Check the article on Flaven.fr: POC with FastAPI for an NLP API with Spacy, SQLAlchemy, Sqlite and… Streamlit](https://flaven.fr/2023/10/poc-with-fastapi-for-an-nlp-api-with-spacy-sqlalchemy-sqlite-and-streamlit/)


**The prompt behind the fastAPI POC in "011_openai_sqlite_nlp_fastapi_streamlit"**
```
# prompt for ChatGP to create nlp api with database

In Python, with the help of Spacy in 3 different languages (ES, FR, EN) and FastAPI, write an API named
("title="TrattorIA") that manage an element named "Post", create 2 endpoints: function "healthcheck" available at
"/healthcheck", function "entities" available at "/entities/{lang}" where "lang" is a variable for the 3 different
languages. For the NER function "entities" used "body: RecordsRequest = Body(..., example=example_request)" where,
example_request is provided by an external json file named example_request.json.

Please define the appropriate json structure according to the code for the API.

The API rely on a sqlite database named "nlp_post_db.db". It has to be structure like a traditional FastAPI project, the
ORM used is sqlalchemy. Below the wanted structure:

nlp_db_app
├── __init__.py
├── crud.py
├── database.py
├── main.py
├── models.py
└── schemas.py

In the file "models.py", the class Post(Base) contains fields like: post_id, post_title, post_body, post_origin_id,
keywords_ner. The API is saving the result of the NER function "entities" available at "/entities/{lang}".

post_id is the primary_key for each post
post_title is the title of the post
post_body is the body of the post
post_origin_id is the id coming form another database
keywords_ner is the result of the NER function "entities" available at "/entities/{lang}"

So, when the post_body is passed to the function "entities", the result is saved the result into a table and especially
entities extracted form the post_body
```


Here are presentation for each GitHub directories attached to this exploration:



- **001_extra_files** 
It contains 2 files 001_fastapi_database.py and create_files_for_fastapi_sql_app.sh. The file "create_files_for_fastapi_sql_app.sh" creates a directory named "sql_app" and inside all the empty files required to start the FastAPI API with a database. The file "001_fastapi_database.py" check if sqlalchemy is properly installed in your environment with the creation of database named "example.db" and add 2 records in it.

- **002_bugbytes_io_crud_api_fastapi** 
A great example documented both by a video and a post from bugbytes.io. Everything you need to know on how creating a CRUD API with GET, POST, PUT and DELETE Endpoints.

- **003_bugbytes_io_crud_api_fastapi_sqlmodel** 
A bit more advanced example than the previous exampl "002_bugbytes_io_crud_api_fastapi". Introducing SQL model.

- **004_bugbytes_io_fastapi_htmx_example** The same code than the two previous examples from bugbytes.io but again taking advantage of the ORM sqlalchemy.

- **005_fastapi_tiangolo_tutorial_sql_databases** The example given by the official documentation of FastAPI with SQLAlchemy.</li>
**007_sql_databases_peewee** 
The example given by the official documentation of FastAPI with Peewee this time.

- **008_fastapi_mysql_restapi** 
Using Docker to create a MYSQL database and a Phpmyaadmin instance connected to FastAPI POC.

- **011_openai_sqlite_nlp_fastapi_streamlit** a simple combination with Streamlit, FastAPI and Spacy to expose "features" like: NER, Summary, Tags extraction for text in French, Spanish, English and Russian. The skeleton has been written by ChatGPT and extended manually after.

