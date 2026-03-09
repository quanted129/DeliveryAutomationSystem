import httpx
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY_YANDEX_GEO")
BASE_URL = os.getenv("URL_YANDEX_GEO")

class GeocodingError(Exception):
    pass

def geocode_address(address_string: str) -> tuple[float, float]:
    """Convert address string, into a coordinate tuple (latitude, longitude)."""

    params = {
        "apikey": API_KEY,
        "geocode": address_string,
        "format": "json"
    }

    try:
        response = httpx.get(BASE_URL, params=params, timeout=5.0)
        response.raise_for_status()
    except httpx.RequestError as e:
        raise GeocodingError(f"Network error communicating with Yandex: {e}")

    data = response.json()

    try:
        feature_member = data["response"]["GeoObjectCollection"]["featureMember"]
        if not feature_member:
            raise GeocodingError(f"Address '{address_string}' not found by Yandex.")

        pos_string = feature_member[0]["GeoObject"]["Point"]["pos"]
        lon_str, lat_str = pos_string.split()

        return float(lat_str), float(lon_str)

    except KeyError:
        raise GeocodingError("Unexpected response format from Yandex.")