from pydantic import BaseModel, Field, field_validator


class WalletCredentials(BaseModel):
    """
    Represents wallet credentials for blockchain operations.

    This model contains the essential information needed for wallet operations:
    the public address, private key, and network identifier.

    **Key Features:**
    - Secure storage of wallet credentials
    - Network-specific validation
    - Simple structure for wallet operations

    **Security Notes:**
    - Private keys should be handled with extreme care
    - This model is typically used for temporary operations
    - Consider encryption for long-term storage

    **Usage Examples:**
    ```python
    # Create wallet credentials
    credentials = WalletCredentials(
        address="0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6",
        private_key="0x1234567890abcdef...",
        network="erc20"
    )

    # Use for wallet operations
    print(f"Address: {credentials.address}")
    print(f"Network: {credentials.network}")
    ```

    **Relationships:**
    - Used by NetworkClient for wallet generation and transfers
    - Temporary storage for wallet operations
    - Network-specific validation and operations
    """

    address: str = Field(..., description="Public address of the wallet in the blockchain")
    private_key: bytes = Field(..., description="Private key of the wallet for blockchain operations")
    network: str = Field(..., description="Blockchain network where the wallet operates (e.g., 'erc20', 'bsc', 'solana')")

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

    @field_validator("network")
    @classmethod
    def validate_network(cls, v: str) -> str:
        """
        Validate that the network identifier is not empty.

        Args:
            v: The network string to validate

        Returns:
            The validated and stripped network identifier

        Raises:
            ValueError: If the network is empty or invalid
        """
        if not v or not v.strip():
            raise ValueError("Network cannot be empty")
        return v.strip()

    class Config:
        """Pydantic configuration for the WalletCredentials model."""
        json_schema_extra = {
            "example": {
                "address": "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6",
                "private_key": "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
                "network": "erc20"
            },
            "description": "Wallet credentials for blockchain operations"
        }
