from typing import Optional

import httpx
from django.conf import settings
from pydantic import Field

from pyhub.mcptools import mcp
from pyhub.mcptools.maps.types import (
    NaverMapRouteOptions,
    NaverMapCarTypes,
    NaverMapResponseLanguages,
    NaverMapFuelTypes,
    NaverMapGeocodingResponseLanguages,
)

ENABLED_MAPS_NAVER_TOOLS = settings.NAVER_MAP_CLIENT_ID and settings.NAVER_MAP_CLIENT_SECRET

NAVER_MAP_HEADERS = {
    "X-NCP-APIGW-API-KEY-ID": settings.NAVER_MAP_CLIENT_ID,
    "X-NCP-APIGW-API-KEY": settings.NAVER_MAP_CLIENT_SECRET,
}


@mcp.tool(enabled=ENABLED_MAPS_NAVER_TOOLS)
async def maps__naver_geocode(
    query: str = Field(
        ...,
        description=(
            "Address to geocode (Korean legal/administrative address only. Place names are not supported). "
            "Both full addresses and partial addresses are supported."
        ),
        examples=[
            "불정로 6",  # 부분 주소
            "분당구 불정로 6",  # 구+도로명
            "경기도 성남시 분당구 불정로 6",  # 전체 주소
        ],
    ),
    coordinate: Optional[str] = Field(
        None,
        description="Coordinates for coordinate-based search (longitude,latitude)",
        examples=["127.1054328,37.3595963"],
    ),
    language: Optional[NaverMapGeocodingResponseLanguages] = Field(
        NaverMapGeocodingResponseLanguages.KOREAN,
        description="Response language",
    ),
) -> str:
    """
    Geocode an address using Naver Maps Geocoding API.
    Converts Korean addresses to coordinates.

    Args:
        query (str): Address to geocode. Must be a legal (법정동) or administrative (행정동) address.
                    Place names or points of interest (e.g., "강남역", "코엑스") are not supported.
                    Both full addresses and partial addresses work:
                    - Full address: "경기도 성남시 분당구 불정로 6"
                    - Partial address: "불정로 6" or "분당구 불정로 6"
        coordinate (str, optional): Coordinates for coordinate-based search in "longitude,latitude" format
        language (NaverMapGeocodingResponseLanguages, optional): Response language. Defaults to kor

    Returns:
        str: JSON response containing geocoding results including coordinates and address details

    Note:
        - This API works best with Korean addresses.
        - Only legal (법정동) or administrative (행정동) addresses are supported.
        - The coordinate parameter can be used to improve search accuracy in specific areas.
        - Place names, landmarks, or business names will not return results.
        - You can use either full addresses or partial addresses. When using partial addresses,
          the API will attempt to find the best match, but may return multiple results.
    """
    api_url = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"
    params = {
        "query": query,
        "language": language,
    }

    if coordinate:
        params["coordinate"] = coordinate

    async with httpx.AsyncClient() as client:
        res = await client.get(api_url, headers=NAVER_MAP_HEADERS, params=params)
        return res.text


@mcp.tool(enabled=ENABLED_MAPS_NAVER_TOOLS)
async def maps__naver_route(
    start_lnglat: str = Field(
        ...,
        description="Starting point coordinates in longitude,latitude format (South Korea only)",
        examples=["127.027619,37.497952"],
    ),
    goal_lnglat: str = Field(
        ...,
        description="Destination coordinates in longitude,latitude format (South Korea only)",
        examples=["126.92361,37.55667"],
    ),
    waypoints: Optional[list[str]] = Field(
        None,
        description=(
            "List of waypoint coordinates (max 5 waypoints). "
            "Each waypoint should be in 'longitude,latitude' format. "
            "For waypoints with two coordinate pairs, use 'lng1,lat1:lng2,lat2' format. "
            "Must be within South Korea (longitude: 124-132°E, latitude: 33-39°N)."
        ),
        examples=[
            # Single coordinate pair examples
            ["127.12345,37.12345", "128.12345,38.12345"],
            # Two coordinate pairs example
            ["127.12345,37.12345:127.23456,37.23456"],
        ],
    ),
    option: Optional[NaverMapRouteOptions] = Field(
        NaverMapRouteOptions.FASTEST,
        description="Route search option",
    ),
    cartype: Optional[NaverMapCarTypes] = Field(
        NaverMapCarTypes.GENERIC_CAR,
        description="Car type for toll fee calculation. Use 1 for all regular passenger vehicles. ",
    ),
    fueltype: Optional[NaverMapFuelTypes] = Field(
        NaverMapFuelTypes.GASOLINE,
        description="Fuel type",
    ),
    mileage: float = Field(14, description="Vehicle fuel efficiency in km/L (kilometers per liter)"),
    lang: Optional[NaverMapResponseLanguages] = Field(
        NaverMapResponseLanguages.KOREAN, description="Response language"
    ),
) -> str:
    """
    Get driving directions between two points using Naver Maps Direction API.
    Only supports locations within South Korea.

    Args:
        start_lnglat (str): Starting point coordinates in "longitude,latitude" format
                           (Must be within South Korea)
        goal_lnglat (str): Destination coordinates in "longitude,latitude" format
                          (Must be within South Korea)
        waypoints (list[str], optional): List of waypoint coordinates (max 5 waypoints).
                                         Each waypoint should be in 'longitude,latitude' format.
                                         For waypoints with two coordinate pairs, use 'lng1,lat1:lng2,lat2' format.
                                         Must be within South Korea (longitude: 124-132°E, latitude: 33-39°N).
        option (NaverMapRouteOptions, optional): Route search option. Defaults to FASTEST.
        cartype (NaverMapCarType, optional): Vehicle type for toll fee calculation.
                                             Use 1 for all regular passenger vehicles.
                                             This only affects toll fee calculations and does not
                                             consider vehicle weight or size.
        fueltype (NaverMapFuelTypes, optional): Fuel type. Defaults to GASOLINE.
        mileage (float, optional): Vehicle fuel efficiency in km/L (kilometers per liter). Defaults to 14.
        lang (NaverMapResponseLanguages, optional): Response language. Defaults to KOREAN.

    Returns:
        str: JSON response containing route information

    Note:
        This API only works for coordinates within South Korea.
        Typical coordinate ranges for South Korea:
        - Latitude: 33° to 39° N (33.0 to 39.0)
        - Longitude: 124° to 132° E (124.0 to 132.0)
    """

    api_url = "https://naveropenapi.apigw.ntruss.com/map-direction/v1/driving"
    params = {
        "start": start_lnglat,
        "goal": goal_lnglat,
        "option": option,
        "cartype": cartype,
        "fueltype": fueltype,
        "mileage": mileage,
        "lang": lang,
    }

    if waypoints:
        if len(waypoints) > 5:
            raise ValueError("Maximum 5 waypoints are allowed")
        params["waypoints"] = "|".join(waypoints)

    async with httpx.AsyncClient() as client:
        res = await client.get(api_url, headers=NAVER_MAP_HEADERS, params=params)
        return res.text
