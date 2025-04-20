require('./utils/tracing').setupTracing();

const express = require('express');
const cors = require('cors');
const logger = require('./utils/logger');
const metricsMiddleware = require('./middleware/metrics');
const loggingMiddleware = require('./middleware/logging');
const errorHandler = require('./middleware/error-handler');
const proxyRoutes = require('./routes/proxy');

const app = express();
const PORT = process.env.PORT || 4000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(metricsMiddleware);
app.use(loggingMiddleware);

// Routes
app.use('/', proxyRoutes);

// Error handling
app.use(errorHandler);

// Start server
app.listen(PORT, () => {
    logger.info(`API Gateway listening on port ${PORT}`);
}); 