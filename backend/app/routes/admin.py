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


@router.get("/blocked_users")
def get_blocked_users(db: Session = Depends(get_db)):
    blocked_users = db.query(BlockedUser).all()
    return {"blocked_users": [user.user_id for user in blocked_users]}

@router.delete("/unblock_user/{user_id}")
def unblock_user(user_id: str, db: Session = Depends(get_db)):
    # Check if the user is blocked
    blocked_user = db.query(BlockedUser).filter(BlockedUser.user_id == user_id).first()
    if not blocked_user:
        raise HTTPException(status_code=404, detail="User not found in blocked list")

    # Remove the user from the BlockedUser table
    db.delete(blocked_user)
    db.commit()
    
    return {"message": f"User {user_id} has been unblocked"}

@router.get("/is_user_blocked/{user_id}")
def is_user_blocked(user_id: str, db: Session = Depends(get_db)):
    blocked_user = db.query(BlockedUser).filter(BlockedUser.user_id == user_id).first()
    if blocked_user:
        return {"is_blocked": True}
    return {"is_blocked": False}