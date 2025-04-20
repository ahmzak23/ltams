import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:4000';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor for adding auth token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor for handling errors
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            localStorage.removeItem('token');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

export const login = async (email, password) => {
    const response = await api.post('/api/v1/login/access-token', {
        username: email,
        password,
    });
    return response.data;
};

export const signup = async (userData) => {
    const response = await api.post('/api/v1/signup', userData);
    return response.data;
};

export const getTickets = async () => {
    const response = await api.get('/api/v1/tickets');
    return response.data;
};

export const createTicket = async (ticketData) => {
    const response = await api.post('/api/v1/tickets', ticketData);
    return response.data;
};

export const updateTicket = async (id, ticketData) => {
    const response = await api.put(`/api/v1/tickets/${id}`, ticketData);
    return response.data;
};

export const deleteTicket = async (id) => {
    const response = await api.delete(`/api/v1/tickets/${id}`);
    return response.data;
};

export const getCurrentUser = async () => {
    const response = await api.get('/api/v1/users/me');
    return response.data;
}; 