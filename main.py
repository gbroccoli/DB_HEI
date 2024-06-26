from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
from database.connection import *
from typing import List, Dict
from pydantic import BaseModel

# routers
from routers.material import materials
from routers.upload import uploads
from routers.users import users
from routers.reports import reports


async def isUsers(request: Request) -> dict:
    id = request.cookies.get('id')

    if not id:
        return RedirectResponse('/login')

    res = await getUser(int(id))

    if not id:
        return RedirectResponse('/login')

    if res['role'] == "Администратор":
        return {
            "admin": True,
            "materOt": False,
            "user": False
        }
    elif res['role'] == "Материально. отвественный":
        return {
            "admin": False,
            "materOt": True,
            "user": False
        }
    elif res['role'] == "Преподаватель":
        return {
            "admin": False,
            "materOt": False,
            'user': True
        }


app = FastAPI()

tempalte = Jinja2Templates(directory="resources/views")

app.mount("/static", StaticFiles(directory="resources/"), name="resources")
app.mount("/public", StaticFiles(directory="public"), name="public")


@app.get("/")
async def index(request: Request):
    return RedirectResponse('/login')


@app.get('/login')
async def login(request: Request):

    auth = request.cookies.get('Auth')

    res = await isUsers(request)

    if auth:

        if res.get('admin'):
            return RedirectResponse('/admin')
        elif res.get('materOt'):
            return RedirectResponse('/materil')
        elif res.get('user'):
            return RedirectResponse('/user')

    return tempalte.TemplateResponse("login/login.j2", {"request": request})


class User(BaseModel):
    login: str
    password: str


@app.post('/login')
async def login(user: User, response: Response):
    res: Dict = await logins(user.login, user.password)

    if not res:
        return JSONResponse(content={"msg": "Invalid username or password"}, status_code=status.HTTP_401_UNAUTHORIZED)

    response.set_cookie(key="Auth", value="true", httponly=True, max_age=7200)
    response.set_cookie(key="id", value=res.get("id"),
                        httponly=True, max_age=7200)

    return {
        "id": res.get("id"),
        "role": res.get("role")
    }


@app.get('/admin')
async def admin(request: Request):
    auth = request.cookies.get('Auth')

    if not auth:
        return RedirectResponse('/')

    res = await isUsers(request)

    if not res.get('admin'):
        return RedirectResponse('/')

    return tempalte.TemplateResponse("admin/index.j2", {"request": request})


@app.get('/logout')
async def logout(request: Request, response: Response):

    response.delete_cookie("Auth")
    response.delete_cookie("id")

    return

app.include_router(materials)
app.include_router(uploads)
app.include_router(users)
app.include_router(reports)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', reload=True)
