from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import RedirectResponse,HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from models import user as userModel

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    userName = form.username
    password = form.password
    user = userModel.getUser(userName)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username")
    elif password != user["password"]:
        raise HTTPException(status_code=400, detail="Incorrect password")
    return RedirectResponse(url="/login/success" + "?username=" + user["username"],status_code=status.HTTP_302_FOUND)

@app.get("/login/success", response_class=HTMLResponse)
async def success(request: Request, username: str):
    return templates.TemplateResponse("success.html", {"request": request, "username": username.upper()})

@app.get("/register")
async def register():
