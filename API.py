from fastapi import FastAPI, Request  
from fastapi.encoders import jsonable_encoder  
from pydantic import BaseModel  
from starlette.responses import JSONResponse  
from typing import Union
from pydantic import BaseModel
from typing import Optional  

# サーバ、兼ルーターの作成  
app = FastAPI()  

# ユーザークラス
class User(BaseModel):
  name: str
  conutry:str

# ハンドラ作成
@app.get("/hello")  
async def index():
  return {"hello": "world"}

@app.get("/country/{countryname}")  
async def country(countryname):
  return {"country": countryname}


# パスパラメータにしないとクエリパラメータ
@app.get("/country/")
async def country1(countryname:str='america',countryno:int=1):
  return {
    "country": countryname,
    'countryno':countryno}



class Item(BaseModel):
    name: str='gorira'
    description: Union[str, None] = None
    price: float=10
    tax: Union[float, None] = None

@app.post("/items/")
async def create_item(item: Item):
    return item


