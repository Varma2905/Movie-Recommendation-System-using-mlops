#!/bin/bash

# Port handled by Railway is $PORT (assigned to Nginx)
# Internal ports for services
export ML_PORT=8001
export BACKEND_PORT=8000
export ML_SERVICE_URL="http://localhost:$ML_PORT"

echo "📦 Starting ML Service on port $ML_PORT..."
cd /app/ml-service && uvicorn main:app --host 0.0.0.0 --port $ML_PORT &

echo "🚀 Starting Backend Gateway on port $BACKEND_PORT..."
cd /app/backend && uvicorn main:app --host 0.0.0.0 --port $BACKEND_PORT &

echo "🌐 Starting Nginx to serve Frontend on port $PORT..."
# Nginx will stay in foreground
nginx -g "daemon off;"
