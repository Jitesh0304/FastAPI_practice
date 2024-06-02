from fastapi import FastAPI, Depends, Body, Cookie
from typing import Annotated

"""
You can create dependencies that have sub-dependencies.
They can be as deep as you need them to be.
"""


app = FastAPI()


def query_extractor(q: str | None = None):
    return q


def query_or_body_extractor(q: str = Depends(query_extractor), extra_query: str | None = Body(None)):
    if q:
        return q
    return extra_query


@app.post('/items/')
async def read_query(query: str = Depends(query_or_body_extractor)):
    return {'final_data': query}


def query_or_cookie_extractor(
    q: Annotated[str, Depends(query_extractor)],
    last_query: Annotated[str | None, Cookie()] = None,
):
    if not q:
        return last_query
    return q


@app.get("/items/")
async def read_query(
    query_or_default: Annotated[str, Depends(query_or_cookie_extractor)],
):
    return {"q_or_cookie": query_or_default}

