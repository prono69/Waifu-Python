import httpx
import random
from typing import Optional, List, Union

from ..API.api import DANBORRU_BASE_URL 

class Danbooru:
    @staticmethod
    async def fetch_images(tag: Optional[str] = None, limit: int = 100) -> List[str]:
        """Fetch image URLs from Danbooru API based on a tag."""
        params = {"limit": limit}
        if tag:
            params["tags"] = tag  

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(DANBORRU_BASE_URL, params=params)
                response.raise_for_status()
                images = response.json()
                return [img["file_url"] for img in images if "file_url" in img]  
            except httpx.HTTPStatusError as e:
                print(f"HTTP error: {e}")
                return []
            except (httpx.RequestError, ValueError) as e:
                print(f"Request error: {e}")
                return []

    @staticmethod
    async def get_random_image(tags: Optional[Union[str, List[str]]] = None) -> Optional[str]:
        """Get a random image URL using a randomly selected tag from the given list."""
        if isinstance(tags, list) and tags:
            tag = random.choice(tags)  
        else:
            tag = tags  

        images = await Danbooru.fetch_images(tag)
        return random.choice(images) if images else None