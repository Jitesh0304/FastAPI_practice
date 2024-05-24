from fastapi import FastAPI, Query, Path
from pydantic import BaseModel


app = FastAPI()


class Product(BaseModel):
    id: int
    name: str
    # price: Optional[float] = None
    price: float | None = None
    # tax: List[float] = []
    tax: list[float]


@app.post('/addData')
async def store_data(prod: Product):
    product_data = prod.dict()
    if prod.price:
        product_data.update({"new_price": prod.price + 10})
        product_data.pop('price', 'Not available')
    return product_data  # return dictionary data
    # return prod                                  ## return basemodel class
    # return {"msg":"ok", **prod.dict()}       ## return any success message and the basemodel class dictionary data
    # return {"msg":"ok", **product_data}           ## return any success message and dictionary data


@app.put('/updateData/{id}')
async def update_data(id: int, prod: Product, q: str | None = None):
    product_data = prod.dict()
    product_data.update({'req_id': id})
    if q:
        product_data.update({'q': q})
    return product_data


# Query class
"""
qr ==> it can be a str value or None ... only one value
Query class take multiple parameters ==>
    None = is the default value ... if no value is comming then it will set to None .. you can pass any value in that (alpha , beta)
    max_length, min_length = these are validation of the qr parameter
    regex = here you can put any regular expression value .. if the value match then only you will allow the qr parameter

"""


@app.get('/getData/{id}')
# async def get_data(id: int, qr: str | None = Query(None)):                ## initial qr = None
# async def get_data(id: int, qr: str | None = Query('alpha')):                     ## intial qr = alpha
# async def get_data(id: int, qr: str = Query(..., max_length=8, min_length=2)):            ## ... => means you can put any value
async def get_data(id: int, 
                   qr: str | None = Query(None,
                                          max_length=10, 
                                          min_length=4, 
                                          regex="^anything$", 
                                          description="Get product data",
                                          title="Simple title")):
    product_data = {'name': 'mobile', 'price': 28, 'req_id': id}
    if qr:
        product_data.update({'query': qr})
    return product_data


"""
qr ==> multiple values are acceptable or None
        ...../get_user?qr=alpha&qr=beta&qr=gamma
"""


@app.get('/get_user')
# multiple values are acceptable or None
async def getuser(qr: list[str] = Query(['alpha', 'beta', 'theta'])):
    # async def getuser(qr: list[str] | None = Query(None)):          ##  multiple values are acceptable or None
    user_data = {'name': 'alpha', 'age': 28, 'city': qr}
    return user_data





"""
qr ==>  ...../getname?qr=alpha  ( now this will not work )
        ...../getname?test-query=alpha  ( this will work because the alias name has been set in the qr parameter)
"""
@app.get('/getname')
# multiple values are acceptable or None
async def getName(qr: str | None = Query(None,
                                         max_length=10, 
                                         min_length=4,
                                         alias="test-query"
                                         )):
    # async def getuser(qr: list[str] | None = Query(None)):          ##  multiple values are acceptable or None
    user_data = {'name': 'alpha', 'age': 28, 'city': qr}
    return user_data




"""
In the above methods the query parameter is expose to the user in url ...
But in this the query parameter is invisible to the user

include_in_schema => you want to include in schema or not
"""
@app.get('/hidden_item')
async def hidden_query(qr: str | None = Query(None, include_in_schema=False)):
    product_data = {'name': 'mobile', 'price': 28}
    if qr:
        product_data.update({'query': qr})
    return {"query": "not found", **product_data}




"""
id is the required str .
(...) in Path is the empty default value but it is required
as per python standard coding you can't define a required parameter after a none required or default parameter
"""
@app.get('/item/{id}')
async def get_item(id: int = Path(..., title=" This is the item id. ", gt=5, le=20), q: str | None = Query(None)):
    item_data = {'product_name':'laptop', 'price': 40909, 'id': id}
    if q:
        item_data.update({'q': q})
    return item_data