#!/bin/bash

# Port handled by Railway is $PORT
export ML_PORT=8001
export BACKEND_PORT=8000
export ML_SERVICE_URL="http://127.0.0.1:$ML_PORT"

echo "------------------------------------------------"
echo "🌟 Starting Movie Recommendation System Bundle"
echo "------------------------------------------------"

# Start ML Service
echo "📦 [1/3] Starting ML Service on port $ML_PORT..."
cd /app/ml-service && uvicorn main:app --host 0.0.0.0 --port $ML_PORT &

# Start Backend
echo "🚀 [2/3] Starting Backend Gateway on port $BACKEND_PORT..."
cd /app/backend && uvicorn main:app --host 0.0.0.0 --port $BACKEND_PORT &

# Wait a moment for services to bind
sleep 5

echo "🌐 [3/3] Starting Nginx on port $PORT..."
# Start Nginx in the foreground
nginx -g "daemon off;"


