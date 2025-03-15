import random
import httpx

from ..API.api import NEKOS_BASE_URL

class NekosBest:
    tags = []

    @staticmethod
    async def get_tags():
        """Fetches all available tags from the endpoints API."""
        url = f"{NEKOS_BASE_URL}/endpoints"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                NekosBest.tags = list(response.json().keys())  
            else:
                NekosBest.tags = []
        return NekosBest.tags

    @staticmethod
    async def fetch_sfw_images(tag=None):
        """Fetches a random image/GIF from nekos.best based on the given tag."""
        if not NekosBest.tags:
            await NekosBest.get_tags()  
        
        tag = tag or random.choice(NekosBest.tags)
        url = f"{NEKOS_BASE_URL}/{tag}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                images = data.get("results", [])
                if images:
                    return images[0].get("url") 
            return None
