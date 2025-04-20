import React, { useState } from 'react';
import { createTicket } from '../utils/api';
import { useNavigate } from 'react-router-dom';

const CreateTicket = () => {
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [price, setPrice] = useState('');
    const [quantity, setQuantity] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await createTicket({
                title,
                description,
                price: parseFloat(price),
                quantity: parseInt(quantity),
            });
            navigate('/tickets');
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to create ticket');
        }
    };

    return (
        <div className="create-ticket">
            <h2>Create New Ticket</h2>
            {error && <div className="error">{error}</div>}
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Title:</label>
                    <input
                        type="text"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>Description:</label>
                    <textarea
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>Price:</label>
                    <input
                        type="number"
                        step="0.01"
                        value={price}
                        onChange={(e) => setPrice(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>Quantity:</label>
                    <input
                        type="number"
                        value={quantity}
                        onChange={(e) => setQuantity(e.target.value)}
                        required
                    />
                </div>
                <button type="submit">Create Ticket</button>
            </form>
        </div>
    );
};

export default CreateTicket; 