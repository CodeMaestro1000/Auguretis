from fastapi import APIRouter, responses, status, Request
from fastapi.templating import Jinja2Templates
from producer import CreateRpcClient
from utils import is_user_logged_in, extract_text
import json

app_router = APIRouter()
templates = Jinja2Templates(directory="templates")

@app_router.get("/search")
async def search(request: Request):
    """
    Handles GET request to search page
    """
    user = await is_user_logged_in(request)
    # if not user: # redirect user if not logged in
    #     return responses.RedirectResponse(f"/login?next=app/search", status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse("search_experts.html", {"request": request, "user": user})


@app_router.get("/experts")
async def get_expert(request: Request, tag: str = ''):
    """
    Handles GET request to stack experts microservice

    Returns a template object with context
    """
    user = await is_user_logged_in(request)
        
    # if not user: # redirect user if not logged in
    #     return responses.RedirectResponse(f"/login?next=app/experts?tag={tag}", status_code=status.HTTP_302_FOUND)
    
    data = {}
    data['experts'] = []
    data['errors'] = []
    data['request'] = request
    if not tag:
        data['errors'].append("Tag cannot be empty")
        return templates.TemplateResponse("home.html", data)
    else:
        rpc_client = CreateRpcClient()
        response = await rpc_client.pubilsh(tag, "get experts", "experts")
        data['experts'] = json.loads(response.decode('utf-8'))
        for payload in data['experts']:
            payload['about'] = extract_text(payload['about'])
        if user:
            data["user"] = user
        return templates.TemplateResponse("experts.html", data)
