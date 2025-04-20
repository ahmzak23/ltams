import React from 'react';
import { Link } from 'react-router-dom';
import TicketList from '../components/TicketList';

const TicketsPage = () => {
    return (
        <div className="tickets-page">
            <div className="container">
                <div className="header">
                    <h1>Tickets</h1>
                    <Link to="/tickets/create" className="create-button">
                        Create New Ticket
                    </Link>
                </div>
                <TicketList />
            </div>
        </div>
    );
};

export default TicketsPage; 