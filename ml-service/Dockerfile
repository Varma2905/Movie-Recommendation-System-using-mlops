FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure model directory exists
RUN mkdir -p model

# Train the model during build (optional, or run as a separate step)
# For simplicity in this demo, we'll run training on start if model doesn't exist
# But ideally, training is a separate pipeline step.
RUN python training/train.py

# EXPOSE 8001
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8001}"]
