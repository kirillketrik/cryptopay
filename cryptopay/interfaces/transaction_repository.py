"""
Transaction repository interface.

Defines the contract for transaction storage and retrieval operations.
"""

from abc import ABC, abstractmethod
from typing import Optional, List

from cryptopay.models import Transaction


class TransactionRepository(ABC):
    """
    Abstract interface for transaction storage and retrieval operations.
    
    This interface defines the contract for transaction-related database operations,
    including storing, retrieving, and managing blockchain transactions.
    
    **Key Operations:**
    - Save transaction
    - Get transaction by hash and network
    - Retrieve transactions by invoice
    - Get transaction by ID
    """

    @abstractmethod
    def save_transaction(self, transaction: Transaction) -> Transaction:
        """
        Save transaction to storage.
        
        Args:
            transaction: The transaction instance to save
            
        Returns:
            The saved transaction with updated ID if needed
            
        Raises:
            Exception: If database operation fails
        """
        pass

    @abstractmethod
    def get_transaction_by_hash_and_network(self, hash: str, network: str) -> Optional[Transaction]:
        """
        Get transaction by hash and network.
        
        Args:
            hash: The transaction hash
            network: The blockchain network
            
        Returns:
            Transaction instance if found, None otherwise
            
        Raises:
            Exception: If database operation fails
        """
        pass

    @abstractmethod
    def get_transaction_by_id(self, transaction_id: int) -> Optional[Transaction]:
        """
        Get transaction by its unique identifier.
        
        Args:
            transaction_id: The transaction identifier
            
        Returns:
            Transaction instance if found, None otherwise
            
        Raises:
            Exception: If database operation fails
        """
        pass

    @abstractmethod
    def get_transactions_by_invoice(self, invoice_id: int) -> List[Transaction]:
        """
        Get all transactions for a specific invoice.
        
        Args:
            invoice_id: The invoice identifier
            
        Returns:
            List of transaction instances for the invoice
            
        Raises:
            Exception: If database operation fails
        """
        pass

    @abstractmethod
    def get_transactions_by_network(self, network: str) -> List[Transaction]:
        """
        Get all transactions for a specific network.
        
        Args:
            network: The blockchain network
            
        Returns:
            List of transaction instances for the network
            
        Raises:
            Exception: If database operation fails
        """
        pass

    @abstractmethod
    def update_transaction(self, transaction: Transaction) -> Transaction:
        """
        Update an existing transaction in storage.
        
        Args:
            transaction: The transaction instance with updated information
            
        Returns:
            The updated transaction
            
        Raises:
            Exception: If database operation fails or transaction not found
        """
        pass

    @abstractmethod
    def delete_transaction(self, transaction_id: int) -> bool:
        """
        Delete a transaction from storage.
        
        Args:
            transaction_id: The transaction identifier to delete
            
        Returns:
            True if transaction was deleted, False if not found
            
        Raises:
            Exception: If database operation fails
        """
        pass

    @abstractmethod
    def get_transactions_by_hash(self, hash: str) -> List[Transaction]:
        """
        Get all transactions with a specific hash (across all networks).
        
        Args:
            hash: The transaction hash
            
        Returns:
            List of transaction instances with the specified hash
            
        Raises:
            Exception: If database operation fails
        """
        pass
