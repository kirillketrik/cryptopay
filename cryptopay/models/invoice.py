from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from cryptopay.enums import InvoiceStatus


class Invoice(BaseModel):
    """
    Represents a payment request for cryptocurrency payments with flexible currency support.
    
    An invoice is a payment request that specifies the amount to be paid, the accepted
    cryptocurrencies, and payment terms. It supports both fiat and cryptocurrency amounts
    and can handle native cryptocurrencies as well as token contracts.
    
    **Key Features:**
    - Flexible currency support (fiat + crypto)
    - Automatic expiration handling
    - Status tracking for payment lifecycle
    - Support for token contracts (ERC-20, etc.)
    - Comprehensive validation and business rules
    
    **Status Lifecycle:**
    - PENDING: Invoice created, waiting for payment
    - PAID: Payment received and confirmed
    - EXPIRED: Invoice expired without payment
    - CANCELLED: Invoice cancelled by user
    
    **Usage Examples:**
    ```python
    # Create a simple crypto-only invoice
    invoice = Invoice(
        id=1,
        user_id=123,
        created_at=1640995200,
        crypto_amount=Decimal("0.0025"),
        crypto_currency="BTC",
        network="erc20"
    )
    
    # Create a fiat-crypto invoice
    invoice = Invoice(
        id=2,
        user_id=123,
        created_at=1640995200,
        expires_at=1641081600,
        fiat_amount=Decimal("100.00"),
        fiat_currency="USD",
        crypto_amount=Decimal("0.0025"),
        crypto_currency="BTC",
        network="erc20"
    )
    
    # Create an ERC-20 token invoice
    invoice = Invoice(
        id=3,
        user_id=123,
        created_at=1640995200,
        crypto_amount=Decimal("100.0"),
        crypto_currency="USDT",
        crypto_currency_address="0xdAC17F958D2ee523a2206206994597C13D831ec7",
        network="erc20"
    )
    ```
    
    **Relationships:**
    - Belongs to one User (user_id)
    - Can have multiple Transactions (one-to-many)
    - References one Wallet (for payment destination)
    - Associated with one ExchangeRate (for price conversion)
    
    **Business Logic:**
    - Invoice expires automatically if not paid by expires_at
    - Status transitions: PENDING → PAID/EXPIRED/CANCELLED
    - Supports both native cryptocurrencies and token contracts
    - Fiat amounts are optional for crypto-only payments
    """

    id: int = Field(..., description="Unique identifier of the invoice")
    user_id: int = Field(..., description="Identifier of the user who owns this invoice")
    updated_at: Optional[int] = Field(None, description="Unix timestamp when invoice was last updated (optional)")
    expires_at: Optional[int] = Field(None, description="Unix timestamp when invoice will expire (optional)")
    created_at: int = Field(..., description="Unix timestamp when invoice was created")
    status: InvoiceStatus = Field(default=InvoiceStatus.PENDING, description="Current status of the invoice")
    fiat_amount: Optional[Decimal] = Field(None, description="Amount of the bill in fiat currency (optional)")
    fiat_currency: Optional[str] = Field(None, description="Fiat currency code (e.g., 'USD', 'EUR') (optional)")
    crypto_amount: Decimal = Field(..., gt=0, description="Amount of the bill in cryptocurrency (required)")
    crypto_currency: str = Field(..., description="Cryptocurrency code (e.g., 'BTC', 'ETH', 'USDT')")
    crypto_currency_address: Optional[str] = Field(None,
                                                   description="Contract address for non-native tokens (e.g., ERC-20 tokens) (optional)")
    network: str = Field(..., description="Blockchain network where transactions should be searched")

    @field_validator("crypto_amount")
    @classmethod
    def validate_crypto_amount(cls, v: Decimal) -> Decimal:
        """
        Validate that the crypto amount is positive.
        
        Args:
            v: The crypto amount to validate
            
        Returns:
            The validated crypto amount
            
        Raises:
            ValueError: If the amount is not positive
        """
        if v <= 0:
            raise ValueError("Crypto amount must be positive")
        return v

    @field_validator("fiat_amount")
    @classmethod
    def validate_fiat_amount(cls, v: Optional[Decimal]) -> Optional[Decimal]:
        """
        Validate that the fiat amount is positive if provided.
        
        Args:
            v: The fiat amount to validate (can be None)
            
        Returns:
            The validated fiat amount or None
            
        Raises:
            ValueError: If the amount is provided but not positive
        """
        if v is not None and v <= 0:
            raise ValueError("Fiat amount must be positive if provided")
        return v

    @field_validator("created_at")
    @classmethod
    def validate_created_at(cls, v: int) -> int:
        """
        Validate that created_at is a valid unix timestamp.
        
        Args:
            v: The timestamp to validate
            
        Returns:
            The validated timestamp
            
        Raises:
            ValueError: If the timestamp is not positive
        """
        if v <= 0:
            raise ValueError("Created timestamp must be positive")
        return v

    @field_validator("expires_at")
    @classmethod
    def validate_expires_at(cls, v: Optional[int], info) -> Optional[int]:
        """
        Validate that expires_at is after created_at if provided.
        
        Args:
            v: The expiration timestamp to validate (can be None)
            info: Validation info containing other field values
            
        Returns:
            The validated expiration timestamp or None
            
        Raises:
            ValueError: If the expiration timestamp is invalid
        """
        if v is not None:
            if v <= 0:
                raise ValueError("Expires timestamp must be positive")

            # Get created_at from the model data
            created_at = info.data.get("created_at") if info.data else None
            if created_at and v <= created_at:
                raise ValueError("Expires timestamp must be after created timestamp")

        return v

    @field_validator("updated_at")
    @classmethod
    def validate_updated_at(cls, v: Optional[int], info) -> Optional[int]:
        """
        Validate that updated_at is after created_at if provided.
        
        Args:
            v: The updated timestamp to validate (can be None)
            info: Validation info containing other field values
            
        Returns:
            The validated updated timestamp or None
            
        Raises:
            ValueError: If the updated timestamp is invalid
        """
        if v is not None:
            if v <= 0:
                raise ValueError("Updated timestamp must be positive")

            # Get created_at from the model data
            created_at = info.data.get("created_at") if info.data else None
            if created_at and v < created_at:
                raise ValueError("Updated timestamp must be after or equal to created timestamp")

        return v

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

    @field_validator("fiat_currency")
    @classmethod
    def validate_fiat_currency(cls, v: Optional[str]) -> Optional[str]:
        """
        Validate that fiat currency is not empty if provided and normalize to uppercase.
        
        Args:
            v: The fiat currency code to validate (can be None)
            
        Returns:
            The normalized fiat currency code or None
            
        Raises:
            ValueError: If the currency code is provided but empty
        """
        if v is not None:
            if not v.strip():
                raise ValueError("Fiat currency cannot be empty if provided")
            return v.strip().upper()
        return v

    class Config:
        """Pydantic configuration for the Invoice model."""
        use_enum_values = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 123,
                "created_at": 1640995200,
                "expires_at": 1641081600,
                "status": "PENDING",
                "fiat_amount": "100.00",
                "fiat_currency": "USD",
                "crypto_amount": "0.0025",
                "crypto_currency": "ETH",
                "network": "erc20"
            },
            "description": "A payment request for cryptocurrency payments with flexible currency support"
        }
