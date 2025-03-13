import React, { useState } from 'react';

const FilterForm = ({ onFilter }) => {
    const [filters, setFilters] = useState({
        city: '',
        state: '',
        source: '',
        start_date: '',
        end_date: '',
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFilters({ ...filters, [name]: value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onFilter(filters);
    };

    return (
        <form onSubmit={handleSubmit} className="mb-4">
            <div className="row">
                <div className="col">
                    <input
                        type="text"
                        name="city"
                        placeholder="Cidade"
                        value={filters.city}
                        onChange={handleChange}
                        className="form-control"
                    />
                </div>
                <div className="col">
                    <input
                        type="text"
                        name="state"
                        placeholder="Estado"
                        value={filters.state}
                        onChange={handleChange}
                        className="form-control"
                    />
                </div>
                <div className="col">
                    <input
                        type="text"
                        name="source"
                        placeholder="Fonte (ex: ticketmaster)"
                        value={filters.source}
                        onChange={handleChange}
                        className="form-control"
                    />
                </div>
                <div className="col">
                    <input
                        type="date"
                        name="start_date"
                        placeholder="Data de Início"
                        value={filters.start_date}
                        onChange={handleChange}
                        className="form-control"
                    />
                </div>
                <div className="col">
                    <input
                        type="date"
                        name="end_date"
                        placeholder="Data de Término"
                        value={filters.end_date}
                        onChange={handleChange}
                        className="form-control"
                    />
                </div>
                <div className="col">
                    <button type="submit" className="btn btn-primary">
                        Filtrar
                    </button>
                </div>
            </div>
        </form>
    );
};

export default FilterForm;