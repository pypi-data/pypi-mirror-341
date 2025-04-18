from typing import Optional, TypedDict
from .chain_ids import ChainIds
from .public_rpc_endpoints import PublicRpcEndpoints


class NativeToken(TypedDict):
    name: str
    symbol: str
    logoURI: str
    decimals: int
    address: str


class Chain(TypedDict):
    chainId: int  # This will use values from ChainIds enum
    name: str
    symbol: str
    rpc: Optional[str]
    logoURI: str
    blockExplorer: str
    publicRpc: str
    coingeckoPlatformId: str
    coingeckoNativeCoin: str
    nativeToken: NativeToken

Chains: dict[int, Chain] = {
    ChainIds.MAINNET: {
        "chainId": ChainIds.MAINNET,
        "name": "Ethereum",
        "symbol": "ETH",
        "publicRpc": PublicRpcEndpoints[ChainIds.MAINNET],
        "rpc": None,  # if not defined in original, assume None
        "logoURI": "https://firebasestorage.googleapis.com/v0/b/new-finance-e41be.appspot.com/o/chainLogos%2Fethereum.svg?alt=media&token=bde4f374-77dc-4a61-9eee-317c7b6b4614",
        "blockExplorer": "https://etherscan.io",
        "coingeckoPlatformId": "ethereum",
        "coingeckoNativeCoin": "ethereum",
        "nativeToken": {
            "name": "Ethereum",
            "symbol": "ETH",
            "logoURI": "https://s2.coinmarketcap.com/static/img/coins/64x64/1027.png",
            "decimals": 18,
            "address": "0x0000000000000000000000000000000000000000"
        }
    },
    ChainIds.AVALANCHE: {
        "chainId": ChainIds.SMART_CHAIN,
        "name": "Binance Smart Chain",
        "symbol": "BNB",
        "publicRpc": PublicRpcEndpoints[ChainIds.SMART_CHAIN],
        "rpc": None,
        "logoURI": "https://firebasestorage.googleapis.com/v0/b/new-finance-e41be.appspot.com/o/chainLogos%2Fbsc.svg?alt=media&token=f7f295fa-25bd-484e-a289-9549b9dccd27",
        "blockExplorer": "https://bscscan.com",
        "coingeckoPlatformId": "binance-smart-chain",
        "coingeckoNativeCoin": "binancecoin",
        "nativeToken": {
            "name": "Binance Coin",
            "symbol": "BNB",
            "logoURI": "https://s2.coinmarketcap.com/static/img/coins/64x64/1839.png",
            "decimals": 18,
            "address": "0x0000000000000000000000000000000000000000"
        }
    },
    ChainIds.SMART_CHAIN: {
        "chainId": ChainIds.SMART_CHAIN,
        "name": "Binance Smart Chain",
        "symbol": "BNB",
        "publicRpc": PublicRpcEndpoints[ChainIds.SMART_CHAIN],
        "rpc": None,
        "logoURI": "https://firebasestorage.googleapis.com/v0/b/new-finance-e41be.appspot.com/o/chainLogos%2Fbsc.svg?alt=media&token=f7f295fa-25bd-484e-a289-9549b9dccd27",
        "blockExplorer": "https://bscscan.com",
        "coingeckoPlatformId": "binance-smart-chain",
        "coingeckoNativeCoin": "binancecoin",
        "nativeToken": {
            "name": "Binance Coin",
            "symbol": "BNB",
            "logoURI": "https://s2.coinmarketcap.com/static/img/coins/64x64/1839.png",
            "decimals": 18,
            "address": "0x0000000000000000000000000000000000000000"
        }
    },
    ChainIds.MATIC: {
        "chainId": ChainIds.MATIC,
        "name": "Polygon",
        "symbol": "MATIC",
        "publicRpc": PublicRpcEndpoints[ChainIds.MATIC],
        "rpc": None,
        "logoURI": "https://firebasestorage.googleapis.com/v0/b/new-finance-e41be.appspot.com/o/chainLogos%2Fpolygon.svg?alt=media&token=3eb8d1c7-de24-4047-862c-e4f07c60176e",
        "blockExplorer": "https://polygonscan.com",
        "coingeckoPlatformId": "polygon-pos",
        "coingeckoNativeCoin": "matic-network",
        "nativeToken": {
            "name": "POL",
            "symbol": "POL",
            "logoURI": "https://s2.coinmarketcap.com/static/img/coins/64x64/3890.png",
            "decimals": 18,
            "address": "0x0000000000000000000000000000000000000000"
        }
    },
    ChainIds.ARBITRUM: {
        "chainId": ChainIds.ARBITRUM,
        "name": "Arbitrum",
        "symbol": "ETH",
        "publicRpc": PublicRpcEndpoints[ChainIds.ARBITRUM],
        "rpc": None,
        "logoURI": "https://firebasestorage.googleapis.com/v0/b/new-finance-e41be.appspot.com/o/chainLogos%2Farbitrum.svg?alt=media&token=60b43410-a8e4-4f51-ac79-8caeabb8316e",
        "blockExplorer": "https://arbiscan.io/",
        "coingeckoPlatformId": "arbitrum-one",
        "coingeckoNativeCoin": "ethereum",
        "nativeToken": {
            "name": "Ethereum",
            "symbol": "ETH",
            "logoURI": "https://s2.coinmarketcap.com/static/img/coins/64x64/1027.png",
            "decimals": 18,
            "address": "0x0000000000000000000000000000000000000000"
        }
    },
    ChainIds.OPTIMISM: {
        "chainId": ChainIds.OPTIMISM,
        "name": "Optimism",
        "symbol": "ETH",
        "publicRpc": PublicRpcEndpoints[ChainIds.OPTIMISM],
        "rpc": None,
        "logoURI": "https://firebasestorage.googleapis.com/v0/b/new-finance-e41be.appspot.com/o/chainLogos%2Foptimism.svg?alt=media&token=338a1750-1f6e-4a8d-a0e1-875cb2d5aed8",
        "blockExplorer": "https://optimistic.etherscan.io/",
        "coingeckoPlatformId": "optimistic-ethereum",
        "coingeckoNativeCoin": "ethereum",
        "nativeToken": {
            "name": "Ethereum",
            "symbol": "ETH",
            "logoURI": "https://s2.coinmarketcap.com/static/img/coins/64x64/1027.png",
            "decimals": 18,
            "address": "0x0000000000000000000000000000000000000000"
        }
    },
    ChainIds.BASE: {
        "chainId": ChainIds.BASE,
        "name": "Base",
        "symbol": "ETH",
        "publicRpc": PublicRpcEndpoints[ChainIds.BASE],
        "rpc": None,
        "logoURI": "https://firebasestorage.googleapis.com/v0/b/new-finance-e41be.appspot.com/o/chainLogos%2Fbase.svg?alt=media&token=288bbdcf-683c-431b-948a-219fe687396e",
        "blockExplorer": "https://basescan.org/",
        "coingeckoPlatformId": "base",
        "coingeckoNativeCoin": "ethereum",
        "nativeToken": {
            "name": "Ethereum",
            "symbol": "ETH",
            "logoURI": "https://s2.coinmarketcap.com/static/img/coins/64x64/1027.png",
            "decimals": 18,
            "address": "0x0000000000000000000000000000000000000000"
        }
    },
    ChainIds.MODE: {
        "chainId": ChainIds.MODE,
        "name": "Mode",
        "symbol": "ETH",
        "publicRpc": PublicRpcEndpoints[ChainIds.MODE],
        "rpc": None,
        "logoURI": "https://s2.coinmarketcap.com/static/img/coins/64x64/31016.png",
        "blockExplorer": "https://modescan.io/",
        "coingeckoPlatformId": "mode",
        "coingeckoNativeCoin": "mode",
        "nativeToken": {
            "name": "Ethereum",
            "symbol": "ETH",
            "logoURI": "https://s2.coinmarketcap.com/static/img/coins/64x64/1027.png",
            "decimals": 18,
            "address": "0x0000000000000000000000000000000000000000"
        }
    },
    ChainIds.SOLANA: {
        "chainId": ChainIds.SOLANA,
        "name": "Solana",
        "symbol": "SOL",
        "publicRpc": PublicRpcEndpoints[ChainIds.SOLANA],
        "rpc": None,
        "logoURI": "https://firebasestorage.googleapis.com/v0/b/new-finance-e41be.appspot.com/o/chainLogos%2Fsolana-plain.svg?alt=media&token=2be82459-25eb-4927-8d77-d8b480428953",
        "blockExplorer": "https://explorer.solana.com/",
        "coingeckoPlatformId": "solana",
        "coingeckoNativeCoin": "solana",
        "nativeToken": {
            "name": "Solana",
            "symbol": "SOL",
            "logoURI": "https://s2.coinmarketcap.com/static/img/coins/64x64/5426.png",
            "decimals": 9,
            "address": ""
        }
    },
    ChainIds.BITCOIN: {
        "chainId": ChainIds.BITCOIN,
        "name": "Bitcoin",
        "symbol": "BTC",
        "publicRpc": PublicRpcEndpoints[ChainIds.BITCOIN],
        "rpc": None,
        "logoURI": "https://www.vhv.rs/dpng/d/527-5278354_bitcoin-icon-bit-coin-png-ico-transparent-png.png",
        "blockExplorer": "https://mempool.space/",
        "coingeckoPlatformId": "bitcoin",
        "coingeckoNativeCoin": "bitcoin",
        "nativeToken": {
            "name": "Bitcoin",
            "symbol": "BTC",
            "logoURI": "https://s2.coinmarketcap.com/static/img/coins/64x64/1.png",
            "decimals": 8,
            "address": ""
        }
    },
    ChainIds.SUI: {
        "chainId": ChainIds.SUI,
        "name": "Sui",
        "symbol": "SUI",
        "publicRpc": PublicRpcEndpoints[ChainIds.SUI],
        "rpc": None,
        "logoURI": "https://s2.coinmarketcap.com/static/img/coins/64x64/20947.png",
        "blockExplorer": "https://suiscan.xyz/mainnet",
        "coingeckoPlatformId": "sui",
        "coingeckoNativeCoin": "sui",
        "nativeToken": {
            "name": "Sui",
            "symbol": "SUI",
            "logoURI": "https://s2.coinmarketcap.com/static/img/coins/64x64/20947.png",
            "decimals": 9,
            "address": ""
        }
    },
    ChainIds.NEWMONEY_CHAIN: {
        "chainId": ChainIds.NEWMONEY_CHAIN,
        "name": "Ethereum",
        "symbol": "ETH",
        "publicRpc": PublicRpcEndpoints[ChainIds.NEWMONEY_CHAIN],
        "rpc": None,
        "logoURI": "",
        "blockExplorer": "https://cashchain.newmoney.ai/",
        "coingeckoPlatformId": "new",
        "coingeckoNativeCoin": "new",
        "nativeToken": {
            "name": "",
            "symbol": "",
            "logoURI": "",
            "decimals": 18,
            "address": ""
        }
    }
}


__all__ = ["Chains"]