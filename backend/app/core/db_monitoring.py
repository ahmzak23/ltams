from sqlalchemy import event, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
import time
from .metrics import (
    DB_CONNECTIONS,
    DB_QUERY_DURATION,
    DB_TRANSACTIONS,
    DB_LOCK_CONTENTION,
    DB_CACHE_HIT_RATIO,
    DB_ACTIVE_CONNECTIONS
)
from .database import SessionLocal
from sqlalchemy.ext.asyncio import AsyncSession

def setup_db_monitoring(engine: Engine):
    @event.listens_for(engine, 'connect')
    def receive_connect(dbapi_connection, connection_record):
        DB_CONNECTIONS.inc()
    
    @event.listens_for(engine, 'checkout')
    def receive_checkout(dbapi_connection, connection_record, connection_proxy):
        DB_CONNECTIONS.inc()
    
    @event.listens_for(engine, 'checkin')
    def receive_checkin(dbapi_connection, connection_record):
        DB_CONNECTIONS.dec()
    
    @event.listens_for(engine, 'begin')
    def receive_begin(conn):
        DB_TRANSACTIONS.inc()
    
    @event.listens_for(engine, 'commit')
    def receive_commit(conn):
        DB_TRANSACTIONS.dec()
    
    @event.listens_for(engine, 'rollback')
    def receive_rollback(conn):
        DB_TRANSACTIONS.dec()
    
    @event.listens_for(Engine, 'before_cursor_execute')
    def before_cursor_execute(session, cursor, statement, parameters, context, executemany):
        context._query_start_time = time.time()
    
    @event.listens_for(Engine, 'after_cursor_execute')
    def after_cursor_execute(session, cursor, statement, parameters, context, executemany):
        total = time.time() - context._query_start_time
        DB_QUERY_DURATION.labels(
            operation=statement.split()[0].upper()
        ).observe(total)
    
    @event.listens_for(Engine, 'handle_error')
    def handle_error(context):
        if 'lock' in str(context.original_exception).lower():
            DB_LOCK_CONTENTION.inc()
        
    # Monitor cache hit ratio (simplified example)
    @event.listens_for(engine, 'before_cursor_execute')
    def monitor_cache(session, cursor, statement, parameters, context, executemany):
        # This is a simplified example. In a real implementation, you would
        # need to track actual cache hits and misses from your database
        DB_CACHE_HIT_RATIO.set(0.95)  # Example value 

async def update_db_metrics(db_session: AsyncSession):
    """Update all database-related metrics"""
    await update_connection_metrics(db_session)
    await update_transaction_metrics(db_session)
    await update_lock_metrics(db_session)
    await update_cache_metrics(db_session)

async def update_connection_metrics(db_session: AsyncSession):
    """Update database connection metrics"""
    query = """
        SELECT count(*) 
        FROM pg_stat_activity 
        WHERE datname = current_database()
    """
    result = await db_session.execute(query)
    count = result.scalar()
    DB_ACTIVE_CONNECTIONS.set(count)

async def update_transaction_metrics(db_session: AsyncSession):
    """Update transaction-related metrics"""
    query = """
        SELECT 
            xact_commit,
            xact_rollback
        FROM pg_stat_database 
        WHERE datname = current_database()
    """
    result = await db_session.execute(query)
    row = result.first()
    if row:
        DB_TRANSACTIONS.labels(type='commit').set(row[0])
        DB_TRANSACTIONS.labels(type='rollback').set(row[1])

async def update_lock_metrics(db_session: AsyncSession):
    """Update database lock metrics"""
    query = """
        SELECT count(*) 
        FROM pg_locks 
        WHERE granted = false
    """
    result = await db_session.execute(query)
    count = result.scalar()
    DB_LOCK_CONTENTION.set(count)

async def update_cache_metrics(db_session: AsyncSession):
    """Update database cache metrics"""
    query = """
        SELECT 
            sum(heap_blks_hit)::float / 
            nullif(sum(heap_blks_hit) + sum(heap_blks_read), 0) * 100
        FROM pg_statio_user_tables
    """
    result = await db_session.execute(query)
    hit_ratio = result.scalar() or 0
    DB_CACHE_HIT_RATIO.set(hit_ratio)

def record_query_duration(duration: float, query_type: str):
    """Record the duration of a database query."""
    DB_QUERY_DURATION.labels(query_type=query_type).observe(duration) 