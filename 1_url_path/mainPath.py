from fastapi import FastAPI
from enum import Enum
from typing import Optional



app = FastAPI()


@app.get('/', description="First URL")  ## , deprecated=True
async def home():
    return {"msg":"welcome"}



@app.get('/strID/{id}')
## if you are not defining type of the expected id .. then by default this will be consider as str 
async def app_page(id):
    return {"your itemID" : id}



@app.get('/intID/{id}')
## here the id will be an integer value
async def app_page(id : int):
    return {"your itemID" : id}



@app.get('/user/me')
async def myprofile():
    return {'msg':'Your profile details'}
## in the above path also [user] is the first path and then [me] is the second path ..
## in the below path [user] is the first path and [name] is the user input field to complete the path ...
## as you can see [user] is in both path and last path is changing ... so remember this
## whenever you have path same path for 2 or more operations .. then use the fixed path first and veriable path at the bottom
@app.get('/user/{name}')
async def userprofile(name:str):
    return {'msg': f'User name is {name}'}


## these are build-in
"""
1    str
2    int
3    float
4    bool
5    bytes

or else ... import it from typing module

from typing import List, Tuple, Set, Dict, Union, Optional

"""



## You can use Enum class for matching the expected field types ..
class FoodTypes(str, Enum):
    vegetables = "veg"
    meat = "meat"
    fruits = "fruit"


@app.get('/food/{name}')
async def get_food(name: FoodTypes):
        ## you can match by checking the value
    print(FoodTypes.meat)
    if name.value == "veg":
        return {'msg':'You have chosen vegetarian food'}
    
        ## you can check by matching the enum type
    elif name == FoodTypes.fruits:
        return {'msg':'You have chosen fruits'}
    
    elif name == FoodTypes.meat:
        return {'msg': 'You have chosen meat for lunch/dinner ..'}

    return {'msg': f'{name} : The verity is not there ..'}




list_of_items = [{'name':'alpha'}, {'name':'beta'}, {'name':'theta'}, {'name':'gamma'}, {'name':'pie'}, {'name':'sin'},
                 {'name':'tan'}, {'name':'cos'}]
"""
query parameters
skip and limit are 2 parameter it take .. skip for what index and limit till waht index you can mension
"""
@app.get('/items')
async def list_item(skip: int = 0, limit: int = 10):
    return list_of_items[skip: skip + limit]




"""
query parameter in a URL ...  ( ? ==> query params)
"""
### multiple query parameter
# @app.get('/get_one_item')
# async def get_item(item_id: int , q: Optional[str] = None):
#     if q:
#         return {"item_id":item_id, "your_query":q}
#     return {"item_id":item_id, "your_query":"You have not send any query params .."}


## one query parameter
@app.get('/get_one_item/{item_id}')
# async def get_item(item_id: int , q: Optional[str] = None):
async def get_item(item_id: int , q: str | None = None):
    if q:
        return {"item_id":item_id, "your_query":q}
    return {"item_id":item_id, "your_query":"You have not send any query params .."}





@app.get('/get_data/{id}')
async def get_new_data(id = int, q : str | None = None, sort: bool = False):
    new_data = {'name': 'alpha', 'id': id}
    if q:
        new_data.update({'query': q})
    if not sort:
        new_data.update({'age':20})
    return new_data
