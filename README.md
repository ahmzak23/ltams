# LTMAS (Logging, Tracking, Alerting & Monitoring Systems)

A comprehensive system for logging, tracking, alerting, and monitoring applications and services.

## Overview

LTMAS provides a centralized platform for:
- Logging and log aggregation
- Request tracking and tracing
- Alerting and notification
- System and application monitoring
- Performance metrics collection and visualization

## Architecture

The system consists of the following components:

- **Frontend**: React-based web interface
- **API Gateway**: Entry point for all API requests
- **Backend**: Core business logic and data processing
- **Worker**: Background task processing
- **Database**: PostgreSQL for data storage
- **Monitoring**: Prometheus for metrics collection and Grafana for visualization
- **Logging**: ELK Stack (Elasticsearch, Logstash, Kibana) for log management
- **Tracing**: Jaeger for distributed tracing
- **Alerting**: Alertmanager for alert routing and notification

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js (for local development)
- Python 3.9+ (for local development)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ltmas.git
   cd ltmas
   ```

2. Start the services:
   ```
   docker-compose up -d
   ```

3. Access the application:
   - Frontend: http://localhost:3000
   - API Gateway: http://localhost:8000
   - Grafana: http://localhost:3001
   - Kibana: http://localhost:5601
   - Jaeger: http://localhost:16686

## Monitoring Dashboards

LTMAS provides several pre-configured Grafana dashboards for monitoring different aspects of the system:

### Database Team Dashboard
- **URL**: http://localhost:3001/d/ltmas-database/ltmas-database-team
- **Description**: Monitors database performance, connections, transactions, and cache hit ratio
- **Key Metrics**: Active connections, transaction counts, database size, cache hit ratio

### System Team Dashboard
- **URL**: http://localhost:3001/d/ltmas-system/ltmas-system-team
- **Description**: Tracks system resources including CPU, memory, and disk usage
- **Key Metrics**: CPU utilization, memory usage, disk space, network I/O

### API Team Dashboard
- **URL**: http://localhost:3001/d/ltmas-api/ltmas-api-team
- **Description**: Monitors API performance and usage patterns
- **Key Metrics**: Request counts, response times, error rates, endpoint usage

### Business Team Dashboard
- **URL**: http://localhost:3001/d/ltmas-business/ltmas-business-team
- **Description**: Tracks business metrics and KPIs
- **Key Metrics**: Ticket counts by status and priority, resolution times, user activity

## Configuration

Configuration files are located in the `config` directory:
- `config/prometheus.yml`: Prometheus configuration
- `config/grafana/provisioning`: Grafana datasources and dashboards
- `config/alertmanager.yml`: Alertmanager configuration
- `config/logstash/pipeline`: Logstash pipeline configuration

## Development

### Local Development

1. Install dependencies:
   ```
   # Frontend
   cd frontend
   npm install

   # Backend
   cd backend
   pip install -r requirements.txt
   ```

2. Start development servers:
   ```
   # Frontend
   cd frontend
   npm run dev

   # Backend
   cd backend
   uvicorn app.main:app --reload
   ```

### Testing

```
# Frontend
cd frontend
npm test

# Backend
cd backend
pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Prometheus](https://prometheus.io/)
- [Grafana](https://grafana.com/)
- [ELK Stack](https://www.elastic.co/elastic-stack)
- [Jaeger](https://www.jaegertracing.io/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://reactjs.org/) 