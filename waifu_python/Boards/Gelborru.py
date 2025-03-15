import httpx
import random
from typing import Optional

from ..API.api import GELBORRU_BASE_URL

class Gelborru:
    MAX_RETRIES = 5  
    @staticmethod
    async def fetch_images(tag: Optional[str] = None, limit: int = 100) -> Optional[str]:
        """Fetch a random SFW image from Gelbooru API with dynamic pagination."""
        async with httpx.AsyncClient() as client:
            total_posts = await Gelborru._get_total_posts(client, tag)
            if not total_posts:
                return None  

            max_pages = max(total_posts // limit, 1)  
            
            for _ in range(Gelborru.MAX_RETRIES):
                try:
                    params = Gelborru._prepare_request(tag, limit, max_pages)
                    posts = await Gelborru._fetch_posts(client, params)
                    if posts:
                        post = random.choice(posts)
                        if image_url := post.get('file_url'):
                            return image_url
                except Exception:
                    pass  

        return None  

    @staticmethod
    async def _get_total_posts(client, tag: Optional[str]) -> int:
        """Fetch the total number of available posts for a given tag."""
        try:
            params = {
                'page': 'dapi',
                's': 'post',
                'q': 'index',
                'json': '1',
                'limit': 1  
            }
            if tag:
                params['tags'] = tag.replace(' ', '_')

            response = await client.get(GELBORRU_BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

            return int(data.get('@attributes', {}).get('count', 0))
        except Exception:
            return 0  

    @staticmethod
    async def _fetch_posts(client, params):
        """Fetch and parse posts from Gelbooru API."""
        try:
            response = await client.get(GELBORRU_BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('post', []) if isinstance(data, dict) else []
        except Exception:
            return []

    @staticmethod
    def _prepare_request(tag: Optional[str], limit: int, max_pages: int):
        """Prepare API request parameters with dynamic pagination."""
        return {
            'page': 'dapi',
            's': 'post',
            'q': 'index',
            'json': '1',
            'limit': limit,
            'pid': random.randint(0, max_pages - 1)  
        } | ({'tags': tag.replace(' ', '_')} if tag else {})
