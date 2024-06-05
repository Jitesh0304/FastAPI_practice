from fastapi import FastAPI, Header, Depends, HTTPException


app = FastAPI()


async def verify_token(x_token: str = Header(...)):
    if x_token != "this-is-your-secrete-token":
        raise HTTPException(status_code= 400, detail="X-header token mismatch")


async def verify_key(x_key: str = Header(...)):
    if x_key != "this-is-your-secrete-key":
        raise HTTPException(status_code= 400, detail="X-header key mismatch")


"""
Dependencies in request body
"""


# @app.get('/item')
# async def get_item(y_token: str = Depends(verify_token)):
#     return {'mobile': 'apple'}


# @app.get('/item-list')
# async def get_items_list(y_key: str = Depends(verify_key)):
#     return [{'mobile': 'apple', 'laptop':'dell'}]


# @app.get('/item-collections')
# async def send_two_header(y_key: str = Depends(verify_key), y_token: str = Depends(verify_token)):
#     return [{'mobile': 'apple'}, {'laptop':'dell'}, {'car':'TATA'}]






"""
Dependencies in path operation decorators
"""


# @app.get('/item', dependencies=[Depends(verify_key)])
# async def get_item():
#     return {'mobile': 'apple'}


# @app.get('/item-list', dependencies=[Depends(verify_token)])
# async def get_items_list():
#     return [{'mobile': 'apple', 'laptop':'dell'}]


# @app.get('/item-collections', dependencies=[Depends(verify_key), Depends(verify_token)])
# async def send_two_header():
#     return [{'mobile': 'apple'}, {'laptop':'dell'}, {'car':'TATA'}]




"""
Global dependencies ..
Declare the dependencies in the FastAPI config . now both headers are required in get request . because 

"""
app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])


@app.get('/item')
async def get_item():
    return {'mobile': 'apple'}


@app.get('/item-list')
async def get_items_list():
    return [{'mobile': 'apple', 'laptop':'dell'}]


@app.get('/item-collections')
async def send_two_header():
    return [{'mobile': 'apple'}, {'laptop':'dell'}, {'car':'TATA'}]





