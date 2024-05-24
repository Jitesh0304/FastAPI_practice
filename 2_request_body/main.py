from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List


app = FastAPI()


class Product(BaseModel):
    id: int
    name: str
    # price: Optional[float] = None
    price: float | None = None
    # tax: List[float] = []
    tax: list[float]



@app.post('/addData')
async def store_data(prod : Product):
    product_data = prod.dict()
    if prod.price:
        product_data.update({"new_price": prod.price + 10})
        product_data.pop('price', 'Not available')
    return product_data                     ## return dictionary data
    # return prod                                  ## return basemodel class
    # return {"msg":"ok", **prod.dict()}       ## return any success message and the basemodel class dictionary data
    # return {"msg":"ok", **product_data}           ## return any success message and dictionary data




        ## query parameter in URL 
@app.put('/updateData/{id}')
async def update_data(id: int, prod : Product, q : str | None = None):
    product_data = prod.dict()
    product_data.update({'req_id': id})
    if q:
        product_data.update({'q': q})
    return product_data


