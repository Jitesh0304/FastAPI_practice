from fastapi import FastAPI, HTTPException, Request, status
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)


app = FastAPI()


items = {"name": "Alpha", "age": 22}


@app.get('/get-item/{item_id}')
async def get_one_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail=f"{item_id} is not a key of the data ..",
                            headers={"X-Error": "Some error has occurred in the code"})
    return {'item': items[item_id]}


"""
Create a custom exception class which will inherited from python Exception class.
You can add any custom validation
"""


class CustomException(Exception):
    def __init__(self, name: str):
        self.name = name


"""
you can add that custom exception class in your app .
create a function which will take input of request and exception class.
And return a JSON response 
"""


# You could add a custom exception handler with @app.exception_handler()
@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        # content=f"Oops .. {exc.name} .. somthing went wrong .",
        content={"message" : f"Oops .. {exc.name} .. somthing went wrong."},
        status_code=400
    )


"""
create a root
add the custom exception in the root_function 
"""


@app.get("/get-data/{name}")
async def get_one_data(name: str):
    if name == "xyz":
        raise CustomException(name=name)
    return {"data_res": "ok"}


"""
 ------   Override the default exception handlers   -----------
FastAPI has some default exception handlers.
These handlers are in charge of returning the default JSON responses when you raise an HTTPException and when 
the request has invalid data.
You can override these exception handlers with your own.
"""


"""
For example, you could want to return a plain text response instead of JSON for these errors:
"""


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


"""
When a request contains invalid data, FastAPI internally raises a RequestValidationError.
And it also includes a default exception handler for it.

To override it, import the RequestValidationError and use it with @app.exception_handler(RequestValidationError)
to decorate the exception handler.

The exception handler will receive a Request and the exception.
"""


# to see the error you can send unacceptable data in request URL query or any other things
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}


# what ever the error you are getting as a response, in that error only you can add other information also
# the detail is the default error what it comes normally
# but body is the new key in that JSON error where you will get some specific details of the error
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "your_sent_data": exc.body}),
        # content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


class Item(BaseModel):
    title: str
    size: int


@app.post("/items/")
async def create_item(item: Item):
    return item


"""
FastAPI's HTTPException error class inherits from Starlette's HTTPException error class.

The only difference is that FastAPI's HTTPException accepts any JSON-able data for the detail field,
while Starlette's HTTPException only accepts strings for it.


"""


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"OMG! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)


@app.get("/getdata/{item_id}")
async def read_data(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}