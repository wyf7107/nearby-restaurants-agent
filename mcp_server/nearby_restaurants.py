from typing import Any
import httpx
import os
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)
load_dotenv(dotenv_path="./.env")
mcp = FastMCP("nearby_restaurants")


GOOGLE_MAP_GEOCODE = "https://maps.googleapis.com/maps/api/geocode/json"
GOOGLE_MAP_SEARCH = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

async def search_nearby_restaurants_func(long: str, lat: str):
    """
    Searches for nearby restaurants using the Google Places API.

    Parameters:
        long (str): Longitude of the location.
        lat (str): Latitude of the location.
        api_key (str): Your Google Maps API key.
        radius (int): Search radius in meters (default is 1000m).

    Returns:
        list: A list of dictionaries representing nearby restaurants, or an empty list if none found.
    """
    params = {
        "location": f"{lat},{long}",
        "radius": 3000,
        "type": "restaurant",
        "key": GOOGLE_API_KEY
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(GOOGLE_MAP_SEARCH, timeout=30.0, params=params)
            response.raise_for_status()
            logger.info(response.json())
            return response.json()
        except Exception as e:
            logger.error(e)
            return None

async def get_geo_from_address(address: str):
    params = {
        "address": address,
        "key": GOOGLE_API_KEY
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(GOOGLE_MAP_GEOCODE, timeout=30.0, params=params)
            response.raise_for_status()
            logger.info(response.json()['results'][0]['geometry']['location'])
            return response.json()
        except Exception:
            return None


@mcp.tool()
async def get_nearby_restaurants(long: str, lat: str) -> str:
    """Get nearby restaurants from a location.

    Args:
        long: longtitiude of the location
        lat: lattitude of the location
    """
    data = await search_nearby_restaurants_func(long, lat)
    if not data:
        return "Unable to find restaurants"
    return data

@mcp.tool()
async def address_to_geocode(address: str) -> str:
    """Convert an address to a geo code.

    Args:
        address: address to convert
    """
    data = await get_geo_from_address(address)
    logger.info(data)
    if not data:
        return "Unable to convert to geo code"
    return data


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')