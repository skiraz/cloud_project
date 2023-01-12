from fastapi import FastAPI
import uvicorn

from pydantic import BaseModel

app = FastAPI()


class test(BaseModel):
    x: int

# this api is for hello world


@app.get("/text")
def hello():
    return {"text": "hello world"}


#

@app.post("/")
def square(t: test):
    return {"squared": t.x*t.x}
