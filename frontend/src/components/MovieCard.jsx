import React from 'react';
import { Film, Star } from 'lucide-react';

const MovieCard = ({ title }) => {
  return (
    <div className="movie-card">
      <div className="movie-icon">
        <Film />
      </div>
      <h3>{title}</h3>
      <div className="movie-footer">
        <Star size={16} fill="#ffd700" color="#ffd700" />
        <span>Highly Similar</span>
      </div>
    </div>
  );
};

export default MovieCard;
