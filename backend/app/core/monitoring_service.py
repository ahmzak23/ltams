import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from .system_monitoring import update_system_metrics
from .db_monitoring import update_db_metrics
from .business_monitoring import update_business_metrics

class MonitoringService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self._running = False
        self._task = None

    async def start(self):
        """Start the monitoring service."""
        if not self._running:
            self._running = True
            self._task = asyncio.create_task(self._monitoring_loop())

    async def stop(self):
        """Stop the monitoring service."""
        if self._running:
            self._running = False
            if self._task:
                self._task.cancel()
                try:
                    await self._task
                except asyncio.CancelledError:
                    pass

    async def _monitoring_loop(self):
        """Main monitoring loop that collects all metrics."""
        while self._running:
            try:
                # Update system metrics
                await update_system_metrics()
                
                # Update database metrics
                await update_db_metrics(self.db)
                
                # Update business metrics
                await update_business_metrics(self.db)
                
                # Wait for 15 seconds before next collection
                await asyncio.sleep(15)
            except Exception as e:
                # Log the error but continue monitoring
                print(f"Error in monitoring loop: {e}")
                await asyncio.sleep(5)  # Wait a bit before retrying 