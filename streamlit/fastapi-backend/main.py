from fastapi import FastAPI
from typing import List, Dict

app = FastAPI()

@app.post("/batch_predict")
async def batch_predict(tweets: List[Dict]):
    # Your model prediction logic here
    results = []
    for tweet in tweets:
        # Apply models and get results (dummy values for example)
        result = {"username": tweet["username"], "tweet": tweet["tweet"], "probability": 0.95, "classification_result": "safe"}
        results.append(result)
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
