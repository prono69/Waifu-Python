import httpx, random
from typing import Optional, Dict, Any

class WaifuIm:
    BASE_URL = "https://api.waifu.im/"

    @staticmethod
    async def fetch_image(tag: Optional[str] = None) -> Dict[str, Any]:
        """Fetch an image from waifu.im API with additional fields.
        
        If a tag is provided, fetch an image for that tag.
        If no tag is provided, fetch a completely random image.
        """
        params = {}
        if tag:
            params["included_tags"] = tag

        url = f"{WaifuIm.BASE_URL}search"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return WaifuIm._parse_image_data(data)
            raise Exception(f"Failed to fetch image: {response.text}")

    @staticmethod
    async def get_tags() -> Dict[str, Any]:
        """Fetch available tags from waifu.im API."""
        url = f"{WaifuIm.BASE_URL}tags"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                return response.json()
            WaifuIm._handle_error_response(response)

    @staticmethod
    async def fetch_sfw_image(tag: Optional[str] = None) -> Dict[str, Any]:
        """Fetch an SFW image from waifu.im API."""
        tags = await WaifuIm.get_tags()
        if "versatile" not in tags:
            return None 

        tag = tag or random.choice(tags["versatile"])

        return await WaifuIm.fetch_image(tag)

    @staticmethod
    async def fetch_nsfw_image(tag: Optional[str] = None) -> Dict[str, Any]:
        """Fetch a NSFW image from waifu.im API."""
        tags = await WaifuIm.get_tags()
        if "nsfw" not in tags:
            return None  

        tag = tag or random.choice(tags["nsfw"])

        return await WaifuIm.fetch_image(tag)

