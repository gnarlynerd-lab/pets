"""
Demo-specific API endpoints
"""
from fastapi import APIRouter, Request, Depends
from typing import Dict, Any
import os
import time

router = APIRouter(prefix="/api/demo", tags=["demo"])

def get_rate_limiter(request: Request):
    """Get rate limiter from app state"""
    return getattr(request.app.state, "rate_limiter", None)

@router.get("/status")
async def get_demo_status(
    request: Request,
    rate_limiter=Depends(get_rate_limiter)
) -> Dict[str, Any]:
    """Get current demo session status"""
    
    if not rate_limiter or not rate_limiter.demo_mode:
        return {
            "demo_mode": False,
            "message": "Demo mode is not enabled"
        }
    
    # Get session ID from request
    session_id = rate_limiter.get_session_id(request)
    
    # Get session data
    session = rate_limiter.sessions.get(session_id)
    if not session:
        return {
            "demo_mode": True,
            "session_exists": False,
            "max_interactions": rate_limiter.max_interactions,
            "session_timeout": rate_limiter.session_timeout,
            "max_sessions": rate_limiter.max_sessions,
            "active_sessions": len(rate_limiter.sessions)
        }
    
    now = time.time()
    time_elapsed = now - session["created_at"]
    time_remaining = max(0, rate_limiter.session_timeout - time_elapsed)
    
    return {
        "demo_mode": True,
        "session_exists": True,
        "session_id": session_id,
        "interactions_used": session["count"],
        "interactions_remaining": rate_limiter.max_interactions - session["count"],
        "max_interactions": rate_limiter.max_interactions,
        "session_time_elapsed": int(time_elapsed),
        "session_time_remaining": int(time_remaining),
        "session_timeout": rate_limiter.session_timeout,
        "active_sessions": len(rate_limiter.sessions),
        "max_sessions": rate_limiter.max_sessions
    }

@router.post("/reset")
async def reset_demo_session(
    request: Request,
    rate_limiter=Depends(get_rate_limiter)
) -> Dict[str, str]:
    """Reset current demo session (for testing)"""
    
    if not rate_limiter or not rate_limiter.demo_mode:
        return {"error": "Demo mode is not enabled"}
    
    # Only allow in development
    if os.getenv("ENVIRONMENT", "production") == "production":
        return {"error": "Reset not allowed in production"}
    
    session_id = rate_limiter.get_session_id(request)
    if session_id in rate_limiter.sessions:
        del rate_limiter.sessions[session_id]
        return {"message": f"Session {session_id} reset successfully"}
    
    return {"message": "No active session to reset"}