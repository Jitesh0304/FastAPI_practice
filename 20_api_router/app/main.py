from fastapi import FastAPI, Depends
from .dependencies import get_query_token, get_token_header
from .router import items, users
# from .router import item_router, user_router      ## you can import this from init file
from .internal import admin

"""
The first version is a "relative import":
        from .routers import items, users

The second version is an "absolute import":
        from app.routers import items, users
"""


app = FastAPI(dependencies=[Depends(get_query_token)])


app.include_router(items.router)
app.include_router(users.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "Some error occurred."}},
)

# app.include_router(
#     users.router,
#     prefix="/users",
#     tags=["admin"],
#     dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "Some error occurred."}},
# )


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


"""
With app.include_router() we can add each APIRouter to the main FastAPI application.

It will include all the routes from that router as part of it.

It will actually internally create a path operation for each path operation that was declared in the APIRouter.

So, behind the scenes, it will actually work as if everything was the same single app.

You can also use .include_router() multiple times with the same router using different prefixes.

This could be useful, for example, to expose the same API under different prefixes, e.g. /api/v1 and /api/latest.

This is an advanced usage that you might need.
"""