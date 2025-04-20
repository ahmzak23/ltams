from prometheus_client import Counter, Gauge, Histogram
from prometheus_client.metrics import MetricWrapperBase

# API Metrics
API_REQUESTS = Counter(
    'api_requests_total',
    'Total number of API requests',
    ['method', 'endpoint', 'status']
)

API_RESPONSE_TIME = Histogram(
    'api_response_time_seconds',
    'API response time in seconds',
    ['method', 'endpoint']
)

# Service Health Metrics
SERVICE_HEALTH = Gauge(
    'service_health',
    'Service health status (1=healthy, 0=unhealthy)',
    ['service']
)

# Database Metrics
DB_CONNECTIONS = Gauge(
    'db_connections',
    'Number of active database connections'
)

DB_QUERY_DURATION = Histogram(
    'db_query_duration_seconds',
    'Database query duration in seconds',
    ['operation']
)

DB_TRANSACTIONS = Gauge(
    'db_transactions',
    'Number of active database transactions'
)

DB_LOCK_CONTENTION = Counter(
    'db_lock_contention_total',
    'Total number of database lock contentions'
)

DB_CACHE_HIT_RATIO = Gauge(
    'db_cache_hit_ratio',
    'Database cache hit ratio'
)

# Business Metrics
TICKETS_CREATED = Counter(
    'tickets_created_total',
    'Total number of tickets created',
    ['priority', 'category']
)

TICKETS_RESOLVED = Counter(
    'tickets_resolved_total',
    'Total number of tickets resolved',
    ['priority', 'category']
)

TICKET_RESOLUTION_TIME = Histogram(
    'ticket_resolution_time_seconds',
    'Time taken to resolve tickets',
    ['priority', 'category']
)

# User Metrics
ACTIVE_USERS = Gauge(
    'active_users',
    'Number of active users',
    ['role']
)

USER_LOGINS = Counter(
    'user_logins_total',
    'Total number of user logins',
    ['role']
)

# System Metrics
SYSTEM_MEMORY_USAGE = Gauge(
    'system_memory_bytes',
    'System memory usage in bytes'
)

SYSTEM_CPU_USAGE = Gauge(
    'system_cpu_percent',
    'System CPU usage percentage'
)

SYSTEM_DISK_USAGE = Gauge(
    'system_disk_bytes',
    'System disk usage in bytes'
)

# System metrics
MEMORY_USED = Gauge('memory_used_bytes', 'Memory used in bytes')
CPU_USAGE = Gauge('cpu_usage_percent', 'CPU usage percentage')
DISK_USED = Gauge('disk_used_bytes', 'Disk space used in bytes')

# Application Metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency in seconds', ['method', 'endpoint'])
ERROR_COUNT = Counter('http_errors_total', 'Total HTTP errors', ['method', 'endpoint', 'error_type'])

# System metrics
MEMORY_USAGE = Gauge('memory_usage_bytes', 'Memory usage in bytes')
CPU_USAGE = Gauge('cpu_usage_percent', 'CPU usage percentage')
DISK_USAGE = Gauge('disk_usage_percent', 'Disk usage percentage')

# HTTP metrics
HTTP_REQUESTS = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
HTTP_REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration in seconds', ['method', 'endpoint'])

# Error metrics
ERROR_COUNT = Counter('error_total', 'Total number of errors', ['type', 'component'])

# Database metrics
DB_ACTIVE_CONNECTIONS = Gauge('db_active_connections', 'Number of active database connections')
DB_TRANSACTIONS = Counter('db_transactions_total', 'Total number of database transactions', ['type'])
DB_QUERY_DURATION = Histogram(
    'db_query_duration_seconds',
    'Database query duration in seconds',
    ['query_type'],
    buckets=(0.1, 0.5, 1.0, 2.0, 5.0, 10.0)
)
DB_LOCK_CONTENTION = Gauge('db_lock_contention', 'Number of contended database locks')
DB_CACHE_HIT_RATIO = Gauge('db_cache_hit_ratio', 'Database cache hit ratio')

# Query Metrics
QUERY_DURATION = Histogram(
    'query_duration_seconds',
    'Duration of database queries in seconds',
    ['query_type'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
)

# Business Metrics
TICKETS_BY_STATUS = Gauge('tickets_by_status', 'Number of tickets by status', ['status'])
TICKETS_BY_PRIORITY = Gauge('tickets_by_priority', 'Number of tickets by priority', ['priority'])

# API Metrics
API_REQUEST_DURATION = Histogram(
    'api_request_duration_seconds',
    'API request duration in seconds',
    ['method', 'endpoint', 'status']
)
API_REQUEST_COUNT = Counter(
    'api_request_total',
    'Total number of API requests',
    ['method', 'endpoint', 'status']
)

def get_all_metrics() -> list[MetricWrapperBase]:
    """Return all metrics for registration."""
    return [
        # Database metrics
        DB_CONNECTIONS, DB_QUERY_DURATION, DB_TRANSACTIONS,
        DB_LOCK_CONTENTION, DB_CACHE_HIT_RATIO,
        
        # API metrics
        API_REQUESTS, API_RESPONSE_TIME,
        
        # Service health metrics
        SERVICE_HEALTH,
        
        # Business metrics
        TICKETS_CREATED, TICKETS_RESOLVED, TICKET_RESOLUTION_TIME,
        
        # User metrics
        ACTIVE_USERS, USER_LOGINS,
        
        # System metrics
        SYSTEM_MEMORY_USAGE, SYSTEM_CPU_USAGE, SYSTEM_DISK_USAGE,
        
        # Additional system metrics
        MEMORY_USED, CPU_USAGE, DISK_USED,
        
        # Application metrics
        REQUEST_COUNT, REQUEST_LATENCY, ERROR_COUNT,
        
        # Query metrics
        QUERY_DURATION,
        
        # Business metrics
        TICKETS_BY_STATUS, TICKETS_BY_PRIORITY,
        
        # API metrics
        API_REQUEST_DURATION, API_REQUEST_COUNT
    ] 