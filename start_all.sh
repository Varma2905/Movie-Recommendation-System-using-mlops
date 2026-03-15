#!/bin/bash

# Port handled by Railway is $PORT
export ML_PORT=8001
export BACKEND_PORT=8000
export ML_SERVICE_URL="http://127.0.0.1:$ML_PORT"

echo "------------------------------------------------"
echo "🌟 MOVIE RECOMMENDATION SYSTEM BUNDLE"
echo "------------------------------------------------"
echo "📍 Railway Port: $PORT"
echo "📍 Backend Port: $BACKEND_PORT"
echo "📍 ML Port:      $ML_PORT"

# Debug: Show the generated Nginx config
echo "📝 Verifying Nginx Configuration..."
cat /etc/nginx/sites-enabled/movie | grep "listen"

# Start ML Service
echo "📦 [1/3] Starting ML Service..."
cd /app/ml-service && uvicorn main:app --host 0.0.0.0 --port $ML_PORT &

# Start Backend
echo "🚀 [2/3] Starting Backend Gateway..."
cd /app/backend && uvicorn main:app --host 0.0.0.0 --port $BACKEND_PORT &

# Wait for services to bind
echo "⏳ Waiting for services to wake up..."
sleep 5

echo "🌐 [3/3] Launching Nginx..."
# Start Nginx in the foreground
nginx -g "daemon off;"



