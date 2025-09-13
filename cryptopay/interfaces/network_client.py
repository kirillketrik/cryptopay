"""
Network client interface.

Defines the contract for blockchain network operations including wallet generation and transfers.
"""

from abc import ABC, abstractmethod
from decimal import Decimal

from cryptopay.models import WalletCredentials


class NetworkClient(ABC):
    """
    Abstract interface for blockchain network operations.
    
    This interface defines the contract for blockchain network interactions,
    including wallet generation and cryptocurrency transfers.
    
    **Key Operations:**
    - Generate private key and address
    - Transfer amount by private key
    - Get network name
    """

    @abstractmethod
    def get_network_name(self) -> str:
        """
        Get the name of the blockchain network.
        """
        pass

    @abstractmethod
    def generate_wallet(self) -> WalletCredentials:
        """
        Generate private key and address for a network.
        
        Returns:
            WalletCredentials instance with generated private key and address
            
        Raises:
            Exception: If wallet generation fails
        """
        pass

    @abstractmethod
    def transfer_amount(
            self,
            private_key: bytes,
            to_address: str,
            amount: Decimal,
            **kwargs
    ) -> str:
        """
        Transfer amount by private key.
        
        Args:
            private_key: The private key for the sender wallet
            to_address: The recipient address
            amount: The amount to transfer
            **kwargs: Additional network-specific parameters (gas_price, gas_limit, etc.)
            
        Returns:
            Transaction hash of the transfer
            
        Raises:
            Exception: If transfer fails
        """
        pass
