import requests, json
from fastapi import APIRouter, HTTPException
from repository import run_search
from schemas import QueryCreate
from core.settings import USERS_ENDPOINT

search_router = APIRouter()

@search_router.post("/search/")
async def send_search(query: QueryCreate):
    api_key = query.api_key
    query_text = query.query
    response = requests.get(f"{USERS_ENDPOINT}/users?api_key={api_key}")
    if response.status_code == 200:
        data = await run_search(query_text)
        if data['statusCode'] == 200:
            payload = json.loads(data["body"])
            return {"results": payload["results"]}
        else:
            return {"results": "Service tempoarily unavailable"}
    else:
        error_body = response.json()
        raise HTTPException(status_code=response.status_code, detail=error_body["detail"])