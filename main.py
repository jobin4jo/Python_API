from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
# import models
import database,schemas,models

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
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ✅ GET /users: Fetch all users
@app.get("/users", response_model=list[schemas.UserResponse])
def read_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()
