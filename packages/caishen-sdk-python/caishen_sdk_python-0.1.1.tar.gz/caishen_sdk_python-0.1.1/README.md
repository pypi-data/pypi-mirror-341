
# Caishen SDK (Python)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/caishen-sdk-python.svg)](https://badge.fury.io/py/caishen-sdk-python)

> The Caishen SDK (Python) provides seamless access to multi-chain crypto wallets with a unified interface for managing assets across various blockchain networks.

---

## ✨ Features

- 🔗 Multi-chain wallet support
- 🌐 Supports major blockchains:
  - Ethereum
  - Bitcoin
  - Solana
  - Cardano
  - Sui, NEAR, Ripple, Tron, TON, Aptos
- 🔒 Secure wallet management
- 🐍 Typed Python API interfaces
- 💸 Token operations: Send, Balance, Swap, Deposit, Withdraw

---

## 📦 Installation

```bash
pip install caishen-sdk-python
> ⚠️ Requires Python ≥ 3.7
```

---

## 🚀 Quick Start

```python
from caishen_sdk_python import CaishenSDK

sdk = CaishenSDK("your-project-key")
```

---

## 🔑 Authentication

You can authenticate as either a **user** or an **agent**.

### Connect as User

```python
await sdk.connect_as_user(
  'USER PROVIDER',
  'USER TOKEN'
)
```

#### ✅ Supported Providers

- `google`
- `facebook`
- `twitter`
- `discord`
- `github`
- `linkedin`
- `reddit`
- `line`
- `kakao`
- `weibo`
- `farcaster`
- `custom`

### Connect as Agent

```python
await sdk.connect_as_agent(
  'AGENT_ID',
  'USER_ID'
)
```

---

## 👛 Wallets

### 🔍 Get Wallet Info
Fetch a wallet associated with a user or agent for a specific chain.
> ⚠️ Note: The privateKey will only be returned if the developer dashboard has explicitly allowed access. With it, you can construct your own signer. If not enabled, the SDK will only return the public data needed to interact via Caishen.
#### 📥 Parameters

| Name        | Type     | Required | Description |
|-------------|----------|----------|-------------|
| `chainType` | string   | ✅        | Blockchain type (`ETHEREUM`, `SOLANA`, etc.) |
| `chainId`   | number   | ❌        | Optional chain ID (e.g., 1 for Ethereum) |
| `account`   | number   | ✅        | Account index or identifier |

#### 📘 Example
```python
wallet = await sdk.crypto.get_wallet({
    "chainType": "ETHEREUM",
    "chainId": 1,
    "account": 0
})
```
#### 📚 Type: `IWalletAccount`
```python
class IWalletAccount:
  address: str
  chainType: str
  publicKey: str
  privateKey: Optional(str)  # Only returned if access is enabled in the dashboard
  account: int
```
> ⚠️ Private key is optional and only available if explicitly enabled in the dashboard.
### MinimalWalletInput

```python
class MinimalWalletInput:
  account: int
  chainType: str
  address: str
```

Used for all `cash` and `swap` functions to avoid sending sensitive data.


### 🌐 Supported Chains
Returns the list of all chain types supported by the backend for wallet creation.

#### 📦 Returns

```python
List[str] // e.g., ['evm', 'solana']
```

#### 📘 Example
```python
chains = await sdk.crypto.get_supported_chain_types()
```

### 🔗 Get EVM RPC URL
Returns the public RPC endpoint URL for a given EVM-compatible chain ID.

### 📥 Parameters

| Name       | Type     | Required | Description |
|------------|----------|----------|-------------|
| `chainId`  | ChainIds | ✅        | Chain ID enum value |

### 📦 Returns
```python
rpc_url = await sdk.crypto.get_rpc(1)
```

---

## 💸 Token Operations

### ➕ Send Token
Send a token or native coin (like ETH, MATIC, SOL) to another address.

#### 📥 Parameters

| Name      | Type                        | Required | Description |
|-----------|-----------------------------|----------|-------------|
| `wallet`  | `IWalletAccount`            | ✅        | Wallet object returned from `getWallet()` |
| `payload` | `{ token?: string; amount: string; toAddress: string; memo?: number }` | ✅ | Transfer details |
> 🚫 Do not pass the full `IWalletAccount` into this function — only `MinimalWalletInput` is required and safer.
- If `payload.token` is **undefined**, the function sends the **native gas token** (e.g. ETH, MATIC).
- If `payload.token` is provided, it sends that **ERC20 or token** instead.

#### 📦 Returns
```python
'transaction_hash'
```
#### 📘 Example
```python
tx_hash = await sdk.crypto.send({
    "wallet": wallet,
    "payload": {
        "token": "0xTokenAddress",  # Optional
        "amount": "0.5",
        "toAddress": "0xRecipientAddress"
    }
})
```

### 📊 Get Balance
Fetch the balance of a wallet for either the **native coin** or a specific **token**.

#### 📥 Parameters

| Name      | Type                         | Required | Description |
|-----------|------------------------------|----------|-------------|
| `wallet`  | `IWalletAccount`             | ✅        | Wallet object |
| `payload` | `{ token?: string }`         | ❌        | If `token` is provided, fetch its balance; otherwise fetch native balance |
> 🚫 Do not pass the full `IWalletAccount` into this function — only `MinimalWalletInput` is required and safer.
#### 📦 Returns

```python
'Balance (in decimal format)'
```

#### Native Balance

```python
native = await sdk.crypto.get_balance({"wallet": wallet, "payload": {}})
```

#### Token Balance

```python
token = await sdk.crypto.get_balance({
    "wallet": wallet,
    "payload": {"token": "0xTokenAddress"}
})
```

---

## 🔁 Token Swap

### 🔍 Get Swap Route
Fetch a possible token swap route across chains.

#### 📥 Parameters

| Field       | Type   | Description |
|-------------|--------|-------------|
| `wallet`    | `Pick<IWalletAccount, 'account'>` | Wallet account info |
| `payload`   | `object` | Swap details including amount, from/to tokens |
> 🚫 Do not pass the full `IWalletAccount` into this function — only `MinimalWalletInput` is required and safer.

#### `payload` structure:

```python
{
  amount: str; // in smallest unit (e.g. wei)
  from: {
    tokenAddress: str;
    chainType: ChainType;
    chainId: Optional(int);
  };
  to: {
    tokenAddress: str;
    chainType: ChainType;
    chainId: Optional(int);
  };
}
```

#### 📦 Returns

```python
class RouteOutput(TypeDict):
  id: str
  fromChainId: int
  fromAmountUSD: str
  fromAmount: str
  fromToken: TokenWithPrice
  fromAddress: Optional(str)
  toChainId: int
  toAmountUSD: str
  toAmount: str
  toAmountMin: str
  toToken: TokenWithPrice
  toAddress: Optional(str)
  confirmationCode: str

```

#### 📘 Example

```python
route = await sdk.crypto.get_swap_route({
    "wallet": {"account": 0},
    "payload": {
        "amount": "1000000000000000000",
        "from": {
            "tokenAddress": "0x...",
            "chainType": "ETHEREUM"
        },
        "to": {
            "tokenAddress": "0x...",
            "chainType": "ETHEREUM"
        }
    }
})
```

### 🔄 Execute Swap
Execute the swap route using a confirmation code.

#### 📥 Parameters

| Field       | Type   | Description |
|-------------|--------|-------------|
| `wallet`    | `Pick<IWalletAccount, 'account', 'chainType'>` | Wallet info |
| `payload`   | `object` | Swap payload including `confirmationCode` |
> 🚫 Do not pass the full `IWalletAccount` into this function — only `MinimalWalletInput` is required and safer.

#### `payload` structure:

```python
{
  confirmationCode: str; # from getSwapRoute()
}
```

#### 📦 Returns

```ts
class RouteExecutedResponse(TypeDict):
  transactionStatus: str
  transactionHash: Optional(str)
  fees: Optional(str)
  error: Optional(str)
```

#### 📘 Example
```python
result = await sdk.crypto.swap({
    "wallet": {"account": 0, "chainType": "ETHEREUM"},
    "payload": {"confirmationCode": "abc123"}
})
```

---

## 🏦 Cash Accounts

### 💰 Get Account Balance
Get current balance of all tokens for a specific account.

#### Parameters

| Name     | Type   | Description              |
|----------|--------|--------------------------|
| account  | number | The account identifier   |

#### Returns

```python
'BalanceResponse'
```
#### 📘 Example

```python
balance = await sdk.cash.get_balance({"account": 1})
```

### 💵 Deposit
Deposit a supported token into the account.

#### Parameters

| Name     | Type                | Description            |
|----------|---------------------|------------------------|
| params   | `DepositCashParams` | Token and amount info  |

#### Returns

```python
TransactionResponse
```

#### 📘 Example

```python
await sdk.cash.deposit({
    "account": 1,
    "tokenAddress": "0x...",
    "amount": "1000000000000000000"
})
```

### 💸 Withdraw
Withdraw a supported token from the account.

#### Parameters

| Name     | Type                 | Description           |
|----------|----------------------|-----------------------|
| params   | `WithdrawCashParams` | Token and amount info |

#### Returns

```python
TransactionResponse
```

#### 📘 Example

```python
await sdk.cash.withdraw({
    "account": 1,
    "tokenAddress": "0x...",
    "amount": "1000000000000000000"
})
```

### 🔁 Send

Send supported tokens between accounts.

#### Parameters

| Name     | Type                   | Description           |
|----------|------------------------|-----------------------|
| params   | `SendTransactionParams`| Token, to/from, etc.  |

#### Returns

```python
TransactionResponse
```

#### 📘 Example

```python
await sdk.cash.send({
    "fromAccount": 1,
    "toAccount": 2,
    "tokenAddress": "0x...",
    "amount": "1000000000000000000"
})
```

### 🪙 Get Supported Tokens

```python
tokens = await sdk.cash.get_supported_tokens()
```

---

## 🛠 Types

### `TokenWithPrice`

```python
type TokenWithPrice = Token & {
  priceUSD: str;
}
```

---

## 🧱 Build from Source

```bash
# Clone & install
pip install setuptools wheel twine

# Build SDK
python setup.py sdist bdist_wheel

# Install locally for development
pip install .
```

---

## 🤝 Contributing

Contributions welcome! Open an issue or submit a pull request.

---

## 📜 License

MIT © [CaishenTech](https://github.com/CaishenTech)

---

## 💬 Support

Please open an issue in the GitHub repository or contact the maintainers for help.

---

Made with ❤️ by **Caishen**

