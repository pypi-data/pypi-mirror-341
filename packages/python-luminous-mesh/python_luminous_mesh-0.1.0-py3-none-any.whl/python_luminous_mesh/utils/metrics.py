import psutil
import time
from typing import List
from prometheus_client import CollectorRegistry, Gauge, Counter
import structlog

logger = structlog.get_logger()


class MetricsCollector:
    """Collects system and application metrics."""

    def __init__(self):
        self.registry = CollectorRegistry()

        self.cpu_usage = Gauge(
            "node_cpu_usage", "CPU usage percentage", registry=self.registry
        )
        self.memory_usage = Gauge(
            "node_memory_usage_bytes", "Memory usage in bytes", registry=self.registry
        )
        self.disk_usage = Gauge(
            "node_disk_usage_bytes", "Disk usage in bytes", registry=self.registry
        )

        self.active_tasks = Gauge(
            "node_active_tasks", "Number of active tasks", registry=self.registry
        )
        self.completed_tasks = Counter(
            "node_completed_tasks_total",
            "Total number of completed tasks",
            registry=self.registry,
        )
        self.failed_tasks = Counter(
            "node_failed_tasks_total",
            "Total number of failed tasks",
            registry=self.registry,
        )

    def collect_metrics(self) -> List[dict]:
        """Collect current metrics."""
        try:
            self.cpu_usage.set(psutil.cpu_percent())
            self.memory_usage.set(psutil.virtual_memory().used)
            self.disk_usage.set(psutil.disk_usage("/").used)

            # Convert to proto format
            metrics = []
            for metric in self.registry.collect():
                for sample in metric.samples:
                    metrics.append(
                        {
                            "metric_name": sample.name,
                            "value": sample.value,
                            "labels": dict(sample.labels),
                        }
                    )

            return metrics

        except Exception as e:
            logger.error("Failed to collect metrics", error=str(e))
            return []

    def record_task_start(self):
        """Record the start of a task."""
        self.active_tasks.inc()

    def record_task_completion(self, success: bool):
        """Record the completion of a task."""
        self.active_tasks.dec()
        if success:
            self.completed_tasks.inc()
        else:
            self.failed_tasks.inc()
