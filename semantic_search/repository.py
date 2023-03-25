"""Handles all business logic for this service"""
import httpx
from core.settings import SEARCH_ENDPOINT_URL

async def run_search(keyword):
    request = {"inputs": keyword}
    async with httpx.AsyncClient() as client:
        response = await client.post(SEARCH_ENDPOINT_URL, json=request)
        return response.json()