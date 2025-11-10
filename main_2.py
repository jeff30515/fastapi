from fastapi import FastAPI,Path,Query,Request
from typing import Annotated  # for type hinting
from fastapi.responses import JSONResponse,HTMLResponse,FileResponse,RedirectResponse,PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi import Body
import json
import mysql.connector
from starlette.middleware.sessions import SessionMiddleware
app =FastAPI()
app.add_middleware(SessionMiddleware,secret_key="123")

@app.get("/hello")
def hello(request: Request,name):
    request.session["data"] = name
    return {"msg":"你好,"+name}

@app.get("/talk")
def talk(request: Request):
    if "data" in request.session:
        name = request.session['data']
        return {"msg":name+",歡迎回來"}
    else:
        return{"msg":"你是誰?"}
    

app.mount("/",StaticFiles(directory="public",html=True))