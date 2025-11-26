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

@app.post("/api/member")
def signup(body = Body(None)): 
    body = json.loads(body)
    name = body["name"]
    email = body["email"]
    password = body["password"]

    cursor = con.cursor()
    cursor.execute("SELECT * FROM member WHERE name = %s", (name,))
    result = cursor.fetchone()
    if result == None:
        cursor.execute("INSERT INTO member(name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        con.commit()
        return {"ok": True}
    else:
        return {"ok": False}

@app.put("/api/member/auth")
def sigin(request: Request,body = Body(None)):
    body = json.loads(body)
    email = body["email"]
    password = body["password"]
    cursor = con.cursor()
    cursor.execute("SELECT * FROM member WHERE email = %s AND password = %s", (email, password))
    result = cursor.fetchone()
    if result == None:
        request.session["member"] = None
        return {"ok": False}
    else:
        request.session["member"] = {
            "name": result[1],
            "email": result[2],
        }
        return {"ok": True}

# 檢查登入
@app.get("/api/member/auth")
def check_status(request: Request):
    if "member" in request.session and request.session["member"] != None:
        member = request.session["member"]
        return {"ok": True,"name": member["name"], "email": member["email"]}
    else:
        return {"ok": False}
    
app.mount("/",StaticFiles(directory="publics",html=True))
