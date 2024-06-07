from sqlalchemy.orm import Session
from . import models, schemas


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password+"_fakehashed"
    db_user = models.User(email= user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    # db_item = models.Item(title= item.title, description= item.description, owner_id=user_id)
    # db_item = models.Item(**item.dict(), owner_id=user_id)
    db_item = models.Item(**item.model_dump(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


"""
In Pydantic v1 the method was called .dict(), it was deprecated (but still supported) in Pydantic v2, 
and renamed to .model_dump().

The examples here use .dict() for compatibility with Pydantic v1, but you should use .model_dump() instead if you can 
use Pydantic v2.
"""