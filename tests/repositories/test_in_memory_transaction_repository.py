"""
Tests for the InMemoryTransactionRepository.
"""

import pytest

from cryptopay.models.transaction import Transaction
from cryptopay.repositories.in_memory_transaction_repository import InMemoryTransactionRepository


@pytest.fixture
def transaction_repository() -> InMemoryTransactionRepository:
    """Fixture to provide an InMemoryTransactionRepository instance."""
    return InMemoryTransactionRepository()


@pytest.fixture
def sample_transaction() -> Transaction:
    """Fixture to provide a sample transaction."""
    return Transaction(
        id=1,
        invoice_id=1,
        hash="0x1234567890abcdef",
        network="bitcoin",
    )


def test_save_and_get_transaction(transaction_repository: InMemoryTransactionRepository, sample_transaction: Transaction):
    """Test saving and retrieving a transaction."""
    transaction_repository.save_transaction(sample_transaction)
    retrieved_transaction = transaction_repository.get_transaction_by_id(sample_transaction.id)
    assert retrieved_transaction == sample_transaction


def test_get_transaction_not_found(transaction_repository: InMemoryTransactionRepository):
    """Test retrieving a non-existent transaction."""
    retrieved_transaction = transaction_repository.get_transaction_by_id(999)
    assert retrieved_transaction is None


def test_get_transaction_by_hash_and_network(transaction_repository: InMemoryTransactionRepository, sample_transaction: Transaction):
    """Test retrieving a transaction by its hash and network."""
    transaction_repository.save_transaction(sample_transaction)
    retrieved_transaction = transaction_repository.get_transaction_by_hash_and_network(
        sample_transaction.hash, sample_transaction.network
    )
    assert retrieved_transaction == sample_transaction


def test_get_transactions_by_invoice(transaction_repository: InMemoryTransactionRepository, sample_transaction: Transaction):
    """Test retrieving transactions by invoice ID."""
    transaction_repository.save_transaction(sample_transaction)
    transactions = transaction_repository.get_transactions_by_invoice(1)
    assert len(transactions) == 1
    assert transactions[0] == sample_transaction


def test_delete_transaction(transaction_repository: InMemoryTransactionRepository, sample_transaction: Transaction):
    """Test deleting a transaction."""
    transaction_repository.save_transaction(sample_transaction)
    assert transaction_repository.delete_transaction(sample_transaction.id) is True
    assert transaction_repository.get_transaction_by_id(sample_transaction.id) is None


def test_delete_transaction_not_found(transaction_repository: InMemoryTransactionRepository):
    """Test deleting a non-existent transaction."""
    assert transaction_repository.delete_transaction(999) is False
