import React, { useState, useEffect } from 'react';
import axios from 'axios';
import EventCard from '../components/EventCard';
import FilterForm from '../components/FilterForm';
import './Home.css';

const Home = () => {
    const [events, setEvents] = useState([]);
    const [filters, setFilters] = useState({});
    const [currentPage, setCurrentPage] = useState(1);
    const [itemsPerPage, setItemsPerPage] = useState(10); // Valor padrão de itens por página

    const fetchEvents = async (filters = {}, page = 1, limit = itemsPerPage) => {
        try {
            const response = await axios.get('http://localhost:5000/events', {
                params: {
                    ...filters,
                    page,
                    limit,
                },
            });
            setEvents(response.data.events);
        } catch (error) {
            console.error('Erro ao buscar eventos:', error);
        }
    };

    useEffect(() => {
        fetchEvents(filters, currentPage, itemsPerPage);
    }, [currentPage, itemsPerPage, filters]);


    const handleFilter = (filters) => {
        setFilters(filters);
        setCurrentPage(1); // Resetar para a primeira página ao aplicar novos filtros
        fetchEvents(filters, 1, itemsPerPage);
    };

    const handleItemsPerPageChange = (event) => {
        const newItemsPerPage = parseInt(event.target.value, 10);
        setItemsPerPage(newItemsPerPage);
        setCurrentPage(1); // Resetar para a primeira página ao alterar a quantidade de itens por página
        fetchEvents(filters, 1, newItemsPerPage);
    };

    return (
        <div className="container">
            <h1 className="my-4">Eventos</h1>
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

            <div className="card-grid">
                {events.map((event) => (
                    <EventCard key={event.id} event={event} />
                ))}
            </div>

            <div className="pagination">
                <button
                    onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
                    disabled={currentPage === 1}
                >
                    Anterior
                </button>
                <span>Página {currentPage}</span>
                <button
                    onClick={() => setCurrentPage((prev) => prev + 1)}
                    disabled={events.length < itemsPerPage}
                >
                    Próxima
                </button>
            </div>

        </div>
    );
};

export default Home;