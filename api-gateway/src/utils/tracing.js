const opentelemetry = require('@opentelemetry/sdk-node');
const { getNodeAutoInstrumentations } = require('@opentelemetry/auto-instrumentations-node');
const { Resource } = require('@opentelemetry/resources');
const { SemanticResourceAttributes } = require('@opentelemetry/semantic-conventions');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-proto');

function setupTracing() {
    const sdk = new opentelemetry.NodeSDK({
        resource: new Resource({
            [SemanticResourceAttributes.SERVICE_NAME]: 'api-gateway',
            [SemanticResourceAttributes.DEPLOYMENT_ENVIRONMENT]: process.env.NODE_ENV || 'development',
        }),
        traceExporter: new OTLPTraceExporter({
            url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT || 'http://otel-collector:4318/v1/traces',
        }),
        instrumentations: [getNodeAutoInstrumentations()],
    });

    sdk.start()
        .then(() => console.log('Tracing initialized'))
        .catch((error) => console.log('Error initializing tracing', error));

    process.on('SIGTERM', () => {
        sdk.shutdown()
            .then(() => console.log('Tracing terminated'))
            .catch((error) => console.log('Error terminating tracing', error))
            .finally(() => process.exit(0));
    });
}

module.exports = { setupTracing }; 