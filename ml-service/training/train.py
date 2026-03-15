import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import mlflow
import mlflow.sklearn
import pickle
import os
import requests

# URL for the dataset
DATA_URL = "https://raw.githubusercontent.com/vamshi121/TMDB-5000-Movie-Dataset/main/tmdb_5000_movies.csv"
# Get the directory where the script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(os.path.dirname(BASE_DIR), "model")

MODEL_PATH = os.path.join(MODEL_DIR, "recommendation_model.pkl")
MOVIES_PATH = os.path.join(MODEL_DIR, "movies_list.pkl")

def load_data():
    print("Downloading dataset...")
    df = pd.read_csv(DATA_URL)
    return df

def preprocess_data(df):
    # Select relevant features
    # For a simple recommendation system, we'll use genres, keywords, tagline, cast, director
    # But for now, let's use 'overview' for content-based matching
    df['overview'] = df['overview'].fillna('')
    return df

def train_model():
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("Movie_Recommendation_System")
    
    with mlflow.start_run():
        df = load_data()
        df = preprocess_data(df)
        
        # TF-IDF Vectorizer
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(df['overview'])
        
        # Calculate Cosine Similarity
        similarity = cosine_similarity(tfidf_matrix, tfidf_matrix)
        
        # Store parameters
        mlflow.log_param("vectorizer", "TfidfVectorizer")
        mlflow.log_param("similarity_metric", "cosine_similarity")
        mlflow.log_param("dataset_size", len(df))
        
        # Save artifacts
        if not os.path.exists(MODEL_DIR):
            os.makedirs(MODEL_DIR)
            
        with open(MODEL_PATH, 'wb') as f:
            pickle.dump(similarity, f)
            
        with open(MOVIES_PATH, 'wb') as f:
            pickle.dump(df[['id', 'title', 'overview']], f)
            
        mlflow.log_artifact(MODEL_PATH)
        mlflow.log_artifact(MOVIES_PATH)
        
        print(f"Model trained and saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_model()
