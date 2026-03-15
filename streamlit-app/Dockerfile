FROM python:3.9-slim

WORKDIR /app

COPY app.py .

RUN pip install streamlit requests pandas

# EXPOSE 8501
CMD ["sh", "-c", "streamlit run app.py --server.port ${PORT:-8501} --server.address 0.0.0.0"]
