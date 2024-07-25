from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.database.db import SessionLocal
from backend.database.models import BlockedUser

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() # Dependency for total tweets

@router.post("/block_user/{user_id}")
def block_user(user_id: str, db: Session = Depends(get_db)):
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    # Add user_id to the blocked users table
    blocked_user = BlockedUser(user_id=user_id)
    db.add(blocked_user)
    db.commit()
    
    return {"message": f"User {user_id} has been blocked"}
