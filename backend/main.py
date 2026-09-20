from fastapi import FastAPI, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from database import get_db, engine
import models, schemas
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
import secrets
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")
active_sessions = {}
models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
def get_current_user(authorization: str = Header(...), db: Session = Depends(get_db)):
    user_id = active_sessions.get(authorization)
    if not user_id:
        raise HTTPException(status_code=401, detail="not authenticated")
    return db.query(models.User).filter(models.User.id == user_id).one_or_none()


@app.get("/posts", response_model=List[schemas.PostOut])
def list_posts(db: Session = Depends(get_db)):
    return db.query(models.Post).order_by(models.Post.created_at.desc()).all()

@app.get("/posts/{post_id}", response_model=schemas.PostOut)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserReg, db: Session = Depends(get_db)):
    new_user = models.User(username=user.username, password_hash=hash_password(user.password))
    db.add(new_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Username is already taken")
    db.refresh(new_user)
    return new_user

@app.post("/login", response_model=schemas.TokenOut)
def login(user: schemas.UserReg, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).one_or_none()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = secrets.token_hex(8)
    active_sessions[token] = db_user.id
    return {"token": token}

@app.post("/posts", response_model=schemas.PostOut)
def create_post(post: schemas.PostCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_post = models.Post(title = post.title, content=post.content, user_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
