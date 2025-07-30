"""
Simple anonymous API for testing
"""
from fastapi import APIRouter, HTTPException, Request, status
from typing import Dict, Any
import uuid
import json

router = APIRouter(prefix="/api/simple", tags=["simple"])

# In-memory storage for testing
sessions = {}

@router.post("/session/create")
async def create_simple_session(request: Request) -> Dict[str, Any]:
    """Create a simple test session"""
    
    session_id = str(uuid.uuid4())
    token = str(uuid.uuid4())
    
    # Create mock pet data
    pet_data = {
        "id": str(uuid.uuid4()),
        "name": "TestPet",
        "traits": {"playfulness": 0.7, "curiosity": 0.6},
        "mood": 0.8,
        "energy": 0.9,
        "health": 1.0,
        "attention": 0.5,
        "needs": {
            "hunger": 0.3,
            "thirst": 0.2,
            "social": 0.6,
            "play": 0.4,
            "rest": 0.1
        },
        "age": 0,
        "stage": "infant",
        "current_emoji_message": "👋 Hello! I'm your new companion!",
        "personality_summary": "A curious and playful digital companion"
    }
    
    # Store session
    sessions[session_id] = {
        "session_id": session_id,
        "token": token,
        "pet": pet_data,
        "created_at": "2024-07-30T20:00:00Z"
    }
    
    return {
        "session_id": session_id,
        "token": token,
        "expires_in": 3600,
        "pet": pet_data
    }

@router.get("/pets/{session_id}")
async def get_simple_pet(session_id: str) -> Dict[str, Any]:
    """Get pet for a session"""
    
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session_data = sessions[session_id]
    return session_data["pet"]

@router.post("/pets/{session_id}/emoji")
async def simple_emoji_interaction(
    session_id: str,
    request_body: Dict[str, Any]
) -> Dict[str, Any]:
    """Handle emoji interaction"""
    
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    emojis = request_body.get("emojis", "")
    
    # Simple emoji responses
    responses = {
        "👋": "👋😊 Hello there!",
        "❤️": "❤️😊 I love you too!",
        "🎉": "🎉🥳 Party time!",
        "😴": "😴💤 Sweet dreams...",
        "🍕": "🍕😋 Yummy!",
    }
    
    # Get response or default
    response = responses.get(emojis, "😊 That's interesting!")
    
    return {
        "emoji_response": response,
        "pet_response": response,
        "surprise_level": 0.5,
        "response_confidence": 0.8,
        "pet_state": {
            "mood": 0.8,
            "energy": 0.9,
            "attention": 0.7
        }
    }