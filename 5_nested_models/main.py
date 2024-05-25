from fastapi import FastAPI, Query, Body
from pydantic import BaseModel, Field, HttpUrl


app = FastAPI()


class Image(BaseModel):
    url : HttpUrl
    size : float



class Items(BaseModel):
    name : str
    brand : str
    pricce : float = Field(...)
    taxs : list[int] = []
    # taxs : set[int] = set()             ## set you can use for taking input of only unique values
    # image : Image | None = None               ## nested model but fill data one time
    image : list[Image] = []            ## list of the model data are acceptable... in a list separate jsons are accepted



class Customer(BaseModel):
    username : str
    address : str
    # item : Items
    item : list[Items] = []     ## you can use nested basemodel field 




"""
You can use a list in the request body ... and you can also use basemodel inside that list
"""
@app.put('/img/{pk}')
async def put(pk : int, image : list[Image] = Body(..., embed=True)):
    return image


"""
Items model is a nested model ... which expect Image model data in image field 
"""
@app.post('/store/{itemID}')
async def save_item(itemID: int, item: Items = Body(..., embed=True), qr: str | None = Query(...)):
    item_data = {'product_name':'laptop', 'price': 40909, 'item_id': itemID, **item.dict()}

    if qr:
        item_data.update({'qr': qr})
    return item_data




"""
You can send dictionary data to server
"""
@app.post('/blog')
async def post_blog(blog: dict[str, int]):
    return blog



"""
Customer is a nested model class
"""
@app.post('/customer')
# async def store_user(user: Customer):
async def store_user(user: Customer = Body(..., embed=True)):
    return user


"""
{
  "user": {
    "username": "alpha",
    "address": "blr",
    "item": [
             {
               "name": "mobile",
               "brand": "samsumg",
               "pricce": 2142,
               "taxs": [12,431,43],
               "image": [
                          {
                            "url": "https://example.com/",
                            "size": 12
                          },
                          {
                            "url": "https://samsung.com/",
                            "size": 98
                          }
                       ]
             },
             {
               "name": "laptop",
               "brand": "MSI",
               "pricce": 35754,
               "taxs": [12,431,43],
               "image": [
                          {
                            "url": "https://msi.com/",
                            "size": 12
                          },
                          {
                            "url": "https://nvidia.com/",
                            "size": 98
                          }
                       ]
             }
        ]
  
    }
}
"""