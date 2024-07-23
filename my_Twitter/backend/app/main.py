
from fastapi import FastAPI
from backend.app.routes import predict, health, store_tweet

app = FastAPI()

app.include_router(predict.router)
app.include_router(health.router)
app.include_router(store_tweet.router)  # Include the store_tweet router

@app.get("/")
def read_root():
    return {"message": "Welcome to the prediction API"}
