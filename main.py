#Imports
import base64
import os
from urllib import request
import webbrowser
from fastapi import FastAPI,Query,Path, HTTPException, status,Body, Request, Response, File, UploadFile, Form
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, HTMLResponse, StreamingResponse, FileResponse
from pydantic import BaseModel, Field, AnyUrl, FilePath
from typing import Optional, List, Dict
import datetime, base64

from db import actors
from db import characters
app=FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

#Actor age
def __init__(self,born_year):
         born_year=born_year;


# Models
class Actor(BaseModel):
    first_name:str
    last_name:str
    born_day:int
    born_month:int
    born_year:int
    awards:Optional [List[str]]
    movies:List[str]
    picture:str
    web:Optional[AnyUrl]
    instagram:Optional[str]

class Character(BaseModel):
    name: str
    lastname: str
    profession: str 
    role: str
    days_out_of_earth: int
    photo:str



#Home
@app.get("/", response_class=HTMLResponse)
def root(request:Request):
    return templates.TemplateResponse("index.html",
                                      {"request":request,
                                       "title":"The Martian WebApp",
                                       })

#Show all actors
@app.get(
    path="/actor",
    status_code=status.HTTP_200_OK,
    response_class=HTMLResponse,

    description="Return all the actors",
    tags=["Actor"]
)
def show_all_actor(request:Request, number:Optional[str]=Query("20", max_length=3)):
    response = []
    for id, actor in list(actors.items())[:int(number)]:
        response.append((id, actor))
    return templates.TemplateResponse("home.html",
                                      {"request":request,
                                       "actors":response,
                                        "edad":get_age,
                                       "title":"All actors"})


#Get age        
def get_age(old):
    date = datetime.date.today()
    year = int(date.strftime("%Y"))
    date=year-old
    return date


#Show an actor by id

@app.post(
    path="/search-actor",
    response_class=RedirectResponse
)
def search_actor(id: str = Form(...)):
    return RedirectResponse("/actor/" + id, status_code=status.HTTP_302_FOUND)


@app.get(
    path="/actor/{id}",
    response_model=Actor,
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Actor"],
    description="Return an Actor by an indicated id"
)
def show_actor(request:Request,id:int=Path(...,gt=0,lt=100)):
    actor = actors.get(id)
    response= templates.TemplateResponse("search.html",
                                       {"request":request,
                                         "actor":actor,
                                         "edad":get_age,
                                         "id":id,
                                         "title":"Actor"})
    if not actor:
        response.status_code = status.HTTP_404_NOT_FOUND
    return response

#About us

@app.get("/about", response_class=HTMLResponse)
def about_us(request:Request):
    return templates.TemplateResponse("aboutme.html",
                                      {"request":request,
                                       "title":"Profile",
                                       })


#Show all characters
@app.get(
    path="/character",
    status_code=status.HTTP_200_OK,
    response_class=HTMLResponse,

    description="Return all the characters from the movie",
    tags=["Character"]
)
def show_all_character(request:Request, number:Optional[str]=Query("20", max_length=3)):
    response = []
    for id, character in list(characters.items())[:int(number)]:
        response.append((id, character))
    return templates.TemplateResponse("home2.html",
                                      {"request":request,
                                       "characters":response,
                                       "title":"All characters"})

#Show a character by id

@app.post(
    path="/search-character",
    response_class=RedirectResponse
)
def search_character(id: str = Form(...)):
    return RedirectResponse("/character/" + id, status_code=status.HTTP_302_FOUND)


@app.get(
    path="/character/{id}",
    response_model=Actor,
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Character"],
    description="Return a character by an indicated id"
)
def show_character(request:Request,id:int=Path(...,gt=0,lt=100)):
    character = characters.get(id)
    response= templates.TemplateResponse("search2.html",
                                       {"request":request,
                                         "character":character,
                                         "id":id,
                                         "title":"Character"})
    if not character:
        response.status_code = status.HTTP_404_NOT_FOUND
    return response

#upload an image
#Upload an image

def is_directory_ready():
    os.makedirs(os.getcwd()+"/img", exist_ok=True)
    return os.getcwd()+"/img/"

@app.get("/upload", response_class=HTMLResponse)
def root(request:Request):
    return templates.TemplateResponse("upload_image.html",
                                      {"request":request,
                                       "title":"Upload an image",
                                       })


@app.post("/upload/image")
def upload(request: Request, file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        dir=is_directory_ready()
        with open(dir +"uploaded_" + file.filename, "wb") as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
        
    base64_encoded_image = base64.b64encode(contents).decode("utf-8")

    return templates.TemplateResponse("display.html", {"request": request,  "myImage": base64_encoded_image})
