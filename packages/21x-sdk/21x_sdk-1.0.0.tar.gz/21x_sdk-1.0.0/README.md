# Introduction

Welcome to the 21X SDK documentation! This SDK is designed to simplify integration with **21X**, the future of trading and settlement for security tokens and crypto assets. As a regulated platform under the **EU DLT Regime**, 21X ensures compliance, security, and transparency, providing a seamless gateway to the fast-growing market of digital assets.

---

## Key Features

The 21X SDK is designed to streamline interactions with the platform, particularly for managing trades and interacting with the smart contract. Below is an overview of its core capabilities:


### 1. **Smart Contract Interaction**
The `OrderBook` class serves as the gateway for interacting with the platform's EVM-based smart contract. It abstracts the complexities of contract operations, enabling seamless integration. Its key features include:

- **Trading Pair Configuration**: Query trading pair configurations, including checking if your wallet is whitelisted to trade on a specific pair and retrieving other important contract-level details.
- **Balance Insights**: Access real-time balance information for trading pairs, including the base token (tokenized asset) and the quote token (e-money token).
- **Token Allowances**: Easily set allowances for base and quote tokens, ensuring the smart contract is authorized to interact with your tokens for trading.
- **Order Placement**: Place buy and sell limit orders directly through the smart contract with support for automatic scaling of price and quantity values.
- **Order Cancellation**: Cancel active orders efficiently using a straightforward method.

This class simplifies complex on-chain operations, allowing developers to focus on building functionality rather than managing low-level blockchain interactions.

### 2. **REST API Integration**
The built-in REST API client supports a range of essential operations to monitor and manage trading activities:
- **Market Data**:
  - List all available trading pairs and their associated contracts.
  - Retrieve real-time price information for trading pairs.
- **Order Tracking**:
  - Fetch all open orders on the platform.
  - View active orders and trades associated with your wallet.


These features enable users to fully leverage the platform's capabilities, whether by interacting with the smart contract for direct transactions or querying the REST API for trading insights and order management.


## Prerequisites

To use this SDK effectively, you’ll need:
- Python 3.9 or higher installed on your system.
- Access credentials for the 21X platform.
- Basic familiarity with REST API and Ethereum smart contract interactions.

## Installation

Get started by installing the SDK via pip:
```bash
pip install 21x-sdk
```

## Quick Start Example

Here’s a quick example of how to initialize the SDK and interact with the platform:
```python
from x21_sdk import Client, OrderBook

# Initialize REST API client
client = Client(base_url="<21x_hostname>/api/v1")

auth_client = AuthenticatedClient(
    base_url="<21x_hostname>/api/v1",
    client_id="<oidc_client_id>",
    client_secret="<oidc_client_secret>",
    token_endpoint="<oidc_token_endpoint>",
)

# Interact with the smart contract
order_book = OrderBook(
  private_key="your_private_key",
  orderbook_addr="0xOrderBookAddress",
  rpc_url="https://polygon-mainnet.g.alchemy.com/v2/YOUR_API_KEY",
)

# Example: Submit a buy order
order_book.create_buy_order(quantity=Decimal(100), price=Decimal(50.5))
```

### Environment Variables

Alternatively, the SDK Client or AuthenticatedClient can be configured using the following environment variables:

- `21X_BASE_URL`: The base URL for the 21X API.
- `21X_AUTH_CLIENT_ID`: The client ID for authentication.
- `21X_AUTH_CLIENT_SECRET`: The client secret for authentication.
- `21X_AUTH_CLIENT_TOKEN_ENDPOINT`: The token endpoint URL for authentication.

## License
Unless otherwise specified, all content, including all source code files and documentation files in this repository are:

Copyright (c) 2025 21X AG

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

SPDX-License-Identifier: Apache-2.0