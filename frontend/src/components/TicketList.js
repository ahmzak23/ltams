import React, { useState, useEffect } from 'react';
import { getTickets, deleteTicket } from '../utils/api';

const TicketList = () => {
    const [tickets, setTickets] = useState([]);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchTickets();
    }, []);

    const fetchTickets = async () => {
        try {
            const data = await getTickets();
            setTickets(data);
            setLoading(false);
        } catch (err) {
            setError('Failed to fetch tickets');
            setLoading(false);
        }
    };

    const handleDelete = async (id) => {
        try {
            await deleteTicket(id);
            setTickets(tickets.filter(ticket => ticket.id !== id));
        } catch (err) {
            setError('Failed to delete ticket');
        }
    };

    if (loading) return <div>Loading...</div>;
    if (error) return <div className="error">{error}</div>;

    return (
        <div className="ticket-list">
            <h2>Tickets</h2>
            {tickets.length === 0 ? (
                <p>No tickets found</p>
            ) : (
                <div className="tickets-grid">
                    {tickets.map((ticket) => (
                        <div key={ticket.id} className="ticket-card">
                            <h3>{ticket.title}</h3>
                            <p>{ticket.description}</p>
                            <div className="ticket-details">
                                <span>Price: ${ticket.price}</span>
                                <span>Quantity: {ticket.quantity}</span>
                                <span>Status: {ticket.status}</span>
                            </div>
                            <div className="ticket-actions">
                                <button onClick={() => handleDelete(ticket.id)}>
                                    Delete
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default TicketList; 