import requests
from typing import Optional, Literal, Any, Callable, Dict
from .constants import BASE_URL
from . import cash
from . import crypto
from .utils import _ModuleWrapper

class CaishenSDK:
    def __init__(self, project_key: str):
        if not project_key:
            raise ValueError("Project key is required")
        
        self.project_key: str = project_key
        self.agent_token: Optional[str] = None
        self.user_token: Optional[str] = None
        self.connected_as: Optional[Literal['agent', 'user']] = None
        self.cash = _ModuleWrapper(self, cash)
        self.crypto = _ModuleWrapper(self, crypto)

    async def connect_as_agent(self, agent_id: Optional[str] = None, user_id: Optional[str] = None) -> str:
        if self.connected_as:
            raise RuntimeError(
                'Already connected as a user or agent. Create a new instance to connect again.'
            )
        
        try:
            response = requests.post(
                f"{BASE_URL}/auth/agents/connect",
                json={"agentId": agent_id, "userId": user_id},
                headers={"projectKey": self.project_key},
            )
            response.raise_for_status()
            self.agent_token = response.json().get("agentToken")
            self.connected_as = "agent"
            return self.agent_token
        except requests.RequestException as e:
            raise RuntimeError(f"Agent authentication failed: {str(e)}")

    async def connect_as_user(self, provider: str, token: str) -> str:
        if self.connected_as:
            raise RuntimeError(
                'Already connected as a user or agent. Create a new instance to connect again.'
            )
        
        try:
            response = requests.post(
                f"{BASE_URL}/auth/users/connect",
                json={"provider": provider, "token": token},
                headers={"projectKey": self.project_key},
            )
            response.raise_for_status()
            self.user_token = response.json().get("userToken")
            self.connected_as = "user"
            return self.user_token
        except requests.RequestException as e:
            raise RuntimeError(f"User authentication failed: {str(e)}")