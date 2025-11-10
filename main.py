from fastapi import FastAPI,Path,Query
from typing import Annotated  # for type hinting
from fastapi.responses import JSONResponse,HTMLResponse,FileResponse,RedirectResponse,PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi import Body
import json
import mysql.connector
con = mysql.connector.connect(
    user="root",
    password="anny880618",
    host="127.0.0.1",
    database="mydb"
)
app = FastAPI()
#uvicorn main:app --reload --port 500
# @app.get("/")
# def index():
#     return {"data":"Home Page"}
@app.get("/")
def root():
    return FileResponse("static/index.html")

@app.get("/baibai")
def getBaibai():
    return FileResponse("白白.png")

@app.get("/data")
def getData():
    return {"data":[2,3,1]}

# @app.get("/square/{number}")
# #驗證number為int
# def getItem(number: Annotated[float,None]):
#     number=float(number)
#     return {"result":number*number}


@app.get("/square/{number}")
#Path參數限制 Query參數驗證
#驗證number範圍gt>0 lt<100
#ge>= le<= gt> lt<
#min_length max_length #驗證字串長度
def getItem(number: Annotated[float,Path(gt=0,lt=100)]):
    number=float(number)
    return {"result":number*number}

@app.get("/hello")
def sayHello(name: str):
    return {"message":f"Hello {name}"}

@app.get("/multiply")
def multiply(
    a: Annotated[int, Query(ge=-10, le=10)],
    b: Annotated[int, Query(ge=-10, le=10)]):
    a,b=int(a),int(b)
    return {"result": a * b}


# PlainTextResponse, HTMLResponse, FileResponse, RedirectResponse
@app.get("/plaintext", response_class=PlainTextResponse)
def getPlainText():
    return "This is a plain text response from FastAPI."

@app.get("/info", response_class=HTMLResponse)
def getInfo():
    html_content="""
    <html>
        <head>
            <title>Info Page</title>
        </head>
        <body>
            <h1>This is an info page</h1>
            <p>Welcome to the info page of our FastAPI application.</p>
        </body>
    </html>
    """
    return html_content

#下載檔案
@app.get("/download", response_class=FileResponse)
def downloadFile():
    file_path="home.html"  # Ensure this file exists in the same directory
    return FileResponse(path=file_path, filename="home.html", media_type='application/octet-stream')   

# 導向
@app.get("/redirect", response_class=RedirectResponse)
def redirectToHome():
    return RedirectResponse(url="/")


@app.get("/test")
def test():
    return{"data":10,"method":"GET"}

@app.post("/test")
def testPost(body = Body(None)):
    data = json.loads(body)
    print(data)
    return{"result":data["x"]}


# 靜態檔案服務
# 綁定首頁
# html=True 代表預設載入index.html
app.mount("/static", StaticFiles(directory="static"), name="static")