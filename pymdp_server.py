#!/usr/bin/env python3
"""
Server using PyMDP-based active inference companions
"""
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import uuid
import time
import sys
import os

# Add current directory to path to import our pymdp companion
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from pymdp_companion import PyMDPEmojiCompanion
    PYMDP_AVAILABLE = True
    print("PyMDP companion loaded successfully")
except ImportError as e:
    print(f"PyMDP companion import failed: {e}")
    PYMDP_AVAILABLE = False

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
sessions = {}
pymdp_companions = {}  # Store PyMDP companions by session_id

@app.get("/health")
async def health():
    return {
        "status": "ok", 
        "pymdp_available": PYMDP_AVAILABLE,
        "active_sessions": len(sessions)
    }

@app.post("/api/simple/session/create")
async def create_session(request_body: dict = Body(default={})):
    session_id = str(uuid.uuid4())
    token = str(uuid.uuid4())
    
    # Check if we have saved state to restore
    saved_state = None
    if request_body and request_body.get("saved_state"):
        saved_state = request_body.get("saved_state")
    
    # Create PyMDP-based companion if available
    if PYMDP_AVAILABLE:
        try:
            pymdp_companion = PyMDPEmojiCompanion(session_id)
            
            # Restore saved state if provided
            if saved_state:
                try:
                    pymdp_companion.load_state(saved_state)
                    print(f"Restored companion state for session {session_id}")
                except Exception as e:
                    print(f"Failed to restore state: {e}")
            
            pymdp_companions[session_id] = pymdp_companion
            companion_type = "PyMDP Active Inference"
        except Exception as e:
            print(f"Failed to create PyMDP companion: {e}")
            companion_type = "Fallback Simple"
    else:
        companion_type = "Fallback Simple"
    
    companion_data = {
        "id": str(uuid.uuid4()),
        "name": "Companion",
        "traits": {"intelligence": 0.9, "curiosity": 0.8, "empathy": 0.7},
        "mood": 0.8,
        "energy": 0.9,
        "health": 1.0,
        "attention": 0.6,
        "needs": {
            "hunger": 0.3,
            "thirst": 0.2,
            "social": 0.7,
            "play": 0.5,
            "rest": 0.1
        },
        "age": 0,
        "stage": "learning",
        "current_emoji_message": "👋😊",
        "personality_summary": f"An intelligent companion using {companion_type}",
        "companion_type": companion_type
    }
    
    sessions[session_id] = {
        "session_id": session_id,
        "token": token,
        "companion": companion_data,
        "created_at": time.time()
    }
    
    return {
        "session_id": session_id,
        "token": token,
        "expires_in": 3600,
        "companion": companion_data
    }

@app.get("/api/simple/companions/{session_id}")
async def get_companion(session_id: str):
    if session_id not in sessions:
        return {"error": "Session not found"}
    return sessions[session_id]["companion"]

@app.post("/api/simple/companions/{session_id}/emoji")
async def companion_emoji_interaction(session_id: str, request_body: dict):
    if session_id not in sessions:
        return {"error": "Session not found"}
    
    emojis = request_body.get("emojis", "")
    response_time = request_body.get("response_time", None)
    
    # Use PyMDP companion if available
    if session_id in pymdp_companions and PYMDP_AVAILABLE:
        try:
            pymdp_companion = pymdp_companions[session_id]
            
            # Process with PyMDP active inference
            interaction_result = pymdp_companion.observe_interaction(emojis, response_time)
            
            # Update session data
            sessions[session_id]["companion"]["current_emoji_message"] = interaction_result["companion_response"]
            sessions[session_id]["companion"]["pymdp_state"] = pymdp_companion.get_state()
            
            return {
                "emoji_response": interaction_result["companion_response"],
                "companion_response": interaction_result["companion_response"],
                "surprise_level": interaction_result["surprise_level"],
                "response_confidence": interaction_result["response_confidence"],
                "engagement_belief": interaction_result["engagement_belief"],
                "relationship_depth": interaction_result["relationship_depth"],
                "companion_state": {
                    "mood": 0.8,
                    "energy": 0.9,
                    "attention": interaction_result["engagement_belief"]
                },
                "active_inference_stats": interaction_result.get("active_inference_stats", {}),
                "context_distribution": interaction_result.get("context_distribution", []),
                "pymdp_state": pymdp_companion.get_state(),  # Include full state for localStorage
                "pymdp_enabled": True
            }
            
        except Exception as e:
            print(f"PyMDP interaction failed: {e}")
            # Fall back to simple response
            pass
    
    # Fallback simple response system
    simple_responses = {
        "❤️": ["💕", "🥰", "😍"],
        "😊": ["😄", "🤗", "😊"],
        "🎉": ["🥳", "🎊", "✨"],
        "🤔": ["💭", "🧐", "❓"],
        "😔": ["🤗", "💕", "😊"],
        "👋": ["👋", "😊", "🙌"],
        "🍕": ["😋", "🤤", "👌"],
        "😴": ["💤", "🌙", "😌"]
    }
    
    # Simple response selection
    if emojis in simple_responses:
        response = simple_responses[emojis][hash(emojis + session_id) % len(simple_responses[emojis])]
    else:
        response = "🤔"
    
    sessions[session_id]["companion"]["current_emoji_message"] = response
    
    return {
        "emoji_response": response,
        "companion_response": response,
        "surprise_level": 0.3,
        "response_confidence": 0.7,
        "engagement_belief": 0.6,
        "relationship_depth": 1,
        "companion_state": {
            "mood": 0.8,
            "energy": 0.9,
            "attention": 0.6
        },
        "pymdp_enabled": False,
        "fallback_reason": "PyMDP not available or failed"
    }

@app.get("/api/simple/companions/{session_id}/stats")
async def get_companion_stats(session_id: str):
    """Get detailed stats about the companion's internal state"""
    if session_id not in sessions:
        return {"error": "Session not found"}
    
    if session_id in pymdp_companions and PYMDP_AVAILABLE:
        try:
            pymdp_companion = pymdp_companions[session_id]
            state = pymdp_companion.get_state()
            
            return {
                "pymdp_enabled": True,
                "context_beliefs": state.get("context_beliefs", []),
                "relationship_beliefs": state.get("relationship_beliefs", []),
                "user_preferences": state.get("user_preferences", {}),
                "conversation_length": len(state.get("conversation_history", [])),
                "context_memory": state.get("context_memory", []),
                "companion_type": "PyMDP Active Inference"
            }
        except Exception as e:
            print(f"Failed to get PyMDP stats: {e}")
    
    return {
        "pymdp_enabled": False,
        "companion_type": "Simple Fallback",
        "stats": "Basic companion without detailed internal state"
    }

if __name__ == "__main__":
    print("Starting PyMDP-enhanced companion server...")
    if PYMDP_AVAILABLE:
        print("✓ PyMDP active inference available")
    else:
        print("⚠ PyMDP not available, using fallback system")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)