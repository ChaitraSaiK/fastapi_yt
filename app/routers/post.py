from .. import models,schemas,oauth2
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, FastAPI, Response, status, HTTPException
from typing import List, Optional
from ..database import get_db
from typing import Optional
from sqlalchemy import func


router = APIRouter(
    prefix= "/posts",
    tags= ['Posts']
)

# my_post = [{"title":"title 1","content" : "content 1", "id": 1}, {"title": "title 2","content" : "content 2", "id": 2}]

# def find_post(id):
#     for p in my_post:
#         if p['id'] == id:
#             return p

# def find_delete_post(id):
#     for i, p in enumerate(my_post):
#         if p['id'] == id:
#             return i

# @app.get('/posts')
# def get_posts():
#     cursor.execute(""" SELECT * FROM posts""")
#     posts = cursor.fetchall()
#     return {'data' : posts}



# @app.post('/posts', status_code=status.HTTP_201_CREATED)
# def create_posts(post : Post):
#     cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s,%s,%s) RETURNING * """, (post.title, post.content, post.published))
#     new_post = cursor.fetchone()
#     conn.commit()
#     return {"data" : new_post}

# @app.get("/posts/{id}")
# def get_post(id :int, response: Response):
#     cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (str(id),))
#     post = cursor.fetchone()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'Post with id {id} does not exists')
#     return {"post detail" : post}

# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """,(str(id),))
#     deleted_post = cursor.fetchone()
#     conn.commit()
#     if deleted_post == None:
#         raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail= f'Post with id {id} does not exists')
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# @app.put("/posts/{id}")
# # def update_post(id: int, post : Post):
# #     # cursor.execute("""UPDATE posts SET title = %s, content = %s, published= %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published,(str(id))))
# #     # updated_post = cursor.fetchone()
# #     # conn.commit()
#     if updated_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'Post with id {id} does not exists')
    
#     return {"message" : updated_post}

# @app.get("/sqlalchemy") #(just to see if our code is wrkng)
# def test_post(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"status" : posts}
     

@router.get("/",response_model=List[schemas.PostOut])
# def get_posts(db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):
def get_posts(db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # posts = db.query(models.Post).filter(models.Post.owner_id == user_id.id).all()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id ==  models.Post.id, isouter = True).group_by (models.Post.id).filter(
    models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter = True).group_by (models.Post.id).filter(models.Post.id == id).first()


    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id {id} does not exists")

    # if post.owner_id != user_id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f'Not authorized to  perform the requested operation')
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# def create_posts(post : schemas.PostCreate, db: Session = Depends(get_db)):
def create_posts(post : schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    print(user_id) #just to check what it prints
    new_post = models.Post(owner_id = user_id.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id {id} does not exists")

    if post.owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f'Not authorized to  perform the requested operation')

    post_query.delete(synchronize_session= False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post : schemas.PostCreate,  db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
         raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id {id} does not exists")

    if post.owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f'Not authorized to  perform the requested operation')

    post_query.update(updated_post.dict(), synchronize_session= False)

    db.commit()
    return post_query.first()