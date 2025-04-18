import requests    
from .schema import SendTransactionParams, TransactionResponse, DepositCashParams, WithdrawCashParams, BalanceResponse, Token
from typing import List
from ..constants import BASE_URL

async def send(self, params: SendTransactionParams) -> TransactionResponse:
    auth_token = self.agent_token or self.user_token
    if not auth_token:
        raise Exception('Authentication required. Connect as user or agent first.')

    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    response = requests.post(
        f"{BASE_URL}/api/cash/send",
        json=params,
        headers=headers,
    )
    response.raise_for_status()
    return response.json()

async def deposit(self, params: DepositCashParams) -> TransactionResponse:
    auth_token = self.agent_token or self.user_token
    if not auth_token:
        raise Exception('Authentication required. Connect as user or agent first.')
    
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    response = requests.post(
        f"{BASE_URL}/api/cash/deposit",
        json=params,
        headers=headers,
    )
    response.raise_for_status()
    return response.json()

async def withdraw(self, params: WithdrawCashParams) -> TransactionResponse:
    auth_token = self.agent_token or self.user_token
    if not auth_token:
        raise Exception('Authentication required. Connect as user or agent first.')
    
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    response = requests.post(
        f"{BASE_URL}/api/cash/withdraw",
        json=params,
        headers=headers,
    )
    response.raise_for_status()
    return response.json()

async def get_balance(self, account: int) -> BalanceResponse:
    auth_token = self.agent_token or self.user_token
    if not auth_token:
        raise Exception('Authentication required. Connect as user or agent first.')
    
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    response = requests.get(
        f"{BASE_URL}/api/cash/balance",
        {"account": account},
        headers=headers,
    )
    response.raise_for_status()
    return response.json()

async def get_supported_tokens(self) -> List[Token]:
    auth_token = self.agent_token or self.user_token
    if not auth_token:
        raise Exception('Authentication required. Connect as user or agent first.')
    
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    response = requests.get(
        f"{BASE_URL}/api/cash/tokens",
        headers=headers,
    )
    response.raise_for_status()
    return response.json()