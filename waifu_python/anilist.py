import httpx
import random
import re
from typing import Optional, Dict, Any, List

class AniList:
    GRAPHQL_URL = "https://graphql.anilist.co"

    @staticmethod
    async def fetch_characters(query: str, variables: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fetch characters from AniList GraphQL API."""
        async with httpx.AsyncClient() as client:
            try:
                headers = {"Content-Type": "application/json", "Accept": "application/json"}
                response = await client.post(AniList.GRAPHQL_URL, headers=headers, json={"query": query, "variables": variables})
                response.raise_for_status()
                data = response.json()
                return data.get("data", {}).get("Page", {}).get("characters", [])
            except Exception as e:
                print(f"Error fetching characters: {e}")
                return []

    @staticmethod
    async def fetch_characters_list(limit: int = 50, search: Optional[str] = None) -> List[Dict[str, Any]]:
        """Fetch characters sorted by popularity, optionally filtered by search."""
        query = """
        query ($page: Int, $perPage: Int, $search: String) {
          Page(page: $page, perPage: $perPage) {
            characters(sort: FAVOURITES_DESC, search: $search) {
              id
              name { full }
              gender
              age
              description
              image { large }
              media { edges { node { title { romaji } } } }
            }
          }
        }
        """
        variables = {"page": 1, "perPage": limit, "search": search}
        return await AniList.fetch_characters(query, variables)

    @staticmethod
    async def fetch_waifus(limit: int = 50, search: Optional[str] = None) -> List[Dict[str, Any]]:
        """Fetch female characters."""
        characters = await AniList.fetch_characters_list(limit, search)
        return [char for char in characters if char.get("gender", "").lower() == "female"]

    @staticmethod
    def clean_description(description: str) -> str:
        """Clean the character's description."""
        if not description:
            return "No description available."
        cleaned = re.sub(r'(<br>|\*\*|__)', '', description)
        return cleaned.strip()

    @staticmethod
    async def get_random_waifus(count: int = 3, search: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get multiple random waifus."""
        waifus = await AniList.fetch_waifus(search=search)
        if not waifus:
            return []
        return [AniList._process_character(w) for w in random.sample(waifus, min(count, len(waifus)))]

    @staticmethod
    async def get_random_characters(count: int = 3, search: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get multiple random characters."""
        characters = await AniList.fetch_characters_list(search=search)
        if not characters:
            return []
        return [AniList._process_character(c) for c in random.sample(characters, min(count, len(characters)))]

    @staticmethod
    def _process_character(character: Dict[str, Any]) -> Dict[str, Any]:
        """Process character data to extract info."""
        media = character.get("media", {}).get("edges", [])
        titles = list({m["node"]["title"]["romaji"] for m in media if m.get("node", {}).get("title")})
        anime_title = AniList._process_titles(titles) if titles else "Unknown"

        return {
            "name": character["name"]["full"],
            "image": character["image"]["large"],
            "age": character.get("age", "Unknown"),
            "gender": character.get("gender", "Unknown"),
            "description": AniList.clean_description(character.get("description", "")),
            "anime": anime_title
        }

    @staticmethod
    def _process_titles(titles: List[str]) -> str:
        """Simplify anime titles by removing common suffixes."""
        processed = [re.sub(r'\s*(?:Season|Part|Cour|Saga|Arc|:|\().*', '', t).strip() for t in titles]
        unique = list(dict.fromkeys(processed))
        return unique[0] if unique else titles[0]
