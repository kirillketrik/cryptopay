"""
Security provider interface.

Defines the contract for secure storage operations including encryption and decryption.
"""

from abc import ABC, abstractmethod
from typing import Optional


class SecurityProvider(ABC):
    """
    Abstract interface for secure storage operations.
    
    This interface defines the contract for secure storage of sensitive data,
    particularly for encrypting and decrypting wallet private keys.
    
    **Key Operations:**
    - Encrypt bytes (for private key storage)
    - Decrypt bytes (for private key retrieval)
    """
    
    @abstractmethod
    def encrypt_bytes(self, data: bytes) -> bytes:
        """
        Encrypt bytes for safe storage.
        
        Args:
            data: The bytes to encrypt (e.g., private key)
            
        Returns:
            Encrypted bytes
            
        Raises:
            Exception: If encryption fails
        """
        pass
    
    @abstractmethod
    def decrypt_bytes(self, encrypted_data: bytes) -> bytes:
        """
        Decrypt bytes for retrieval.
        
        Args:
            encrypted_data: The encrypted bytes to decrypt
            
        Returns:
            Decrypted bytes
            
        Raises:
            Exception: If decryption fails
        """
        pass
    
        """
        Delete an encryption key.
        
        Args:
            key_id: The key identifier to delete
            
        Returns:
            True if key was deleted, False if not found
            
        Raises:
            Exception: If operation fails
        """
        pass
