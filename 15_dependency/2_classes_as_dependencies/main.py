from fastapi import FastAPI, Depends
from typing import Annotated, Any


app = FastAPI()


fake_items_db = [{'item_name': 'mobile'}, {'item_name': 'bike'}, {'item_name': 'pizza'}]


class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


@app.get('/item')
# using annotated
# async def get_item(common: Annotated[CommonQueryParams, Depends(CommonQueryParams)]):
# you can use Any also
# async def read_items(common: Annotated[Any, Depends(CommonQueryParams)])
async def get_item(common: CommonQueryParams = Depends(CommonQueryParams)):
    response_data = {}
    if common.q:
        response_data.update({'q': common.q})
    items = fake_items_db[common.skip: common.skip + common.limit]
    response_data.update({'items_data': items})
    return response_data


@app.get('/items/')
# no need to mention type annotation
# async def read_items(common=Depends(CommonQueryParams)):
# you can mention like below example
# async def read_items(common: CommonQueryParams = Depends()):      # Annotated[CommonQueryParams, Depends()]
async def read_items(common: CommonQueryParams = Depends(CommonQueryParams)):
    response_data = {}
    if common.q:
        response_data.update({'q': common.q})
    items = fake_items_db[common.skip: common.skip + common.limit]
    response_data.update({'items_data': items})
    return response_data


class CommonQueryWithID:
    def __init__(self, item_id: int, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit
        self.item_id = item_id


@app.get('/item/{item_id}')
async def read_any_item(common=Depends(CommonQueryWithID)):
    if common.item_id < len(fake_items_db):
        data = fake_items_db[common.item_id]
    else:
        data = {'error': 'data not available'}
    return data


class CommonQueryWithoutID:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


@app.get('/one_item/{item_id}')
async def read_one_item(item_id: int, common=Depends(CommonQueryWithoutID)):
    if item_id < len(fake_items_db):
        data = fake_items_db[item_id]
    else:
        data = {'error': 'data not available'}
    return data
