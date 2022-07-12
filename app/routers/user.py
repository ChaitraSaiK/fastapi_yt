from .. import models,schemas, utils
from sqlalchemy.orm import Session
from fastapi import APIRouter, FastAPI, Depends, Response, status, HTTPException
from typing import List
from ..database import get_db


router = APIRouter(
    prefix= "/users",
    tags= ['Users']
)


# To create user
@router.post("/", status_code=status.HTTP_201_CREATED,response_model= schemas.UserOut)
def create_user(user : schemas.UserCreate, db: Session = Depends(get_db)):
    # hashed_password = pwd_context.hash(user.password)

    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return  new_user


#To retrieve user
@router.get('/{id}',response_model=schemas.UserOut)
def get_user(id :int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"User with id {id} is not found")
    return user


# To retrieve all users
@router.get('/', response_model = List[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users
  