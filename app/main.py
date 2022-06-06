from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from enum import Enum

templates=Jinja2Templates(directory="templates")

class ModelSize(str, Enum):
    small = "S"
    medium = "M"
    large = "L"

app=FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/",response_class=HTMLResponse)
async def root(request: Request):    
    return templates.TemplateResponse("index.html", {"request": request,"message": "Hello World"})

@app.get("/users/me",response_class=HTMLResponse)
async def read_user_me(request: Request):   
    return templates.TemplateResponse("users/index.html", {"request": request,"user_id": "the current user"})


@app.get("/users/{user_id}",response_class=HTMLResponse)
async def read_user(user_id: str,request: Request):    
    return templates.TemplateResponse("users/index.html", {"request": request,"user_id": user_id})

@app.get("/items/{item_id}",response_class=HTMLResponse)
async def read_item(item_id: int,request: Request):   
    return templates.TemplateResponse("item.html", {"request": request,"item_id": item_id})   

@app.get("/models/{model_name}")
async def get_model(model_name: ModelSize):
    if model_name == ModelSize.small:
        return {"model_name": model_name, "message": "Small Size"}

    if model_name.value == "medium":
        return {"model_name": model_name, "message": "Medium Size"}

    return {"model_name": model_name, "message": "Large Size"}
