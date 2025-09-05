from fastapi import FastAPI
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel

items = []

class Item(BaseModel):
    name: str
    description: str = None
    price:float = None
    quantity: int = None

app = FastAPI(
    title="My FastAPI API",
    version = "1.0.0",
    description = "API de Exemplo com FastAPI"
)

users = {
    "user1": "password1",
    "user2": "password2"
}

security = HTTPBasic()

def verify_password(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password
    if username in users and users[username] == password:
        return username
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais invalidas",
        headers={"www-Authenticate": "Basic"}
    )

@app.get('/')
async def home():
    return "Hello FastAPI!"

@app.get("/hello")
async def hellow(username: str = Depends(verify_password)):
    return {"message": f"Hello, {username}!"}

@app.get('/items')
async def get_itemns():
    return items

@app.post('/items', status_code=201)
async def create_item(item:Item):
    items.append(item.dict())
    return item

@app.put('/items/{item_id}')
async def update_item(item_id: int, item: Item):
    if 0 <= item_id < len(items):
        items[item_id].update(item.dict())
        return items[item_id]
    raise HTTPException(status_code=404, detail="Item não encontrado")

@app.delete('/items/{item_id}')
async def delete_item(item_id: int):
    if 0 <= item_id < len(items):
        removed_item = items.pop(item_id)
        return removed_item
    raise HTTPException(status_code=404, detail='Item não encontrado')