from fastapi import FastAPI, Form

app = FastAPI()


"""
The way HTML forms (<form></form>) sends the data to the server normally uses a "special" encoding for that data,
it's different from JSON.

FastAPI will make sure to read that data from the right place instead of JSON.
"""


@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(..., min_length=8, regex="")):
    print(password)
    return {"username": username}
