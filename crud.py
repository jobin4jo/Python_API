from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models import User
from schemas import UserRegistration

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.name == username).first()

def create_user(db: Session, user: UserRegistration):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(name=user.name, password=hashed_password, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)