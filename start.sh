#!/bin/bash
# This is a helper script for deployment detection
echo "Starting Movie Recommendation System..."
cd streamlit-app && streamlit run app.py --server.port $PORT --server.address 0.0.0.0
