import React from 'react';
import './EventCard.css';

const EventCard = ({ event }) => {
    return (
        <div className="card">
            <div className="front-page">
                <img src={event.image_url} alt={event.title} className="card-image" />
                <div className="card-info">
                    <h2 className="card-title">{event.title}</h2>
                    <p className="card-subtitle">{event.city}, {event.state}</p>
                </div>
            </div>
            <div className="back-page">
                <div className="card-content">
                    <h3>{event.title}</h3>
                    <p className="card-description">{event.synopsis}</p>
                    <a href={event.purchase_url} target="_blank" rel="noopener noreferrer" className="card-button">
                        Comprar Ingresso
                    </a>
                </div>
            </div>
        </div>
    );
};

export default EventCard;