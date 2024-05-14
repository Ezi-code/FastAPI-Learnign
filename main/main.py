from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    data = {"Hello": "World", "About": "FastAPI", "Version": "0.1.0"}
    return data


@app.get("/about")
def read_about():
    return {"About": "FastAPI"}
