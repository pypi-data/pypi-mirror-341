from typing import Dict, Any
import aiohttp
from .models import EUCResponse

class EUCClient:
    """
    Client for fetching and patching data from the UPS companion API.
    """

    def __init__(self, url: str = "http://localhost:4679/euc-data.js"):
        self.url = url

    async def fetch_data(self) -> EUCResponse:
        """
        Fetch the full JSON data from the API endpoint by posting the initial payload.
        """
        payload = {"cmd": "getData", "fromDate": 0}
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, json=payload) as response:
                response.raise_for_status()  # Raise an exception for HTTP errors
                json_data = await response.json(content_type=None)
                return EUCResponse.from_dict(json_data)

    async def fetch_patch(self, from_date: int) -> Dict[str, Any]:
        """
        Fetch a patch update using a POST request with the 'fromDate' parameter.
        Returns a dictionary containing only the updated fields.
        """
        payload = {"cmd": "getData", "fromDate": from_date}
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, json=payload) as response:
                response.raise_for_status()
                patch_data = await response.json(content_type=None)
                return patch_data

    async def update_data(self, euc_response: EUCResponse) -> None:
        """
        Fetch a partial update and patch the provided EUCData instance.
        """
        patch = await self.fetch_patch(euc_response.lastUpdate)
        euc_response.patch(patch)