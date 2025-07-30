"""
Authentication and migration endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session

from ..database.db_connection import get_db
from ..database.models import PetState, InteractionHistory, User
from ..middleware.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/migrate-anonymous-data")
async def migrate_anonymous_data(
    request_body: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Migrate anonymous session data to authenticated user account"""
    
    session_id = request_body.get("session_id")
    if not session_id:
        raise HTTPException(status_code=400, detail="session_id is required")
    
    # Find pet associated with the session
    pet_state = db.query(PetState).filter(PetState.session_id == session_id).first()
    if not pet_state:
        raise HTTPException(status_code=404, detail="No pet found for this session")
    
    # Check if pet already has an owner (shouldn't happen but safety check)
    if pet_state.owner_id and pet_state.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="This pet already belongs to another user")
    
    # Update pet ownership
    pet_state.owner_id = current_user.id
    pet_state.session_id = None  # Clear session ID
    pet_state.updated_at = datetime.utcnow()
    
    # Count interactions to migrate
    interactions_count = db.query(InteractionHistory)\
        .filter(InteractionHistory.session_id == session_id)\
        .count()
    
    # Update all interactions to belong to the user
    db.query(InteractionHistory)\
        .filter(InteractionHistory.session_id == session_id)\
        .update({
            "user_id": current_user.id,
            "session_id": None
        })
    
    db.commit()
    
    # Return migration results
    vital_stats = pet_state.vital_stats or {}
    return {
        "success": True,
        "pet": {
            "id": pet_state.pet_id,
            "name": pet_state.pet_name,
            "traits": pet_state.traits,
            "mood": vital_stats.get("happiness", 0.5),
            "energy": vital_stats.get("energy", 0.8),
            "health": vital_stats.get("health", 1.0),
            "attention": pet_state.attention_level / 100.0,
            "age": pet_state.age,
            "stage": pet_state.development_stage
        },
        "interactions_migrated": interactions_count,
        "message": f"Successfully migrated {interactions_count} interactions to your account"
    }

@router.post("/login")
async def login(
    credentials: Dict[str, str],
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Mock login endpoint for demo purposes"""
    # This is a simplified login for demo purposes
    # In production, use proper authentication with JWT tokens
    
    username = credentials.get("username")
    password = credentials.get("password")
    
    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password required")
    
    # Mock authentication - in production, verify against database with hashed passwords
    if username == "demo" and password == "demo123":
        return {
            "access_token": "demo-token-12345",
            "token_type": "bearer",
            "user": {
                "id": "demo-user-id",
                "username": username,
                "email": "demo@example.com"
            }
        }
    
    raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/signup")
async def signup(
    user_data: Dict[str, str],
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Mock signup endpoint for demo purposes"""
    # This is a simplified signup for demo purposes
    # In production, properly hash passwords and validate data
    
    username = user_data.get("username")
    email = user_data.get("email")
    password = user_data.get("password")
    
    if not all([username, email, password]):
        raise HTTPException(status_code=400, detail="Username, email, and password required")
    
    # Check if user exists (mock check)
    if username == "demo":
        raise HTTPException(status_code=409, detail="Username already exists")
    
    # Create user (mock response)
    return {
        "success": True,
        "message": "Account created successfully",
        "user": {
            "id": f"user-{username}",
            "username": username,
            "email": email
        }
    }