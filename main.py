import uvicorn
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from app import app as dashboard


# Define the FastAPI server
app = FastAPI()

# Mount
app.mount("/dashboard", WSGIMiddleware(dashboard.server)) # type: ignore


@app.get("/")
def index():
    return "ROUTE ACTIVE"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
