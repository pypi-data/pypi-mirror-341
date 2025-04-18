from enum import Enum
from dataclasses import dataclass
from typing import Optional

# Base URL for the API
BASE_URL = 'https://build.caishen.tech'
# BASE_URL = 'https://build.caishen.xyz'  # Uncomment this if needed

class ChainType(Enum):
    BITCOIN = 'BITCOIN'
    SOLANA = 'SOLANA'
    ETHEREUM = 'ETHEREUM'
    SUI = 'SUI'
    APTOS = 'APTOS'
    TON = 'TON'
    NEAR = 'NEAR'
    TRON = 'TRON'
    XRP = 'XRP'
    CARDANO = 'CARDANO'
    COSMOS = 'COSMOS'

@dataclass
class IWalletAccount:
    chain_type: ChainType
    account: int
    chain_id: Optional[int] = None
    rpc: Optional[str] = None

__all__ = ['ChainType', 'IWalletAccount', 'BASE_URL']