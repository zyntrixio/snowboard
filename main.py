from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from app import app as dash
import uvicorn

app = FastAPI()
app.mount("/dashboard", WSGIMiddleware(dash.server))  # type: ignore


@app.get("/")
def index():
    return "hello"


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
