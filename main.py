from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
# import models
import database,schemas,models
from schemas import UserRegistration,loginrequest
from crud import get_user_by_username, create_user,verify_password
from auth import  create_access_token,decode_access_token
# models.Base.metadata.create_all(bind=database.engine)
from routes.v1 import router as v1_router
from routes.v2 import router as v2_router
app = FastAPI()
# middleware configuration:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# v1_router = APIRouter()

# @app.get("/api/v1/example")
# def example_endpoint():
#     return {"message": "This is an example endpoint"}

# app.include_router(v1_router, prefix="/api/v1")

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

@app.post("/login")
def login(request:loginrequest,db: Session = Depends(get_db)):
    user = get_user_by_username(db,request.name)
    if not user or not verify_password(request.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token = create_access_token(data={"sub": user.name})
    return {"access_token": access_token, "token_type": "bearer"}

app.include_router(v1_router, prefix="/api/v1")
app.include_router(v2_router, prefix="/api/v2")