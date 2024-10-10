################
# File main.py #
################

from serverConfig import create_conn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, LLM World!"}



def _feedMessage(conn):
    conn.sudo('uvicorn main:app --host 89.32.250.198 --port 9000')


def feedMessage(**kwargs):
    _feedMessage(create_conn())