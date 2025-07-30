"""
Rate limiting middleware for demo deployments
"""
import os
import time
from collections import defaultdict
from datetime import datetime, timedelta
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger(__name__)

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware to enforce rate limits in demo mode"""
    
    def __init__(self, app):
        super().__init__(app)
        self.demo_mode = os.getenv("DEMO_MODE", "false").lower() == "true"
        self.max_interactions = int(os.getenv("MAX_INTERACTIONS", "50"))
        self.session_timeout = int(os.getenv("SESSION_TIMEOUT", "1800"))  # 30 minutes
        self.max_sessions = int(os.getenv("MAX_SESSIONS", "10"))
        
        # In-memory storage (consider Redis for production)
        self.sessions = {}  # session_id -> {count, last_activity, created_at}
        self.cleanup_interval = 300  # Clean up every 5 minutes
        self.last_cleanup = time.time()
        
        if self.demo_mode:
            logger.info(f"Rate limiting enabled: {self.max_interactions} interactions, "
                       f"{self.session_timeout}s timeout, {self.max_sessions} max sessions")
    
    def get_session_id(self, request: Request) -> str:
        """Extract session ID from request"""
        # Try to get from various sources
        session_id = request.headers.get("X-Session-ID")
        if not session_id and hasattr(request.state, "session_id"):
            session_id = request.state.session_id
        return session_id or "default"
    
    def cleanup_sessions(self):
        """Remove expired sessions"""
        now = time.time()
        if now - self.last_cleanup < self.cleanup_interval:
            return
        
        expired = []
        for sid, data in self.sessions.items():
            if now - data["last_activity"] > self.session_timeout:
                expired.append(sid)
        
        for sid in expired:
            del self.sessions[sid]
            logger.info(f"Cleaned up expired session: {sid}")
        
        self.last_cleanup = now
    
    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting if not in demo mode
        if not self.demo_mode:
            return await call_next(request)
        
        # Skip for non-interaction endpoints
        if request.method == "OPTIONS" or request.url.path in ["/", "/health", "/api/health", "/api/demo/status"]:
            return await call_next(request)
        
        # Clean up expired sessions
        self.cleanup_sessions()
        
        # Get session ID
        session_id = self.get_session_id(request)
        now = time.time()
        
        # Check if this is an interaction endpoint
        is_interaction = "emoji" in request.url.path and request.method == "POST"
        
        # Initialize or get session
        if session_id not in self.sessions:
            if len(self.sessions) >= self.max_sessions:
                logger.warning(f"Max sessions reached: {self.max_sessions}")
                return JSONResponse(
                    status_code=429,
                    content={
                        "error": "Demo at capacity",
                        "message": "Maximum number of demo sessions reached. Please try again later."
                    }
                )
            
            self.sessions[session_id] = {
                "count": 0,
                "last_activity": now,
                "created_at": now
            }
            logger.info(f"New session created: {session_id}")
        
        session = self.sessions[session_id]
        
        # Check session timeout
        if now - session["last_activity"] > self.session_timeout:
            del self.sessions[session_id]
            return JSONResponse(
                status_code=440,
                content={
                    "error": "Session expired",
                    "message": "Your demo session has expired. Please refresh to start a new session."
                }
            )
        
        # Update last activity
        session["last_activity"] = now
        
        # Check interaction limit for interaction endpoints
        if is_interaction:
            if session["count"] >= self.max_interactions:
                remaining_time = self.session_timeout - (now - session["created_at"])
                return JSONResponse(
                    status_code=429,
                    content={
                        "error": "Interaction limit reached",
                        "message": f"You've reached the {self.max_interactions} interaction limit for this demo.",
                        "interactions_used": session["count"],
                        "session_time_remaining": int(remaining_time)
                    }
                )
            
            # Increment counter after successful interaction
            response = await call_next(request)
            if response.status_code < 400:
                session["count"] += 1
                logger.debug(f"Session {session_id}: {session['count']}/{self.max_interactions} interactions")
            return response
        
        # For non-interaction endpoints, just pass through
        return await call_next(request)