# konachan.py
import httpx
import random
from typing import Optional, List, Union

from ..API.api import KONACHAN_BASE_URL

class Konachan:
    @classmethod
    async def fetch_images(cls, tag: Optional[str] = None, limit: int = 1, max_retries: int = 10) -> List[str]:
        """
        Fetch image URLs from Konachan API with retry logic.
        When limit is 1, fetches 1000 images and returns a random one.
        """
        params = {"limit": 1000} if limit == 1 else {"limit": limit}
        if tag:
            params["tags"] = tag

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/58.0.3029.110 Safari/537.3"
            )
        }

        attempt = 0
        async with httpx.AsyncClient(timeout=10.0, headers=headers) as client:
            while attempt < max_retries:
                try:
                    response = await client.get(f"{KONACHAN_BASE_URL}/post.json", params=params)
                    response.raise_for_status()
                    
                    if not response.content:
                        print(f"Empty response from API on attempt {attempt + 1}")
                        attempt += 1
                        continue

                    images = response.json()
                    if not isinstance(images, list):
                        print(f"Unexpected response format on attempt {attempt + 1}: {images}")
                        attempt += 1
                        continue

                    file_urls = [img["file_url"] for img in images if "file_url" in img]

                    if limit == 1:
                        if not file_urls:
                            print(f"No images found on attempt {attempt + 1}")
                            attempt += 1
                            continue
                        return [random.choice(file_urls)]
                    return file_urls[:limit]

                except httpx.HTTPStatusError as e:
                    print(f"HTTP error on attempt {attempt + 1}: {e.response.status_code} {e.response.text}")
                except httpx.RequestError as e:
                    print(f"Request failed on attempt {attempt + 1}: {str(e)}")
                except ValueError as e:
                    print(f"JSON decoding failed on attempt {attempt + 1}: {str(e)}")
                attempt += 1
            return []

    @classmethod
    async def get_random_image(cls, tags: Optional[Union[str, List[str]]] = None, max_retries: int = 10) -> Optional[str]:
        """
        Get a random image URL by fetching up to 1000 images and selecting one.
        """
        attempt = 0
        while attempt < max_retries:
            try:
                if isinstance(tags, list) and tags:
                    tag = random.choice(tags)
                else:
                    tag = tags

                images = await cls.fetch_images(tag, limit=1)
                if images:
                    return images[0]
                
                print(f"No images found, retrying... ({attempt + 1}/{max_retries})")
                attempt += 1
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                attempt += 1

        print("Max retries exceeded")
        return None


    @staticmethod
    async def sfw_fetch_images(limit: int = 1, max_retries: int = 10) -> List[str]:
        """
        Fetch safe-for-work images by including the 'rating:safe' tag.
        """
        return await Konachan.fetch_images(tag="rating:safe", limit=limit, max_retries=max_retries)

    @staticmethod
    async def nsfw_fetch_images(limit: int = 1, max_retries: int = 10) -> List[str]:
        """
        Fetch not safe-for-work images by including the 'rating:explicit' tag.
        """
        return await Konachan.fetch_images(tag="rating:explicit", limit=limit, max_retries=max_retries)