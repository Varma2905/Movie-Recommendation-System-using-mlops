from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI(title="Backend Gateway API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ML Service URL (internal or external)
ML_SERVICE_URL = os.getenv("ML_SERVICE_URL", "http://localhost:8001")

@app.get("/")
def read_root():
    return {"message": "Welcome to Movie Recommendation Backend API"}

@app.get("/recommend/{movie_title}")
def get_recommendation(movie_title: str):
    try:
        response = requests.get(f"{ML_SERVICE_URL}/recommend/{movie_title}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json().get("detail", "Error from ML service"))
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"ML Service unavailable: {str(e)}")

@app.get("/list-movies")
def list_movies():
    try:
        response = requests.get(f"{ML_SERVICE_URL}/movies")
        return response.json()
    except Exception as e:
        return {"movies": []}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
