import requests
from typing import List
from fastapi import APIRouter, HTTPException
from repository import make_bigquery_request
from schemas import ShowItems
from core.settings import USERS_ENDPOINT
from main import client

expert_router = APIRouter()

@expert_router.get("/experts/", response_model= List[ShowItems])
async def get_experts(tag: str, api_key: str):
    """
    Handles GET request to get_experts route

    Asynchronous because the bigquery request might take some time

    Returns data in json format or raises a HTTP exception
    """
    response = requests.get(f"{USERS_ENDPOINT}/users?api_key={api_key}")
    if response.status_code == 200:
        data = await make_bigquery_request(client, tag)
        return data
    else:
        error_body = response.json()
        raise HTTPException(status_code=response.status_code, detail=error_body["detail"])