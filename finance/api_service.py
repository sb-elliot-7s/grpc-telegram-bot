from dataclasses import dataclass

import aiohttp

from configs import get_configs


@dataclass
class APIService:
    api_key: str

    async def request(self, quotes: str, url: str = '/api/v3/quote/') -> dict | list[dict]:
        path = f'{url}{quotes}'
        async with aiohttp.ClientSession(base_url=get_configs().base_url) as session:
            async with session.get(url=path, params={'apikey': self.api_key}) as response:
                if response.status == 200:
                    return await response.json()
