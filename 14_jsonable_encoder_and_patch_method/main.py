from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from typing import Literal


app = FastAPI()


# class Item(BaseModel):
#     title: str
#     timestamp: datetime
#     description: str | None = None
#
#
# fake_db = {}
#
#
# @app.put('/items/{id}')
# def update_item(id: str, item: Item):
#     json_data = jsonable_encoder(item)
#     fake_db[id]: json_data
#     return "Success"


class Item(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 10.5
    tags: list[str] = []


items = {
    "mobile": {"name": "S24", "price": 88400.0},
    "bike": {"name": "Shine", "description": "Honda bike", "price": 98030.0, "tax": 11.3},
    "laptop": {"name": "MSI", "description": None, "price": 67040.0, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item)
# async def read_item(item_id: str):
async def read_item(item_id: Literal['mobile', 'bike', 'laptop']):
    return items[item_id]


"""
Update replacing with PUT
PUT is used to receive data that should replace the existing data.
"""


@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    # convert the input data to JSON data
    update_item_encoded = jsonable_encoder(item)
    # replace the new data with the updated data
    items[item_id] = update_item_encoded
    return update_item_encoded


"""
Partial updates with PATCH
You can also use the HTTP PATCH operation to partially update data.
This means that you can send only the data that you want to update, leaving the rest intact.

Using Pydantic's exclude_unset parameter
If you want to receive partial updates, it's very useful to use the parameter exclude_unset in 
Pydantic's model's .model_dump().

Like item.model_dump(exclude_unset=True).

In Pydantic v1 the method was called .dict(), it was deprecated (but still supported) in Pydantic v2,
and renamed to .model_dump().

That would generate a dict with only the data that was set when creating the item model, excluding default values.

Then you can use this to generate a dict with only the data that was set (sent in the request), omitting default values.
"""


@app.patch('/items/{item_id}', response_model=Item)
# async def update_item(item_id: str, item: Item):
async def update_item(item_id: Literal['mobile', 'bike', 'laptop'], item: Item):
    # get the item data from the items dictionary
    store_item_data = items.get(item_id)
    # check the key is valid or not
    if store_item_data is not None:
        store_item_data = store_item_data
    # if the data is not present then convert the input data to json_data using converter
    else:
        store_item_data = jsonable_encoder(item)
    # map the json_input data with the model fields and create a model instance
    store_item_model = Item(**store_item_data)
    # convert the model data to dictionary format . (exclude_unset = True) will neglect the not present fields
    # (exclude_unset=True) helps in partial update
    update_data = item.model_dump(exclude_unset=True)       # pydantic v2
    # update_data = item.dict(exclude_unset=True)           # pydantic v1
    # print(update_data)
    # update the new data with the old data . store_item_model is a instance of the model class . and send the new data
    # in update parameter
    updated_item = store_item_model.model_copy(update=update_data)      # pydantic v2
    # updated_item = store_item_model.copy(update=update_data)          # pydantic v1
    # now store the new updated data in the existing dictionary
    items[item_id] = jsonable_encoder(updated_item)
    # return update item
    return updated_item


"""
Partial updates recap¶
In summary, to apply partial updates you would:

(Optionally) use PATCH instead of PUT.
Retrieve the stored data.
Put that data in a Pydantic model.
Generate a dict without default values from the input model (using exclude_unset).

This way you can update only the values actually set by the user, instead of overriding values already stored 
with default values in your model.

Create a copy of the stored model, updating it's attributes with the received partial updates 
(using the update parameter).

Convert the copied model to something that can be stored in your DB (for example, using the jsonable_encoder).
This is comparable to using the model's .model_dump() method again, but it makes sure (and converts) the values 
to data types that can be converted to JSON, for example, datetime to str.

Save the data to your DB.
Return the updated model.
"""