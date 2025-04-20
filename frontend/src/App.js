import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import TicketsPage from './pages/TicketsPage';
import CreateTicketPage from './pages/CreateTicketPage';
import { setupTracing } from './utils/tracing';
import './App.css';

function App() {
    useEffect(() => {
        setupTracing();
    }, []);

    const isAuthenticated = () => {
        return !!localStorage.getItem('token');
    };

    const PrivateRoute = ({ children }) => {
        return isAuthenticated() ? children : <Navigate to="/login" />;
    };

    return (
        <Router>
            <div className="app">
                <Routes>
                    <Route path="/login" element={<LoginPage />} />
                    <Route
                        path="/tickets"
                        element={
                            <PrivateRoute>
                                <TicketsPage />
                            </PrivateRoute>
                        }
                    />
                    <Route
                        path="/tickets/create"
                        element={
                            <PrivateRoute>
                                <CreateTicketPage />
                            </PrivateRoute>
                        }
                    />
                    <Route path="/" element={<Navigate to="/tickets" />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App; 