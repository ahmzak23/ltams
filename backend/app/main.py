from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from prometheus_client import make_asgi_app
from .core.monitoring_service import MonitoringService
from .core.metrics import get_all_metrics

from app.core.config import settings
from app.db.session import engine
from app.api.api_v1.api import api_router

# Initialize tracing
resource = Resource.create(attributes={
    "service.name": "backend",
    "environment": "development"
})

trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

# Configure OTLP exporter
otlp_exporter = OTLPSpanExporter(endpoint=settings.OTEL_EXPORTER_OTLP_ENDPOINT)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

app = FastAPI(
    title="Ticket Booking API",
    description="Backend API for the ticket booking system",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Initialize monitoring service
monitoring_service = None

@app.on_event("startup")
async def startup_event():
    global monitoring_service
    from .db.session import async_session
    monitoring_service = MonitoringService(async_session)
    await monitoring_service.start()

@app.on_event("shutdown")
async def shutdown_event():
    if monitoring_service:
        await monitoring_service.stop()

# Include API router
app.include_router(api_router, prefix="/api/v1")

# Instrument FastAPI
FastAPIInstrumentor.instrument_app(app)

# Instrument SQLAlchemy
SQLAlchemyInstrumentor().instrument(engine=engine)

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 