import { WebTracerProvider } from '@opentelemetry/sdk-trace-web';
import { BatchSpanProcessor } from '@opentelemetry/sdk-trace-base';
import { ZoneContextManager } from '@opentelemetry/context-zone';
import { Resource } from '@opentelemetry/resources';
import { SemanticResourceAttributes } from '@opentelemetry/semantic-conventions';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { registerInstrumentations } from '@opentelemetry/instrumentation';
import { getWebAutoInstrumentations } from '@opentelemetry/auto-instrumentations-web';

export function setupTracing() {
    const resource = new Resource({
        [SemanticResourceAttributes.SERVICE_NAME]: 'frontend',
        [SemanticResourceAttributes.DEPLOYMENT_ENVIRONMENT]: process.env.NODE_ENV || 'development',
    });

    const provider = new WebTracerProvider({ resource });

    const exporter = new OTLPTraceExporter({
        url: process.env.REACT_APP_OTEL_EXPORTER_OTLP_ENDPOINT || 'http://localhost:4318/v1/traces',
    });

    provider.addSpanProcessor(new BatchSpanProcessor(exporter));

    // Initialize the provider
    provider.register({
        contextManager: new ZoneContextManager(),
    });

    // Register auto instrumentations
    registerInstrumentations({
        instrumentations: [
            getWebAutoInstrumentations({
                // Instrument XMLHttpRequest
                '@opentelemetry/instrumentation-xml-http-request': {
                    enabled: true,
                    propagateTraceHeaderCorsUrls: [
                        /.+/g, // Propagate to all URLs
                    ],
                },
                // Instrument fetch
                '@opentelemetry/instrumentation-fetch': {
                    enabled: true,
                    propagateTraceHeaderCorsUrls: [
                        /.+/g, // Propagate to all URLs
                    ],
                },
            }),
        ],
    });
} 