import React, { useState, useEffect } from 'react';
import axios from 'axios';
import EventCard from '../components/EventCard';
import FilterForm from '../components/FilterForm';
import EventCarousel from '../components/EventCarousel';
import logo from '../assets/logo-parnacultura2.png';
import './Home.css';

const API_URL = "https://event-search-iqm2.onrender.com";

const Home = () => {
    const [events, setEvents] = useState([]);
    const [filters, setFilters] = useState({});
    const [currentPage, setCurrentPage] = useState(1);
    const [itemsPerPage, setItemsPerPage] = useState(10);
    const [totalPages, setTotalPages] = useState(1);
    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const fetchEvents = async (filters = {}, page = 1, per_page = itemsPerPage) => {
        setIsLoading(true);
        try {
            const response = await axios.get(`${API_URL}/events`, {
                params: {
                    ...filters,
                    page,
                    per_page,
                },
            });
            console.log("Eventos recebidos:", response.data.events); // Depuração
            setEvents(response.data.events);
            setTotalPages(response.data.pagination.total_pages);
            setError(null);
        } catch (error) {
            console.error('Erro ao buscar eventos:', error);
            setError("Erro ao carregar eventos. Tente novamente mais tarde.");
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchEvents(filters, currentPage, itemsPerPage);
    }, [currentPage, itemsPerPage, filters]);

    const handleFilter = (filters) => {
        console.log("Filtros enviados:", filters); // Depuração
        setFilters(filters);
        setCurrentPage(1);
        fetchEvents(filters, 1, itemsPerPage);
    };

    const handleItemsPerPageChange = (event) => {
        const newItemsPerPage = parseInt(event.target.value, 10);
        console.log("Novos itens por página:", newItemsPerPage); // Depuração
        setItemsPerPage(newItemsPerPage);
        setCurrentPage(1);
        fetchEvents(filters, 1, newItemsPerPage);
    };

    return (
        <div className="container">
            <div className="logo-container">
                <img
                    src={logo}
                    alt="ParnaCultura Logo"
                    className="logo"
                />
            </div>
            <FilterForm onFilter={handleFilter} />

            <div className="mb-3">
                <label htmlFor="itemsPerPage">Itens por página:</label>
                <select
                    id="itemsPerPage"
                    value={itemsPerPage}
                    onChange={handleItemsPerPageChange}
                >
                    <option value={5}>5</option>
                    <option value={10}>10</option>
                    <option value={20}>20</option>
                    <option value={50}>50</option>
                </select>
            </div>

            <div className="mb-3">
                <EventCarousel />
            </div>

            {error && <div className="alert alert-danger">{error}</div>}

            {isLoading ? (
                <div className="text-center">
                    <div className="spinner-border text-primary" role="status">
                        <span className="visually-hidden">Carregando...</span>
                    </div>
                </div>
            ) : (
                events.length > 0 ? (
                    <div className="card-grid">
                        {events.map((event) => (
                            <EventCard key={event.id} event={event} />
                        ))}
                    </div>
                ) : (
                    <div className="alert alert-info">Nenhum evento encontrado.</div>
                )
            )}

            <div className="pagination">
                <button
                    onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
                    disabled={currentPage === 1}
                >
                    Anterior
                </button>
                <span>Página {currentPage} de {totalPages}</span>
                <button
                    onClick={() => setCurrentPage((prev) => prev + 1)}
                    disabled={currentPage >= totalPages}
                >
                    Próxima
                </button>
            </div>
        </div>
    );
};

export default Home;