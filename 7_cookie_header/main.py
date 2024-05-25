from typing import Annotated

from fastapi import FastAPI, Cookie, Header

app = FastAPI()


@app.get("/items/")
# async def read_items(cookie_id: Annotated[str | None, Cookie()] = None):
async def read_items(cookie_id: str | None = Cookie(None),
                     accept_encoding: str | None = Header(None),
                     sec_fetch_site: str | None = Header(None),
                     accept: str | None = Header(None),
                     x_token: list[str] | None = Header(None),):
    return {"cookie_id": cookie_id, "Accept-Encoding": accept_encoding, 
            "Sec-Fetch-Site": sec_fetch_site, "Accept": accept, "X-token": x_token}
