from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import time
from .metrics import API_REQUESTS, API_RESPONSE_TIME
import psutil
from prometheus_client import start_http_server
from .metrics import (
    MEMORY_USED, CPU_USAGE, DISK_USED,
    REQUEST_COUNT, REQUEST_LATENCY, ERROR_COUNT,
    MEMORY_USAGE, DISK_USAGE,
    DB_ACTIVE_CONNECTIONS, DB_TRANSACTIONS,
    DB_QUERY_DURATION, DB_LOCK_CONTENTION,
    DB_CACHE_HIT_RATIO,
    TICKETS_BY_STATUS, TICKETS_BY_PRIORITY
)
from .db_monitoring import update_db_metrics
import asyncio
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

class MonitoringMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Process the request
        response = await call_next(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Record metrics
        API_REQUESTS.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code
        ).inc()
        
        API_RESPONSE_TIME.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(duration)
        
        return response 

def collect_system_metrics():
    """Collect system metrics and update Prometheus gauges."""
    # Memory metrics
    memory = psutil.virtual_memory()
    MEMORY_USED.set(memory.used)
    
    # CPU metrics
    CPU_USAGE.set(psutil.cpu_percent())
    
    # Disk metrics
    disk = psutil.disk_usage('/')
    DISK_USED.set(disk.used)

def track_request_metrics(method: str, endpoint: str, status: int, duration: float):
    """Track HTTP request metrics."""
    REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status).inc()
    REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(duration)

def track_error(method: str, endpoint: str, error_type: str):
    """Track HTTP error metrics."""
    ERROR_COUNT.labels(method=method, endpoint=endpoint, error_type=error_type).inc()

def start_metrics_server(port: int = 8000):
    """Start the Prometheus metrics server."""
    start_http_server(port)

def update_metrics():
    """Update all metrics periodically."""
    while True:
        try:
            collect_system_metrics()
            update_db_metrics()
            time.sleep(15)  # Update every 15 seconds
        except Exception as e:
            print(f"Error updating metrics: {e}")
            time.sleep(15)  # Wait before retrying 

class MonitoringService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self._running = False
        self._task = None

    async def start(self):
        """Start the monitoring service"""
        if not self._running:
            self._running = True
            self._task = asyncio.create_task(self._monitor_loop())

    async def stop(self):
        """Stop the monitoring service"""
        if self._running:
            self._running = False
            if self._task:
                self._task.cancel()
                try:
                    await self._task
                except asyncio.CancelledError:
                    pass

    async def _monitor_loop(self):
        """Main monitoring loop"""
        while self._running:
            try:
                # Update system metrics
                self._update_system_metrics()
                
                # Update database metrics
                await update_db_metrics(self.db_session)
                
                # Update business metrics
                await self._update_business_metrics()
                
                # Wait for next update interval
                await asyncio.sleep(15)  # Update every 15 seconds
                
            except Exception as e:
                print(f"Error in monitoring loop: {e}")
                await asyncio.sleep(5)  # Wait before retrying

    def _update_system_metrics(self):
        """Update system-level metrics"""
        # Memory usage
        memory = psutil.virtual_memory()
        MEMORY_USAGE.set(memory.used)
        
        # CPU usage
        CPU_USAGE.set(psutil.cpu_percent())
        
        # Disk usage
        disk = psutil.disk_usage('/')
        DISK_USAGE.set(disk.percent)

    async def _update_business_metrics(self):
        """Update business-level metrics"""
        # Get ticket counts by status
        status_query = """
            SELECT status, COUNT(*) as count
            FROM tickets
            GROUP BY status
        """
        result = await self.db_session.execute(status_query)
        for status, count in result:
            TICKETS_BY_STATUS.labels(status=status).set(count)

        # Get ticket counts by priority
        priority_query = """
            SELECT priority, COUNT(*) as count
            FROM tickets
            GROUP BY priority
        """
        result = await self.db_session.execute(priority_query)
        for priority, count in result:
            TICKETS_BY_PRIORITY.labels(priority=priority).set(count) 