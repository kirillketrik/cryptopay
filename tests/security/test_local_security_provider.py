"""
Tests for the LocalSecurityProvider.
"""

import pytest
from cryptography.fernet import Fernet, InvalidToken

from cryptopay.security.local_security_provider import LocalSecurityProvider


@pytest.fixture
def secret_key() -> bytes:
    """
    Fixture to provide a secret key for testing.
    """
    return Fernet.generate_key()


@pytest.fixture
def security_provider(secret_key: bytes) -> LocalSecurityProvider:
    """
    Fixture to provide a LocalSecurityProvider instance.
    """
    return LocalSecurityProvider(secret_key)


def test_encrypt_decrypt_success(security_provider: LocalSecurityProvider):
    """
    Test that data can be encrypted and decrypted successfully.
    """
    data = b"test data"
    encrypted_data = security_provider.encrypt_bytes(data)
    decrypted_data = security_provider.decrypt_bytes(encrypted_data)
    assert decrypted_data == data


def test_decrypt_with_different_key_fails(security_provider: LocalSecurityProvider):
    """
    Test that decryption fails with a different key.
    """
    data = b"test data"
    encrypted_data = security_provider.encrypt_bytes(data)

    # Create a new security provider with a different key
    different_key = Fernet.generate_key()
    different_security_provider = LocalSecurityProvider(different_key)

    with pytest.raises(InvalidToken):
        different_security_provider.decrypt_bytes(encrypted_data)


def test_encrypt_empty_data(security_provider: LocalSecurityProvider):
    """
    Test that empty data can be encrypted and decrypted.
    """
    data = b""
    encrypted_data = security_provider.encrypt_bytes(data)
    decrypted_data = security_provider.decrypt_bytes(encrypted_data)
    assert decrypted_data == data
