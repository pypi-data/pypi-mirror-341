import platform
import socket
import psutil
from typing import Dict, List
import structlog

logger = structlog.get_logger()


class NodeStatusManager:
    """Manages node status information."""

    def __init__(self):
        self._hostname = socket.gethostname()
        self._ip_address = socket.gethostbyname(self._hostname)
        self._version = "0.1.0"  # Should match package version
        self._architecture = platform.machine()
        self._state = "HEALTHY"
        self._status_message = "Node is healthy"

    def get_basic_info(self) -> Dict:
        """Get basic node information."""
        return {
            "hostname": self._hostname,
            "ip_address": self._ip_address,
            "version": self._version,
            "supported_model_types": ["cpu", "gpu"] if self._has_gpu() else ["cpu"],
            "architecture": self._architecture,
        }

    def get_capabilities(self) -> Dict:
        """Get node capabilities."""
        return {
            "cpu_cores": psutil.cpu_count(),
            "memory_total": psutil.virtual_memory().total,
            "disk_total": psutil.disk_usage("/").total,
            "gpu_available": self._has_gpu(),
            "supported_features": self._get_supported_features(),
        }

    def get_current_status(self) -> Dict:
        """Get current node status."""
        resources = self._get_resource_status()
        return {
            "state": self._state,
            "status_message": self._status_message,
            "resources": resources,
        }

    def update_status(self, state: str, message: str):
        """Update node status."""
        self._state = state
        self._status_message = message
        logger.info("Node status updated", state=state, message=message)

    def _has_gpu(self) -> bool:
        """Check if GPU is available."""
        try:
            import torch

            return torch.cuda.is_available()
        except ImportError:
            return False

    def _get_supported_features(self) -> List[str]:
        """Get list of supported features."""
        features = ["streaming", "metrics", "health_check"]
        if self._has_gpu():
            features.append("gpu_acceleration")
        return features

    def _get_resource_status(self) -> Dict[str, Dict]:
        """Get current resource status."""
        cpu_percent = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")

        resources = {
            "cpu": {
                "name": "CPU",
                "usage_percentage": cpu_percent,
                "status": "healthy" if cpu_percent < 80 else "warning",
            },
            "memory": {
                "name": "Memory",
                "usage_percentage": memory.percent,
                "status": "healthy" if memory.percent < 80 else "warning",
            },
            "disk": {
                "name": "Disk",
                "usage_percentage": disk.percent,
                "status": "healthy" if disk.percent < 80 else "warning",
            },
        }

        # if self._has_gpu():
        #     import torch

        #     gpu_memory = (
        #         torch.cuda.memory_allocated(0)
        #         / torch.cuda.get_device_properties(0).total_memory
        #         * 100
        #     )
        #     resources["gpu"] = {
        #         "name": "GPU",
        #         "usage_percentage": gpu_memory,
        #         "status": "healthy" if gpu_memory < 80 else "warning",
        #     }

        return resources
