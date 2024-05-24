from fastapi import FastAPI, Query, Path, Body
from pydantic import BaseModel, Field



app = FastAPI()


class Product(BaseModel):
    name : str
    description : str | None = None
    price : float
    tax : float


class User(BaseModel):
    first_name : str
    last_name : str
    mobile : int | None = None
    city : str

"""
id is the required str .
(...) in Path is the empty default value but it is required
as per python standard coding you can't define a required parameter after a none required or default parameter

You can pass mutiple base model class in the function

using Body() you can pass extra field in the body json 
"""
@app.put('/product/{id}')
async def update_product( *, 
                   id: int = Path(..., title=" This is the item id. ", ge=5, le=20), 
                   q: str | None = Query(None),
                   prod: Product | None = None,
                   user : User,
                   brand : str = Body(...)):
    item_data = {'product_name':'laptop', 'price': 40909, 'id': id, 'brand': brand}
    if q:
        item_data.update({'q': q})
    if prod:
        item_data.update(**prod.dict())
    if user:
        item_data.update(**user.dict())
    return item_data





"""
embed = True  ..... it means the json should contaion user as the key and values will be another json having all fields of User class
"""
@app.put('/user/{id}')
async def update_user( *, 
                   id: int = Path(..., title=" This is the item id. ", ge=5, le=20), 
                   q: str | None = Query(None),
                   user : User = Body(..., embed = True)):
    item_data = {'product_name':'laptop', 'price': 40909, 'id': id}
    if q:
        item_data.update({'q': q})
    if user:
        item_data.update(**user.dict())
    return item_data





"""
using Field you can define what type of validation you want 
"""

class Employee(BaseModel):
    first_name : str
    last_name : str = Field(..., title="fill last name field ", max_length=10)
    mobile : int | None = None
    city : str


@app.post('/saveEmp/{id}')
async def save_emp( *, 
                   id: int = Path(..., title=" This is the item id. ", ge=5, le=50), 
                   q: str | None = Query(None),
                   emp : Employee = Body(..., embed = True)):
    item_data = {'product_name':'laptop', 'price': 40909, 'id': id}
    if q:
        item_data.update({'q': q})
    if emp:
        item_data.update(**emp.dict())
    return item_data