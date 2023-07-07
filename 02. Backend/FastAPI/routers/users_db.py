# Clase en vídeo: https://youtu.be/_y9qQZXE24A?t=20480

### Users DB API ###

from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.client import db_client
from db.schemas.user import user_sch, users_schema
from bson import ObjectId

router = APIRouter(prefix = "/userdb",
                   tags = ["userdb"],
                   responses = {status.HTTP_404_NOT_FOUND: {"message" : "No encontrado"}})

# Inicia el server: uvicorn users:app --reload

@router.get("/", response_model = list[User])
async def users():
    return users_schema(db_client.local.users.find())

# Path
@router.get("/{id}")
async def user(id: str):
    return search_user("_id", ObjectId(id))

@router.get("/")    
async def user(id: str):
    return search_user("_id", ObjectId(id))

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")
    
    user_dict = dict(user)
    del  user_dict["id"]

    id = db_client.local.users.insert_one(user_dict).inserted_id
    new_user = user_sch(db_client.local.users.find_one({"_id":id}))

    return User(**new_user)

@router.put("/", response_model=User)
async def user(user: User):

    user_dict = dict(user)
    del  user_dict["id"]

    try:
        db_client.local.user.find_one_and_replace(
            {"_id": ObjectId(user.id)}, user_dict)
    except:
        return {"error": "No se ha actualizado el usuario"}
    
    return search_user("_id", ObjectId(user.id))

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def user(id: str):
    found = db_client.local.users.find_one_and_delete({"_id": ObjectId(id)})
    if not found:
        return {"error": "No se ha eliminado el usuario"}
    else:
        return user

def search_user_by_email(email: str):
    
    try:
        user = db_client.local.users.find_one({"email":email})
        return User(**user_sch(user))
    except:
        return {"error":"No se ha encontrado el ususario"}
    
def search_user(field: str, key):
    try:
        user = db_client.local.users.find_one({field:key})
        return User(**user_sch(user))
    except:
        return {"error":"No se ha encontrado el ususario"}