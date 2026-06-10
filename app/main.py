
from fastapi import FastAPI 
from httpx import post
from . import model 
from .database import engine
model.Base.metadata.create_all(bind=engine)
from .router import post , user , auth ,vote
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


orign=["*"] 
app.add_middleware(
    CORSMiddleware,
    allow_origins=orign,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#model.Base.metadata.create_all(bind=engine) #ye line hume tabhi chalani hai jab humne apne model me koi changes kiya ho taki wo database me reflect ho jaye


@app.get("/")
def read_root():
    return {"welcome to my api!!!!"}



app.include_router(post.router)#yaha router include karna hai taki hume post ke sare endpoints mil jaye
app.include_router(user.router) 
app.include_router(auth.router)
app.include_router(vote.router)