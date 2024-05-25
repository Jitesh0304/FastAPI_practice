from fastapi import FastAPI, Body
from pydantic import BaseModel, Field, EmailStr
from typing import Literal




app = FastAPI()


class Items(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []



"""
UserModel has some specific fields .. That is a basemodel class
"""
class UserModel(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None



"""
UserIn class is created by inheriting the UserModel class .. and here one more field is added ( i.e. = password )
So for this model class you need all 3 fields of UserModel and password from UserIn class .. total 4 fields required to send data
"""
class UserIn(UserModel):
    password: str


"""
UserOut class is created by inheriting the UserModel class ... So the required fields are same as UserModel ( 3 fields )
"""
class UserOut(UserModel):
    pass



"""
response_model => help you to show the user exact same schema you have mentioned
"""
# @app.post('/item', response_model= Items)
@app.post('/item', response_model= list[Items])         ## you can show a list of Items in response
async def store_item(item_data: Items | None = None):
    return item_data



"""
Here you can see UserOut is the response_model 
UserIn is the required data model class
"""
@app.post("/user", response_model=UserOut)
async def create_user(user: UserIn) -> UserOut:
    return user






item_data = {
    "mobile" : {"name": "apple", "description": "it is a good mobile", "price": 3254.2, "tax": 12.4, "tags": ['15 pro', '14 max']},
    "laptop" : {"name": "lenovo", "description": "office laptop", "price": 24999, "tags": ['i5', 'i7']},
    "watch" : {"name": "noise", "description": "kind of good", "price": 354.2, "tax": 10.7, "tags": ['one', 'two']},
}


"""
Literal take a list of values .. and it gives you a drop down of those values
"""
@app.get('/retrieve_item/{item_name}', response_model=Items)
async def retrieve_item(item_name: Literal["mobile", "laptop", "watch"]):
    return item_data[item_name]


"""
response_model_exclude_unset => suppose some fields data are not there .. and you wnt to retrieve only those field which
field has any data ... In this case you can use this field to retrieve not null data
"""
@app.get('/get_item/{item_name}', response_model=Items, response_model_exclude_unset=True)
async def get_one_item(item_name: Literal["mobile", "laptop", "watch"]):
    return item_data[item_name]




"""
response_model_include => suppose you want to retrieve only specific fields data .. then you can mension all those fields here
"""
@app.get('/get_item_include/{item_name}', response_model=Items, response_model_include={'name', 'price'})
async def get_one_item_include(item_name: Literal["mobile", "laptop", "watch"]):
    return item_data[item_name]




"""
response_model_exclude => suppose you don't want to retrieve some fields data .. then you can mension all those field here
"""
@app.get('/get_item_exclude/{item_name}', response_model=Items, response_model_exclude={'tags', 'price', 'tax'})
async def get_one_item_exclude(item_name: Literal["mobile", "laptop", "watch"]):
    return item_data[item_name]


