#!/bin/bash

# Port handled by Railway is $PORT (assigned to Nginx)
# We use high ports for internal services to avoid conflicts
export ML_PORT=10001
export BACKEND_PORT=10000
export ML_SERVICE_URL="http://127.0.0.1:$ML_PORT"

echo "------------------------------------------------"
echo "🌟 MOVIE RECOMMENDATION SYSTEM BUNDLE"
echo "------------------------------------------------"
echo "📍 Public Port (Nginx): $PORT"
echo "📍 Backend (Internal):  $BACKEND_PORT"
echo "📍 ML Service (Internal): $ML_PORT"

# Start ML Service
echo "📦 [1/3] Starting ML Service..."
cd /app/ml-service && uvicorn main:app --host 127.0.0.1 --port $ML_PORT &

# Start Backend
echo "🚀 [2/3] Starting Backend Gateway..."
cd /app/backend && uvicorn main:app --host 127.0.0.1 --port $BACKEND_PORT &

# Wait for services to bind
echo "⏳ Waiting for services to wake up..."
sleep 5

echo "🌐 [3/3] Launching Nginx..."
# Start Nginx in the foreground
nginx -g "daemon off;"




