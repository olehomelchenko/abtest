from fastapi import FastAPI
from processing import Processor

app = FastAPI()


@app.get("/")
def main():
    return {"message": "Hello world"}


@app.get("/getjson")
def get_json(data: str):
    p = Processor(data)
    p.parse_init_data()
    return p.variations_list