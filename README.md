# Pay with Crypto

A Python library for handling cryptocurrency payments. This library provides a flexible and extensible framework for creating and managing invoices, generating wallets, tracking blockchain transactions, and handling exchange rates between fiat and cryptocurrencies.

## Features

*   **Invoice Management:** Create and manage invoices with support for both fiat and cryptocurrency amounts.
*   **Wallet Generation:** Generate and manage cryptocurrency wallets for various blockchain networks.
*   **Transaction Tracking:** Monitor and verify blockchain transactions associated with invoices.
*   **Exchange Rate Handling:** Fetch and manage exchange rates between different currencies.
*   **Extensible Design:** Use of interfaces allows for easy extension and integration with different services and databases.
*   **Pydantic Models:** Data validation and settings management powered by Pydantic.

## Core Concepts

The library is built around a few core concepts:

*   **Invoices:** Represent a payment request. An invoice can be for a specific amount in fiat or cryptocurrency and has a status that tracks its lifecycle (`PENDING`, `PAID`, `EXPIRED`, `CANCELLED`).
*   **Wallets:** Securely store cryptocurrency addresses and encrypted private keys. Each wallet is associated with a user and a specific blockchain network.
*   **Transactions:** Represent a payment on the blockchain. Each transaction is linked to an invoice and has a unique hash for verification.
*   **Exchange Rates:** Store the conversion rate between a cryptocurrency and a fiat currency.

## Getting Started

### Installation

To install the library, you can use poetry:

```bash
poetry install
```

### Usage

Here is a basic example of how to use the library:

```python
from decimal import Decimal
from cryptopay.models import Invoice
from cryptopay.enums import InvoiceStatus

# Create a new invoice
invoice = Invoice(
    id=1,
    user_id=123,
    created_at=1640995200,
    crypto_amount=Decimal("0.0025"),
    crypto_currency="BTC",
    network="erc20"
)

print(f"Created invoice {invoice.id} with status {invoice.status}")
```

## Project Structure

The project is structured as follows:

*   `cryptopay/`: The main package directory.
    *   `enums/`: Contains enumerations used in the project.
    *   `interfaces/`: Defines the abstract interfaces for the core components.
    *   `models/`: Contains the Pydantic data models.
*   `tests/`: Contains the test suite for the project.

## Dependencies

*   [Python 3.12+](https://www.python.org/)
*   [Poetry](https://python-poetry.org/) for dependency management.
*   [Pydantic](https://pydantic-docs.helpmanual.io/) for data validation.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
