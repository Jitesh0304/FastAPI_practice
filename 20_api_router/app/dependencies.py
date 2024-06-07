from fastapi import Header, HTTPException


async def get_token_header(x_token: str = Header()):
    if x_token != "fake-super-secret-token":
        raise HTTPException(
            status_code= 403,
            detail="X-Token header invalid"
        )


async def get_query_token(token: str):
    if token != 'random-token':
        raise HTTPException(
            status_code=403,
            detail="Token is not correct"
        )
