from fastapi import FastAPI, Depends, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
from fastapi.exceptions import HTTPException



app = FastAPI()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl= 'token')


# @app.get('/items/')
# async def read_items(token: str = Depends(oauth2_scheme)):
#     return {'token': token}


# create a fake db
fake_users_db = {
    "alpha": {
        "username": "alpha",
        "full_name": "alpha xyz",
        "email": "alpha@gmail.com",
        "hashed_password": "secret_alpha",
        "disabled": False,
    },
    "beta": {
        "username": "beta",
        "full_name": "beta abc",
        "email": "beta@gmail.com",
        "hashed_password": "secret_beta",
        "disabled": True,
    },
}


# create a user base model
class User(BaseModel):
    username: str
    email: EmailStr | None = None
    full_name: str | None = None
    disabled: bool | None = None


# inherite the base user class and create a class to store user data in DB
class UserInDB(User):
    hashed_password: str


# create fake password and return the password
def fake_hash_password(password: str):
    return f"secret_"+password


# check the user is present in db or not .. if yes then create a user object using the userin pydentic class and
# return the pydentic class
def get_user(db, username: str):
    if username in db:
        user_dictionary = db[username]
        return UserInDB(**user_dictionary)


# create a fuction to return the user by validating token
def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    return user
    

# get the current user data ... and it depends on the scheme => oauth2_scheme
# oauth2_scheme => it will ask you to authenticate youself first
async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "Invalid authentication credentials",
            headers= {'WWW-Authenticate': 'Bearer'}
        )
    return user


# check the current user is a active user or not 
async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, 
                            detail= "Inactive user")
    return current_user


# this is a rout to get token as response
# OAuth2PasswordRequestForm => this will give you a form in docs page to fill the data
@app.post('/token')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # check the user name is present in the fake db or not
    user_dict = fake_users_db.get(form_data.username)

    if not user_dict:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail='Incorrect username or password')
    
    # convert the user data to a pydantica class object
    user = UserInDB(**user_dict)
    # convert the user password to hashed password before validating
    hashed_password = fake_hash_password(form_data.password)

    # match both passwords 
    if hashed_password != user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    # return the token in response
    return {"access_token": user.username, "token_type": "bearer"}


# once you are authenticated .. then you can use this rout to get the data
@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


