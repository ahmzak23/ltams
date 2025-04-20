# Observability Demo Application

This project demonstrates modern observability practices using a microservices-based ticket booking system. It showcases the integration of logging, metrics, and distributed tracing with practical examples of alerts, dashboards, and observability configurations.

## Architecture

The application consists of the following components:

### Application Services
- Frontend (React)
- API Gateway (Node.js/Express)
- Backend Service (Python/FastAPI)
- Background Worker (Python)
- PostgreSQL Database

### Observability Stack
- OpenTelemetry Collector - Telemetry pipeline
- Prometheus - Metrics collection and storage
- Loki - Log aggregation
- Tempo - Distributed tracing backend
- Grafana - Visualization and dashboards
- AlertManager - Alert management and routing

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Make (optional, for using Makefile commands)

### Setup and Running

1. Clone the repository:
```bash
git clone <repository-url>
cd observability-demo
```

2. Start the application:
```bash
docker-compose up -d
```

3. Access the services:
- Frontend: http://localhost:3000
- Grafana: http://localhost:3001 (admin/admin)
- Prometheus: http://localhost:9090
- AlertManager: http://localhost:9093

## Project Structure

```
.
├── frontend/                 # React frontend application
├── api-gateway/             # Node.js API Gateway
├── backend/                 # Python/FastAPI backend service
├── worker/                  # Background worker service
├── observability/          # Observability configurations
│   ├── prometheus/        # Prometheus config and rules
│   ├── grafana/          # Grafana dashboards and provisioning
│   ├── loki/            # Loki configuration
│   ├── tempo/           # Tempo configuration
│   ├── otel-collector/  # OpenTelemetry Collector config
│   └── alertmanager/    # AlertManager configuration
└── docker-compose.yml    # Docker Compose configuration
```

## Observability Features

### Logging
- Structured JSON logging across all services
- Log correlation with trace IDs
- Centralized logging with Loki
- Log rotation and retention policies

### Metrics
- RED metrics (Rate, Error, Duration) for all endpoints
- USE metrics (Utilization, Saturation, Errors) for infrastructure
- Business metrics (bookings, users, conversion rates)
- Custom application metrics

### Distributed Tracing
- Full request tracing across services
- Span attributes for business context
- Database query tracing
- External API call tracing

### Dashboards
- Service-specific dashboards
- Cross-service dashboards
- Business metrics dashboards
- SLO dashboards
- Infrastructure dashboards

### Alerting
- Service health alerts
- Performance degradation alerts
- Error rate alerts
- Business metric anomaly alerts

## Development

### Adding New Services

1. Create a new service directory
2. Add service to docker-compose.yml
3. Implement OpenTelemetry instrumentation
4. Add service-specific dashboards
5. Configure appropriate alerts

### Modifying Observability Configuration

1. Update relevant configuration in observability/ directory
2. Restart affected services:
```bash
docker-compose restart <service-name>
```

## Production Considerations

- Secure credentials and sensitive configurations
- Implement proper retention policies for logs and metrics
- Configure appropriate sampling rates for traces
- Set up backup and disaster recovery
- Monitor storage usage for metrics and logs
- Implement proper access controls and authentication

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 