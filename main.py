from typing import List, Union, Optional
from pydantic import EmailStr

from fastapi import FastAPI, status, HTTPException, Path, Query
import uvicorn

from models import User, Order

users: List[User] = []

app = FastAPI()
db = {}


@app.post("/orders/", response_model=Order)
def create_order(order: Order):
    if order.email in db:
        raise HTTPException(400, "Замовлення з таким Email вже існує.")
    db[order.email] = order
    return order

@app.get("/orders/{email}", response_model=Order)
def get_order(email: EmailStr):
    if email not in db:
        raise HTTPException(404, "Не знайдено.")
    return db[email]


@app.post("/users/", status_code=status.HTTP_201_CREATED, response_model=User)
async def add_user(user: User):
    users.append(user)
    return user


@app.get("/users/", status_code=status.HTTP_202_ACCEPTED, response_model=List[User])
async def get_users():
    return users


@app.get("/users/{full_name}/", status_code=status.HTTP_201_CREATED, response_model=User)
async def get_user(full_name: str = Path(..., example='Вася Пупкін')):
    user = next((user for user in users if user.full_name == full_name), None)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="такого користувача не знайдено")
    return user


@app.delete("/users/", status_code=status.HTTP_204_NO_CONTENT)
async def remove_user(full_name: str = Query(...)):
    user = next((user for user in users if user.full_name == full_name), None)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого користувача не знайдено")
    users.remove(user)
    return None


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)