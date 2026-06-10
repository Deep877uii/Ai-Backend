from ..import model, schemas, utils
from fastapi import APIRouter , status , HTTPException, Depends ,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router =APIRouter(
    prefix="/users", #yaha prefix dena hai taki hume sare endpoints ke aage /users lag jaye     
    tags=["Users"]
)

@router.post("/",status_code = status.HTTP_201_CREATED,response_model=schemas.response_user)#yaha response model dena hai kyuki hume ek user return karna hai jo create hua hai
async def create_user(user : schemas.create_user , db: Session = Depends(get_db)):
    
    # hashed_password = pwd_context.hash(user.password)
    hashed_password= utils.hash(user.password)
    user.password = hashed_password
    new_user = model.user(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.response_user, status_code=status.HTTP_200_OK) #yaha response model dena hai kyuki hume ek user return karna hai jo id ke basis pe mil raha hai
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(model.user).filter(model.user.id == id).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id : {id} was not found")
    return user
