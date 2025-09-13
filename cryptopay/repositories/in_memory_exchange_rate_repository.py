"""
In-memory implementation of the ExchangeRateRepository interface.
"""

from decimal import Decimal
from typing import Dict, List, Optional

from cryptopay.interfaces.exchange_rate_repository import ExchangeRateRepository
from cryptopay.models.exchange_rate import ExchangeRate


class InMemoryExchangeRateRepository(ExchangeRateRepository):
    """
    In-memory implementation of the ExchangeRateRepository.

    This repository stores exchange rates in a dictionary for testing and development purposes.
    """

    def __init__(self):
        self._exchange_rates: Dict[str, ExchangeRate] = {}

    @staticmethod
    def _get_key(fiat_currency: str, crypto_currency: str) -> str:
        return f"{fiat_currency.upper()}_{crypto_currency.upper()}"

    def save_exchange_rate(self, exchange_rate: ExchangeRate) -> ExchangeRate:
        """Saves an exchange rate to the repository."""
        key = self._get_key(exchange_rate.fiat_currency, exchange_rate.crypto_currency)
        self._exchange_rates[key] = exchange_rate
        return exchange_rate

    def get_exchange_rate(
        self, fiat_currency: str, crypto_currency: str
    ) -> Optional[ExchangeRate]:
        """Retrieves an exchange rate by its currency pair."""
        key = self._get_key(fiat_currency, crypto_currency)
        return self._exchange_rates.get(key)

    def get_exchange_rates_by_crypto_currency(self, crypto_currency: str) -> List[ExchangeRate]:
        """Retrieves all exchange rates for a given cryptocurrency."""
        return [
            rate
            for rate in self._exchange_rates.values()
            if rate.crypto_currency == crypto_currency.upper()
        ]

    def get_exchange_rates_by_fiat_currency(self, fiat_currency: str) -> List[ExchangeRate]:
        """Retrieves all exchange rates for a given fiat currency."""
        return [
            rate
            for rate in self._exchange_rates.values()
            if rate.fiat_currency == fiat_currency.upper()
        ]

    def update_exchange_rate(
        self, 
        fiat_currency: str, 
        crypto_currency: str, 
        rate: Decimal, 
        reverted_rate: Decimal, 
        last_updated_at: int
    ) -> ExchangeRate:
        """Updates an exchange rate."""
        key = self._get_key(fiat_currency, crypto_currency)
        if key not in self._exchange_rates:
            raise ValueError(f"Exchange rate for {fiat_currency}/{crypto_currency} not found")
        exchange_rate = self._exchange_rates[key]
        exchange_rate.rate = rate
        exchange_rate.reverted_rate = reverted_rate
        exchange_rate.last_updated_at = last_updated_at
        return exchange_rate
