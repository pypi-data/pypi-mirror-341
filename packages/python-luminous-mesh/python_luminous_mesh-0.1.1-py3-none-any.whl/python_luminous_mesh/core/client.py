import grpc
import time
from typing import Optional, Dict, Any
import structlog
from tenacity import retry, stop_after_attempt, wait_exponential

from ..auth.credentials import CredentialsManager
from ..config.settings import ClientSettings
from ..utils.metrics import MetricsCollector
from ..utils.status import NodeStatusManager

logger = structlog.get_logger()


class LuminousMeshClient:
    """Main client class for interacting with the Luminous Mesh control plane."""

    def __init__(
        self,
        settings: ClientSettings,
        credentials_manager: Optional[CredentialsManager] = None,
    ):
        self.settings = settings
        self.credentials_manager = credentials_manager or CredentialsManager()
        self.status_manager = NodeStatusManager()
        self.metrics_collector = MetricsCollector()
        self._channel = None
        self._stub = None
        self._session_id = None

    async def connect(self) -> bool:
        """Establish connection with the control plane."""
        try:
            credentials = await self.credentials_manager.get_credentials()
            self._channel = grpc.aio.secure_channel(
                self.settings.control_plane_endpoint, credentials
            )

            self._stub = NodeServiceStub(self._channel)

            # Perform authentication
            auth_response = await self._authenticate()
            if not auth_response.success:
                logger.error("Authentication failed", error=auth_response.message)
                return False

            self._session_id = auth_response.session_id

            # Start background tasks
            await self._start_background_tasks()

            logger.info("Successfully connected to control plane")
            return True

        except Exception as e:
            logger.error("Failed to connect", error=str(e))
            return False

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def _authenticate(self) -> AuthenticationResponse:
        """Perform authentication with the control plane."""
        request = AuthenticationRequest(
            node_id=self.settings.node_id,
            auth_token=await self.credentials_manager.get_auth_token(),
            certificate=await self.credentials_manager.get_certificate(),
            basic_info=self.status_manager.get_basic_info(),
            capabilities=self.status_manager.get_capabilities(),
        )
        return await self._stub.Authenticate(request)

    async def _start_background_tasks(self):
        """Start background tasks for streaming, metrics, and token rotation."""
        # Start status streaming
        self._status_stream_task = asyncio.create_task(self._stream_status())

        # Start token rotation
        self._token_rotation_task = asyncio.create_task(
            self._rotate_token_periodically()
        )

    async def _stream_status(self):
        """Stream node status updates to control plane."""
        while True:
            try:
                async for command in self._stub.StreamConnection(
                    self._generate_status_updates()
                ):
                    await self._handle_command(command)
            except Exception as e:
                logger.error("Status stream error", error=str(e))
                await asyncio.sleep(5)  # Wait before reconnecting

    async def _generate_status_updates(self):
        """Generate status updates for streaming."""
        while True:
            status_update = NodeStatusUpdate(
                node_id=self.settings.node_id,
                session_id=self._session_id,
                status=self.status_manager.get_current_status(),
                metrics=self.metrics_collector.collect_metrics(),
                timestamp=int(time.time()),
            )
            yield status_update
            await asyncio.sleep(self.settings.status_update_interval)

    async def _handle_command(self, command: ControlPlaneCommand):
        """Handle incoming commands from control plane."""
        try:
            if command.HasField("config_update"):
                await self._handle_config_update(command.config_update)
            elif command.HasField("health_check"):
                await self._handle_health_check(command.health_check)
            elif command.HasField("disconnect"):
                await self._handle_disconnect(command.disconnect)
        except Exception as e:
            logger.error(
                "Error handling command", command_id=command.command_id, error=str(e)
            )

    async def _rotate_token_periodically(self):
        """Periodically rotate authentication token."""
        while True:
            await asyncio.sleep(self.settings.token_rotation_interval)
            try:
                response = await self._stub.RotateToken(
                    TokenRotationRequest(
                        node_id=self.settings.node_id,
                        current_token=await self.credentials_manager.get_auth_token(),
                        session_id=self._session_id,
                    )
                )
                await self.credentials_manager.update_auth_token(
                    response.new_token, response.expiry
                )
            except Exception as e:
                logger.error("Token rotation failed", error=str(e))

    async def close(self):
        """Clean up resources and close connection."""
        if self._channel:
            await self._channel.close()
        if hasattr(self, "_status_stream_task"):
            self._status_stream_task.cancel()
        if hasattr(self, "_token_rotation_task"):
            self._token_rotation_task.cancel()
