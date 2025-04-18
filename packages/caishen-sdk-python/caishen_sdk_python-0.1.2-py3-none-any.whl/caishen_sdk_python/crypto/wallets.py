import requests
from typing import Optional
from enum import Enum
from ..constants import BASE_URL, PublicRpcEndpoints, ChainIds

# Function to get wallet
async def get_wallet(self, chain_type: str, account: int, chain_id: Optional[int] = None) -> dict:
    if not chain_type or account is None:
        raise ValueError('chainType and account number are required')

    auth_token = self.agent_token or self.user_token
    if not auth_token:
        raise ValueError('Authenticate as an agent or user before fetching wallets')

    try:
        response = requests.get(
            f"{BASE_URL}/api/crypto/wallets",
            params={"chainType": chain_type, "account": account, "chainId": chain_id},
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        raise ValueError(f"Failed to get wallet: {error.response.json().get('message', error)}") from error

# Function to get supported chain types
async def get_supported_chain_types(self) -> list:
    try:
        auth_token = self.agent_token or self.user_token
        if not auth_token:
            raise ValueError('Authenticate as an agent or user before fetching wallets')

        response = requests.get(
            f"{BASE_URL}/api/crypto/wallets/supported",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        raise ValueError("Failed to get supported chain types") from error

async def get_rpc(chain_id: ChainIds) -> str:
    if chain_id.value not in PublicRpcEndpoints:
        raise ValueError(f"RPC for {chain_id} not supported")
    return PublicRpcEndpoints[chain_id.value]

__all__ = ['get_wallet', 'get_supported_chain_types', 'get_rpc']