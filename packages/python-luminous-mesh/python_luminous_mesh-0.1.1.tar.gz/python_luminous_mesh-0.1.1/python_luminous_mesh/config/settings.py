from dataclasses import dataclass
from typing import Optional
import yaml
import os


@dataclass
class ClientSettings:
    """Configuration settings for the Luminous Mesh client."""

    # Node identification
    node_id: str
    hostname: str

    # Connection settings
    control_plane_endpoint: str
    bootstrap_token: Optional[str] = None

    # Intervals (in seconds)
    status_update_interval: int = 30
    token_rotation_interval: int = 3600  # 1 hour
    metrics_collection_interval: int = 60

    # Resource limits
    max_concurrent_tasks: int = 10
    max_memory_mb: int = 1024
    max_cpu_usage: float = 0.8

    # Paths
    cert_directory: str = "/etc/luminous-mesh/certs"
    config_directory: str = "/etc/luminous-mesh/config"

    @classmethod
    def from_yaml(cls, path: str) -> "ClientSettings":
        """Load settings from a YAML file."""
        with open(path, "r") as f:
            config = yaml.safe_load(f)
        return cls(**config)

    @classmethod
    def from_env(cls) -> "ClientSettings":
        """Load settings from environment variables."""
        return cls(
            node_id=os.environ["LUMINOUS_MESH_NODE_ID"],
            hostname=os.environ["HOSTNAME"],
            control_plane_endpoint=os.environ["LUMINOUS_MESH_CONTROL_PLANE"],
            bootstrap_token=os.environ.get("LUMINOUS_MESH_BOOTSTRAP_TOKEN"),
            status_update_interval=int(
                os.environ.get("LUMINOUS_MESH_STATUS_INTERVAL", "30")
            ),
            token_rotation_interval=int(
                os.environ.get("LUMINOUS_MESH_TOKEN_ROTATION", "3600")
            ),
            metrics_collection_interval=int(
                os.environ.get("LUMINOUS_MESH_METRICS_INTERVAL", "60")
            ),
            max_concurrent_tasks=int(os.environ.get("LUMINOUS_MESH_MAX_TASKS", "10")),
            max_memory_mb=int(os.environ.get("LUMINOUS_MESH_MAX_MEMORY", "1024")),
            max_cpu_usage=float(os.environ.get("LUMINOUS_MESH_MAX_CPU", "0.8")),
            cert_directory=os.environ.get(
                "LUMINOUS_MESH_CERT_DIR", "/etc/luminous-mesh/certs"
            ),
            config_directory=os.environ.get(
                "LUMINOUS_MESH_CONFIG_DIR", "/etc/luminous-mesh/config"
            ),
        )

    @property
    def cert_path(self) -> str:
        """Get the path to the node certificate."""
        return os.path.join(self.cert_directory, "node.crt")

    @property
    def key_path(self) -> str:
        """Get the path to the node private key."""
        return os.path.join(self.cert_directory, "node.key")

    @property
    def ca_cert_path(self) -> str:
        """Get the path to the CA certificate."""
        return os.path.join(self.cert_directory, "ca.crt")
