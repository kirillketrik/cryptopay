"""
Tests for the InMemoryInvoiceRepository.
"""

import pytest
from decimal import Decimal
from time import time

from cryptopay.enums import InvoiceStatus
from cryptopay.models.invoice import Invoice
from cryptopay.repositories.in_memory_invoice_repository import InMemoryInvoiceRepository


@pytest.fixture
def invoice_repository() -> InMemoryInvoiceRepository:
    """Fixture to provide an InMemoryInvoiceRepository instance."""
    return InMemoryInvoiceRepository()


@pytest.fixture
def sample_invoice() -> Invoice:
    """Fixture to provide a sample invoice."""
    return Invoice(
        user_id=1,
        crypto_amount=Decimal("1.0"),
        crypto_currency="BTC",
        network="bitcoin",
        created_at=int(time()),
        id=1
    )


def test_save_and_get_invoice(invoice_repository: InMemoryInvoiceRepository, sample_invoice: Invoice):
    """Test saving and retrieving an invoice."""
    invoice_repository.save_invoice(sample_invoice)
    retrieved_invoice = invoice_repository.get_invoice_by_id(sample_invoice.id)
    assert retrieved_invoice == sample_invoice


def test_get_invoice_not_found(invoice_repository: InMemoryInvoiceRepository):
    """Test retrieving a non-existent invoice."""
    retrieved_invoice = invoice_repository.get_invoice_by_id(999)
    assert retrieved_invoice is None


def test_get_invoices_by_user(invoice_repository: InMemoryInvoiceRepository, sample_invoice: Invoice):
    """Test retrieving invoices by user ID."""
    invoice_repository.save_invoice(sample_invoice)
    invoices = invoice_repository.get_invoices_by_user(1)
    assert len(invoices) == 1
    assert invoices[0] == sample_invoice


def test_get_invoices_by_status(invoice_repository: InMemoryInvoiceRepository, sample_invoice: Invoice):
    """Test retrieving invoices by status."""
    invoice_repository.save_invoice(sample_invoice)
    invoices = invoice_repository.get_invoices_by_status(InvoiceStatus.PENDING)
    assert len(invoices) == 1
    assert invoices[0] == sample_invoice


def test_update_invoice_status(invoice_repository: InMemoryInvoiceRepository, sample_invoice: Invoice):
    """Test updating an invoice's status."""
    invoice_repository.save_invoice(sample_invoice)
    invoice_repository.update_invoice_status(sample_invoice.id, InvoiceStatus.PAID)
    updated_invoice = invoice_repository.get_invoice_by_id(sample_invoice.id)
    assert updated_invoice.status == InvoiceStatus.PAID


def test_delete_invoice(invoice_repository: InMemoryInvoiceRepository, sample_invoice: Invoice):
    """Test deleting an invoice."""
    invoice_repository.save_invoice(sample_invoice)
    assert invoice_repository.delete_invoice(sample_invoice.id) is True
    assert invoice_repository.get_invoice_by_id(sample_invoice.id) is None


def test_delete_invoice_not_found(invoice_repository: InMemoryInvoiceRepository):
    """Test deleting a non-existent invoice."""
    assert invoice_repository.delete_invoice(999) is False
