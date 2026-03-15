import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Search, Film, Loader2 } from 'lucide-react';
import MovieCard from './components/MovieCard';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [movieTitle, setMovieTitle] = useState('');
  const [recommendations, setRecommendations] = useState([]);
  const [moviesList, setMoviesList] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [selectedMovieInfo, setSelectedMovieInfo] = useState(null);

  useEffect(() => {
    // Fetch movies list for dropdown suggestions (optional)
    const fetchMovies = async () => {
      try {
        const response = await axios.get(`${API_URL}/list-movies`);
        setMoviesList(response.data.movies || []);
      } catch (err) {
        console.error("Failed to fetch movies list", err);
      }
    };
    fetchMovies();
  }, []);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!movieTitle) return;

    setLoading(true);
    setError('');
    setRecommendations([]);

    try {
      const response = await axios.get(`${API_URL}/recommend/${movieTitle}`);
      setRecommendations(response.data.recommendations);
      setSelectedMovieInfo({
        title: response.data.movie,
        overview: response.data.overview
      });
    } catch (err) {
      setError(err.response?.data?.detail || 'Movie not found or service is down.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1><span>🍿</span> Movie<span>Mind</span></h1>
        <p>AI-Powered Recommendations for Your Next Binge</p>
      </header>

      <main className="content">
        <form onSubmit={handleSearch} className="search-box">
          <div className="input-wrapper">
            <Film className="search-icon" size={20} />
            <select 
              value={movieTitle} 
              onChange={(e) => setMovieTitle(e.target.value)}
              className="movie-select"
            >
              <option value="">-- Select a Movie --</option>
              {moviesList.sort().map((movie, index) => (
                <option key={index} value={movie}>{movie}</option>
              ))}
            </select>
          </div>
          <button type="submit" disabled={loading || !movieTitle}>
            {loading ? <Loader2 className="animate-spin" /> : 'Get Recommendations'}
          </button>
        </form>

        {error && <div className="error-message">{error}</div>}

        {selectedMovieInfo && (
          <div className="selected-movie-info fade-in">
            <div className="info-card">
              <div className="info-header">
                <h2>{selectedMovieInfo.title}</h2>
                <span className="badge">Action & Story</span>
              </div>
              <p className="storyline"><strong>Storyline:</strong> {selectedMovieInfo.overview}</p>
            </div>
          </div>
        )}

        {recommendations.length > 0 && (
          <div className="recommendations-section">
            <h2>Recommended for You</h2>
            <div className="movies-grid">
              {recommendations.map((movie, index) => (
                <MovieCard key={index} title={movie} />
              ))}
            </div>
          </div>
        )}

        {!loading && recommendations.length === 0 && !error && (
          <div className="empty-state">
            <p>Type a movie title above to get started!</p>
          </div>
        )}
      </main>

      <footer className="footer">
        <p>&copy; 2026 MovieMind MLOps Project</p>
      </footer>
    </div>
  );
}

export default App;
