"""
Exchange rate provider interface.

Defines the contract for retrieving exchange rates from external sources.
"""

from abc import ABC, abstractmethod
from typing import List

from cryptopay.models import ExchangeRate


class ExchangeRateProvider(ABC):
    """
    Abstract interface for exchange rate retrieval from external sources.
    
    This interface defines the contract for fetching cryptocurrency exchange rates
    from various external providers (APIs, exchanges, etc.).
    
    **Key Operations:**
    - Get exchange rate for currency pairs
    - Get supported fiat and crypto currencies
    """
    
    @abstractmethod
    def get_exchange_rate(self, fiat_currency: str, crypto_currency: str) -> ExchangeRate:
        """
        Get exchange rate for pair (fiat/crypto).
        
        Args:
            fiat_currency: The fiat currency code (e.g., "USD", "EUR")
            crypto_currency: The cryptocurrency code (e.g., "BTC", "ETH")
            
        Returns:
            ExchangeRate instance with rate information
            
        Raises:
            Exception: If rate retrieval fails
        """
        pass
    
    @abstractmethod
    def get_supported_fiat_currencies(self) -> List[str]:
        """
        Get list of supported fiat currencies by this provider.
        
        Returns:
            List of supported fiat currencies
            
        Raises:
            Exception: If operation fails
        """
        pass

    @abstractmethod
    def get_supported_crypto_currencies(self) -> List[str]:
        """
        Get list of supported crypto currencies by this provider.
        
        Returns:
            List of supported crypto currencies
            
        Raises:
            Exception: If operation fails
        """
        pass
