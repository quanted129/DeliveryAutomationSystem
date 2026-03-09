import httpx
from typing import List, Tuple
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("URL_OSRM_TABLE")

def get_time_matrix(coordinates: List[Tuple[float, float]]) -> list[list[float]]:
    """Convert all points into a "distance matrix" (duration-based)"""
    coord_strings = [f"{lon},{lat}" for lat, lon in coordinates]
    url = BASE_URL + ";".join(coord_strings)

    try:
        response = httpx.get(url, timeout=10.0)
        print(response.url)
        response.raise_for_status()
        data = response.json()
        return data.get("durations", [])
    except httpx.RequestError as e:
        print(f"OSRM Error: {e}")
        return []