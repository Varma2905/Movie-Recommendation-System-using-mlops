# Combined Dockerfile for Movie Recommendation System
# Runs ML Service, Backend, and Frontend (via Nginx) in one container.

# --- Stage 1: Build Frontend ---
FROM node:18-slim AS frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
# In production, we use relative paths via Nginx proxy
ARG REACT_APP_API_URL=/api
ENV REACT_APP_API_URL=$REACT_APP_API_URL
RUN npm run build

# --- Stage 2: Final Image ---
FROM python:3.9-slim

# Install Nginx and other utilities
RUN apt-get update && apt-get install -y nginx gettext-base && rm -rf /var/lib/apt/lists/*

# Remove default nginx site to avoid conflicts
RUN rm /etc/nginx/sites-enabled/default

WORKDIR /app

# Copy Backend and ML Service code
COPY backend /app/backend
COPY ml-service /app/ml-service

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Ensure model directory exists and train it
RUN mkdir -p /app/ml-service/model
RUN cd /app/ml-service && python training/train.py

# Copy Frontend build to Nginx directory
COPY --from=frontend-build /app/frontend/build /usr/share/nginx/html

# Copy Nginx config template
COPY nginx.conf.template /etc/nginx/nginx.conf.template

# Copy and prepare startup script
COPY start_all.sh /app/start_all.sh
RUN chmod +x /app/start_all.sh

# Railway uses $PORT, so we need to substitute it in the nginx config
# Railway uses $PORT, so we need to substitute it in the nginx config
CMD ["/bin/sh", "-c", "envsubst '${PORT}' < /etc/nginx/nginx.conf.template > /etc/nginx/sites-enabled/movie && /app/start_all.sh"]

