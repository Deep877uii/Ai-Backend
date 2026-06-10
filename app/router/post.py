from unittest import result

from sqlalchemy import func

from ..import model, schemas
from fastapi import APIRouter , status ,Response, HTTPException, Depends ,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List , Optional
from .. import outh2

router =APIRouter(
    prefix="/posts", #yaha prefix dena hai taki hume sare endpoints ke aage /posts lag jaye
    tags=["Posts"]
)


@router.get("/sqlalchemy")
def test_db(db: Session = Depends(get_db)):
    posts= db.query(model.Post).all()
    return{"data": posts}


@router.get("/",response_model = List[schemas.response_post_vote]) #list yaha hi dena hai kyuki hume list of posts return karna hai
async def get_post(db: Session = Depends(get_db),Limit : int = 10 , Skip : int = 0 ,search : Optional[str] = ""):

    # cursor.execute('SELECT * FROM "Post"')
    # posts = cursor.fetchall()

    #posts= db.query(model.Post).filter(model.Post.title.contains(search)).limit(Limit).offset(Skip).all()

    posts = db.query(
            model.Post,
            func.count(model.vote.post_id).label("votes")
        ).join(model.vote,model.vote.post_id == model.Post.id,isouter=True).filter(model.Post.title.contains(search)).group_by(model.Post.id).limit(Limit).offset(Skip).all()

    return posts



# @app.post("/create_posts")
# async def create_post(payload: dict = Body(...)):
#     print(payload)
#     return {"new_post":f"title: {payload['title']}, content: {payload['content']}"}

@router.post("/" ,status_code = status.HTTP_201_CREATED ,response_model=schemas.response_post) #yaha response model dena hai kyuki hume ek post return karna hai jo create hua hai
async def create_post(post : schemas.create_post , db: Session = Depends(get_db), current_user: int = Depends(outh2.get_current_user)):

    # cursor.execute("""INSERT INTO "Post" ("title","content","publisher","rating") 
    #                 VALUES(%s,%s,%s,%s) RETURNING *""",(post.title,post.content,post.publisher,post.rating))
    # conn.commit()
    # new_post=cursor.fetchone()


    # post_dict =post.dict()
    # post_dict["id"] = randrange(0,1000000)
    # my_posts.append(post_dict)
    #print(post.dict())
    
    new_post = model.Post(owner_id = current_user.id ,**post.dict())
    #new_post = model.Post(title=post.title,content=post.content,publisher=post.publisher,rating=post.rating)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    #return {"data" :new_post}
    return new_post


# @app.get("/posts/{id}")
# async def get_post(id):
#     print(id)
#     return {"data" :my_posts[int(id)]}

# @router.get ("/latest",response_model=schemas.response_post) #yaha response model dena hai kyuki hume ek post return karna hai jo latest hai
# async def get_latest_post():
#     post = post[len(post)-1 ]
#     return post

# @router.get("/{id}",response_model = schemas.response_post)
# async def get_post(id : int , db: Session = Depends(get_db),current_user: int = Depends(outh2.get_current_user)):#yaha pe hum user_id ko get_current_user se le rahe hai taki hume pata chale ki kaun sa user request kar raha hai
#     #cursor.execute("""SELECT * FROM  "Post" WHERE "id"=%s""",(id,))
#     #post = cursor.fetchone()
#     post = db.query(model.Post,func.count(model.vote.post_id).label("votes")).join(
#         model.vote,model.vote.post_id == model.Post.id,isouter=True).group_by(
#             model.Post.id).filter(model.Post.id == id).first()
#     if post ==None:
#         raise HTTPException (status_code = status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} was not found")
#     print(post)
#     return post

@router.get("/{id}", response_model=schemas.response_post)
async def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(outh2.get_current_user)
):
    post = db.query(model.Post).filter(model.Post.id == id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found"
        )

    return post


@router.delete("/{id}", status_code =status.HTTP_204_NO_CONTENT)#yaha status code dena hai kyuki hume kuch return nahi karna hai
async def delete_post(id : int, db: Session = Depends(get_db),current_user: int = Depends(outh2.get_current_user)):
    # cursor.execute("""Delete from "Post" where "id"=%s""",(id,))
    # conn.commit()
    # delete_post = cursor.fetchone()
    delete_post = db.query(model.Post).filter(model.Post.id == id)
    if delete_post.first() == None:
        raise HTTPException (status_code = status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} was not found")
    
    if delete_post.first().owner_id != current_user.id:
        raise HTTPException(detail="Not authorized to perform requested action", status_code=status.HTTP_403_FORBIDDEN)

    delete_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}" ,status_code = status.HTTP_200_OK,response_model=schemas.response_post)
async def update_post(id: int, Post: schemas.create_post, db: Session = Depends(get_db), current_user: int = Depends(outh2.get_current_user)):
    # cursor.execute("""UPDATE "Post" SET "title"=%s,"content"=%s,"publisher"=%s,"rating"=%s WHERE "id"=%s RETURNING *""" , 
    # (Post.title,Post.content,Post.publisher,Post.rating,id))
    # updated_post = cursor.fetchone()
    # conn.commit()
    update_post = db.query(model.Post).filter(model.Post.id == id)
    if update_post.first() == None:
        raise HTTPException (status_code = status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} was not found")
    update_post.update(Post.dict(),synchronize_session=False)

    if update_post.first().owner_id != current_user.id:
        raise HTTPException(detail="Not authorized to perform requested action", status_code=status.HTTP_403_FORBIDDEN)
    db.commit()
    return Response(status_code=status.HTTP_200_OK) 