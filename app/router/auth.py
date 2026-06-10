from fastapi import APIRouter , status , HTTPException, Depends ,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, model, utils , outh2
from fastapi.security import OAuth2PasswordRequestForm

router =APIRouter(tags=["Authentication"])

@router.post("/login",response_model=schemas.Token) #yaha response model dena hai kyuki hume token return karna hai
# async def login(user_credentials: schemas.user_login, db: Session = Depends(get_db)):
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # user = db.query(model.user).filter(model.user.email == user_credentials.email).first()
    user = db.query(model.user).filter(model.user.email == user_credentials.username).first()#yaha pe hum username use kar rahe hai kyuki OAuth2PasswordRequestForm me username field hota hai email ke badle
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    if not utils.verify(user_credentials.password, user.password):#yaha pe hum user ke plain password ko database me stored hashed password ke sath compare kar rahe hai
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    #create a token and return it
    access_token = outh2.create_access_token(data={"user_id": user.id})
    return schemas.Token(access_token=access_token, token_type="bearer")