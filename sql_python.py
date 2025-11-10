from fastapi import FastAPI,Path,Query
from typing import Annotated  # for type hinting
from fastapi.responses import JSONResponse,HTMLResponse,FileResponse,RedirectResponse,PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi import Body
import json
import mysql.connector
app = FastAPI()
@app.get("/")
def root():
    return ("hello world")

con = mysql.connector.connect(
    user="root",
    password="anny880618",
    host="127.0.0.1",
    database="mydb"
)

print("資料庫連線成功")
cursor = con.cursor()
productname = "拿鐵咖啡"
productid = 2
cursor.execute("update product set name = %s where id = %s", (productname, productid))
cursor.execute("select * from product")
data = cursor.fetchall()
print(data)
#逐一取得資料
for row in data:
    print(row[0], row[1])
# cursor.execute("delete from product where id = 7")
con.commit()
con.close()