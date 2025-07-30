"""
Anonymous session API endpoints for demo mode
"""
from fastapi import APIRouter, HTTPException, Request, Depends, status
from typing import Dict, Any, Optional
import uuid
import time
from datetime import datetime
from sqlalchemy.orm import Session

from ..database.db_connection import get_db
from ..database.models import PetState, InteractionHistory
from ..database.pet_repository import PetRepository

router = APIRouter(prefix="/api/anonymous", tags=["anonymous"])

# In-memory session store (in production, use Redis)
anonymous_sessions: Dict[str, Dict[str, Any]] = {}

@router.post("/session/create")
async def create_anonymous_session(
    request: Request,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Create a new anonymous session and assign a pet"""
    
    # Get pet_model from app state
    pet_model = request.app.state.pet_model
    if not pet_model:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Pet model not initialized"
        )
    
    # Generate session ID
    session_id = str(uuid.uuid4())
    
    # Create session data
    anonymous_sessions[session_id] = {
        "created_at": time.time(),
        "last_activity": time.time(),
        "interaction_count": 0
    }
    
    # Create pet for this session using existing method
    pet = pet_model.create_pet_for_session(session_id=session_id)
    
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create pet for session"
        )
    
    # Get pet state from agent
    pet_state = pet.get_state()
    
    # Generate initial greeting
    initial_message = pet.generate_emoji_response("👋", {
        "is_first_interaction": True,
        "time_of_day": datetime.now().strftime("%H:%M")
    })
    
    return {
        "session_id": session_id,
        "pet": {
            "id": pet.unique_id,
            "name": pet.name,
            "traits": pet_state.get("traits", {}),
            "mood": pet_state.get("mood", 0.5),
            "energy": pet_state.get("energy", 0.8),
            "health": pet_state.get("health", 1.0),
            "attention": pet_state.get("attention", 0.5),
            "needs": pet_state.get("needs", {}),
            "age": pet_state.get("age", 0),
            "stage": pet_state.get("stage", "infant"),
            "current_emoji_message": initial_message,
            "personality_summary": pet.get_personality_summary()
        }
    }

@router.get("/pets/{session_id}")
async def get_session_pet(
    session_id: str,
    request: Request,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get pet state for a session"""
    
    # Check if session exists
    if session_id not in anonymous_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Update last activity
    anonymous_sessions[session_id]["last_activity"] = time.time()
    
    # Get pet_model from app state
    pet_model = request.app.state.pet_model
    if not pet_model:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Pet model not initialized"
        )
    
    # Find pet by session ID
    pet = None
    for agent in pet_model.schedule.agents:
        if hasattr(agent, 'session_id') and agent.session_id == session_id:
            pet = agent
            break
    
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found for session")
    
    # Get pet state
    pet_state = pet.get_state()
    
    return {
        "id": pet.unique_id,
        "name": pet.name,
        "traits": pet_state.get("traits", {}),
        "mood": pet_state.get("mood", 0.5),
        "energy": pet_state.get("energy", 0.8),
        "health": pet_state.get("health", 1.0),
        "attention": pet_state.get("attention", 0.5),
        "needs": pet_state.get("needs", {}),
        "age": pet_state.get("age", 0),
        "stage": pet_state.get("stage", "infant"),
        "current_emoji_message": pet_state.get("current_emoji_message", "😊"),
        "personality_summary": pet.get_personality_summary()
    }

@router.post("/pets/{session_id}/emoji")
async def anonymous_emoji_interaction(
    session_id: str,
    request_body: Dict[str, Any],
    request: Request,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Handle emoji interaction for anonymous session"""
    
    # Check if session exists
    if session_id not in anonymous_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Update session activity
    session_data = anonymous_sessions[session_id]
    session_data["last_activity"] = time.time()
    session_data["interaction_count"] += 1
    
    # Get emoji sequence
    emojis = request_body.get("emojis", "")
    context = request_body.get("context", {})
    
    # Get pet_model from app state
    pet_model = request.app.state.pet_model
    if not pet_model:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Pet model not initialized"
        )
    
    # Find pet by session ID
    pet = None
    for agent in pet_model.schedule.agents:
        if hasattr(agent, 'session_id') and agent.session_id == session_id:
            pet = agent
            break
    
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found for session")
    
    # Process emoji interaction using the pet's method
    response_emoji = pet.generate_emoji_response(emojis, context)
    
    # Process the interaction
    pet.process_emoji_interaction(emojis, context)
    
    # Get updated pet state
    pet_state = pet.get_state()
    
    # Save interaction to history
    interaction = InteractionHistory(
        pet_id=pet.unique_id,
        session_id=session_id,
        interaction_type="emoji",
        input_data={"emojis": emojis, "context": context},
        output_data={
            "response": response_emoji,
            "pet_state": pet_state
        },
        timestamp=datetime.utcnow()
    )
    db.add(interaction)
    db.commit()
    
    return {
        "emoji_response": response_emoji,
        "pet_response": response_emoji,  # For compatibility
        "surprise_level": 0.5,  # Could be calculated from pet state
        "response_confidence": 0.8,
        "pet_state": {
            "mood": pet_state.get("mood", 0.5),
            "energy": pet_state.get("energy", 0.8),
            "attention": pet_state.get("attention", 0.5)
        }
    }

@router.get("/pets/{session_id}/memories")
async def get_session_memories(
    session_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get interaction memories for a session"""
    
    # Check if session exists
    if session_id not in anonymous_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Get recent interactions from database
    interactions = db.query(InteractionHistory)\
        .filter(InteractionHistory.session_id == session_id)\
        .order_by(InteractionHistory.timestamp.desc())\
        .limit(20)\
        .all()
    
    memories = []
    for interaction in interactions:
        memory = {
            "timestamp": interaction.timestamp.isoformat(),
            "type": interaction.interaction_type,
            "input": interaction.input_data.get("emojis", ""),
            "response": interaction.output_data.get("response", ""),
            "pet_state": interaction.output_data.get("pet_state", {})
        }
        memories.append(memory)
    
    return {"memories": memories}

# Session cleanup (run periodically)
async def cleanup_expired_sessions(max_age_seconds: int = 1800):
    """Remove expired anonymous sessions (30 minutes default)"""
    current_time = time.time()
    expired_sessions = []
    
    for session_id, data in anonymous_sessions.items():
        if current_time - data["last_activity"] > max_age_seconds:
            expired_sessions.append(session_id)
    
    for session_id in expired_sessions:
        del anonymous_sessions[session_id]
    
    return len(expired_sessions)