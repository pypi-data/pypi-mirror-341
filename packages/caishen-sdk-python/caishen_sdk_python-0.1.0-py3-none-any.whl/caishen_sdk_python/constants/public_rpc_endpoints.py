from .chain_ids import ChainIds

PublicRpcEndpoints = {
    ChainIds.MAINNET: 'https://rpc.ankr.com/eth',
    ChainIds.SMART_CHAIN: 'https://bsc-dataseed.binance.org/',
    ChainIds.MATIC: 'https://polygon-rpc.com/',
    ChainIds.OPTIMISM: 'https://optimism.publicnode.com',
    ChainIds.ARBITRUM: 'https://arb1.arbitrum.io/rpc',
    ChainIds.AVALANCHE: 'https://api.avax.network/ext/bc/C/rpc',
    ChainIds.BASE: 'https://mainnet.base.org',
    ChainIds.MANTLE: 'https://rpc.mantle.xyz',
    ChainIds.MODE: 'https://mainnet.mode.network',
    ChainIds.SOLANA: 'https://solana-mainnet.g.alchemy.com/v2/demo',
    ChainIds.SUI: 'https://fullnode.mainnet.sui.io',
    ChainIds.BITCOIN: 'https://api.blockcypher.com/v1/btc/main',
    ChainIds.NEWMONEY_CHAIN: 'https://cashchain-rpc.newmoney.ai',
}

__all__ = ["PublicRpcEndpoints"]