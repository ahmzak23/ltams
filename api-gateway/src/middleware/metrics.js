const promBundle = require('express-prom-bundle');

const metricsMiddleware = promBundle({
    includeMethod: true,
    includePath: true,
    includeStatusCode: true,
    includeUp: true,
    customLabels: { service: 'api-gateway' },
    promClient: {
        collectDefaultMetrics: {
            timeout: 5000
        }
    }
});

module.exports = metricsMiddleware; 