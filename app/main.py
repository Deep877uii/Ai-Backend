from fastapi import FastAPI
from .router import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origin = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome Deepu"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
