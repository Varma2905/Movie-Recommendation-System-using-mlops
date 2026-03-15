from fastapi import FastAPI, HTTPException
import pickle
import pandas as pd
import os
from typing import Optional, Any

app = FastAPI(title="ML Recommendation Service")

@app.get("/")
def read_root():
    return {"message": "ML Recommendation Service is up and running!", "status": "healthy"}

# Relative to the running directory (ml-service)
MODEL_PATH = os.path.join("model", "recommendation_model.pkl")
MOVIES_PATH = os.path.join("model", "movies_list.pkl")

# Global variables to hold model in memory
similarity: Optional[Any] = None
movies: Optional[pd.DataFrame] = None

def load_resources():
    """Load model artifacts from disk."""
    global similarity, movies
    if not os.path.exists(MODEL_PATH) or not os.path.exists(MOVIES_PATH):
        print("Model files not found. Run training first.")
        return False
    
    try:
        with open(MODEL_PATH, 'rb') as f:
            similarity = pickle.load(f)
        with open(MOVIES_PATH, 'rb') as f:
            movies = pickle.load(f)
        print("Model and movies list loaded successfully.")
        return True
    except Exception as e:
        print(f"Error loading model: {e}")
        return False

# Initial load attempt
load_resources()

@app.get("/recommend/{movie_title}")
def recommend(movie_title: str):
    global similarity, movies
    
    # Try to reload if not present
    if similarity is None or movies is None:
        if not load_resources():
            raise HTTPException(status_code=503, detail="Model not trained. Please run training/train.py first.")

    # We can safely use 'movies' and 'similarity' now because we checked for None above
    assert movies is not None
    assert similarity is not None

    # Smart Search Logic
    try:
        search_query = movie_title.lower().strip()
        
        # 1. Try exact match (case-insensitive)
        match = movies[movies['title'].str.lower() == search_query]
        
        # 2. If no exact match, try if titles CONTAIN the search query
        if match.empty:
            match = movies[movies['title'].str.lower().str.contains(search_query, na=False)]
            
        # 3. If still no match, try removing spaces and symbols (for "spiderman" -> "Spider-Man")
        if match.empty:
            query_clean = "".join(e for e in search_query if e.isalnum())
            db_clean = movies['title'].str.lower().str.replace(r'\W+', '', regex=True)
            match = movies[db_clean.str.contains(query_clean, na=False)]

        if match.empty:
            raise HTTPException(status_code=404, detail=f"'{movie_title}' not found. Try searching with a different keyword.")
        
        # Pick the first match found
        idx = match.index[0]
        actual_title = movies.iloc[idx]['title']
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search Error: {str(e)}")

    # Get similarity scores
    distances = similarity[idx]
    
    # Sort and get top 5 (excluding the movie itself)
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommendations = []
    for i in movie_list:
        recommendations.append(movies.iloc[i[0]]['title'])
        
    return {
        "movie": actual_title, 
        "overview": movies.iloc[idx]['overview'],
        "recommendations": recommendations
    }

@app.get("/movies")
def get_movies():
    if movies is None:
        return {"movies": []}
    return {"movies": movies['title'].tolist()}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
