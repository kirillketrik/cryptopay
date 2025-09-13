"""
Wallet repository interface.

Defines the contract for wallet storage and retrieval operations.
"""

from abc import ABC, abstractmethod
from typing import Optional

from cryptopay.models import Wallet


class WalletRepository(ABC):
    """
    Abstract interface for wallet storage and retrieval operations.
    
    This interface defines the contract for wallet-related database operations,
    including creating, retrieving, and managing cryptocurrency wallets.
    
    **Key Operations:**
    - Get wallet for user by network
    - Save generated wallet
    - Retrieve wallet by ID
    - Update wallet information
    """

    @abstractmethod
    def get_wallet_for_user(self, user_id: int, network: str) -> Optional[Wallet]:
        """
        Get wallet for user based on user_id and network.
        
        Args:
            user_id: The user identifier
            network: The blockchain network (e.g., "erc20", "bsc", "solana")
            
        Returns:
            Wallet instance if found, None otherwise
            
        Raises:
            Exception: If database operation fails
        """
        pass

    @abstractmethod
    def save_wallet(self, wallet: Wallet) -> Wallet:
        """
        Save a generated wallet to storage.
        
        Args:
            wallet: The wallet instance to save
            
        Returns:
            The saved wallet with updated ID if needed
            
        Raises:
            Exception: If database operation fails
        """
        pass

    @abstractmethod
    def get_wallet_by_id(self, wallet_id: int) -> Optional[Wallet]:
        """
        Get wallet by its unique identifier.
        
        Args:
            wallet_id: The wallet identifier
            
        Returns:
            Wallet instance if found, None otherwise
            
        Raises:
            Exception: If database operation fails
        """
        pass

    @abstractmethod
    def get_wallets_by_user(self, user_id: int) -> list[Wallet]:
        """
        Get all wallets for a specific user.
        
        Args:
            user_id: The user identifier
            
        Returns:
            List of wallet instances for the user
            
        Raises:
            Exception: If database operation fails
        """
        pass
