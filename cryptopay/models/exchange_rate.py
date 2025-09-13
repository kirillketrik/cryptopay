from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class ExchangeRate(BaseModel):
    """
    Represents the current exchange rate between a cryptocurrency and fiat currency.
    
    An exchange rate provides the conversion rate between a cryptocurrency and a fiat
    currency, including both the direct rate and its inverse. This is used for
    converting amounts in invoices and calculating prices.
    
    **Key Features:**
    - Bidirectional conversion rates (crypto ↔ fiat)
    - Timestamp tracking for rate freshness
    - Currency code normalization
    - Positive rate validation
    
    **Rate Calculations:**
    - `rate`: 1 crypto = X fiat (e.g., 1 BTC = 40000 USD)
    - `reverted_rate`: 1 fiat = X crypto (e.g., 1 USD = 0.000025 BTC)
    - The rates are mathematical inverses: rate * reverted_rate = 1
    
    **Usage Examples:**
    ```python
    # Create a Bitcoin to USD exchange rate
    rate = ExchangeRate(
        id=1,
        rate=Decimal("40000.00"),
        reverted_rate=Decimal("0.000025"),
        fiat_currency="USD",
        crypto_currency="BTC",
        last_updated_at=1640995200
    )
    
    # Create an Ethereum to EUR exchange rate
    rate = ExchangeRate(
        id=2,
        rate=Decimal("2200.00"),
        reverted_rate=Decimal("0.000454545"),
        fiat_currency="EUR",
        crypto_currency="ETH",
        last_updated_at=1640995200
    )
    
    # Convert amounts using the rate
    crypto_amount = Decimal("0.0025")
    fiat_amount = crypto_amount * rate.rate  # 0.0025 * 40000 = 100 USD
    ```
    
    **Business Logic:**
    - Rate and reverted_rate are mathematical inverses
    - Rates are updated periodically from external sources
    - Used for converting between fiat and crypto amounts in invoices
    - Currency codes are normalized to uppercase
    - All rates must be positive values
    """
    
    id: Optional[int] = Field(..., description="Unique identifier of the exchange rate")
    rate: Decimal = Field(..., gt=0, description="Exchange rate (1 crypto = X fiat)")
    reverted_rate: Decimal = Field(..., gt=0, description="Inverse exchange rate (1 fiat = X crypto)")
    fiat_currency: str = Field(..., description="Fiat currency code (e.g., 'USD', 'EUR')")
    crypto_currency: str = Field(..., description="Cryptocurrency code (e.g., 'BTC', 'ETH')")
    last_updated_at: int = Field(..., description="Unix timestamp when rate was last updated")
    
    @field_validator("rate")
    @classmethod
    def validate_rate(cls, v: Decimal) -> Decimal:
        """
        Validate that the exchange rate is positive.
        
        Args:
            v: The exchange rate to validate
            
        Returns:
            The validated exchange rate
            
        Raises:
            ValueError: If the rate is not positive
        """
        if v <= 0:
            raise ValueError("Exchange rate must be positive")
        return v
    
    @field_validator("reverted_rate")
    @classmethod
    def validate_reverted_rate(cls, v: Decimal) -> Decimal:
        """
        Validate that the reverted rate is positive.
        
        Args:
            v: The reverted rate to validate
            
        Returns:
            The validated reverted rate
            
        Raises:
            ValueError: If the reverted rate is not positive
        """
        if v <= 0:
            raise ValueError("Reverted rate must be positive")
        return v
    
    @field_validator("last_updated_at")
    @classmethod
    def validate_last_updated_at(cls, v: int) -> int:
        """
        Validate that last_updated_at is a valid unix timestamp.
        
        Args:
            v: The timestamp to validate
            
        Returns:
            The validated timestamp
            
        Raises:
            ValueError: If the timestamp is not positive
        """
        if v <= 0:
            raise ValueError("Last updated timestamp must be positive")
        return v
    
    @field_validator("fiat_currency")
    @classmethod
    def validate_fiat_currency(cls, v: str) -> str:
        """
        Validate that fiat currency is not empty and normalize to uppercase.
        
        Args:
            v: The fiat currency code to validate
            
        Returns:
            The normalized fiat currency code
            
        Raises:
            ValueError: If the currency code is empty
        """
        if not v or not v.strip():
            raise ValueError("Fiat currency cannot be empty")
        return v.strip().upper()
    
    @field_validator("crypto_currency")
    @classmethod
    def validate_crypto_currency(cls, v: str) -> str:
        """
        Validate that crypto currency is not empty and normalize to uppercase.
        
        Args:
            v: The crypto currency code to validate
            
        Returns:
            The normalized crypto currency code
            
        Raises:
            ValueError: If the currency code is empty
        """
        if not v or not v.strip():
            raise ValueError("Crypto currency cannot be empty")
        return v.strip().upper()
    
    class Config:
        """Pydantic configuration for the ExchangeRate model."""
        json_schema_extra = {
            "example": {
                "id": 1,
                "rate": "40000.00",
                "reverted_rate": "0.000025",
                "fiat_currency": "USD",
                "crypto_currency": "BTC",
                "last_updated_at": 1640995200
            },
            "description": "Current exchange rate between a cryptocurrency and fiat currency"
        }
