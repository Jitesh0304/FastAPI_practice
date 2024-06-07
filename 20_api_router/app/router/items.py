from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_token_header


"""
This code lives in the module app.routers.items, the file app/routers/items.py.
And we need to get the dependency function from the module app.dependencies, the file app/dependencies.py.

So we use a relative import with .. for the dependencies:


Having dependencies in the APIRouter can be used, for example, to require authentication for a whole group of path operations.
Even if the dependencies are not added individually to each one of them.

The prefix, tags, responses, and dependencies parameters are (as in many other cases) just a feature from FastAPI to help you
avoid code duplication.
"""


router = APIRouter(
    prefix='/items',
    tags=['items'],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}}
)


fake_items_db = {
    "car": {
        "name": "BMW"
        }, 
    "food": {
        "name": "Burger"
        }
    }



"""
As the path of each path operation has to start with /

the prefix must not include a final /.

All these path operations will have the list of dependencies evaluated/executed before them.
If you also declare dependencies in a specific path operation, they will be executed too.
The router dependencies are executed first, then the dependencies in the decorator, and then the normal parameter dependencies.


We are not adding the prefix /items nor the tags=["items"] to each path operation because we added them to the APIRouter.

But we can still add more tags that will be applied to a specific path operation, and also some extra responses specific to
that path operation:
"""


@router.get('/')
async def read_items():
    return fake_items_db


@router.get("/{item_id}")
async def read_item_by_id(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(
            status_code=400,
            detail="Item does not exists."
        )
    return fake_items_db[item_id]


@router.put(
    '/{item_id}',
    tags=['update item'],
    responses={403: {"description": "Operation forbidden"}}
)
async def update_item(item_id: str, name: str):
    if item_id != 'car':
        raise HTTPException(
            status_code=400,
            detail="You can modify only car item"
        )
    updated_data = fake_items_db["car"].update({'name': name})
    return {'car': updated_data}

