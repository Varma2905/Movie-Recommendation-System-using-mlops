## How to Run Locally

### 1. Prerequisites
- Python 3.9+
- Node.js & npm
- Docker & Docker Compose (optional, but recommended)

### 2. Manual Setup (Without Docker)
#### ML Service:
```bash
cd ml-service
pip install -r requirements.txt
python training/train.py  # Wait for training to complete
uvicorn main:app --host 0.0.0.0 --port 8001
```

#### Backend:
```bash
cd backend
pip install fastapi uvicorn requests
uvicorn main:app --host 0.0.0.0 --port 8000
```

#### Frontend:
```bash
cd frontend
npm install
npm start
```

### 3. Setup with Docker (Recommended)
```bash
docker-compose up --build
```
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- ML Service API: `http://localhost:8001`
- Streamlit: `http://localhost:8501`

## MLflow Tracking
During training, MLflow logs experiments locally in the `mlruns` directory (within `ml-service`). You can view the dashboard by running:
```bash
cd ml-service
mlflow ui
```

## Internal Connection Flow
1. **Frontend (React)**: Sends a request to `localhost:8000/recommend/{movie}`.
2. **Backend (FastAPI)**: Receives request, forwards it to `ml-service:8001/recommend/{movie}`.
3. **ML Service (FastAPI)**: Loads the similarity matrix, performs search, and returns JSON.
4. **Result**: Displayed in the React UI with movie cards.

## Deployment to Railway

### Step 1: Push to GitHub
Create a new repository and push all files.

### Step 2: Railway Connection
1. Login to [Railway.app](https://railway.app/).
2. Create a "New Project" -> "Deploy from GitHub repo".
3. Deploy **ML Service** first:
   - Root Directory: `ml-service`
   - Port: `8001`
4. Deploy **Backend**:
   - Root Directory: `backend`
   - Set Environment Variable: `ML_SERVICE_URL` = (The URL of your deployed ML Service).
   - Port: `8000`
5. Deploy **Frontend**:
   - Root Directory: `frontend`
   - Set Environment Variable: `REACT_APP_API_URL` = (The URL of your deployed Backend).
# Movie-Recommendation-System-using-mlops
