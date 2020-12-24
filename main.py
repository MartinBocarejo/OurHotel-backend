from db.user_db import UserInDB
from db.user_db import update_user, get_user, post_user
from models.user_models import UserIn, UserOut, LogIn
from fastapi import FastAPI, HTTPException

api = FastAPI()

from fastapi.middleware.cors import CORSMiddleware
origins = [
    "http://localhost.tiangolo.com", "https://localhost.tiangolo.com",
    "http://localhost", "http://localhost:8080", # Origenes validos
]
api.add_middleware(
    CORSMiddleware, allow_origins=origins,
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)



@api.post("/user/login/")
async def loguin(Log_in: LogIn):
    password_origin = post_user(Log_in.username)
    if password_origin == None:
        raise HTTPException(status_code=404, detail="El usuario no existe")
    if password_origin != Log_in.password:
        raise HTTPException(status_code=400, detail="Usuario y/o contraseña Incorrecta")
    return {"Existe": True}


@api.put("/user/perfil/")
async def new_phone(user_in: UserIn):
    user_in_db = get_user(user_in.username)
    if user_in_db == None:
        raise HTTPException(status_code=404, detail="El usuario no existe")
    if user_in_db.password == user_in.password:
        user_in_db.phone = user_in.phone
        user_in_db = update_user(user_in_db)
        user_out = UserOut(**user_in_db.dict())
        return  user_out
    return "Contraseña incorrecta" 


@api.get("/user/perfil/{username}")
async def view_user(username: str):
    user_in_db = get_user(username)
    if user_in_db == None:
        raise HTTPException(status_code=404, detail="El usuario no existe")
    user_out = UserOut(**user_in_db.dict())
    return  user_out









    
