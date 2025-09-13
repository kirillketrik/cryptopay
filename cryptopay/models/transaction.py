from pydantic import BaseModel, Field, field_validator


class Transaction(BaseModel):
    """
    Represents a blockchain transaction that pays an invoice.
    
    A transaction is a record of a payment made on a blockchain network to fulfill
    an invoice. It contains the transaction hash and network information for
    tracking and verification purposes.
    
    **Key Features:**
    - Links to specific invoice for payment tracking
    - Stores blockchain transaction hash for verification
    - Network-specific transaction handling
    - Hash validation for data integrity
    
    **Usage Examples:**
    ```python
    # Create a transaction for an invoice
    transaction = Transaction(
        id=1,
        invoice_id=1,
        hash="0xa1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456",
        network="erc20"
    )
    
    # Validate transaction data
    print(f"Transaction {transaction.id} for invoice {transaction.invoice_id}")
    print(f"Hash: {transaction.hash}")
    print(f"Network: {transaction.network}")
    ```
    
    **Relationships:**
    - Belongs to one Invoice (invoice_id)
    - Executed on one blockchain network
    
    **Business Logic:**
    - Each transaction is linked to exactly one invoice
    - Transaction hash must be unique within the network
    - Network must match the invoice's network
    - Hash validation ensures data integrity
    """
    
    id: int = Field(..., description="Unique identifier of the transaction")
    invoice_id: int = Field(..., description="Identifier of the invoice being paid")
    hash: str = Field(..., description="Hash of the transaction in the blockchain")
    network: str = Field(..., description="Blockchain network where the transaction was executed")
    
    @field_validator("hash")
    @classmethod
    def validate_hash(cls, v: str) -> str:
        """
        Validate that the transaction hash is not empty and properly formatted.
        
        Args:
            v: The transaction hash to validate
            
        Returns:
            The validated and stripped transaction hash
            
        Raises:
            ValueError: If the hash is empty or invalid
        """
        if not v or not v.strip():
            raise ValueError("Transaction hash cannot be empty")
        return v.strip()
    
    class Config:
        """Pydantic configuration for the Transaction model."""
        use_enum_values = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "invoice_id": 1,
                "hash": "0xa1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456",
                "network": "erc20"
            },
            "description": "A blockchain transaction that pays an invoice"
        }
