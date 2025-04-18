import requests
from typing import Dict
from ..constants import BASE_URL


async def swap(self, wallet: Dict, payload: Dict) -> dict:
    auth_token = self.agent_token or self.user_token
    if not auth_token:
        raise Exception('Authentication required. Connect as user or agent first.')

    try:
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = requests.post(
            f"{BASE_URL}/api/crypto/swap",
            json={'wallet': wallet, 'payload': payload},
            headers=headers,
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise Exception(f"Failed to execute the swap route: {str(e)}")


async def get_swap_route(self, wallet: Dict, payload: Dict) -> dict:
    auth_token = self.agent_token or self.user_token
    if not auth_token:
        raise Exception('Authentication required. Connect as user or agent first.')

    try:
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = requests.post(
            f"{BASE_URL}/api/crypto/swap-route",
            json={'wallet': wallet, 'payload': payload},
            headers=headers,
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise Exception(f"Failed to get route to execute: {str(e)}")
    
__all__ = ['swap', 'get_swap_route']