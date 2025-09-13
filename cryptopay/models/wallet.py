from pydantic import BaseModel, Field, field_validator


class Wallet(BaseModel):
    """
    Represents a cryptocurrency wallet for storing and managing digital assets.
    
    A wallet is a digital container that holds cryptocurrency addresses and their associated
    private keys. Each wallet is tied to a specific blockchain network and user account.
    
    **Key Features:**
    - Secure storage of encrypted private keys
    - Support for multiple blockchain networks
    - User association for access control
    - Network-specific address validation
    
    **Security Notes:**
    - Private keys are stored encrypted as bytes for security
    - Address validation ensures network compatibility
    - User association provides access control
    
    **Usage Examples:**
    ```python
    # Create a new wallet
    wallet = Wallet(
        id=1,
        user_id=123,
        network="erc20",
        address="0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6",
        private_key_encrypted=b"encrypted_private_key_data"
    )
    
    # Validate wallet data
    print(f"Wallet {wallet.id} for user {wallet.user_id}")
    print(f"Network: {wallet.network}")
    print(f"Address: {wallet.address}")
    ```
    
    **Relationships:**
    - Belongs to one User (user_id)
    - Can be associated with multiple Invoices (as payment destination)
    - Supports one blockchain network per wallet instance
    """

    id: int = Field(..., description="Unique identifier of the wallet")
    user_id: int = Field(..., description="Identifier of the user linked to this wallet")
    network: str = Field(..., description="Blockchain network where the wallet was created (e.g., 'erc20', 'bsc', 'solana')")
    address: str = Field(..., description="Public address of the wallet in the blockchain")
    private_key_encrypted: bytes = Field(..., description="Encrypted private key of the wallet for secure storage")

    @field_validator("address")
    @classmethod
    def validate_address(cls, v: str) -> str:
        """
        Validate that the wallet address is not empty and properly formatted.
        
        Args:
            v: The address string to validate
            
        Returns:
            The validated and stripped address
            
        Raises:
            ValueError: If the address is empty or invalid
        """
        if not v or not v.strip():
            raise ValueError("Wallet address cannot be empty")
        return v.strip()

    class Config:
        """Pydantic configuration for the Wallet model."""
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 123,
                "network": "erc20",
                "address": "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6",
                "private_key_encrypted": b"i_am_encrypted_private_key"
            },
            "description": "A cryptocurrency wallet for storing and managing digital assets"
        }
