
from fastapi import FastAPI
from backend.app.routes import predict, health

app = FastAPI()

app.include_router(predict.router)
app.include_router(health.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the prediction API"}
