from fastapi import APIRouter,Depends,status, Response,HTTPException
from typing import List

from ..import schemas,database,models
from sqlalchemy.orm import Session

from . import oauth2

router = APIRouter(
    prefix="/blog",
    tags=['blogs']
)

get_db=database.get_db


@router.get('/',response_model=List[schemas.ShowBlog],)
def all(db: Session=Depends(database.get_db),current_user: schemas.AppUser=Depends(oauth2.get_current_user)):
    blogs =db.query(models.Blog).all()
    return blogs

@router.post('/')
def create(request: schemas.Blog,db: Session=Depends(get_db)):
    new_blog=models.Blog(title=request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return  new_blog

# @router.get('/',response_model=List[schemas.ShowBlog])
# def all(db: Session=Depends(get_db)):
#     blogs =db.query(models.Blog).all()
#     return blogs

@router.get('/{id}', response_model=schemas.ShowBlog)
def show(id,response: Response,db: Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} not found")
        # response.status_code=status.HTTP_404_NOT_FOUND
    return blog

@router.delete('/{id}')
def delete(id,db: Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return "done"   

@router.put('/{id}')
def update(id,request: schemas.Blog, db: Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} not found")
    blog.update(request.dict())
    db.commit()
    return "updated"

