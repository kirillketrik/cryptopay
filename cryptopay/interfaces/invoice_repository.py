"""
Invoice repository interface.

Defines the contract for invoice storage and management operations.
"""

from abc import ABC, abstractmethod
from typing import Optional, List

from cryptopay.enums import InvoiceStatus
from cryptopay.models import Invoice


class InvoiceRepository(ABC):
    """
    Abstract interface for invoice storage and management operations.
    
    This interface defines the contract for invoice-related database operations,
    including creating, updating, and managing payment invoices.
    
    **Key Operations:**
    - Save created invoice
    - Update invoice status
    - Retrieve invoice by ID
    - Get invoices by user
    - Get expired invoices
    """

    @abstractmethod
    def save_invoice(self, invoice: Invoice) -> Invoice:
        """
        Save a created invoice to storage.
        
        Args:
            invoice: The invoice instance to save
            
        Returns:
            The saved invoice with updated ID if needed
            
        Raises:
            Exception: If database operation fails
        """
        pass

    @abstractmethod
    def update_invoice_status(self, invoice_id: int, status: InvoiceStatus) -> Invoice:
        """
        Update invoice status.
        
        Args:
            invoice_id: The invoice identifier
            status: The new status to set
            
        Returns:
            The updated invoice
            
        Raises:
            Exception: If database operation fails or invoice not found
        """
        pass

    @abstractmethod
    def get_invoice_by_id(self, invoice_id: int) -> Optional[Invoice]:
        """
        Get invoice by its unique identifier.
        
        Args:
            invoice_id: The invoice identifier
            
        Returns:
            Invoice instance if found, None otherwise
            
        Raises:
            Exception: If database operation fails
        """
        pass

    @abstractmethod
    def get_invoices_by_user(self, user_id: int) -> List[Invoice]:
        """
        Get all invoices for a specific user.
        
        Args:
            user_id: The user identifier
            
        Returns:
            List of invoice instances for the user
            
        Raises:
            Exception: If database operation fails
        """
        pass

    @abstractmethod
    def get_invoices_by_status(self, status: InvoiceStatus) -> List[Invoice]:
        """
        Get all invoices with a specific status.
        
        Args:
            status: The invoice status to filter by
            
        Returns:
            List of invoice instances with the specified status
            
        Raises:
            Exception: If database operation fails
        """
        pass

    @abstractmethod
    def get_expired_invoices(self, current_timestamp: int) -> List[Invoice]:
        """
        Get all invoices that have expired.
        
        Args:
            current_timestamp: Current unix timestamp for comparison
            
        Returns:
            List of expired invoice instances
            
        Raises:
            Exception: If database operation fails
        """
        pass

    @abstractmethod
    def update_invoice(self, invoice: Invoice) -> Invoice:
        """
        Update an existing invoice in storage.
        
        Args:
            invoice: The invoice instance with updated information
            
        Returns:
            The updated invoice
            
        Raises:
            Exception: If database operation fails or invoice not found
        """
        pass

    @abstractmethod
    def delete_invoice(self, invoice_id: int) -> bool:
        """
        Delete an invoice from storage.
        
        Args:
            invoice_id: The invoice identifier to delete
            
        Returns:
            True if invoice was deleted, False if not found
            
        Raises:
            Exception: If database operation fails
        """
        pass
