"""
Security validators for input sanitization and validation
"""
import re
import unicodedata
from typing import Dict, Any, Optional
from fastapi import HTTPException, status

# Security constants
MAX_EMOJI_LENGTH = 50  # Maximum emoji sequence length
MAX_CONTEXT_SIZE = 1024  # Maximum context JSON size in bytes
MAX_SESSION_AGE = 1800  # 30 minutes
MAX_PETS_PER_IP = 5  # Maximum pets per IP address
MAX_INTERACTIONS_PER_SESSION = 100  # Maximum interactions per session
ALLOWED_CONTEXT_KEYS = {"source", "time_of_day", "is_first_interaction", "mood_hint"}

# Emoji validation pattern - comprehensive Unicode ranges
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags
    "\U00002500-\U00002BEF"  # chinese char
    "\U00002702-\U000027B0"
    "\U000024C2-\U0001F251"
    "\U0001f926-\U0001f937"
    "\U00010000-\U0010ffff"
    "\u2640-\u2642"
    "\u2600-\u2B55"
    "\u200d"
    "\u23cf"
    "\u23e9"
    "\u231a"
    "\ufe0f"  # dingbats
    "\u3030"
    "\u0020"  # space
    "]+$", 
    flags=re.UNICODE
)

def validate_session_id(session_id: str) -> str:
    """Validate and sanitize session ID"""
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Session ID is required"
        )
    
    # Check if it's a valid UUID format
    uuid_pattern = re.compile(
        r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$',
        re.IGNORECASE
    )
    
    if not uuid_pattern.match(session_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid session ID format"
        )
    
    return session_id.lower()

def validate_emoji_input(emojis: str) -> str:
    """Validate and sanitize emoji input"""
    if not emojis:
        return ""
    
    # Remove any control characters
    cleaned = "".join(ch for ch in emojis if unicodedata.category(ch)[0] != "C" or ch == " ")
    
    # Check length
    if len(cleaned) > MAX_EMOJI_LENGTH:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Emoji sequence too long (max {MAX_EMOJI_LENGTH} characters)"
        )
    
    # Validate it contains only emojis and spaces
    if cleaned and not EMOJI_PATTERN.match(cleaned):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid characters in emoji sequence"
        )
    
    return cleaned

def validate_context(context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Validate and sanitize context data"""
    if not context:
        return {}
    
    # Check size
    import json
    context_str = json.dumps(context)
    if len(context_str.encode('utf-8')) > MAX_CONTEXT_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Context data too large (max {MAX_CONTEXT_SIZE} bytes)"
        )
    
    # Filter to allowed keys only
    filtered_context = {}
    for key in ALLOWED_CONTEXT_KEYS:
        if key in context:
            value = context[key]
            # Sanitize string values
            if isinstance(value, str):
                # Remove any HTML/script tags
                value = re.sub(r'<[^>]+>', '', value)
                # Limit length
                value = value[:100]
            filtered_context[key] = value
    
    return filtered_context

def validate_pet_name(name: Optional[str]) -> Optional[str]:
    """Validate and sanitize pet name"""
    if not name:
        return None
    
    # Remove any control characters and limit length
    cleaned = "".join(ch for ch in name if unicodedata.category(ch)[0] != "C")
    cleaned = cleaned.strip()[:50]
    
    # Check for minimum length
    if len(cleaned) < 1:
        return None
    
    # Remove any HTML/script tags
    cleaned = re.sub(r'<[^>]+>', '', cleaned)
    
    # Allow only alphanumeric, spaces, and basic punctuation
    if not re.match(r'^[\w\s\-\.\']+$', cleaned, re.UNICODE):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Pet name contains invalid characters"
        )
    
    return cleaned

def sanitize_output(data: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize data before sending to client"""
    # Remove any internal fields
    sensitive_fields = ['_sa_instance_state', 'password', 'secret', 'token', 'key']
    
    def clean_dict(d):
        if not isinstance(d, dict):
            return d
        
        cleaned = {}
        for k, v in d.items():
            # Skip sensitive fields
            if any(field in k.lower() for field in sensitive_fields):
                continue
            
            # Recursively clean nested dicts
            if isinstance(v, dict):
                cleaned[k] = clean_dict(v)
            elif isinstance(v, list):
                cleaned[k] = [clean_dict(item) if isinstance(item, dict) else item for item in v]
            else:
                cleaned[k] = v
        
        return cleaned
    
    return clean_dict(data)

def get_client_ip(request) -> str:
    """Extract client IP from request, considering proxies"""
    # Check for proxy headers
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        # Take the first IP in the chain
        return forwarded.split(",")[0].strip()
    
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip
    
    # Fallback to direct connection
    return request.client.host if request.client else "unknown"