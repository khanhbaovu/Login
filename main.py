from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import RedirectResponse,HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from models import user as userModel

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

SECRET = "secret-key"
manager = LoginManager(SECRET,tokenUrl="/login",use_cookie=True)
manager.cookie_name = "some-name"


@manager.user_loader
def user_loader(userName):
    return userModel.getUser(userName)

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    userName = form.username
    password = form.password
    user = user_loader(userName)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username")
    elif password != user["password"]:
        raise HTTPException(status_code=400, detail="Incorrect password")
    access_token = manager.create_access_token(
        data={"sub":user['username']}
    )
    resp = RedirectResponse(url="/login/success" + "?username=" + user["username"],status_code=status.HTTP_302_FOUND)
    manager.set_cookie(resp,access_token)
    print("Error")
    return resp

@app.get("/login/success", response_class=HTMLResponse)
async def success(request: Request, username: str, token:str =Depends(manager)):
    return templates.TemplateResponse("success.html", {"request": request, "username": username.upper()})

@app.get("/register", response_class=HTMLResponse)
async def register(request : Request):
    return templates.TemplateResponse("register.html", {"request" : request})

@app.post("/register/authen")
async def register(form : OAuth2PasswordRequestForm = Depends()):
    userName = form.username
    password = form.password
    if userModel.checkUserName(userName):
        userModel.addUser(userName, password)
    else:
        raise HTTPException(status_code=400, detail="UserName exists")
    return RedirectResponse(url="/",status_code=status.HTTP_302_FOUND)
