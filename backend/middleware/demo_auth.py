"""
Demo authentication middleware for password-protected demo deployments
"""
import os
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger(__name__)

class DemoAuthMiddleware(BaseHTTPMiddleware):
    """Middleware to check demo password if demo mode is enabled"""
    
    def __init__(self, app, demo_password: str = None):
        super().__init__(app)
        self.demo_mode = os.getenv("DEMO_MODE", "false").lower() == "true"
        self.demo_password = demo_password or os.getenv("DEMO_PASSWORD", "AFFINITY2024")
        
        if self.demo_mode:
            logger.info("Demo mode enabled with password protection")
    
    async def dispatch(self, request: Request, call_next):
        # Skip auth for health checks and CORS preflight
        if request.method == "OPTIONS" or request.url.path in ["/", "/health", "/api/health"]:
            return await call_next(request)
        
        # Only check password in demo mode
        if self.demo_mode:
            # Get password from header
            provided_password = request.headers.get("X-Demo-Password", "")
            
            if provided_password != self.demo_password:
                logger.warning(f"Invalid demo password attempt from {request.client.host}")
                return JSONResponse(
                    status_code=401,
                    content={"error": "Invalid demo password"}
                )
        
        # Continue with request
        response = await call_next(request)
        return response