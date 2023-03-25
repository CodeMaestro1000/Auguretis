from producer import CreateRpcClient
from fastapi.security.utils import get_authorization_scheme_param
from fastapi import Request
from bs4 import BeautifulSoup

def extract_text(text: str):
    if text:
        soup = BeautifulSoup(text, features="html.parser")
        elem = soup.find('p')
        if elem:
            elem_text = elem.text
            if len(elem_text) > 100:
                elem_text = elem_text[:100] + "..."
            return elem_text

    return '' 

async def is_user_logged_in(request: Request) -> str:
    """Returns the current username of user if logged in"""
    rpc_client = CreateRpcClient()
    token = request.cookies.get("access_token")
    _, param = get_authorization_scheme_param(token)  # scheme will hold "Bearer" and param will hold actual token value

    response = await rpc_client.pubilsh(param, "validate login")
    if response.decode('utf-8') == "No user logged in":
        return None
    
    return response.decode('utf-8').split(' ')[0]
