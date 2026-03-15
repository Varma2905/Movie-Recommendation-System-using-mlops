import streamlit as st
import requests
import pandas as pd
import os

st.set_page_config(page_title="MovieMind - ML Admin Test", layout="wide", page_icon="🎬")

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        background-color: #0f172a;
        color: white;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background: linear-gradient(135deg, #6366f1 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem;
        font-weight: bold;
    }
    .movie-card {
        background-color: #1e293b;
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.1);
        text-align: center;
        margin-bottom: 1rem;
    }
    .storyline-box {
        background-color: rgba(99, 102, 241, 0.1);
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid #6366f1;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🍿 MovieMind ML Testing Dashboard")
st.write("Test your MLOps pipeline and recommendation logic here.")

# Sidebar Configuration
st.sidebar.header("🛠️ Configuration")
DEFAULT_BACKEND = os.environ.get("BACKEND_URL", "http://localhost:8000")
BACKEND_URL = st.sidebar.text_input("Backend API URL", DEFAULT_BACKEND)

# Fetch Movies List
@st.cache_data
def get_movie_list():
    try:
        response = requests.get(f"{BACKEND_URL}/list-movies")
        if response.status_code == 200:
            return sorted(response.json().get("movies", []))
    except:
        return []
    return []

movies_list = get_movie_list()

if not movies_list:
    st.error("⚠️ Connection Error: Could not fetch movies from Backend. Make sure your Backend (Port 8000) is running!")
else:
    # Movie Selection
    selected_movie = st.selectbox("🎯 Select a Movie to get Recommendations:", [""] + movies_list)

    if st.button("Generate Recommendations ✨"):
        if selected_movie:
            try:
                with st.spinner("🧠 AI is thinking..."):
                    response = requests.get(f"{BACKEND_URL}/recommend/{selected_movie}")
                    if response.status_code == 200:
                        data = response.json()
                        recs = data.get("recommendations", [])
                        overview = data.get("overview", "No storyline available.")
                        
                        # Display Selected Movie Info
                        st.markdown(f"""
                            <div class="storyline-box">
                                <h2 style='color: #6366f1; margin: 0;'>{selected_movie}</h2>
                                <p style='font-style: italic; color: #94a3b8; margin-bottom: 1rem;'>Action & Story</p>
                                <p><strong>Storyline:</strong> {overview}</p>
                            </div>
                        """, unsafe_allow_html=True)

                        # Display Recommendations
                        st.subheader("🚀 You might also like:")
                        if recs:
                            cols = st.columns(len(recs))
                            for i, rec in enumerate(recs):
                                with cols[i]:
                                    st.markdown(f"""
                                        <div class="movie-card">
                                            <p style='font-weight: bold; margin: 0;'>{rec}</p>
                                        </div>
                                    """, unsafe_allow_html=True)
                        else:
                            st.warning("No recommendations found.")
                    else:
                        st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"Failed to connect to backend: {str(e)}")
        else:
            st.warning("Please select a movie first.")

st.divider()

# Health Check Section
with st.expander("🔍 System Health Check"):
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Backend (8000)**")
        try:
            r = requests.get(f"{BACKEND_URL}/")
            st.success(f"Online: {r.json().get('message')}")
        except:
            st.error("Offline")
            
    with col2:
        st.write("**ML Service (8001)**")
        try:
            # We assume ML service is on 8001 based on previous setup
            r = requests.get("http://localhost:8001/")
            st.success(f"Online: {r.json().get('message')}")
        except:
            st.error("Offline")
