import requests
from typing import Dict, Optional
from ..constants import BASE_URL

async def send(self, wallet: Dict, payload: Dict) -> str:
    auth_token = self.agent_token or self.user_token
    if not auth_token:
        raise Exception('Authentication required. Connect as user or agent first.')

    try:
        headers = {
            "Authorization": f"Bearer {auth_token}"
        }
        response = requests.post(
            f"{BASE_URL}/api/crypto/send",
            json={'wallet': wallet, 'payload': payload},
            headers=headers,
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise Exception(f"Failed to send transaction: {str(e)}")

async def get_balance(self, wallet: Dict, payload: Dict) -> str:
    auth_token = self.agent_token or self.user_token
    if not auth_token:
        raise Exception('Authentication required. Connect as user or agent first.')

    try:
        headers = {
            "Authorization": f"Bearer {auth_token}"
        }
        response = requests.get(
            f"{BASE_URL}/api/crypto/balance",
            {**wallet, 'tokenAddress': payload.get('token')},
            headers=headers,
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise Exception(f"Failed to get balance: {str(e)}")

async def get_token_balances(self, wallet: Dict) -> dict:
    auth_token = self.agent_token or self.user_token
    if not auth_token:
        raise Exception('Authentication required. Connect as user or agent first.')

    try:
        headers = {
            "Authorization": f"Bearer {auth_token}"
        }
        response = await requests.get(
            f"{BASE_URL}/api/crypto/balances",
            {**wallet },
            headers=headers,
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise Exception(f"Failed to get balance: {str(e)}")
    
__all__ = ['send', 'get_balance', 'get_token_balances']