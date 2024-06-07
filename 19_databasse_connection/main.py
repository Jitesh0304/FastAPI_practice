from fastapi import FastAPI, Depends, HTTPException
from . import crud, schemas, models
from sqlalchemy.orm import Session
from .database import SessionLocal, engine


models.Base.metadata.create_all(bind= engine)


app = FastAPI()


"""
Now use the SessionLocal class we created in the sql_app/database.py file to create a dependency.

We need to have an independent database session/connection (SessionLocal) per request, use the same session through 
all the request and then close it after the request is finished.

And then a new session will be created for the next request.

For that, we will create a new dependency with yield, as explained before in the section about Dependencies with yield.

Our dependency will create a new SQLAlchemy SessionLocal that will be used in a single request, and then close it once the 
request is finished.

The parameter db is actually of type SessionLocal, but this class (created with sessionmaker()) is a "proxy" of a 
SQLAlchemy Session, so, the editor doesn't really know what methods are provided.

But by declaring the type as Session, the editor now can know the available methods (.add(), .query(), .commit(), etc) 
and can provide better support (like completion). The type declaration doesn't affect the actual object.

"""


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# But as SQLAlchemy doesn't have compatibility for using await directly . That's why we are using synchronous code
@app.post('/user', response_model= schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400, detail="Email already registered"
        )
    return crud.create_user(db= db, user= user)


@app.get('/users', response_model= list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    all_user = crud.get_users(db= db, skip=skip, limit=limit)
    return all_user


@app.get('/user/{user_id}', response_model=schemas.User)
def read_one_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=400, detail=f"User having {user_id} user ID does not exist."
        )
    return user


@app.post('/user/{user_id}/items', response_model=schemas.Item)
def create_item_for_user(user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get('/items', response_model=list[schemas.Item])
def read_all_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    all_items = crud.get_items(db=db, skip=skip, limit=limit)
    return all_items