from fastapi import FastAPI, Depends
from typing import Annotated

app = FastAPI()

"""
"Dependency Injection" means, in programming, that there is a way for your code (in this case, your path operation 
functions) to declare things that it requires to work and use: "dependencies".

And then, that system (in this case FastAPI) will take care of doing whatever is needed to provide your code with 
those needed dependencies ("inject" the dependencies).

sync function also acceptable as a dependencies
dependencies helps in minimizing code repetition

You can use async def or normal def.

And you can declare dependencies with async def inside of normal def path operation functions, or def dependencies
inside of async def path operation functions, etc.
"""
# It is just a function that can take all the same parameters that a path operation function can take


# def hello():
#     return {'hello': 'world'}


# you can add multiple dependencies
# def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100, tst: dict = Depends(hello)):
#     return {'q': q, 'skip': skip, 'limit': limit, **tst}


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {'q': q, 'skip': skip, 'limit': limit}


CommonsDep = Annotated[dict, Depends(common_parameters)]


# @app.get('/item/')
# async def read_item(common: dict = Depends(common_parameters)):
# async def read_item(common: CommonsDep):
#     return common
@app.get('/item/')
async def read_item(common: Annotated[dict, Depends(common_parameters)]):
    return common


@app.get('/users')
# async def read_users(commons: CommonsDep):
async def read_users(commons: dict = Depends(common_parameters)):
    return commons


