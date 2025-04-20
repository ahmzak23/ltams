const logger = require('../utils/logger');

const loggingMiddleware = (req, res, next) => {
    const start = Date.now();
    const { method, url, headers } = req;

    res.on('finish', () => {
        const duration = Date.now() - start;
        const { statusCode } = res;

        logger.info('Request processed', {
            method,
            url,
            statusCode,
            duration,
            requestId: headers['x-request-id'],
            userAgent: headers['user-agent']
        });
    });

    next();
};

module.exports = loggingMiddleware; 