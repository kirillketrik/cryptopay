"""
Blockchain reader interface.

Defines the contract for blockchain transaction monitoring and network operations.
"""

from abc import ABC, abstractmethod
from typing import Optional

from cryptopay.models import Transaction, Wallet, Invoice


class BlockchainReader(ABC):
    """
    Abstract interface for blockchain transaction monitoring and network operations.
    
    This interface defines the contract for reading blockchain data, including
    searching for transactions and getting network information. Can be implemented
    using RPC nodes or third-party APIs.
    
    **Key Operations:**
    - Search new transactions for wallet addresses
    - Get network status
    """
    
    @abstractmethod
    def search_transactions_for_wallet(
        self, 
        wallet: Wallet, 
        invoice: Invoice
    ) -> Optional[Transaction]:
        """
        Search for transactions matching the invoice requirements for the wallet.
        
        Args:
            wallet: The wallet instance to monitor
            invoice: The invoice instance containing payment requirements
            
        Returns:
            Transaction instance if found, None otherwise
            
        Raises:
            Exception: If blockchain operation fails
        """
        pass
    
    
    @abstractmethod
    def is_network_available(self, network: str) -> bool:
        """
        Check if a network is currently available.
        
        Args:
            network: The blockchain network to check
            
        Returns:
            True if network is available, False otherwise
            
        Raises:
            Exception: If operation fails
        """
        pass

