"""
Secure anonymous session API endpoints for demo mode
"""
from fastapi import APIRouter, HTTPException, Request, Depends, status, Header
from typing import Dict, Any, Optional
import uuid
import time
import os
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import text

from ..database.db_connection import get_db
from ..database.models import PetState, InteractionHistory
from ..database.pet_repository import PetRepository
from ..security.validators import (
    validate_session_id, validate_emoji_input, validate_context,
    validate_pet_name, sanitize_output, get_client_ip
)
from ..security.session_manager import SecureSessionManager

router = APIRouter(prefix="/api/anonymous", tags=["anonymous"])

# Initialize logger
logger = logging.getLogger(__name__)

# Initialize secure session manager
session_manager = SecureSessionManager(secret_key=os.getenv("SESSION_SECRET_KEY"))

@router.post("/session/create")
async def create_anonymous_session(
    request: Request,
    db: Session = Depends(get_db),
    x_session_token: Optional[str] = Header(None)
) -> Dict[str, Any]:
    """Create a new anonymous session and assign a pet"""
    
    # Get client IP for rate limiting
    client_ip = get_client_ip(request)
    
    try:
        # Create secure session
        session_info = session_manager.create_session(client_ip)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(e)
        )
    
    # Get pet_model from app state
    pet_model = request.app.state.pet_model
    if not pet_model:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Pet model not initialized"
        )
    
    session_id = session_info["session_id"]
    
    # Create pet for this session using existing method
    pet = pet_model.create_pet_for_session(session_id=session_id)
    
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create pet for session"
        )
    
    # Store pet ID in session
    session_manager.sessions[session_id]["pet_id"] = pet.unique_id
    
    # Get pet state from agent
    pet_state = pet.get_state()
    
    # Generate initial greeting using emoji interaction
    try:
        logger.info(f"Generating initial greeting for pet {pet.unique_id}")
        initial_response = pet.receive_emoji_message("👋", session_token)
        initial_message = initial_response.get("pet_response", "Hello! 👋")
        logger.info(f"Initial greeting generated: {initial_message}")
    except Exception as e:
        logger.error(f"Error generating initial greeting: {e}")
        initial_message = "Hello! 👋"
    
    # Sanitize output
    response_data = {
        "session_id": session_id,
        "token": session_info["token"],
        "expires_in": session_info["expires_in"],
        "pet": {
            "id": pet.unique_id,
            "name": pet.name,
            "traits": pet_state.get("traits", {}),
            "mood": round(pet_state.get("mood", 0.5), 2),
            "energy": round(pet_state.get("energy", 0.8), 2),
            "health": round(pet_state.get("health", 1.0), 2),
            "attention": round(pet_state.get("attention", 0.5), 2),
            "needs": pet_state.get("needs", {}),
            "age": pet_state.get("age", 0),
            "stage": pet_state.get("stage", "infant"),
            "current_emoji_message": initial_message,
            "personality_summary": pet.get_personality_summary()
        }
    }
    
    return sanitize_output(response_data)

@router.get("/pets/{session_id}")
async def get_session_pet(
    session_id: str,
    request: Request,
    db: Session = Depends(get_db),
    x_session_token: Optional[str] = Header(None)
) -> Dict[str, Any]:
    """Get pet state for a session"""
    
    # Validate session ID format
    session_id = validate_session_id(session_id)
    
    # Get client IP
    client_ip = get_client_ip(request)
    
    # Validate session
    try:
        session = session_manager.validate_session(
            session_id, 
            token=x_session_token,
            client_ip=client_ip
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    
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
    
    # Get session info
    session_info = session_manager.get_session_info(session_id)
    
    response_data = {
        "id": pet.unique_id,
        "name": pet.name,
        "traits": pet_state.get("traits", {}),
        "mood": round(pet_state.get("mood", 0.5), 2),
        "energy": round(pet_state.get("energy", 0.8), 2),
        "health": round(pet_state.get("health", 1.0), 2),
        "attention": round(pet_state.get("attention", 0.5), 2),
        "needs": pet_state.get("needs", {}),
        "age": pet_state.get("age", 0),
        "stage": pet_state.get("stage", "infant"),
        "current_emoji_message": pet_state.get("current_emoji_message", "😊"),
        "personality_summary": pet.get_personality_summary(),
        "session_info": session_info
    }
    
    return sanitize_output(response_data)

@router.post("/pets/{session_id}/emoji")
async def anonymous_emoji_interaction(
    session_id: str,
    request_body: Dict[str, Any],
    request: Request,
    db: Session = Depends(get_db),
    x_session_token: Optional[str] = Header(None)
) -> Dict[str, Any]:
    """Handle emoji interaction for anonymous session"""
    
    # Validate session ID format
    session_id = validate_session_id(session_id)
    
    # Get client IP
    client_ip = get_client_ip(request)
    
    # Validate session
    try:
        session = session_manager.validate_session(
            session_id,
            token=x_session_token,
            client_ip=client_ip
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    
    # Validate and sanitize input
    emojis = validate_emoji_input(request_body.get("emojis", ""))
    context = validate_context(request_body.get("context", {}))
    
    if not emojis:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Emoji input is required"
        )
    
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
    
    # Increment interaction count
    session_manager.increment_interaction_count(session_id)
    
    # Process emoji interaction using the pet's method
    emoji_response = pet.receive_emoji_message(emojis, session_id)
    response_emoji = emoji_response.get("pet_response", "😊")
    
    # Get updated pet state
    pet_state = pet.get_state()
    
    # Save interaction to history (with parameterized query for safety)
    interaction = InteractionHistory(
        pet_id=pet.unique_id,
        session_id=session_id,
        interaction_type="emoji",
        input_data={"emojis": emojis, "context": context},
        output_data={
            "response": response_emoji,
            "mood": round(pet_state.get("mood", 0.5), 2),
            "energy": round(pet_state.get("energy", 0.8), 2)
        },
        timestamp=datetime.utcnow()
    )
    db.add(interaction)
    db.commit()
    
    response_data = {
        "emoji_response": response_emoji,
        "pet_response": response_emoji,  # For compatibility
        "surprise_level": 0.5,  # Could be calculated from pet state
        "response_confidence": 0.8,
        "pet_state": {
            "mood": round(pet_state.get("mood", 0.5), 2),
            "energy": round(pet_state.get("energy", 0.8), 2),
            "attention": round(pet_state.get("attention", 0.5), 2)
        },
        "interactions_remaining": session_manager.sessions[session_id].get("interactions_remaining", 0)
    }
    
    return sanitize_output(response_data)

@router.get("/pets/{session_id}/memories")
async def get_session_memories(
    session_id: str,
    request: Request,
    db: Session = Depends(get_db),
    x_session_token: Optional[str] = Header(None),
    limit: int = 20
) -> Dict[str, Any]:
    """Get interaction memories for a session"""
    
    # Validate session ID format
    session_id = validate_session_id(session_id)
    
    # Validate limit
    limit = min(max(1, limit), 50)  # Between 1 and 50
    
    # Get client IP
    client_ip = get_client_ip(request)
    
    # Validate session
    try:
        session = session_manager.validate_session(
            session_id,
            token=x_session_token,
            client_ip=client_ip
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    
    # Get recent interactions from database using parameterized query
    interactions = db.query(InteractionHistory)\
        .filter(InteractionHistory.session_id == session_id)\
        .order_by(InteractionHistory.timestamp.desc())\
        .limit(limit)\
        .all()
    
    memories = []
    for interaction in interactions:
        memory = {
            "timestamp": interaction.timestamp.isoformat(),
            "type": interaction.interaction_type,
            "input": interaction.input_data.get("emojis", ""),
            "response": interaction.output_data.get("response", ""),
            "mood": interaction.output_data.get("mood", 0.5),
            "energy": interaction.output_data.get("energy", 0.8)
        }
        memories.append(memory)
    
    return sanitize_output({"memories": memories, "count": len(memories)})

@router.get("/session/stats")
async def get_session_stats(
    request: Request,
    x_admin_key: Optional[str] = Header(None)
) -> Dict[str, Any]:
    """Get session statistics (admin only)"""
    
    # Verify admin key
    admin_key = os.getenv("ADMIN_API_KEY")
    if not admin_key or x_admin_key != admin_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    stats = session_manager.get_stats()
    return sanitize_output(stats)