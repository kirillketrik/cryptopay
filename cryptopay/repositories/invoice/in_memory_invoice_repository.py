"""
In-memory implementation of the InvoiceRepository interface.
"""

from typing import Dict, List, Optional

from cryptopay.enums import InvoiceStatus
from cryptopay.interfaces.invoice_repository import InvoiceRepository
from cryptopay.models.invoice import Invoice


class InMemoryInvoiceRepository(InvoiceRepository):
    """
    In-memory implementation of the InvoiceRepository.

    This repository stores invoices in a dictionary for testing and development purposes.
    """

    def __init__(self):
        self._invoices: Dict[int, Invoice] = {}
        self._next_id = 1

    def save_invoice(self, invoice: Invoice) -> Invoice:
        """Saves an invoice to the repository."""
        if invoice.id is None:
            invoice.id = self._next_id
            self._next_id += 1
        self._invoices[invoice.id] = invoice
        return invoice

    def get_invoice_by_id(self, invoice_id: int) -> Optional[Invoice]:
        """Retrieves an invoice by its ID."""
        return self._invoices.get(invoice_id)

    def get_invoices_by_user(self, user_id: int) -> List[Invoice]:
        """Retrieves all invoices for a given user."""
        return [inv for inv in self._invoices.values() if inv.user_id == user_id]

    def get_invoices_by_status(self, status: InvoiceStatus) -> List[Invoice]:
        """Retrieves all invoices with a given status."""
        return [inv for inv in self._invoices.values() if inv.status == status]

    def get_expired_invoices(self, current_timestamp: int) -> List[Invoice]:
        """Retrieves all expired invoices."""
        return [
            inv
            for inv in self._invoices.values()
            if inv.expires_at is not None and inv.expires_at < current_timestamp
        ]

    def update_invoice_status(self, invoice_id: int, status: InvoiceStatus) -> Invoice:
        """Updates the status of an invoice."""
        invoice = self.get_invoice_by_id(invoice_id)
        if invoice:
            invoice.status = status
            return invoice
        raise ValueError(f"Invoice with id {invoice_id} not found")

    def update_invoice(self, invoice: Invoice) -> Invoice:
        """Updates an invoice."""
        if invoice.id is None or invoice.id not in self._invoices:
            raise ValueError(f"Invoice with id {invoice.id} not found")
        self._invoices[invoice.id] = invoice
        return invoice

    def delete_invoice(self, invoice_id: int) -> bool:
        """Deletes an invoice."""
        if invoice_id in self._invoices:
            del self._invoices[invoice_id]
            return True
        return False
