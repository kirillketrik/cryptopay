"""
In-memory implementation of the TransactionRepository interface.
"""

from typing import Dict, List, Optional

from cryptopay.interfaces.transaction_repository import TransactionRepository
from cryptopay.models.transaction import Transaction


class InMemoryTransactionRepository(TransactionRepository):
    """
    In-memory implementation of the TransactionRepository.

    This repository stores transactions in a dictionary for testing and development purposes.
    """

    def __init__(self):
        self._transactions: Dict[int, Transaction] = {}
        self._next_id = 1

    def save_transaction(self, transaction: Transaction) -> Transaction:
        """Saves a transaction to the repository."""
        if transaction.id is None:
            transaction.id = self._next_id
            self._next_id += 1
        self._transactions[transaction.id] = transaction
        return transaction

    def get_transaction_by_id(self, transaction_id: int) -> Optional[Transaction]:
        """Retrieves a transaction by its ID."""
        return self._transactions.get(transaction_id)

    def get_transaction_by_hash_and_network(
        self, tx_hash: str, network: str
    ) -> Optional[Transaction]:
        """Retrieves a transaction by its hash and network."""
        for tx in self._transactions.values():
            if tx.hash == tx_hash and tx.network == network:
                return tx
        return None

    def get_transactions_by_invoice(self, invoice_id: int) -> List[Transaction]:
        """Retrieves all transactions for a given invoice."""
        return [tx for tx in self._transactions.values() if tx.invoice_id == invoice_id]

    def get_transactions_by_network(self, network: str) -> List[Transaction]:
        """Retrieves all transactions for a given network."""
        return [tx for tx in self._transactions.values() if tx.network == network]

    def get_transactions_by_hash(self, tx_hash: str) -> List[Transaction]:
        """Retrieves all transactions for a given hash."""
        return [tx for tx in self._transactions.values() if tx.hash == tx_hash]

    def update_transaction(self, transaction: Transaction) -> Transaction:
        """Updates a transaction."""
        if transaction.id is None or transaction.id not in self._transactions:
            raise ValueError(f"Transaction with id {transaction.id} not found")
        self._transactions[transaction.id] = transaction
        return transaction

    def delete_transaction(self, transaction_id: int) -> bool:
        """Deletes a transaction."""
        if transaction_id in self._transactions:
            del self._transactions[transaction_id]
            return True
        return False
