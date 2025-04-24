from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
# import models
import database,schemas,models
from schemas import UserRegistration,Token
from crud import get_user_by_username, create_user
from auth import  create_access_token,decode_access_token
# models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root(db: Session = Depends(get_db)):
    return {"msg": "Hello FastAPI + SQLite + Alembic!"}

# ✅ POST /users: Insert user
@app.post("/users", response_model=schemas.UserResponse)
def create_userdata(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ✅ GET /users: Fetch all users
@app.get("/users", response_model=list[schemas.UserResponse])
def read_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@app.post("/register")
def register(user: UserRegistration, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, user.name)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    create_user(db, user)
    return {"message": "User created"}

@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
