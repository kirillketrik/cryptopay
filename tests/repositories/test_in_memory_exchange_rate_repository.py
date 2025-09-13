"""
Tests for the InMemoryExchangeRateRepository.
"""

import pytest
from decimal import Decimal
from time import time

from cryptopay.models.exchange_rate import ExchangeRate
from cryptopay.repositories.in_memory_exchange_rate_repository import InMemoryExchangeRateRepository


@pytest.fixture
def exchange_rate_repository() -> InMemoryExchangeRateRepository:
    """Fixture to provide an InMemoryExchangeRateRepository instance."""
    return InMemoryExchangeRateRepository()


@pytest.fixture
def sample_exchange_rate() -> ExchangeRate:
    """Fixture to provide a sample exchange rate."""
    return ExchangeRate(
        id=1,
        rate=Decimal("50000.0"),
        reverted_rate=Decimal("0.00002"),
        fiat_currency="USD",
        crypto_currency="BTC",
        last_updated_at=int(time()),
    )


def test_save_and_get_exchange_rate(exchange_rate_repository: InMemoryExchangeRateRepository, sample_exchange_rate: ExchangeRate):
    """Test saving and retrieving an exchange rate."""
    exchange_rate_repository.save_exchange_rate(sample_exchange_rate)
    retrieved_rate = exchange_rate_repository.get_exchange_rate(
        sample_exchange_rate.fiat_currency, sample_exchange_rate.crypto_currency
    )
    assert retrieved_rate == sample_exchange_rate


def test_get_exchange_rate_not_found(exchange_rate_repository: InMemoryExchangeRateRepository):
    """Test retrieving a non-existent exchange rate."""
    retrieved_rate = exchange_rate_repository.get_exchange_rate("USD", "ETH")
    assert retrieved_rate is None


def test_get_exchange_rates_by_crypto_currency(exchange_rate_repository: InMemoryExchangeRateRepository, sample_exchange_rate: ExchangeRate):
    """Test retrieving exchange rates by cryptocurrency."""
    exchange_rate_repository.save_exchange_rate(sample_exchange_rate)
    rates = exchange_rate_repository.get_exchange_rates_by_crypto_currency("BTC")
    assert len(rates) == 1
    assert rates[0] == sample_exchange_rate


def test_update_exchange_rate(exchange_rate_repository: InMemoryExchangeRateRepository, sample_exchange_rate: ExchangeRate):
    """Test updating an exchange rate."""
    exchange_rate_repository.save_exchange_rate(sample_exchange_rate)
    new_rate = Decimal("55000.0")
    new_reverted_rate = Decimal("0.00001818")
    new_timestamp = int(time())
    updated_rate = exchange_rate_repository.update_exchange_rate(
        sample_exchange_rate.fiat_currency,
        sample_exchange_rate.crypto_currency,
        new_rate,
        new_reverted_rate,
        new_timestamp,
    )
    assert updated_rate.rate == new_rate
    assert updated_rate.reverted_rate == new_reverted_rate
    assert updated_rate.last_updated_at == new_timestamp
