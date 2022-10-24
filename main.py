#Imports
import os
import webbrowser
from fastapi import FastAPI,Query,Path, HTTPException, status,Body, Request, Response, File, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, HTMLResponse, StreamingResponse, FileResponse
from pydantic import BaseModel, Field, AnyUrl, FilePath
from typing import Optional, List, Dict

from db import actors

app=FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def root(request:Request):
    return templates.TemplateResponse("index.html",
                                      {"request":request,
                                       "title":"The Martian WebApp",
                                       "text":"This is a text no hardcoded"})

    



class Actor(BaseModel):
    first_name:str
    last_name:str
    born_day:int
    born_month:int
    born_year:int
    awards:List[str]
    movies:List[str]
 
    web:Optional[AnyUrl]
    instagram:str

#Upload an image

def is_directory_ready():
    os.makedirs(os.getcwd()+"/img", exist_ok=True)
    return os.getcwd()+"/img/"

@app.post(
    path="/upload",
    status_code=status.HTTP_201_CREATED
)
async def upload_pic(
        image:UploadFile=File(...)
):
    dir=is_directory_ready()
    with open(dir+image.filename, "wb") as myimage:
        content = await image.read()
        myimage.write(content)
        myimage.close()

    return "Image succesfully uploaded"

#Show all actors
@app.get(
    path="/actor",
    status_code=status.HTTP_200_OK,
    response_class=HTMLResponse,

    description="Return all the actors",
    tags=["Actor"]
)
def show_all_actor(request:Request, number:Optional[str]=Query("5", max_length=3)):
    response = []
    for id, actor in list(actors.items())[:int(number)]:
        response.append((id, actor))
    return templates.TemplateResponse("home.html",
                                      {"request":request,
                                       "actors":response,
                                       "title":"All actors"})


#Show an actor by id

@app.get(
    path="/actor/{id}",
    response_model=Actor,
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Actor"],
    description="Return an Actor by an indicated id"
)
def show_actor(id:int=Path(...,gt=0,lt=100)):
    actor = actors.get(id)
    if not actor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The actor does not participate in this movie")
    return actor

