from fastapi import status,HTTPException,Depends,APIRouter
from .. import models,schema,utils
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List

router=APIRouter(prefix="/users",tags=["Users"])


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schema.ResponseUser)
def create_user(user:schema.CreateUser,db: Session = Depends(get_db)):
    user.password=utils.hash(user.password)
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/",response_model=List[schema.ResponseUser])
def get_all_users(db: Session = Depends(get_db)):
    users=db.query(models.User).all()
    return users



@router.get("/{id}",response_model=schema.ResponseUser)
def get_user(id:int,db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail=f"user with id = {id} doesnot exit")

    return user

# EXTRA
@router.delete("/")
def delete_all_users(db: Session = Depends(get_db)):
    users=db.query(models.User).delete(synchronize_session=False)
    db.commit()
    return 