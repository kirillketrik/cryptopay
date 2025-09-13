"""
Exchange rate repository interface.

Defines the contract for exchange rate storage and retrieval operations.
"""

from abc import ABC, abstractmethod
from typing import Optional, List
from decimal import Decimal

from cryptopay.models import ExchangeRate


class ExchangeRateRepository(ABC):
    """
    Abstract interface for exchange rate storage and retrieval operations.
    
    This interface defines the contract for exchange rate-related database operations,
    including storing, retrieving, and updating cryptocurrency exchange rates.
    
    **Key Operations:**
    - Get saved exchange rate by fiat_currency and crypto_currency
    - Update exchange rate (last_updated_at, rate, reverted_rate)
    - Retrieve exchange rates by currency pairs
    """
    
    @abstractmethod
    def get_exchange_rate(self, fiat_currency: str, crypto_currency: str) -> Optional[ExchangeRate]:
        """
        Get saved exchange rate by fiat_currency and crypto_currency.
        
        Args:
            fiat_currency: The fiat currency code (e.g., "USD", "EUR")
            crypto_currency: The cryptocurrency code (e.g., "BTC", "ETH")
            
        Returns:
            ExchangeRate instance if found, None otherwise
            
        Raises:
            Exception: If database operation fails
        """
        pass
    
    @abstractmethod
    def update_exchange_rate(
        self, 
        fiat_currency: str, 
        crypto_currency: str, 
        rate: Decimal, 
        reverted_rate: Decimal, 
        last_updated_at: int
    ) -> ExchangeRate:
        """
        Update exchange rate (last_updated_at, rate, reverted_rate).
        
        Args:
            fiat_currency: The fiat currency code
            crypto_currency: The cryptocurrency code
            rate: The exchange rate (1 crypto = X fiat)
            reverted_rate: The inverse exchange rate (1 fiat = X crypto)
            last_updated_at: Unix timestamp when rate was updated
            
        Returns:
            The updated ExchangeRate instance
            
        Raises:
            Exception: If database operation fails
        """
        pass
    
    @abstractmethod
    def save_exchange_rate(self, exchange_rate: ExchangeRate) -> ExchangeRate:
        """
        Save a new exchange rate to storage.
        
        Args:
            exchange_rate: The exchange rate instance to save
            
        Returns:
            The saved exchange rate with updated ID if needed
            
        Raises:
            Exception: If database operation fails
        """
        pass

    @abstractmethod
    def get_exchange_rates_by_crypto_currency(self, crypto_currency: str) -> List[ExchangeRate]:
        """
        Get all exchange rates for a specific cryptocurrency.
        
        Args:
            crypto_currency: The cryptocurrency code
            
        Returns:
            List of ExchangeRate instances for the cryptocurrency
            
        Raises:
            Exception: If database operation fails
        """
        pass
    
    @abstractmethod
    def get_exchange_rates_by_fiat_currency(self, fiat_currency: str) -> List[ExchangeRate]:
        """
        Get all exchange rates for a specific fiat currency.
        
        Args:
            fiat_currency: The fiat currency code
            
        Returns:
            List of ExchangeRate instances for the fiat currency
            
        Raises:
            Exception: If database operation fails
        """
        pass
