import psutil
from .metrics import MEMORY_USAGE, CPU_USAGE, DISK_USAGE

def update_system_metrics():
    """Update system metrics."""
    # Memory usage
    memory = psutil.virtual_memory()
    MEMORY_USAGE.set(memory.used)
    
    # CPU usage
    cpu_percent = psutil.cpu_percent(interval=1)
    CPU_USAGE.set(cpu_percent)
    
    # Disk usage
    disk = psutil.disk_usage('/')
    DISK_USAGE.set(disk.percent) 