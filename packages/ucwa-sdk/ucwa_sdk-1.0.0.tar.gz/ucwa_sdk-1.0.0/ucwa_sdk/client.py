import aiohttp
from .memory import MemoryAPI
from .model import ModelAPI
from .config import BASE_URL
from .utils import get_headers

class UCWAClient:
    def __init__(self, api_key: str, base_url: str = BASE_URL):
        self.api_key = api_key
        self.base_url = base_url
        self.memory = MemoryAPI(self)
        self.model = ModelAPI(self)

    async def get_session(self):
        return aiohttp.ClientSession(headers=get_headers(self.api_key))
