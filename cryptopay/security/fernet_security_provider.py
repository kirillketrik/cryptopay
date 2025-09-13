"""
Local security provider implementation.

This module provides a local security provider that uses the `cryptography` library
to encrypt and decrypt data.
"""

from cryptography.fernet import Fernet

from cryptopay.interfaces.security_provider import SecurityProvider


class FernetSecurityProvider(SecurityProvider):
    """
    Local security provider using Fernet encryption.

    This provider uses a symmetric encryption algorithm (Fernet) to secure data.
    It requires a secret key for encryption and decryption.

    **Key Features:**
    - Symmetric encryption using Fernet
    - Secure key-based encryption
    - Simple and effective for local use

    **Security Notes:**
    - The secret key must be kept secret
    - This provider is suitable for local or single-server deployments
    - For distributed systems, consider a more robust key management solution

    **Usage Examples:**
    ```python
    # Generate a secret key
    secret_key = Fernet.generate_key()

    # Create a security provider
    security_provider = LocalSecurityProvider(secret_key)

    # Encrypt and decrypt data
    data = b"my secret data"
    encrypted_data = security_provider.encrypt_bytes(data)
    decrypted_data = security_provider.decrypt_bytes(encrypted_data)

    assert data == decrypted_data
    ```
    """

    def __init__(self, secret_key: bytes):
        """
        Initialize the security provider with a secret key.

        Args:
            secret_key: The secret key for encryption and decryption
        """
        self.fernet = Fernet(secret_key)

    def encrypt_bytes(self, data: bytes) -> bytes:
        """
        Encrypt bytes for safe storage.

        Args:
            data: The bytes to encrypt

        Returns:
            Encrypted bytes
        """
        return self.fernet.encrypt(data)

    def decrypt_bytes(self, encrypted_data: bytes) -> bytes:
        """
        Decrypt bytes for retrieval.

        Args:
            encrypted_data: The encrypted bytes to decrypt

        Returns:
            Decrypted bytes
        """
        return self.fernet.decrypt(encrypted_data)
