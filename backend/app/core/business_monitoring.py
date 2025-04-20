from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from .metrics import TICKETS_BY_STATUS, TICKETS_BY_PRIORITY

async def update_business_metrics(db: AsyncSession):
    """Update business-specific metrics."""
    # Get ticket counts by status
    status_query = text("""
        SELECT status, COUNT(*) 
        FROM tickets 
        GROUP BY status
    """)
    result = await db.execute(status_query)
    for status, count in result:
        TICKETS_BY_STATUS.labels(status=status).set(count)
    
    # Get ticket counts by priority
    priority_query = text("""
        SELECT priority, COUNT(*) 
        FROM tickets 
        GROUP BY priority
    """)
    result = await db.execute(priority_query)
    for priority, count in result:
        TICKETS_BY_PRIORITY.labels(priority=priority).set(count) 