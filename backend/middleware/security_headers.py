"""
Security headers middleware for production deployment
"""
import os
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses"""
    
    async def dispatch(self, request: Request, call_next: Callable):
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        
        # HSTS header for HTTPS deployments
        if request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        # CSP header - adjust based on your needs
        csp_directives = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'",  # Adjust as needed
            "style-src 'self' 'unsafe-inline'",
            "img-src 'self' data: https:",
            "font-src 'self'",
            "connect-src 'self' wss: https:",
            "frame-ancestors 'none'",
            "base-uri 'self'",
            "form-action 'self'"
        ]
        response.headers["Content-Security-Policy"] = "; ".join(csp_directives)
        
        # Remove server header if present
        response.headers.pop("Server", None)
        
        # Add custom server header to obscure technology
        response.headers["Server"] = "DKS/1.0"
        
        return response

class EnhancedCORSMiddleware(BaseHTTPMiddleware):
    """Enhanced CORS middleware with security in mind"""
    
    def __init__(self, app):
        super().__init__(app)
        # Get allowed origins from environment
        allowed_origins_str = os.getenv("CORS_ORIGINS", "http://localhost:3000")
        self.allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",")]
        self.allow_credentials = os.getenv("CORS_ALLOW_CREDENTIALS", "true").lower() == "true"
        
    async def dispatch(self, request: Request, call_next: Callable):
        # Handle preflight requests
        if request.method == "OPTIONS":
            return self.preflight_response(request)
        
        response = await call_next(request)
        
        # Add CORS headers
        origin = request.headers.get("origin")
        if origin in self.allowed_origins:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = str(self.allow_credentials).lower()
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Session-ID, X-Session-Token"
            response.headers["Access-Control-Max-Age"] = "86400"  # 24 hours
        
        return response
    
    def preflight_response(self, request: Request):
        """Handle CORS preflight requests"""
        origin = request.headers.get("origin")
        
        if origin not in self.allowed_origins:
            return JSONResponse(
                status_code=403,
                content={"error": "CORS origin not allowed"}
            )
        
        response = JSONResponse(content={})
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = str(self.allow_credentials).lower()
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Session-ID, X-Session-Token"
        response.headers["Access-Control-Max-Age"] = "86400"
        
        return response