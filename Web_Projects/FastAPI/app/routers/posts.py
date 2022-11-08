from fastapi import Response,status,HTTPException,Depends,APIRouter
from .. import models,schema,oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional

router=APIRouter(prefix="/posts",tags=["Posts"])  # tags is helpful for documentation for grouping


@router.get("/",response_model=List[schema.ResponsePost])
def get_all_post(db: Session = Depends(get_db),skip:int=0,search:Optional[str]="",limit:int =None):
    if limit:
        return db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    else:
        return db.query(models.Post).filter(models.Post.title.contains(search)).offset(skip).all()


@router.get("/{id}",response_model=List[schema.ResponsePost])
def get_individual_post(id:int,db: Session = Depends(get_db),
    current_user:schema.User=Depends(oauth2.get_current_user)):
    if id==0:
        return db.query(models.Post).filter(models.Post.user_id==current_user.id).all()
    if id==-1:
        return get_all_post(db=db)
    post=db.query(models.Post).filter(models.Post.id==id).all()
    if not len(post):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail=f"post with id = {id} doesnot exit")
    return post


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schema.ResponsePost)
def create_posts(post:schema.CreatePost,db: Session = Depends(get_db),current_user:schema.User=Depends(oauth2.get_current_user)):
    new_post=models.Post(user_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


"""
@router.get("/{id}",response_model=schema.ResponsePost)
def get_post(id:int,db: Session = Depends(get_db)):
    post=db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail=f"post with id = {id} doesnot exit")
    return post

"""
    
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db),current_user:schema.User=Depends(oauth2.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    if post_query.first()==None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail=f"post with id = {id} doesnot exit")
    # when http 204 is used no data can be sent 
    if post_query.first().user_id !=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                detail=f"not authorized to perform this action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schema.ResponsePost)
def update_post_put(id:int,changed_post:schema.CreatePost,db: Session = Depends(get_db),current_user:schema.User=Depends(oauth2.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    if not post_query.first():
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail=f"post with id = {id} doesnot exit")
            
    if post_query.first().user_id !=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                detail=f"not authorized to perform this action")

    post_query.update(changed_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()

    
