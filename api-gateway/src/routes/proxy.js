const express = require('express');
const axios = require('axios');
const logger = require('../utils/logger');

const router = express.Router();
const BACKEND_URL = process.env.BACKEND_URL || 'http://backend:8000';

// Proxy middleware
const proxyRequest = async (req, res, next) => {
    const requestId = req.headers['x-request-id'];
    const startTime = Date.now();

    try {
        const response = await axios({
            method: req.method,
            url: `${BACKEND_URL}${req.path}`,
            data: req.body,
            headers: {
                ...req.headers,
                host: new URL(BACKEND_URL).host
            },
            params: req.query
        });

        const duration = Date.now() - startTime;
        logger.info('Proxied request completed', {
            path: req.path,
            method: req.method,
            statusCode: response.status,
            duration,
            requestId
        });

        res.status(response.status).json(response.data);
    } catch (error) {
        if (error.response) {
            const duration = Date.now() - startTime;
            logger.error('Proxy request failed', {
                path: req.path,
                method: req.method,
                statusCode: error.response.status,
                error: error.message,
                duration,
                requestId
            });

            res.status(error.response.status).json(error.response.data);
        } else {
            next(error);
        }
    }
};

// Proxy all API requests
router.all('/api/*', proxyRequest);

// Health check endpoint
router.get('/health', (req, res) => {
    res.json({ status: 'healthy' });
});

module.exports = router; 