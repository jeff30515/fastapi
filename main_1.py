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
    database="fastapi"
)
app = FastAPI()

@app.post("/api/message")
def create_message(body = Body(None)):
    body = json.loads(body)
    author = body["author"]
    content = body["content"]
    cursor = con.cursor()
    cursor.execute("INSERT INTO message(author, content) VALUES (%s, %s)", (author, content))
    con.commit()
    return {"ok": True}

@app.get("/createMessage")
def create_message(
    author: Annotated[str, None],
    content: Annotated[str, None]
):
    cursor = con.cursor()
    cursor.execute("INSERT INTO message(author, content) VALUES (%s, %s)", (author, content))
    con.commit()
    return {"message": "Message created successfully"}

@app.get("/api/message")
def get_messages():
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM message")
    messages = cursor.fetchall()
    return messages

@app.delete("/api/message/{message_id}")
def delete_message(message_id):
    cursor = con.cursor()
    cursor.execute("DELETE FROM message WHERE id = %s", [message_id])
    con.commit()
    return {"ok": True}

app.mount("/", StaticFiles(directory="public",html=True))
print("資料庫連線成功")