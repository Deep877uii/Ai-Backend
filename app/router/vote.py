from fastapi import APIRouter , status , HTTPException, Depends ,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, model, utils , outh2 ,database 
from fastapi.security import OAuth2PasswordRequestForm


router =APIRouter(
    prefix="/vote", #yaha prefix dena hai taki hume sare endpoints ke aage /users lag jaye     
    tags=["Vote"]
)


@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db : Session= Depends(database.get_db),current_user : int = Depends(outh2.get_current_user)):

    post = db.query(model.Post).filter(model.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {vote.post.id} not found")
    
    vote_query = db.query(model.vote).filter(
        model.vote.post_id == vote.post_id,model.vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if (vote.direction ==1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail = 
                                f"user{current_user.id}has already voted{vote.post_id}")
        new_vote = model.vote(post_id = vote.post_id , user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "u make a vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = "Vote not exit")

        vote_query.delete(synchronize_session=False)
        db.commit()

        return{"message": "deleted vote"}