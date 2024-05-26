from fastapi import FastAPI, File, UploadFile, Form, Body
from typing import Annotated  # Union
from fastapi.responses import HTMLResponse

app = FastAPI()

"""
you can write bytes in required type data

The files will be uploaded as "form data".

If you declare the type of your path operation function parameter as bytes, 
FastAPI will read the file for you and you will receive the contents as bytes.
"""


@app.post('/files/')
# async def create_file(file: bytes = File(...)):
# async def create_file(file: Annotated[bytes | None, File()] = None):
async def create_file(file: bytes | None = File(None, description="A file read as bytes")):
    if not file:
        return {'msg': 'You are not sending any file '}
    return {'file_size': len(file)}


"""
Using UploadFile has several advantages over bytes:

You don't have to use File() in the default value of the parameter.
It uses a "spooled" file:
A file stored in memory up to a maximum size limit, and after passing this limit it will be stored in disk.
This means that it will work well for large files like images, videos, large binaries, etc. without consuming all 
the memory.

You can also use File() with UploadFile, for example, to set additional metadata:
"""


@app.post('/upload-file/')
# async def upload_file(file: UploadFile):
# async def upload_file(file: UploadFile | None = None):
async def upload_file(file: Annotated[UploadFile, File(description="A file read as UploadFile")]):
    if not file:
        return {"message": "No upload file sent"}
    # data = await file.seek(0)
    # file_data = await file.read()
    return {'file_name': file.filename, 'size': file.size, 'content': file.content_type}  # 'data': str(file_data)


@app.post("/multiple-files/")
# async def create_files(files: Annotated[list[bytes], File()]):
async def create_files(files: list[bytes] = File()):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/multiple-uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}


@app.get("/")
async def main():
    content = """
                <body>
                <form action="/multiple-files/" enctype="multipart/form-data" method="post">
                <input name="files" type="file" multiple>
                <input type="submit">
                </form>
                <form action="/multiple-uploadfiles/" enctype="multipart/form-data" method="post">
                <input name="files" type="file" multiple>
                <input type="submit">
                </form>
                </body>
              """
    return HTMLResponse(content=content)


"""
The files and form fields will be uploaded as form data and you will receive the files and form fields.
And you can declare some of the files as bytes and some as UploadFile.

You can declare multiple File and Form parameters in a path operation, but you can't also declare Body fields 
that you expect to receive as JSON, as the request will have the body encoded using multipart/form-data instead
of application/json.

This is not a limitation of FastAPI, it's part of the HTTP protocol.
"""


@app.post("/multiple-type-data/")
async def create_file(file_a: bytes = File(...), file_b: UploadFile = File(...), token: str = Form(...),
                      summary: str = Body(...)):    # Body() json data will be converted into form-data
    return {
        "file_size": len(file_a),
        "token": token,
        "file_b_content_type": file_b.content_type,
        "summary_details": summary
    }
