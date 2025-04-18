import requests
from types import SimpleNamespace
from typing import Optional, Literal, Dict, Any, Callable
# Import the crypto and cash modules (the __init__.py of each will export the functions)
from . import crypto
from . import cash

class CaishenSDK:
    def __init__(self, project_key: str):
        if not project_key:
            raise ValueError("Project key is required")
        self.project_key: str = project_key
        self.agent_token: Optional[str] = None
        self.user_token: Optional[str] = None
        self.connected_as: Optional[Literal['agent', 'user']] = None
        self.cash = self._bind_module(cash)
        self.crypto = self._bind_module(crypto)

    def _bind_module(self, module: Any) -> Dict[str, Callable]:
        bound: Dict[str, Callable] = {}
        for key in dir(module):
            fn = getattr(module, key)
            if callable(fn) and not key.startswith("_"):
                bound[key] = fn.__get__(self)
        return SimpleNamespace(**bound)
        # bound = {}
        # for key in dir(module):
        #     fn = getattr(module, key)
        #     if callable(fn) and not key.startswith("_"):
        #         bound[key] = fn.__get__(self)
        # return bound

    def say_hello(self, name: str = "World") -> str:
        """
        Returns a hello message.
        
        Args:
            name (str): The name to greet. Defaults to "World".
            
        Returns:
            str: A greeting message.
        """
        return f"Hello, {name}!"
