################
# File main.py #
################

# from serverConfig import create_conn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, LLM World!"}


# def feedMessage(conn):
#     conn.sudo('uvicorn main:app --host 0.0.0.0 --port 8000')


# def feedMessage(**kwargs):
#     _feedMessage(create_conn())