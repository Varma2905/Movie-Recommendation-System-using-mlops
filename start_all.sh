#!/bin/bash

# Port handled by Railway is $PORT (assigned to Nginx)
# Internal ports for services
export ML_PORT=8001
export BACKEND_PORT=8000
export ML_SERVICE_URL="http://localhost:$ML_PORT"

echo "------------------------------------------------"
echo "🌟 Starting Movie Recommendation System Bundle"
echo "------------------------------------------------"

echo "📦 [1/3] Starting ML Service on port $ML_PORT..."
cd /app/ml-service && uvicorn main:app --host 0.0.0.0 --port $ML_PORT > ml_service.log 2>&1 &
ML_PID=$!

echo "🚀 [2/3] Starting Backend Gateway on port $BACKEND_PORT..."
cd /app/backend && uvicorn main:app --host 0.0.0.0 --port $BACKEND_PORT > backend.log 2>&1 &
BACKEND_PID=$!

echo "🌐 [3/3] Starting Nginx to serve Frontend on port $PORT..."
echo "🔗 Frontend will proxy /api to Backend at localhost:$BACKEND_PORT"

# Ensure Nginx substituted the PORT correctly
# (Already handled in Dockerfile CMD, but good to keep in mind)

# Start Nginx in the foreground
nginx -g "daemon off;"

