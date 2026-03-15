FROM python:3.9-slim

WORKDIR /app

COPY main.py .
RUN pip install fastapi uvicorn requests

# EXPOSE 8000 is still fine but Railway ignores it and uses $PORT
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
