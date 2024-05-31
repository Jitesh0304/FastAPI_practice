from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum
from functools import reduce

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str
    price: float
    tax: float | None = None
    tags: set[str] = set()


class Match(Enum):
    item = "Item_cls"
    user = "USER"


# @app.post('/items', response_model=Item, tags=['ITEM'])
# @app.post('/items', response_model=Item, tags=[Match.item])
@app.post('/items', response_model=Item, tags=[Match.item, Match.user, 'ITEM'],
          response_description="The created item",)
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name           (bold font)
    - *description*: a long description         (style font)
    - _price_: required                         (italic font)
    - __tax__: if the item doesn't have tax, you can omit this          (bold font)
    - tags: a set of unique tag strings for this item               (normal font)
    """
    return item


@app.get('/items', tags=['ITEM'])
async def read_item():
    return {'name': 'ball', 'price': 210}


@app.get('/users/{num}', tags=['User', 'List items'],
         summary="You will get a list of users",
         description="Send the total number of users you want in response",
         )
async def get_user_list(num: int):
    user_data = {'name': 'alpha', 'age': 24}
    final_list = [user_data for _ in range(num)]
    # return [{'name': 'alpha', 'age': 24}]
    return final_list


@app.get("/items/", tags=[Match.item], deprecated=True)
async def get_items():
    return ["Portal gun", "Plumbus"]


@app.get("/users/", tags=[Match.user])
async def read_users():
    return ["Rick", "Morty"]
