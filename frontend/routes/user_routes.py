from fastapi import APIRouter, Request, responses, status
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from config.settings import USERS_ENDPOINT
import httpx
from producer import CreateRpcClient
from forms import UserCreateForm, LoginForm
from schemas import UserCreate
from utils import is_user_logged_in

templates = Jinja2Templates(directory="templates")
frontend_users_router = APIRouter()

# ******************************************* Frontend main routes ***********************************************
# ********************* Uses RPC (RabbitMQ) pattern for communication with Users microservice ********************

@frontend_users_router.get("/")
async def home(request: Request):
    """
    Handles GET request to home route

    Returns a TemplateResponse
    """
    user = await is_user_logged_in(request)
    if not user: # redirect user if not logged in
        return templates.TemplateResponse("home.html", {"request": request})

    return templates.TemplateResponse("home.html", {"request": request, "user": user})

@frontend_users_router.get("/signup")
@frontend_users_router.post("/signup")
async def signup(request: Request):
    """
    Handles GET and POST Request to signup route
    
    Returns a TemplateResponse (GET, Form validation errors) or RedirectResponse (POST)
    """
    if request.method == "GET":
        return templates.TemplateResponse("signup.html", {"request": request})
    
    if request.method == "POST":
        form = UserCreateForm(request)
        rpc_client = CreateRpcClient()# uses AMPQ_URL by default

        await form.load_data()
        if await form.is_valid():
            user = UserCreate(username=form.username, email=form.email, password=form.password)
            
            response = await rpc_client.pubilsh(jsonable_encoder(user), "user create")
            response = response.decode('utf-8')

            if response == 'Success':
                return responses.RedirectResponse("/login?msg=Registration Successful&style=success&head=Welcome", status_code=status.HTTP_302_FOUND)

            elif response == "Failure: User Already exists":
                form.__dict__.get("errors").append("Duplicate username or email")
                return templates.TemplateResponse("signup.html", form.__dict__)
            else:
                form.__dict__.get("errors").append("Something went wrong")
                return templates.TemplateResponse("signup.html", form.__dict__)

        return templates.TemplateResponse("signup.html", form.__dict__) # returns if the form isn't valid

@frontend_users_router .get("/login")
@frontend_users_router .post("/login")
async def login(request: Request, msg: str = '', style: str = '', head: str = '', next: str = ''):
    """
    Handles GET and POST Request to login route
    
    Returns a TemplateResponse (GET,  Form validation errors) or RedirectResponse (POST)
    """
    if request.method == "GET":
        return templates.TemplateResponse("login.html", {"request": request, "msg": msg, "style": style, "head": head})
    
    if request.method == "POST":
        form = LoginForm(request)
        rpc_client = CreateRpcClient()# uses AMPQ_URL by default

        await form.load_data()
        if await form.is_valid():
            data = form.form_dict() # create dict for username and password of form # see implementation of LoginForm

            login_response = await rpc_client.pubilsh(data, "login")
            login_response = login_response.decode('utf-8')

            if login_response == "Incorrect email/password":
                form.__dict__.update(msg="")
                form.__dict__.get("errors").append("Incorrect Email or Password")
                return templates.TemplateResponse("login.html", form.__dict__)
            
            # access token will be stored in login response if successful
            else: 
                if next: # send user to the previous page if there was one
                    response = responses.RedirectResponse(f"/{next}", status_code=status.HTTP_302_FOUND)
                else:
                    response = responses.RedirectResponse(f"{frontend_users_router.url_path_for('home')}", status_code=status.HTTP_302_FOUND)
                response.set_cookie(key="access_token", value=f"Bearer {login_response}", httponly=True)  #set HttpOnly cookie in response
                return response
        
        return templates.TemplateResponse("login.html", form.__dict__) # returns if form.is_valid() fails

@frontend_users_router .get("/logout")
async def logout(request: Request):
    """
    Handles GET request to logout route

    Returns a RedirectResponse
    """
    user = await is_user_logged_in(request)
    if user:
        response = responses.RedirectResponse(f"{frontend_users_router .url_path_for('login')}", status_code=status.HTTP_302_FOUND)
        response.delete_cookie("access_token")
        return response
    return responses.RedirectResponse(f"{frontend_users_router .url_path_for('login')}", status_code=status.HTTP_302_FOUND)
        
# ********************* Routes for frontend validation of email and username *******************
# ********************* Uses REST for communication with Users microservice ********************

@frontend_users_router.get("/verify-email/{email}/")
async def verify_email(email: str):
    """
    Handles GET request to verify_email route

    Verifies email doesn't exist with RESTful request to Users microservice

    Returns a dict
    """
    # async with httpx.AsyncClient() as client:
    #     response = await client.get(f"{USERS_ENDPOINT}/users/email-exists/{email}/")       
    #     if response.json()['exists'] == "False": # No user
    #         return {'status': '200'}
    #     else:
    #         return {'status': '400'}
    rpc_client = CreateRpcClient()
    response = await rpc_client.pubilsh(email, "validate email")
    response = response.decode('utf-8')
    if response == 'not found':
        return {'status': '200'}
    return {'status': '400'}

@frontend_users_router.get("/verify-username/{username}/")
async def verify_username(username: str):
    """
    Handles GET request to verify_username route

    Verifies username doesn't exist with RESTful request to Users microservice

    Returns a dict
    """
    # async with httpx.AsyncClient() as client:
    #     response = await client.get(f"{USERS_ENDPOINT}/users/user-exists/{username}/")
    #     if response.json()['exists'] == "False": # No user
    #         return {'status': '200'}
    #     else:
    #         return {'status': '400'}
    rpc_client = CreateRpcClient()
    response = await rpc_client.pubilsh(username, "validate username")
    response = response.decode('utf-8')
    if response == 'not found':
        return {'status': '200'}
    return {'status': '400'}