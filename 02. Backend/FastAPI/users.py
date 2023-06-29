from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

# Inicia el server: uvicorn users:app --reload

# Entidad user

class User(BaseModel):
    id: int
    name: str
    surname : str
    url: str
    age: int 

users_list = [User(id = 1,name = "Brais", surname = "Moure", url = "http://moure.dev", age = 35),
            User(id = 2, name = "César", surname ="Garcia", url =  "http://cesar.dev", age = 23),
            User(id = 3, name = "Daniel", surname ="Ramirez", url = "http://daniel.dev", age = 32)]

@app.get("/users")
async def users():
    return users_list

# Path
@app.get("/user/{id}")
async def user(id:int):
    return search_user(id)

@app.post("/user/")
async def user(user: User):
    if type(search_user(user.id)) == User:
        return {"error":"El ususario ya existe"}
    else: 
        users_list.append(user)
        return user

@app.put("/user/")
async def user(user: User):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        return {"error": "No se ha actualizado el usuario"}
    else:
        return user

@app.delete("/user/{id}")
async def user(id: int):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
    if not found:
        return {"error": "No se ha eliminado el usuario"}
    else:
        return user

# Query
@app.get("/user/")
async def user(id:int):
    return search_user(id)
    
def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error":"No se ha encontrado el ususario"}
    