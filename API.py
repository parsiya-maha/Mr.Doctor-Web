# ---------------------------------------------------------------------------------------- Imports
#-----------------------------------------------------------------------------------------Mahdi

from fastapi import FastAPI, Request
from fastapi import FastAPI, File, UploadFile, Form , Body
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import webbrowser

from SMAmodel import LoginDataset,data_path,data_password,is_image_path,image_formats

from AI.BrainTumors import BrainTumorsPredictImage
from AI.BreastCancer import BreastCancerPredictImage
from AI.CervicalCancer import CervicalCancerPredictImage
from AI.LungCancer import LungCancerPredictImage
from AI.KidneyStone import KidneyStonePredictImage
from AI.ToRecognize import ToRecognizePredictImage
from AI import ToRecognizeAndPredictImage

import uvicorn

from DataBase import check_login_data_in_json,SignUp

# ---------------------------------------------------------------------------------------- Instance vars

#make api sample
app = FastAPI()

print(os.path.exists("static"))

#mount api to '/static' folder
app.mount("/static", StaticFiles(directory="static"), name="static")

#make template smaplle
templates = Jinja2Templates(directory="templates")

# ---------------------------------------------------------------------------------------- home

@app.get("/",
        tags=["Home"],
        summary="API for start of website (home)."
        )

async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

# ---------------------------------------------------------------------------------------- started

@app.get("/templates/test-start.html",
        tags=["Login","Start"],
        summary="API for started page (login)."
        )

async def started(request : Request):
    return templates.TemplateResponse(request=request, name="test-start.html")

# ---------------------------------------------------------------------------------------- main

@app.get("/templates/main.html",
        tags=["Main"],
        summary="API for main page (AI page)."
        )

async def main(request : Request):
    return templates.TemplateResponse(request=request, name="main.html")

# ---------------------------------------------------------------------------------------- article_brain

@app.get("/templates/articlebrain.html",
        tags=["Article"],
        summary="API for /articlebrain.html page."
        )

async def article_brain(request : Request):
    return templates.TemplateResponse(request=request, name="articlebrain.html")

# ---------------------------------------------------------------------------------------- article_kidney

@app.get("/templates/articleKidney.html",
        tags=["Article"],
        summary="API for /articleKidney.html page."
        )

async def article_kidney(request : Request):
    return templates.TemplateResponse(request=request, name="articleKidney.html")

# ---------------------------------------------------------------------------------------- article_lung

@app.get("/templates/articlelung.html",
        tags=["Article"],
        summary="API for /articlelung.html page."
        )

async def article_lung(request : Request):
    return templates.TemplateResponse(request=request, name="articlelung.html")

# ---------------------------------------------------------------------------------------- upload_image

@app.post("/templates/main.html/upload",
        tags=["Upload Image"],
        summary="Upload image and give the AI result."
        )

async def upload_image(image: UploadFile = File(...), option: str = Form(...)):
    try:
        contents = await image.read()
        # Here you can do something with the image data, for example, save it to disk
        path = option + "_" + image.filename

        if not is_image_path(path):
            
            return {"massage":"ERROR (bad format of image.)","path":path,"result":f"image format\
 most be {','.join(image_formats)}"}

        with open(path, "wb") as f:
            f.write(contents)

        if option == "BrainTumors":
            from AI.BrainTumors import BrainTumorsPredictImage as predict_model

        elif option == "BreastCancer" :
            from AI.BreastCancer import BreastCancerPredictImage as predict_model

        elif option == "CervicalCancer" :
            from AI.CervicalCancer import CervicalCancerPredictImage as predict_model

        elif option == "LungCancer":
            from AI.LungCancer import LungCancerPredictImage as predict_model

        elif option == "KidneyStone":
            from AI.KidneyStone import KidneyStonePredictImage as predict_model

        elif option == "ToRecognize":
            from AI.ToRecognize import ToRecognizePredictImage as predict_model

        elif option == "ToRecognizeAndPredict":
            from AI import ToRecognizeAndPredictImage as predict_model

        else :
            return {"massage":"ERROR in process","path":path,"result":f"No {option} model found."}

        # predict model
        res = predict_model(path)

        # remove download file
        os.remove(path)
        
        return {"massage":"Successfully","path":path,"result":res}

    except Exception as Ex:
            return {"ERROR massage":str(Ex),
            "ERROR type":Ex.__class__.__name__
            }

# ---------------------------------------------------------------------------------------- check_login_input_data

@app.post("/templates/test-start.html/login",
        tags=["Login"],
        summary="Post login data to api and check them."
        )

async def check_login_input_data(username:str = Form(...),password:str = Form(...)):
    res = check_login_data_in_json(username,password)

    if res : 
        return {"massage":"Successfully login","massage_bool":True}

    return {"massage":"Username or Password was wrong","massage_bool":False}

# ---------------------------------------------------------------------------------------- signup


#-----------------------------------------------------------------------

@app.get('/templates/test-start.html/signup',
        tags = ['Signup'],
        summary = 'If we have error in signup the function return string else (all thing OK) return True',
        description = 'If we have error in signup the function return string else (all thing OK) return True',
        status_code=200
        )

def add_user_signup(
    fname: str= Form(...),
    lname: str= Form(...),
    username: str= Form(...),
    email: str= Form(...),
    password: str= Form(...),
    rpassword: str= Form(...)
                   ):    
    
    """'If we have error in signup the function return string else (all thing OK) return True'

    Returns:
        _type_: 
            1- All thing was OK   : -> True (bool)
            2- When we have error : -> str  (string)
    """
    
    res = SignUp.signup_in_app_json(fname=fname,lname=lname,username=username,email=email,password=password,rpassword=rpassword)

    return {
        'massage' : res,
        'status code' : 200
    }


# ---------------------------------------------------------------------------------------- start api

if __name__ == "__main__":
    uvicorn.run("API:app",host="127.0.0.1" ,port=8000, log_level="info")