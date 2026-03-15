FROM python:3.9-slim

WORKDIR /app

# Install system dependencies (only if really needed, keeping it minimal)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything
COPY . .

# Set working directory to the streamlit app folder
WORKDIR /app/streamlit-app

# Expose the port (Railway uses $PORT, so we don't strictly need this, but good practice)
EXPOSE 8080

# Run the app using the PORT environment variable provided by Railway
CMD ["sh", "-c", "streamlit run app.py --server.port ${PORT:-8080} --server.address 0.0.0.0"]
