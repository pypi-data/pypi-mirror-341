import asyncio
import argparse
import sys
import structlog
from typing import Optional

from .core.client import LuminousMeshClient
from .config.settings import ClientSettings

logger = structlog.get_logger()


async def main(config_path: Optional[str] = None):
    """Main entry point for the Luminous Mesh client."""
    try:
        if config_path:
            settings = ClientSettings.from_yaml(config_path)
        else:
            settings = ClientSettings.from_env()

        client = LuminousMeshClient(settings)

        if not await client.connect():
            logger.error("Failed to connect to control plane")
            sys.exit(1)

        # Keep the client running
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("Shutting down client...")
        finally:
            await client.close()

    except Exception as e:
        logger.error("Fatal error", error=str(e))
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Luminous Mesh Node Client")
    parser.add_argument("--config", type=str, help="Path to configuration file")

    args = parser.parse_args()

    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ]
    )

    asyncio.run(main(args.config))
