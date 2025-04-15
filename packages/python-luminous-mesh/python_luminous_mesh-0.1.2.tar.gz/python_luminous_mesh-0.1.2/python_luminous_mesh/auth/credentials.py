import os
import time
from typing import Optional, Tuple
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
import grpc
import structlog

logger = structlog.get_logger()


class CredentialsManager:
    """Manages node credentials including certificates and authentication tokens."""

    def __init__(
        self,
        cert_path: Optional[str] = None,
        key_path: Optional[str] = None,
        ca_cert_path: Optional[str] = None,
    ):
        self.cert_path = cert_path or os.environ.get("LUMINOUS_MESH_CERT_PATH")
        self.key_path = key_path or os.environ.get("LUMINOUS_MESH_KEY_PATH")
        self.ca_cert_path = ca_cert_path or os.environ.get("LUMINOUS_MESH_CA_CERT_PATH")
        self._auth_token = None
        self._token_expiry = 0

    async def generate_csr(self) -> Tuple[bytes, bytes]:
        """Generate a new private key and CSR."""
        # Generate private key
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

        # Generate CSR
        csr = (
            x509.CertificateSigningRequestBuilder()
            .subject_name(
                x509.Name(
                    [
                        x509.NameAttribute(NameOID.COMMON_NAME, "luminous-mesh-node"),
                        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Luminous Mesh"),
                    ]
                )
            )
            .sign(private_key, hashes.SHA256())
        )

        # Serialize private key and CSR
        private_key_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

        csr_bytes = csr.public_bytes(serialization.Encoding.PEM)

        return private_key_bytes, csr_bytes

    async def store_credentials(
        self, certificate: bytes, private_key: bytes, ca_certificate: bytes
    ):
        """Store the node's credentials to disk."""
        os.makedirs(os.path.dirname(self.cert_path), exist_ok=True)

        # Write certificate
        with open(self.cert_path, "wb") as f:
            f.write(certificate)

        # Write private key
        with open(self.key_path, "wb") as f:
            f.write(private_key)

        # Write CA certificate
        with open(self.ca_cert_path, "wb") as f:
            f.write(ca_certificate)

    async def get_credentials(self) -> grpc.ChannelCredentials:
        """Get channel credentials for gRPC connection."""
        try:
            with open(self.cert_path, "rb") as f:
                cert = f.read()
            with open(self.key_path, "rb") as f:
                key = f.read()
            with open(self.ca_cert_path, "rb") as f:
                ca_cert = f.read()

            return grpc.ssl_channel_credentials(
                root_certificates=ca_cert, private_key=key, certificate_chain=cert
            )
        except Exception as e:
            logger.error("Failed to load credentials", error=str(e))
            raise

    async def get_certificate(self) -> bytes:
        """Get the node's certificate."""
        try:
            with open(self.cert_path, "rb") as f:
                return f.read()
        except Exception as e:
            logger.error("Failed to read certificate", error=str(e))
            raise

    async def update_auth_token(self, token: str, expiry: int):
        """Update the authentication token."""
        self._auth_token = token
        self._token_expiry = expiry

    async def get_auth_token(self) -> Optional[str]:
        """Get the current authentication token."""
        if self._auth_token and time.time() < self._token_expiry:
            return self._auth_token
        return None
