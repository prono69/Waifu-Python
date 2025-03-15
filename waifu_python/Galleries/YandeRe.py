import httpx
import random
from typing import Optional, List, Union

from ..API.api import YANDE_RE_BASE_URL

class Yandere:
    @staticmethod
    async def fetch_images(tag: Optional[str] = None, limit: int = 1, max_retries: int = 15) -> List[str]:
        """
        Fetch image URLs from Yande.re API based on a tag with retry logic.
        When limit is 1, fetch up to 1000 images and return a random one.
        """
        # Override limit to 1000 if requesting a single image to increase randomness
        params = {"limit": 1000} if limit == 1 else {"limit": limit}
        if tag:
            params["tags"] = tag
        
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 15.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/58.0.3029.110 Safari/537.3"
            )
        }

        async with httpx.AsyncClient(timeout=15.0, headers=headers) as client:
            for _ in range(max_retries):
                try:
                    response = await client.get(YANDE_RE_BASE_URL, params=params)
                    response.raise_for_status()
                    
                    if not response.content:
                        continue

                    images = response.json()
                    if not isinstance(images, list):
                        continue

                    file_urls = [img["file_url"] for img in images if "file_url" in img]

                    if limit == 1:
                        return [random.choice(file_urls)] if file_urls else []
                    else:
                        return file_urls[:limit]

                except (httpx.HTTPStatusError, httpx.RequestError, ValueError):
                    continue
                
            return []
