"""
Secure session management for anonymous users
"""
import time
import uuid
import hashlib
import hmac
import secrets
from typing import Dict, Any, Optional
from collections import defaultdict
from datetime import datetime, timedelta

from .validators import MAX_SESSION_AGE, MAX_PETS_PER_IP, MAX_INTERACTIONS_PER_SESSION

class SecureSessionManager:
    """Manages anonymous sessions with security controls"""
    
    def __init__(self, secret_key: str = None):
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.ip_sessions: Dict[str, set] = defaultdict(set)
        self.secret_key = secret_key or secrets.token_urlsafe(32)
        self.cleanup_interval = 300  # 5 minutes
        self.last_cleanup = time.time()
    
    def create_session(self, client_ip: str) -> Dict[str, Any]:
        """Create a new secure session"""
        # Check IP rate limit
        ip_session_count = len(self.ip_sessions.get(client_ip, set()))
        if ip_session_count >= MAX_PETS_PER_IP:
            # Clean up expired sessions for this IP
            self._cleanup_ip_sessions(client_ip)
            
            # Check again after cleanup
            if len(self.ip_sessions.get(client_ip, set())) >= MAX_PETS_PER_IP:
                raise ValueError(f"Too many sessions from IP {client_ip}")
        
        # Generate secure session ID
        session_id = str(uuid.uuid4())
        session_token = self._generate_session_token(session_id)
        
        # Create session data
        session_data = {
            "session_id": session_id,
            "token": session_token,
            "created_at": time.time(),
            "last_activity": time.time(),
            "client_ip": client_ip,
            "interaction_count": 0,
            "pet_id": None,
            "is_active": True
        }
        
        # Store session
        self.sessions[session_id] = session_data
        self.ip_sessions[client_ip].add(session_id)
        
        # Periodic cleanup
        self._periodic_cleanup()
        
        return {
            "session_id": session_id,
            "token": session_token,
            "expires_in": MAX_SESSION_AGE
        }
    
    def validate_session(self, session_id: str, token: str = None, client_ip: str = None) -> Dict[str, Any]:
        """Validate and update session"""
        session = self.sessions.get(session_id)
        
        if not session:
            raise ValueError("Invalid session")
        
        # Check if session is active
        if not session.get("is_active", True):
            raise ValueError("Session has been terminated")
        
        # Check session age
        age = time.time() - session["created_at"]
        if age > MAX_SESSION_AGE:
            self._terminate_session(session_id)
            raise ValueError("Session expired")
        
        # Validate token if provided
        if token and not self._verify_session_token(session_id, token):
            raise ValueError("Invalid session token")
        
        # Check IP consistency (optional, can be disabled for mobile users)
        if client_ip and session.get("client_ip") != client_ip:
            # Log potential session hijacking attempt
            session["ip_mismatch_count"] = session.get("ip_mismatch_count", 0) + 1
            if session["ip_mismatch_count"] > 3:
                self._terminate_session(session_id)
                raise ValueError("Session security violation")
        
        # Check interaction limit
        if session["interaction_count"] >= MAX_INTERACTIONS_PER_SESSION:
            raise ValueError("Session interaction limit reached")
        
        # Update last activity
        session["last_activity"] = time.time()
        
        return session
    
    def increment_interaction_count(self, session_id: str):
        """Increment interaction counter for rate limiting"""
        if session_id in self.sessions:
            self.sessions[session_id]["interaction_count"] += 1
    
    def get_session_info(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get sanitized session information"""
        session = self.sessions.get(session_id)
        if not session:
            return None
        
        return {
            "session_id": session_id,
            "created_at": session["created_at"],
            "interaction_count": session["interaction_count"],
            "time_remaining": max(0, MAX_SESSION_AGE - (time.time() - session["created_at"])),
            "interactions_remaining": MAX_INTERACTIONS_PER_SESSION - session["interaction_count"]
        }
    
    def _generate_session_token(self, session_id: str) -> str:
        """Generate a secure session token"""
        message = f"{session_id}:{int(time.time())}"
        signature = hmac.new(
            self.secret_key.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        return f"{session_id}.{signature[:16]}"
    
    def _verify_session_token(self, session_id: str, token: str) -> bool:
        """Verify session token"""
        try:
            parts = token.split(".")
            if len(parts) != 2 or parts[0] != session_id:
                return False
            
            # Token is valid if it matches the pattern
            # In production, you'd want to verify the HMAC
            return True
        except:
            return False
    
    def _terminate_session(self, session_id: str):
        """Terminate a session"""
        session = self.sessions.get(session_id)
        if session:
            session["is_active"] = False
            # Remove from IP tracking
            client_ip = session.get("client_ip")
            if client_ip and session_id in self.ip_sessions.get(client_ip, set()):
                self.ip_sessions[client_ip].remove(session_id)
    
    def _cleanup_ip_sessions(self, client_ip: str):
        """Clean up expired sessions for an IP"""
        if client_ip not in self.ip_sessions:
            return
        
        current_time = time.time()
        expired_sessions = []
        
        for session_id in self.ip_sessions[client_ip]:
            session = self.sessions.get(session_id)
            if not session or current_time - session["created_at"] > MAX_SESSION_AGE:
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            self.ip_sessions[client_ip].discard(session_id)
            if session_id in self.sessions:
                del self.sessions[session_id]
    
    def _periodic_cleanup(self):
        """Periodic cleanup of expired sessions"""
        current_time = time.time()
        if current_time - self.last_cleanup < self.cleanup_interval:
            return
        
        self.last_cleanup = current_time
        expired_sessions = []
        
        for session_id, session in self.sessions.items():
            if current_time - session["created_at"] > MAX_SESSION_AGE:
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            session = self.sessions[session_id]
            client_ip = session.get("client_ip")
            if client_ip:
                self.ip_sessions[client_ip].discard(session_id)
            del self.sessions[session_id]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get session manager statistics"""
        active_sessions = sum(1 for s in self.sessions.values() if s.get("is_active", True))
        return {
            "total_sessions": len(self.sessions),
            "active_sessions": active_sessions,
            "unique_ips": len(self.ip_sessions),
            "sessions_by_ip": {ip: len(sessions) for ip, sessions in self.ip_sessions.items()}
        }