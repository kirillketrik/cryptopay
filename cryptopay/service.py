"""
Crypto Payments Service

Main service class that implements all the use cases for the crypto payments library.
This class orchestrates interactions between all the interfaces to provide a complete
cryptocurrency payment solution.
"""

import time
from typing import Optional
from decimal import Decimal

from cryptopay.models import (
    Wallet,
    Invoice,
    Transaction,
    ExchangeRate,
    WalletCredentials,
)
from cryptopay.enums import InvoiceStatus
from cryptopay.interfaces import (
    WalletRepository,
    InvoiceRepository,
    ExchangeRateRepository,
    TransactionRepository,
    BlockchainReader,
    NetworkClient,
    SecurityProvider,
    ExchangeRateProvider,
)


class CryptoPaymentsService:
    """
    Main service class for cryptocurrency payment operations.

    This service implements all the core use cases for the crypto payments library,
    orchestrating interactions between repositories, blockchain readers, network clients,
    and external providers.

    **Use Cases Implemented:**
    - Get wallet for user (with automatic generation if needed)
    - Create fiat invoice (with exchange rate conversion)
    - Create crypto invoice (direct cryptocurrency payment)
    - Check invoice status (with blockchain monitoring)

    **Dependencies:**
    - All repository interfaces for data persistence
    - Blockchain reader for transaction monitoring
    - Network client for wallet generation and transfers
    - Security provider for private key encryption
    - Exchange rate provider for fiat/crypto conversions
    """

    def __init__(
        self,
        wallet_repository: WalletRepository,
        invoice_repository: InvoiceRepository,
        exchange_rate_repository: ExchangeRateRepository,
        transaction_repository: TransactionRepository,
        blockchain_reader: BlockchainReader,
        network_client: NetworkClient,
        security_provider: SecurityProvider,
        exchange_rate_provider: ExchangeRateProvider,
    ):
        """
        Initialize the crypto payments service with all required dependencies.

        Args:
            wallet_repository: Repository for wallet operations
            invoice_repository: Repository for invoice operations
            exchange_rate_repository: Repository for exchange rate operations
            transaction_repository: Repository for transaction operations
            blockchain_reader: Reader for blockchain operations
            network_client: Client for network operations
            security_provider: Provider for security operations
            exchange_rate_provider: Provider for exchange rate operations
        """
        self.wallet_repository = wallet_repository
        self.invoice_repository = invoice_repository
        self.exchange_rate_repository = exchange_rate_repository
        self.transaction_repository = transaction_repository
        self.blockchain_reader = blockchain_reader
        self.network_client = network_client
        self.security_provider = security_provider
        self.exchange_rate_provider = exchange_rate_provider

    def get_wallet_for_user(self, user_id: int, network: str) -> Wallet:
        """
        Get wallet for user (user_id, network).

        **Use Case Flow:**
        1. Try to get from repository (if success, it is final)
        2. Generate wallet with help of NetworkClient
        3. Encrypt private_key with SecurityProvider
        4. Save it to repository

        Args:
            user_id: The user identifier
            network: The blockchain network (e.g., "erc20", "bsc", "solana")

        Returns:
            Wallet instance for the user and network

        Raises:
            Exception: If wallet creation or storage fails
        """
        # Step 1: Try to get from repository
        existing_wallet = self.wallet_repository.get_wallet_for_user(user_id, network)
        if existing_wallet:
            return existing_wallet

        # Step 2: Generate wallet with help of NetworkClient
        wallet_credentials = self.network_client.generate_wallet()

        # Step 3: Encrypt private_key with SecurityProvider
        private_key_encrypted = self.security_provider.encrypt_bytes(
            wallet_credentials.private_key
        )

        # Step 4: Save it to repository
        wallet = Wallet(
            id=0,  # Will be set by repository
            user_id=user_id,
            network=network,
            address=wallet_credentials.address,
            private_key_encrypted=private_key_encrypted
        )

        return self.wallet_repository.save_wallet(wallet)

    def create_fiat_invoice(
        self,
        user_id: int,
        network: str,
        fiat_amount: Decimal,
        fiat_currency: str,
        expires_at: Optional[int] = None
    ) -> Invoice:
        """
        Create fiat invoice (user_id, network, fiat_amount, fiat_currency, expires_at[Optional]).

        **Use Case Flow:**
        1. Get exchange rate
        2. Get wallet for user
        3. Create and save invoice

        Args:
            user_id: The user identifier
            network: The blockchain network
            fiat_amount: The amount in fiat currency
            fiat_currency: The fiat currency code (e.g., "USD", "EUR")
            expires_at: Optional expiration timestamp

        Returns:
            Created Invoice instance

        Raises:
            Exception: If invoice creation fails
        """
        # Step 1: Get exchange rate
        exchange_rate_data = self.exchange_rate_provider.get_exchange_rate(
            fiat_currency, self.network_client.get_network_name()
        )
        if not exchange_rate_data:
            raise Exception(f"Exchange rate not available for {fiat_currency}/{self.network_client.get_network_name()}")

        # Calculate crypto amount from fiat amount
        crypto_amount = fiat_amount * exchange_rate_data.reverted_rate

        # Step 2: Get wallet for user
        wallet = self.get_wallet_for_user(user_id, network)

        # Step 3: Create and save invoice
        current_time = int(time.time())
        invoice = Invoice(
            id=0,  # Will be set by repository
            user_id=user_id,
            created_at=current_time,
            updated_at=current_time,
            expires_at=expires_at,
            status=InvoiceStatus.PENDING,
            fiat_amount=fiat_amount,
            fiat_currency=fiat_currency,
            crypto_amount=crypto_amount,
            crypto_currency=self.network_client.get_network_name(),
            network=network
        )

        return self.invoice_repository.save_invoice(invoice)

    def create_crypto_invoice(
        self,
        user_id: int,
        network: str,
        crypto_amount: Decimal,
        crypto_currency: str,
        crypto_currency_address: Optional[str] = None,
        expires_at: Optional[int] = None
    ) -> Invoice:
        """
        Create crypto invoice (user_id, network, crypto_amount, crypto_currency, crypto_currency_address[Optional], expires_at[Optional]).

        **Use Case Flow:**
        1. Get wallet for user
        2. Create and save invoice

        Args:
            user_id: The user identifier
            network: The blockchain network
            crypto_amount: The amount in cryptocurrency
            crypto_currency: The cryptocurrency code (e.g., "BTC", "ETH", "USDT")
            crypto_currency_address: Optional contract address for tokens
            expires_at: Optional expiration timestamp

        Returns:
            Created Invoice instance

        Raises:
            Exception: If invoice creation fails
        """
        # Step 1: Get wallet for user
        wallet = self.get_wallet_for_user(user_id, network)

        # Step 2: Create and save invoice
        current_time = int(time.time())
        invoice = Invoice(
            id=0,  # Will be set by repository
            user_id=user_id,
            created_at=current_time,
            updated_at=current_time,
            expires_at=expires_at,
            status=InvoiceStatus.PENDING,
            crypto_amount=crypto_amount,
            crypto_currency=crypto_currency,
            crypto_currency_address=crypto_currency_address,
            network=network
        )

        return self.invoice_repository.save_invoice(invoice)

    def check_invoice_status(self, invoice_id: int) -> Invoice:
        """
        Check invoice status (invoice_id).

        **Use Case Flow:**
        1. Get invoice from repository
        2. Check "status is PENDING" (if not it is final step)
        3. Get transaction by blockchain reader (if we can't get it, check expired and it is final step)
        4. Check if such transaction already in repository (if same transaction was already saved, check expired and it is final step)
        5. Save transaction to repository
        6. Update invoice status

        Args:
            invoice_id: The invoice identifier

        Returns:
            Updated Invoice instance

        Raises:
            Exception: If status check fails
        """
        # Step 1: Get invoice from repository
        invoice = self.invoice_repository.get_invoice_by_id(invoice_id)
        if not invoice:
            raise Exception(f"Invoice with ID {invoice_id} not found")

        # Step 2: Check "status is PENDING" (if not it is final step)
        if invoice.status != InvoiceStatus.PENDING:
            return invoice

        # Check if invoice has expired
        current_time = int(time.time())
        if invoice.expires_at and current_time > invoice.expires_at:
            invoice.status = InvoiceStatus.EXPIRED
            return self.invoice_repository.update_invoice_status(invoice_id, InvoiceStatus.EXPIRED)

        # Step 3: Get transaction by blockchain reader
        wallet = self.wallet_repository.get_wallet_for_user(invoice.user_id, invoice.network)

        if not wallet:
            raise Exception(f"Wallet not found for user {invoice.user_id} and network {invoice.network}")

        transaction = self.blockchain_reader.search_transactions_for_wallet(wallet, invoice)

        # If we can't get transaction, check expired and it is final step
        if not transaction:
            if invoice.expires_at and current_time > invoice.expires_at:
                invoice.status = InvoiceStatus.EXPIRED
                return self.invoice_repository.update_invoice_status(invoice_id, InvoiceStatus.EXPIRED)
            return invoice

        # Step 4: Check if such transaction already in repository
        existing_transaction = self.transaction_repository.get_transaction_by_hash_and_network(
            transaction.hash, transaction.network
        )
        if existing_transaction:
            # If same transaction was already saved, check expired and it is final step
            if invoice.expires_at and current_time > invoice.expires_at:
                invoice.status = InvoiceStatus.EXPIRED
                return self.invoice_repository.update_invoice_status(invoice_id, InvoiceStatus.EXPIRED)
            return invoice

        # Step 5: Save transaction to repository
        self.transaction_repository.save_transaction(transaction)

        # Step 6: Update invoice status
        invoice.status = InvoiceStatus.PAID
        self.invoice_repository.update_invoice_status(invoice_id, InvoiceStatus.PAID)
        return invoice

    def get_invoice_status(self, invoice_id: int) -> InvoiceStatus:
        """
        Get the current status of an invoice.

        Args:
            invoice_id: The invoice identifier

        Returns:
            Current InvoiceStatus

        Raises:
            Exception: If invoice not found
        """
        invoice = self.invoice_repository.get_invoice_by_id(invoice_id)
        if not invoice:
            raise Exception(f"Invoice with ID {invoice_id} not found")

        return invoice.status

    def get_user_invoices(self, user_id: int) -> list[Invoice]:
        """
        Get all invoices for a specific user.

        Args:
            user_id: The user identifier

        Returns:
            List of Invoice instances for the user
        """
        return self.invoice_repository.get_invoices_by_user(user_id)

    def transfer_from_wallet(
        self,
        user_id: int,
        network: str,
        to_address: str,
        amount: Decimal,
        **kwargs
    ) -> str:
        """
        Transfer cryptocurrency from a user's wallet.

        Args:
            user_id: The user identifier
            network: The blockchain network
            to_address: The recipient address
            amount: The amount to transfer
            **kwargs: Additional network-specific parameters

        Returns:
            Transaction hash of the transfer

        Raises:
            Exception: If transfer fails
        """
        # Get user's wallet
        wallet = self.get_wallet_for_user(user_id, network)

        # Decrypt private key
        private_key_bytes = self.security_provider.decrypt_bytes(wallet.private_key_encrypted)
        private_key = private_key_bytes.decode('utf-8')

        # Perform transfer
        return self.network_client.transfer_amount(
            private_key=private_key,
            to_address=to_address,
            amount=amount,
            **kwargs
        )
