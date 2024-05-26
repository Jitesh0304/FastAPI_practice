from fastapi import FastAPI, status
from pydantic import BaseModel, Field, EmailStr
from typing import Union, Literal

app = FastAPI()


class BaseUserModel(BaseModel):
    email: EmailStr
    username: str
    fullname: str | None = None


class UserIn(BaseUserModel):
    password: str


class UserOut(BaseUserModel):
    pass


class UserInDB(BaseUserModel):
    hashed_password: str


# create hashed password in this function
def fake_password_hasher(raw_pass: str):
    return "secrete"+raw_pass


# save new user in this function
def fake_save_user(user: UserIn):
    hashed_pass = fake_password_hasher(user.password)
    # user_save_in_db = UserInDB(**user.dict(), hashed_password=hashed_pass)
    # model_dump() = also convert the pydantic class to a dictionary data
    user_save_in_db = UserInDB(**user.model_dump(), hashed_password=hashed_pass)
    print("User data saved ...")
    return user_save_in_db


@app.post('/createUser', response_model=UserOut, status_code=201)
async def create_user_account(user: UserIn):
    new_user = fake_save_user(user)
    return new_user


class Items(BaseModel):
    description: str
    type: str


# in this class you can see . after inheriting the parent class I am updating the type value to a new value
class CarItem(Items):
    type: str = "Car"


# in this class you can see . after inheriting the parent class I am updating type to a new value and adding
# size new field size
class PlaneItem(Items):
    type: str = "Plane"
    size: int


# define a dictionary
items_data = {
    "item_1": {
        "description": "I have a Fortuner",
        "type": "Car"
    },
    "item_2": {
        "description": "I like Airbus planes ..",
        "type": "Plane",
        "size": 400,
    }
}


# Literal help to take input from the user on the specific fields whatever you have defined inside Literal
@app.get('/get_item/{item_id}', response_model=Union[PlaneItem, CarItem])
async def get_one_item(item_id: Literal['item_1', 'item_2']) -> PlaneItem | CarItem:
    return items_data[item_id]


class ListOfItems(BaseModel):
    name: str
    type: str
    description: str | None = Field(None)


list_data = [
    {
        "name": "Fortuner",
        # "description": "I have a Fortuner",
        "type": "SUV"
    },
    {
        "description": "It is a TATA product ",
        "type": "Small SUV",
        "name": "Punch",
    }
]


# you can send list of items in response
@app.get('/get_list_items', response_model=list[ListOfItems], status_code=status.HTTP_200_OK)
async def get_all_items():
    return list_data


# you can define what response you want to send to user . a dictionary data which has string value as key and
# float value as value of the key
@app.get("/keyword-weights/", response_model=dict[str, float])
async def read_keyword_weights():
    return {"foo": 2.3, "bar": 3.4}
