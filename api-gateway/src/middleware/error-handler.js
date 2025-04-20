const logger = require('../utils/logger');

const errorHandler = (err, req, res, next) => {
    logger.error('Error occurred', {
        error: err.message,
        stack: err.stack,
        path: req.path,
        method: req.method,
        requestId: req.headers['x-request-id']
    });

    res.status(err.status || 500).json({
        error: {
            message: err.message,
            status: err.status || 500,
            requestId: req.headers['x-request-id']
        }
    });
};

module.exports = errorHandler; 