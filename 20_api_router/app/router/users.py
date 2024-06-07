from fastapi import APIRouter


router = APIRouter()


"""
You can think of APIRouter as a "mini FastAPI" class.

All the same options are supported.

All the same parameters, responses, dependencies, tags, etc.
"""


@router.get('/users/', tags=['users'])
async def read_users():
    return [{'name':'alpha'},{'name':'beta'}]


@router.get('/users/me', tags=['users'])
async def read_user_me():
    return {'name': 'alpha'}


@router.get('/users/{user_name}', tags=['users'])
async def read_one_user(user_name: str):
    return {'name': user_name}

