"""
DKS Digital Pet System Main Application Entry Point
"""
import asyncio
import logging
import time
from typing import Optional, Dict, Any
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import json
import uuid
from typing import Optional

from backend.models.pet_model import PetModel
from backend.communication.redis_manager import RedisManager
from backend.visualization.data_collector import DataCollector
from backend.database import init_db, PetRepository, get_db
from backend.database.models import PetEnvironment, User
from backend.auth import (
    authenticate_user, create_user, create_access_token, get_current_active_user,
    get_user_by_email, get_password_hash
)
from backend.auth.schemas import UserCreate, UserLogin, UserResponse, Token, PasswordChange
from datetime import timedelta, datetime
from sqlalchemy.orm import Session
from pydantic import BaseModel


class CreatePetRequest(BaseModel):
    pet_name: Optional[str] = None


class UpdatePetNameRequest(BaseModel):
    new_name: str


class AnonymousInteractionRequest(BaseModel):
    pet_id: Optional[str] = None
    emojis: str
    context: Optional[Dict[str, Any]] = None


class MigrateAnonymousDataRequest(BaseModel):
    session_id: str


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app for web API and WebSocket connections
app = FastAPI(title="DKS Agent System", version="1.0.0")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
pet_model: Optional[PetModel] = None
redis_manager: Optional[RedisManager] = None
data_collector: Optional[DataCollector] = None
connected_clients = set()


@app.on_event("startup")
async def startup_event():
    """Initialize the system on startup"""
    global pet_model, redis_manager, data_collector
    
    logger.info("Starting DKS Digital Pet System...")
    
    # Initialize database
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
    
    # Initialize Redis connection
    redis_manager = RedisManager()
    await redis_manager.initialize()
    
    # Initialize data collector
    data_collector = DataCollector()
    
    # Create initial pet model
    pet_model = PetModel(
        num_pets=5,
        redis_manager=redis_manager,
        data_collector=data_collector
    )
    
    # Load any existing pets from database
    try:
        existing_pets = PetRepository.get_all_pets()
        logger.info(f"Found {len(existing_pets)} existing pets in database")
    except Exception as e:
        logger.error(f"Failed to load existing pets: {e}")
    
    logger.info("DKS Digital Pet System initialized successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown"""
    global redis_manager
    
    logger.info("Shutting down DKS Digital Pet System...")
    
    if redis_manager:
        await redis_manager.close()
    
    logger.info("DKS Digital Pet System shutdown complete")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "DKS Digital Pet System is running", "status": "healthy"}


@app.get("/api/status")
async def get_status():
    """Get system status"""
    if not pet_model:
        return {"status": "initializing"}
    
    return {
        "status": "running",
        "step": pet_model.schedule.steps,
        "num_pets": len(pet_model.schedule.agents),
        "active_users": len(pet_model.active_users)
    }


@app.post("/api/simulation/start")
async def start_simulation():
    """Start the simulation"""
    if not pet_model:
        return {"error": "Model not initialized"}
    
    # Start simulation in background
    asyncio.create_task(run_simulation())
    return {"message": "Simulation started"}


@app.post("/api/simulation/stop")
async def stop_simulation():
    """Stop the simulation"""
    if pet_model:
        pet_model.running = False
    return {"message": "Simulation stopped"}


@app.post("/api/simulation/reset")
async def reset_simulation():
    """Reset the simulation"""
    global pet_model
    
    if pet_model:
        pet_model = PetModel(
            num_pets=5,
            redis_manager=redis_manager,
            data_collector=data_collector
        )
    
    return {"message": "Simulation reset"}


@app.post("/api/pets/save")
async def save_all_pets():
    """Save all current pet states to database"""
    if not pet_model:
        return {"error": "Model not initialized"}
    
    try:
        saved_count = 0
        for agent in pet_model.schedule.agents:
            if hasattr(agent, 'unique_id'):
                result = PetRepository.save_pet_from_agent(agent)
                if result:
                    saved_count += 1
        
        return {
            "message": f"Saved {saved_count} pets to database",
            "saved_count": saved_count,
            "total_pets": len(pet_model.schedule.agents)
        }
    except Exception as e:
        logger.error(f"Error saving pets: {e}")
        return {"error": f"Failed to save pets: {str(e)}"}


@app.get("/api/pets/load")
async def load_pets_from_db():
    """Load all pets from database"""
    try:
        pets = PetRepository.get_all_pets()
        pets_data = [pet.to_dict() for pet in pets]
        
        return {
            "message": f"Loaded {len(pets)} pets from database",
            "count": len(pets),
            "pets": pets_data
        }
    except Exception as e:
        logger.error(f"Error loading pets: {e}")
        return {"error": f"Failed to load pets: {str(e)}"}


# Authentication endpoints
@app.get("/auth/test")
async def test_auth():
    """Test auth endpoint"""
    return {"message": "Auth system working"}

@app.post("/auth/register")
async def register_user(user_data: UserCreate):
    """Register a new user"""
    try:
        with get_db() as db:
            # Check if user already exists
            if get_user_by_email(db, user_data.email):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
            
            user = create_user(
                db=db,
                username=user_data.username,
                email=user_data.email,
                password=user_data.password,
                user_preferences=user_data.user_preferences
            )
            
            return {
                "user_id": user.user_id,
                "username": user.username,
                "email": user.email,
                "message": "User created successfully"
            }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}"
        )


@app.post("/auth/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login and get access token"""
    try:
        with get_db() as db:
            user = authenticate_user(db, form_data.username, form_data.password)  # username field contains email
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect email or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # Update last login
            from datetime import datetime as dt
            user.last_login = dt.utcnow()
            db.commit()
            
            access_token_expires = timedelta(minutes=30)
            access_token = create_access_token(
                data={"sub": user.username}, expires_delta=access_token_expires
            )
            return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during token login: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Token login failed: {str(e)}"
        )


@app.post("/auth/login")
async def login_user(login_data: UserLogin):
    """Login with email and password"""
    try:
        with get_db() as db:
            user = authenticate_user(db, login_data.email, login_data.password)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect email or password"
                )
            
            # Update last login
            from datetime import datetime as dt
            user.last_login = dt.utcnow()
            db.commit()
            
            access_token_expires = timedelta(minutes=30)
            access_token = create_access_token(
                data={"sub": user.username}, expires_delta=access_token_expires
            )
            return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during login: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )


@app.get("/auth/me")
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """Get current user information"""
    return {
        "user_id": current_user.user_id,
        "username": current_user.username,
        "email": current_user.email,
        "user_preferences": current_user.user_preferences,
        "token_balance": current_user.token_balance,
        "created_at": current_user.created_at.isoformat() if current_user.created_at else None,
        "last_login": current_user.last_login.isoformat() if current_user.last_login else None
    }


@app.post("/auth/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Change user password"""
    from backend.auth import verify_password
    
    # Verify current password
    if not verify_password(password_data.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password"
        )
    
    # Update password
    current_user.password_hash = get_password_hash(password_data.new_password)
    db.commit()
    
    return {"message": "Password updated successfully"}


@app.post("/auth/migrate-anonymous-data")
async def migrate_anonymous_data(
    migration_request: MigrateAnonymousDataRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Migrate anonymous pet data to authenticated user account"""
    try:
        session_id = migration_request.session_id
        
        with get_db() as db:
            
            # Find the anonymous pet by session_id
            from backend.database.models import PetState, PetInteraction
            anonymous_pet_state = db.query(PetState).filter(PetState.session_id == session_id).first()
            if not anonymous_pet_state:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Anonymous session not found"
                )
            
            # Check if user already has pets (optional - we could allow multiple pets)
            existing_pets = db.query(PetState).filter(PetState.owner_id == current_user.user_id).all()
            if existing_pets:
                logger.warning(f"User {current_user.user_id} already has pets, merging anonymous data")
            
            # Transfer ownership of the anonymous pet to the authenticated user
            anonymous_pet_state.owner_id = current_user.user_id
            anonymous_pet_state.session_id = None  # Clear session_id as it's now owned
            
            # Update interactions to reference the user instead of session
            session_user_id = f"session_{session_id}"
            interactions = db.query(PetInteraction).filter(PetInteraction.user_id == session_user_id).all()
            for interaction in interactions:
                interaction.user_id = current_user.user_id
            
            # Commit all changes
            db.commit()
            
            # Get the migrated pet data
            pet_agent = pet_model.get_pet_by_id(anonymous_pet_state.pet_id)
            if pet_agent:
                pet_data = {
                    "id": pet_agent.unique_id,
                    "name": pet_agent.name,
                    "owner_id": current_user.user_id,
                    "traits": pet_agent.personality_traits,
                    "mood": float(pet_agent.mood),
                    "energy": float(pet_agent.energy),
                    "health": float(pet_agent.health),
                    "attention": float(pet_agent.attention),
                    "needs": {
                        "hunger": float(pet_agent.hunger),
                        "thirst": float(pet_agent.thirst), 
                        "social": float(pet_agent.social_need),
                        "play": float(pet_agent.play_need),
                        "rest": float(pet_agent.rest_need)
                    },
                    "age": float(pet_agent.age),
                    "stage": pet_agent.life_stage,
                    "current_emoji_message": pet_agent.current_emoji_message,
                    "personality_summary": pet_agent.get_personality_summary()
                }
            else:
                # Fallback to database data if agent not found in model
                pet_data = anonymous_pet_state.to_dict()
                pet_data["owner_id"] = current_user.user_id
            
            logger.info(f"Successfully migrated anonymous session {session_id} to user {current_user.user_id}")
            
            return {
                "message": "Anonymous data migrated successfully",
                "pet": pet_data,
                "interactions_migrated": len(interactions) if interactions else 0
            }
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error migrating anonymous data: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Migration failed: {str(e)}"
        )


# Anonymous session endpoints (no authentication required)
@app.post("/api/anonymous/session/create")
async def create_anonymous_session():
    """Create a new anonymous session and assign a companion"""
    try:
        # Generate session ID
        session_id = str(uuid.uuid4())
        
        if not pet_model:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Pet model not initialized"
            )
        
        # Create a pet for this session
        pet = pet_model.create_pet_for_session(session_id=session_id)
        
        if not pet:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create pet for session"
            )
        
        return {
            "session_id": session_id,
            "pet": {
                "id": pet.unique_id,
                "name": pet.name if hasattr(pet, 'name') else f"Pet_{pet.unique_id[:8]}",
                "session_id": pet.session_id if hasattr(pet, 'session_id') else session_id,
                "attention": pet.attention_level,
                "health": pet.health,
                "mood": pet.mood,
                "energy": pet.energy,
                "age": pet.age,
                "stage": pet.development_stage,
                "traits": pet.traits,
                "needs": pet.needs,
                "position": pet.pos
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating anonymous session: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create anonymous session: {str(e)}"
        )


@app.get("/api/anonymous/pets/{session_id}")
async def get_anonymous_pet(session_id: str):
    """Get pet state for anonymous session"""
    if not pet_model:
        raise HTTPException(status_code=500, detail="Model not initialized")
    
    # Find pet by session_id
    pet = None
    for agent in pet_model.schedule.agents:
        if hasattr(agent, 'session_id') and agent.session_id == session_id:
            pet = agent
            break
    
    if not pet:
        raise HTTPException(status_code=404, detail=f"No pet found for session {session_id}")
    
    # Get consciousness information from semantic system
    consciousness_info = pet.get_consciousness_info()
    
    return {
        "id": pet.unique_id,
        "name": pet.name if hasattr(pet, 'name') else f"Pet_{pet.unique_id[:8]}",
        "session_id": pet.session_id if hasattr(pet, 'session_id') else session_id,
        "traits": pet.traits,
        "attention": pet.attention_level,
        "health": pet.health,
        "mood": pet.mood,
        "energy": pet.energy,
        "age": pet.age,
        "stage": pet.development_stage,
        "needs": pet.needs,
        "behavior_patterns": pet.behavior_patterns,
        "position": pet.pos,
        "current_emoji_message": getattr(pet, 'current_emoji_message', None),
        "personality_summary": getattr(pet, 'personality_summary', None),
        "consciousness": consciousness_info
    }


@app.post("/api/anonymous/pets/{session_id}/emoji")
async def anonymous_emoji_interact(session_id: str, interaction: AnonymousInteractionRequest):
    """Emoji interaction for anonymous users"""
    if not pet_model:
        raise HTTPException(status_code=500, detail="Model not initialized")
    
    # Find pet by session_id
    pet = None
    for agent in pet_model.schedule.agents:
        if hasattr(agent, 'session_id') and agent.session_id == session_id:
            pet = agent
            break
    
    if not pet:
        raise HTTPException(status_code=404, detail=f"No pet found for session {session_id}")
    
    if not interaction.emojis:
        raise HTTPException(status_code=400, detail="emojis field is required")
    
    try:
        # Create anonymous user context
        user_context = {
            "user_id": f"session_{session_id}",
            "intensity": 0.5,
            "user_emotional_state": "neutral"
        }
        
        # Process emoji interaction
        response_data = pet.interact_with_emoji(interaction.emojis, user_context)
        
        # Store interaction in Redis if available
        if redis_manager:
            await redis_manager.store_interaction(
                sender_id=f"session_{session_id}",
                receiver_id=pet.unique_id,
                message_type='emoji_communication',
                content={
                    'user_emojis': interaction.emojis,
                    'pet_response': response_data['pet_response'],
                    'timestamp': response_data['timestamp'],
                    'surprise_level': response_data['surprise_level']
                }
            )
        
        # Store interaction in database
        try:
            PetRepository.record_interaction(
                pet_id=pet.unique_id,
                interaction_type="emoji_communication",
                content={
                    'user_emojis': interaction.emojis,
                    'pet_response': response_data['pet_response'],
                    'surprise_level': response_data['surprise_level']
                },
                user_id=f"session_{session_id}",
                mood_impact=response_data.get('mood_change', 0),
                attention_impact=response_data.get('attention_change', 0)
            )
        except Exception as e:
            logger.warning(f"Failed to save anonymous interaction to database: {e}")
        
        # Save updated pet state
        try:
            saved_pet = PetRepository.save_pet_from_agent(pet)
            if saved_pet:
                logger.info(f"Anonymous pet state saved to database after emoji interaction")
        except Exception as e:
            logger.error(f"Error saving anonymous pet state: {e}")
        
        logger.info(f"Anonymous emoji interaction: {session_id} -> {pet.unique_id} | {interaction.emojis} -> {response_data['pet_response']}")
        
        return {
            'emoji_response': response_data['pet_response'],
            'surprise_level': response_data['surprise_level'],
            'response_confidence': response_data.get('response_confidence', 0.5),
            'timestamp': response_data['timestamp'],
            'user_insights': response_data.get('user_insights', {}),
            'pet_state': {
                'mood': pet.mood,
                'energy': pet.energy,
                'attention': pet.attention_level,
                'needs': pet.needs
            }
        }
        
    except Exception as e:
        logger.error(f"Error processing anonymous emoji interaction: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process emoji interaction: {str(e)}")


@app.post("/api/anonymous/pets/{session_id}/interact")
async def anonymous_general_interact(session_id: str, interaction: Dict[str, Any]):
    """General interaction for anonymous users"""
    if not pet_model:
        raise HTTPException(status_code=500, detail="Model not initialized")
    
    # Find pet by session_id  
    pet = None
    for agent in pet_model.schedule.agents:
        if hasattr(agent, 'session_id') and agent.session_id == session_id:
            pet = agent
            break
    
    if not pet:
        raise HTTPException(status_code=404, detail=f"No pet found for session {session_id}")
    
    interaction_type = interaction.get("type")
    content = interaction.get("content", {})
    
    if not interaction_type:
        raise HTTPException(status_code=400, detail="interaction type is required")
    
    try:
        # Add interaction to model queue using session as user_id
        success = pet_model.add_user_interaction(
            f"session_{session_id}", 
            pet.unique_id, 
            interaction_type, 
            content
        )
        
        if success:
            return {
                "message": f"Anonymous interaction {interaction_type} with {pet.unique_id} queued successfully",
                "pet_state": {
                    'mood': pet.mood,
                    'energy': pet.energy,
                    'attention': pet.attention_level,
                    'needs': pet.needs
                }
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to queue interaction")
            
    except Exception as e:
        logger.error(f"Error processing anonymous interaction: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process interaction: {str(e)}")


@app.get("/api/users/pets")
async def get_user_pets(current_user: User = Depends(get_current_active_user)):
    """Get pets belonging to the authenticated user"""
    try:
        pets = PetRepository.get_user_pets(current_user.user_id)
        pets_data = [pet.to_dict() for pet in pets]
        
        return {
            "message": f"Found {len(pets)} pets for user {current_user.username}",
            "count": len(pets),
            "pets": pets_data,
            "user_id": current_user.user_id
        }
    except Exception as e:
        logger.error(f"Error getting user pets: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user pets"
        )


@app.post("/api/pets/create")
async def create_pet_for_user(
    request: CreatePetRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Create a new pet for the authenticated user"""
    try:
        if not pet_model:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Pet model not initialized"
            )
        
        # Create the pet in the model
        pet = pet_model.create_pet_for_user(
            owner_id=current_user.user_id,
            pet_name=request.pet_name
        )
        
        if not pet:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create pet"
            )
        
        # Return pet data
        return {
            "message": "Pet created successfully",
            "pet": {
                "id": pet.unique_id,
                "name": pet.name,
                "owner_id": pet.owner_id,
                "attention": pet.attention_level,
                "health": pet.health,
                "mood": pet.mood,
                "energy": pet.energy,
                "age": pet.age,
                "stage": pet.development_stage,
                "traits": pet.traits,
                "needs": pet.needs,
                "position": pet.pos
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating pet: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create pet: {str(e)}"
        )


@app.put("/api/pets/{pet_id}/name")
async def update_pet_name(
    pet_id: str,
    request: UpdatePetNameRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Update a pet's name"""
    try:
        if not pet_model:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Pet model not initialized"
            )
        
        # Get the pet from the model
        pet = pet_model.get_pet_by_id(pet_id)
        if not pet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pet {pet_id} not found"
            )
        
        # Check if the current user owns this pet (if the pet has an owner)
        if hasattr(pet, 'owner_id') and pet.owner_id and pet.owner_id != current_user.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to modify this pet"
            )
        
        # Update the pet's name in memory
        old_name = pet.name if hasattr(pet, 'name') else f"Pet_{pet_id[:8]}"
        pet.name = request.new_name
        
        # Update the pet's name in the database
        updates = {"pet_name": request.new_name}
        updated_pet = PetRepository.update_pet(pet_id, updates)
        
        if not updated_pet:
            # Pet might not exist in database yet, try to save it
            saved_pet = PetRepository.save_pet_from_agent(pet)
            if not saved_pet:
                logger.warning(f"Failed to save pet {pet_id} to database after name update")
        
        logger.info(f"Pet {pet_id} name updated from '{old_name}' to '{request.new_name}' by user {current_user.user_id}")
        
        return {
            "message": "Pet name updated successfully",
            "pet_id": pet_id,
            "old_name": old_name,
            "new_name": request.new_name
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating pet name: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update pet name: {str(e)}"
        )


@app.get("/api/pets")
async def get_all_pets():
    """Get all pets in the system"""
    if not pet_model:
        return {"error": "Model not initialized"}
    
    pets_data = []
    for agent in pet_model.schedule.agents:
        pet_data = {
            "id": agent.unique_id,
            "name": agent.name if hasattr(agent, 'name') else f"Pet_{agent.unique_id[:8]}",
            "owner_id": agent.owner_id if hasattr(agent, 'owner_id') else None,
            "attention": agent.attention_level,
            "health": agent.health,
            "mood": agent.mood,
            "energy": agent.energy,
            "age": agent.age,
            "stage": agent.development_stage,
            "traits": agent.traits,
            "needs": agent.needs,
            "position": agent.pos
        }
        pets_data.append(pet_data)
    
    return {"pets": pets_data}


@app.get("/api/pets/{pet_id}")
async def get_pet(pet_id: str):
    """Get details for a specific pet"""
    if not pet_model:
        return {"error": "Model not initialized"}
    
    pet = pet_model.get_pet_by_id(pet_id)
    if not pet:
        return {"error": f"Pet {pet_id} not found"}
    
    # Collect detailed pet data
    pet_data = {
        "id": pet.unique_id,
        "name": pet.name if hasattr(pet, 'name') else f"Pet_{pet.unique_id[:8]}",
        "owner_id": pet.owner_id if hasattr(pet, 'owner_id') else None,
        "traits": pet.traits,
        "attention": pet.attention_level,
        "attention_history": pet.attention_history[-20:],
        "health": pet.health,
        "mood": pet.mood,
        "energy": pet.energy,
        "age": pet.age,
        "stage": pet.development_stage,
        "needs": pet.needs,
        "behavior_patterns": pet.behavior_patterns,
        "behavior_history": pet.behavior_history[-10:],
        "behavior_mutations": pet.behavior_mutations[-5:],
        "human_relationships": {k: v for k, v in pet.human_relationships.items() if abs(v) > 0.1},
        "pet_relationships": {k: v for k, v in pet.pet_relationships.items() if abs(v) > 0.1},
        "position": pet.pos,
        "interaction_count": pet.interaction_count,
        "lifetime_attention": pet.lifetime_attention,
        "current_region": pet.current_region_id
    }
    
    # Add boundary and cognitive data if available
    if hasattr(pet, "energy_system") and hasattr(pet.energy_system, "boundary_system"):
        boundary_system = pet.energy_system.boundary_system
        pet_data["boundary"] = {
            "permeability": boundary_system.boundary_permeability,
            "size": boundary_system.boundary_size,
            "status": boundary_system.get_status(),
            "assimilated_elements_count": len(boundary_system.assimilated_elements)
        }
        
        # Add info about assimilated elements
        assimilated_elements = []
        for elem_id, elem_data in boundary_system.assimilated_elements.items():
            assimilated_elements.append({
                "id": elem_id,
                "type": elem_data["type"],
                "assimilated_at": elem_data["assimilated_at"]
            })
        pet_data["assimilated_elements"] = assimilated_elements
    
    if hasattr(pet, "energy_system") and hasattr(pet.energy_system, "exchange_system"):
        exchange_system = pet.energy_system.exchange_system
        projections = []
        for proj_id, proj_data in exchange_system.external_projections.items():
            projections.append({
                "id": proj_id,
                "type": proj_data["type"],
                "region_id": proj_data["region_id"],
                "stability": proj_data["stability"],
                "created_at": proj_data["created_at"]
            })
        pet_data["projections"] = projections
    
    if hasattr(pet, "cognitive_system"):
        pet_data["cognitive"] = {
            "areas": pet.cognitive_system.cognitive_areas,
            "developmental_stage": pet.cognitive_system.developmental_stage,
            "recent_developments": pet.cognitive_system.recent_developments[-5:]
        }
    
    # Get consciousness information from semantic system
    consciousness_info = pet.get_consciousness_info()
    pet_data["consciousness"] = consciousness_info
    
    return pet_data


@app.post("/api/pets/interact")
async def interact_with_pet(
    interaction: Dict[str, Any],
    current_user: User = Depends(get_current_active_user)
):
    """Endpoint for user interactions with pets (requires authentication)"""
    if not pet_model:
        return {"error": "Model not initialized"}
    
    user_id = current_user.user_id  # Use authenticated user's ID
    pet_id = interaction.get("pet_id")
    interaction_type = interaction.get("type")  # feed, play, pet, train, check
    content = interaction.get("content", {})
    
    if not pet_id or not interaction_type:
        return {"error": "Missing required parameters"}
    
    # Check if pet exists
    pet = pet_model.get_pet_by_id(pet_id)
    if not pet:
        return {"error": f"Pet {pet_id} not found"}
    
    # Add interaction to model queue
    success = pet_model.add_user_interaction(user_id, pet_id, interaction_type, content)
    
    if success:
        return {"message": f"Interaction {interaction_type} with {pet_id} queued successfully"}
    else:
        return {"error": "Failed to queue interaction"}


@app.post("/api/pets/emoji")
async def emoji_interact_with_pet(
    interaction: Dict[str, Any],
    current_user: User = Depends(get_current_active_user)
):
    """Dedicated endpoint for emoji-based communication with pets"""
    if not pet_model:
        raise HTTPException(status_code=500, detail="Model not initialized")
    
    # Extract and validate parameters
    user_id = current_user.user_id  # Use authenticated user's ID
    pet_id = interaction.get("pet_id")
    emoji_message = interaction.get("emojis", "")
    
    if not pet_id:
        raise HTTPException(status_code=400, detail="pet_id is required")
    
    if not emoji_message:
        raise HTTPException(status_code=400, detail="emojis field is required")
    
    # Get the pet
    pet = pet_model.get_pet_by_id(pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail=f"Pet {pet_id} not found")
    
    try:
        # Create user context for enhanced user modeling
        user_context = {
            "user_id": user_id,
            "intensity": 0.5,  # Default intensity
            "user_emotional_state": "neutral"
        }
        
        # Process emoji interaction through enhanced user modeling system
        response_data = pet.interact_with_emoji(emoji_message, user_context)
        
        # Store interaction data in Redis for persistence
        if redis_manager:
            await redis_manager.store_interaction(
                sender_id=user_id,
                receiver_id=pet_id,
                message_type='emoji_communication',
                content={
                    'user_emojis': emoji_message,
                    'pet_response': response_data['pet_response'],
                    'timestamp': response_data['timestamp'],
                    'surprise_level': response_data['surprise_level']
                }
            )
        
        # Store interaction in database
        try:
            PetRepository.record_interaction(
                pet_id=pet_id,
                interaction_type="emoji_communication",
                content={
                    'user_emojis': emoji_message,
                    'pet_response': response_data['pet_response'],
                    'surprise_level': response_data['surprise_level']
                },
                user_id=user_id,
                mood_impact=response_data.get('mood_change', 0),
                attention_impact=response_data.get('attention_change', 0)
            )
        except Exception as e:
            logger.warning(f"Failed to save interaction to database: {e}")
        
        # Add to model's interaction tracking
        pet_model.add_user_interaction(user_id, pet_id, "emoji_communication", {
            'user_emojis': emoji_message,
            'pet_response': response_data['pet_response']
        })
        
        # Save updated pet state to database
        try:
            saved_pet = PetRepository.save_pet_from_agent(pet)
            if saved_pet:
                logger.info(f"Pet state saved to database after emoji interaction")
            else:
                logger.warning(f"Failed to save pet state to database")
        except Exception as e:
            logger.error(f"Error saving pet state to database: {e}")
        
        logger.info(f"Emoji interaction processed: {user_id} -> {pet_id} | {emoji_message} -> {response_data['pet_response']}")
        
        # Return response in the format expected by frontend
        return {
            'emoji_response': response_data['pet_response'],
            'surprise_level': response_data['surprise_level'],
            'response_confidence': response_data.get('response_confidence', 0.5),
            'timestamp': response_data['timestamp'],
            'user_insights': response_data.get('user_insights', {})
        }
        
    except Exception as e:
        logger.error(f"Error processing emoji interaction: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process emoji interaction: {str(e)}")


@app.get("/api/pets/{pet_id}/emoji-stats")
async def get_pet_emoji_stats(pet_id: str):
    """Get emoji communication statistics for a specific pet"""
    if not pet_model:
        raise HTTPException(status_code=500, detail="Model not initialized")
    
    pet = pet_model.get_pet_by_id(pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail=f"Pet {pet_id} not found")
    
    try:
        stats = pet.get_emoji_communication_stats()
        fep_emoji_stats = pet.fep_system.get_emoji_usage_stats()
        
        return {
            'pet_id': pet_id,
            'communication_stats': stats,
            'fep_learning_stats': fep_emoji_stats,
            'current_emoji_preferences': dict(pet.fep_system.emoji_preferences),
            'timestamp': time.time()
        }
        
    except Exception as e:
        logger.error(f"Error getting emoji stats for pet {pet_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get emoji stats: {str(e)}")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication with frontend"""
    global connected_clients, pet_model
    
    await websocket.accept()
    connected_clients.add(websocket)
    logger.info(f"WebSocket client connected. Total clients: {len(connected_clients)}")
    
    try:
        # Send initial connection confirmation
        await websocket.send_text(json.dumps({
            "type": "connection_established",
            "message": "Connected to DKS Digital Pet System",
            "timestamp": str(asyncio.get_event_loop().time())
        }))
        
        # Send initial pet data if available
        if pet_model:
            pets_data = []
            for agent in pet_model.schedule.agents:
                if hasattr(agent, 'unique_id'):
                    pet_data = {
                        "id": agent.unique_id,
                        "position": agent.pos,
                        "traits": agent.traits,
                        "attention": agent.attention_level,
                        "health": agent.health,
                        "mood": agent.mood,
                        "energy": agent.energy,
                        "stage": agent.development_stage,
                        "needs": agent.needs
                    }
                    pets_data.append(pet_data)
            
            await websocket.send_text(json.dumps({
                "type": "simulation_update",
                "pets": pets_data,
                "step": pet_model.schedule.steps,
                "timestamp": str(asyncio.get_event_loop().time())
            }))
        
        # Listen for messages from client
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                
                if message.get("type") == "ping":
                    # Respond to ping with pong
                    await websocket.send_text(json.dumps({
                        "type": "pong",
                        "timestamp": str(asyncio.get_event_loop().time())
                    }))
                
                elif message.get("type") == "get_pets":
                    # Send current pet data
                    if pet_model:
                        pets_data = []
                        for agent in pet_model.schedule.agents:
                            if hasattr(agent, 'unique_id'):
                                pet_data = {
                                    "id": agent.unique_id,
                                    "position": agent.pos,
                                    "traits": agent.traits,
                                    "attention": agent.attention_level,
                                    "health": agent.health,
                                    "mood": agent.mood,
                                    "energy": agent.energy,
                                    "stage": agent.development_stage,
                                    "needs": agent.needs
                                }
                                pets_data.append(pet_data)
                        
                        await websocket.send_text(json.dumps({
                            "type": "pets_data",
                            "pets": pets_data,
                            "timestamp": str(asyncio.get_event_loop().time())
                        }))
                
                elif message.get("type") == "interact_with_pet":
                    # Handle pet interaction
                    pet_id = message.get("pet_id")
                    interaction_type = message.get("interaction_type", "attention")
                    
                    if pet_model and pet_id:
                        pet = pet_model.get_pet_by_id(pet_id)
                        if pet:
                            # Simulate interaction based on type
                            if interaction_type == "attention":
                                pet.receive_attention(user_id="websocket_user", amount=10)
                            elif interaction_type == "play":
                                pet.needs["play"] = max(0, pet.needs["play"] - 20)
                            elif interaction_type == "feed":
                                pet.needs["hunger"] = max(0, pet.needs["hunger"] - 30)
                            
                            # Send updated pet data
                            await websocket.send_text(json.dumps({
                                "type": "pet_updated",
                                "pet_id": pet_id,
                                "pet_data": {
                                    "id": pet.unique_id,
                                    "attention": pet.attention_level,
                                    "health": pet.health,
                                    "mood": pet.mood,
                                    "energy": pet.energy,
                                    "needs": pet.needs
                                },
                                "timestamp": str(asyncio.get_event_loop().time())
                            }))
                
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON received from WebSocket client: {data}")
            except Exception as e:
                logger.error(f"Error processing WebSocket message: {e}")
    
    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        if websocket in connected_clients:
            connected_clients.remove(websocket)
        logger.info(f"WebSocket client removed. Total clients: {len(connected_clients)}")


async def broadcast_to_clients(message: dict):
    """Broadcast message to all connected WebSocket clients"""
    global connected_clients
    
    if not connected_clients:
        return
    
    message_str = json.dumps(message)
    disconnected_clients = set()
    
    for client in connected_clients:
        try:
            await client.send_text(message_str)
        except Exception as e:
            logger.error(f"Error sending to WebSocket client: {e}")
            disconnected_clients.add(client)
    
    # Remove disconnected clients
    connected_clients -= disconnected_clients


async def run_simulation():
    """Run the simulation loop"""
    if not pet_model:
        return
    
    pet_model.running = True
    logger.info("Starting simulation loop...")
    
    # Counter for periodic saves
    save_counter = 0
    save_interval = 100  # Save every 100 steps
    
    while pet_model.running:
        try:
            # Step the model
            pet_model.step()
            save_counter += 1
            
            # Periodically save pet states to database
            if save_counter >= save_interval:
                save_counter = 0
                try:
                    for agent in pet_model.schedule.agents:
                        if hasattr(agent, 'unique_id'):
                            PetRepository.save_pet_from_agent(agent)
                    logger.debug(f"Saved {len(pet_model.schedule.agents)} pets to database")
                except Exception as e:
                    logger.error(f"Failed to save pets to database: {e}")
            
            # Collect and broadcast data
            if data_collector:
                metrics = data_collector.get_current_metrics()
                network_data = pet_model.get_network_data()
                
                await broadcast_to_clients({
                    "type": "simulation_update",
                    "step": pet_model.schedule.steps,
                    "metrics": metrics,
                    "network": network_data,
                    "environment": pet_model.environment_state
                })
            
            # Small delay to prevent overwhelming the system
            await asyncio.sleep(0.1)
            
        except Exception as e:
            logger.error(f"Error in simulation loop: {e}")
            break
    
    # Save final states when simulation ends
    try:
        for agent in pet_model.schedule.agents:
            if hasattr(agent, 'unique_id'):
                PetRepository.save_pet_from_agent(agent)
        logger.info("Saved final pet states to database")
    except Exception as e:
        logger.error(f"Failed to save final pet states: {e}")
    
    logger.info("Simulation loop ended")


@app.get("/api/environment")
async def get_environment():
    """Get current environment state"""
    if not pet_model or not hasattr(pet_model, "environment"):
        return {"error": "Environment not initialized"}
    
    # Get basic environment state
    env_state = pet_model.environment.get_state()
    
    # Add summary of pet locations
    pet_locations = {}
    for region_id, region in env_state["regions"].items():
        if "current_pets" in region:
            pet_locations[region_id] = len(region["current_pets"])
    
    # Format response
    return {
        "time_of_day": env_state["time_of_day"],
        "day_of_week": env_state["day_of_week"],
        "day_count": env_state["day_count"],
        "weather": env_state["weather"],
        "weather_effects": env_state["weather_effects"],
        "ambient_energy": env_state["ambient_energy"],
        "social_atmosphere": env_state["social_atmosphere"],
        "novelty_level": env_state["novelty_level"],
        "emotional_tone": env_state["emotional_tone"],
        "regions": {
            k: {
                "name": v["name"], 
                "pet_count": len(v.get("current_pets", [])),
                "resources": v.get("resources", {})
            } for k, v in env_state["regions"].items()
        },
        "pet_locations": pet_locations,
        "resources": env_state["resources"],
        "active_events": env_state["active_events"]
    }


@app.get("/api/pets/{pet_id}/boundary")
async def get_pet_boundary(pet_id: str):
    """Get details about a pet's fluid boundary system"""
    if not pet_model:
        return {"error": "Model not initialized"}
    
    pet = pet_model.get_pet_by_id(pet_id)
    if not pet:
        return {"error": f"Pet {pet_id} not found"}
    
    if not hasattr(pet, "energy_system") or not hasattr(pet.energy_system, "boundary_system"):
        return {"error": "Pet doesn't have boundary system"}
    
    boundary = pet.energy_system.boundary_system
    
    return {
        "pet_id": pet_id,
        "permeability": boundary.boundary_permeability,
        "size": boundary.boundary_size,
        "stability": 1.0 - boundary.boundary_permeability,
        "maintenance_cost": boundary.boundary_maintenance_cost,
        "assimilated_elements": [
            {
                "id": elem_id,
                "type": elem["type"],
                "assimilated_at": elem["assimilated_at"]
            }
            for elem_id, elem in boundary.assimilated_elements.items()
        ],
        "history": boundary.boundary_history[-20:]
    }


@app.get("/api/pets/{pet_id}/cognition")
async def get_pet_cognition(pet_id: str):
    """Get cognitive development data for a specific pet"""
    if not pet_model:
        raise HTTPException(status_code=500, detail="Model not initialized")
    
    pet = pet_model.get_pet_by_id(pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail=f"Pet {pet_id} not found")
    
    try:
        if hasattr(pet, "cognitive_system"):
            return {
                'pet_id': pet_id,
                'cognitive_areas': pet.cognitive_system.cognitive_areas,
                'developmental_stage': pet.cognitive_system.developmental_stage,
                'recent_developments': pet.cognitive_system.recent_developments[-10:],
                'learning_rate': pet.cognitive_system.learning_rate,
                'timestamp': time.time()
            }
        else:
            return {
                'pet_id': pet_id,
                'error': 'Cognitive system not available for this pet',
                'timestamp': time.time()
            }
        
    except Exception as e:
        logger.error(f"Error getting cognition data for pet {pet_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get cognition data: {str(e)}")


@app.get("/api/pets/{pet_id}/user-profile/{user_id}")
async def get_user_profile(pet_id: str, user_id: str):
    """Get user profile and relationship data for a specific user-pet pair"""
    if not pet_model:
        raise HTTPException(status_code=500, detail="Model not initialized")
    
    pet = pet_model.get_pet_by_id(pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail=f"Pet {pet_id} not found")
    
    try:
        if hasattr(pet, 'user_modeling'):
            profile = pet.get_user_profile(user_id)
            return {
                'pet_id': pet_id,
                'user_id': user_id,
                'profile': profile,
                'timestamp': time.time()
            }
        else:
            return {
                'pet_id': pet_id,
                'user_id': user_id,
                'error': 'User modeling system not available',
                'timestamp': time.time()
            }
        
    except Exception as e:
        logger.error(f"Error getting user profile for pet {pet_id}, user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get user profile: {str(e)}")


@app.post("/api/pets/{pet_id}/predict-user-behavior")
async def predict_user_behavior(pet_id: str, request: Dict[str, Any]):
    """Predict user behavior based on learned patterns"""
    if not pet_model:
        raise HTTPException(status_code=500, detail="Model not initialized")
    
    pet = pet_model.get_pet_by_id(pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail=f"Pet {pet_id} not found")
    
    user_id = request.get("user_id")
    context = request.get("context", {})
    
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required")
    
    try:
        if hasattr(pet, 'user_modeling'):
            prediction = pet.predict_user_behavior(user_id, context)
            return {
                'pet_id': pet_id,
                'user_id': user_id,
                'prediction': prediction,
                'context': context,
                'timestamp': time.time()
            }
        else:
            return {
                'pet_id': pet_id,
                'user_id': user_id,
                'error': 'User modeling system not available',
                'timestamp': time.time()
            }
        
    except Exception as e:
        logger.error(f"Error predicting user behavior for pet {pet_id}, user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to predict user behavior: {str(e)}")


@app.get("/api/pets/{pet_id}/adaptation-recommendations/{user_id}")
async def get_adaptation_recommendations(pet_id: str, user_id: str):
    """Get recommendations for how the pet should adapt to a specific user"""
    if not pet_model:
        raise HTTPException(status_code=500, detail="Model not initialized")
    
    pet = pet_model.get_pet_by_id(pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail=f"Pet {pet_id} not found")
    
    try:
        if hasattr(pet, 'user_modeling'):
            recommendations = pet.get_adaptation_recommendations(user_id)
            return {
                'pet_id': pet_id,
                'user_id': user_id,
                'recommendations': recommendations,
                'timestamp': time.time()
            }
        else:
            return {
                'pet_id': pet_id,
                'user_id': user_id,
                'error': 'User modeling system not available',
                'timestamp': time.time()
            }
        
    except Exception as e:
        logger.error(f"Error getting adaptation recommendations for pet {pet_id}, user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get adaptation recommendations: {str(e)}")


@app.get("/api/pets/{pet_id}/relationship-insights/{user_id}")
async def get_relationship_insights(pet_id: str, user_id: str):
    """Get detailed relationship insights between pet and user"""
    if not pet_model:
        raise HTTPException(status_code=500, detail="Model not initialized")
    
    pet = pet_model.get_pet_by_id(pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail=f"Pet {pet_id} not found")
    
    try:
        if hasattr(pet, 'user_modeling'):
            profile = pet.get_user_profile(user_id)
            
            # Extract relationship insights
            relationship_insights = {
                'pet_id': pet_id,
                'user_id': user_id,
                'personality': profile.get('personality', {}),
                'relationship': profile.get('relationship', {}),
                'memory': profile.get('memory', {}),
                'insights': profile.get('insights', {}),
                'timestamp': time.time()
            }
            
            return relationship_insights
        else:
            return {
                'pet_id': pet_id,
                'user_id': user_id,
                'error': 'User modeling system not available',
                'timestamp': time.time()
            }
        
    except Exception as e:
        logger.error(f"Error getting relationship insights for pet {pet_id}, user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get relationship insights: {str(e)}")


# Memory endpoints for consciousness visualizations
@app.get("/api/pets/{pet_id}/memories")
async def get_pet_memories(pet_id: str, limit: int = 20):
    """Get semantic memories for consciousness visualization"""
    if not pet_model:
        raise HTTPException(status_code=500, detail="Model not initialized")
    
    pet = pet_model.get_pet_by_id(pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail=f"Pet {pet_id} not found")
    
    try:
        memories = []
        if hasattr(pet, 'semantic_system') and pet.semantic_system:
            raw_memories = pet.semantic_system._get_recent_semantic_memories(limit=limit)
            
            for i, mem_data in enumerate(raw_memories):
                memory = {
                    'id': f"mem_{i}_{int(time.time())}",
                    'timestamp': mem_data.get('timestamp', time.time() * 1000),
                    'interaction_type': mem_data.get('type', 'unknown'),
                    'content': mem_data.get('content', ''),
                    'semantic_tags': mem_data.get('semantic_tags', []),
                    'emotional_context': {
                        'valence': mem_data.get('emotional_context', {}).get('valence', 0),
                        'arousal': mem_data.get('emotional_context', {}).get('arousal', 0),
                        'dominance': mem_data.get('emotional_context', {}).get('dominance', 0)
                    },
                    'significance': mem_data.get('significance_score', 0.5),
                    'associations': mem_data.get('associations', []),
                    'cluster_id': mem_data.get('cluster_id')
                }
                memories.append(memory)
        
        return {
            'pet_id': pet_id,
            'memories': memories,
            'total_count': len(memories),
            'timestamp': time.time()
        }
        
    except Exception as e:
        logger.error(f"Error getting memories for pet {pet_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get memories: {str(e)}")


@app.get("/api/anonymous/pets/{session_id}/memories")
async def get_anonymous_pet_memories(session_id: str, limit: int = 20):
    """Get semantic memories for anonymous pets"""
    try:
        if not pet_model:
            raise HTTPException(status_code=500, detail="Model not initialized")
        
        # Find pet by session_id
        pet = None
        for agent in pet_model.schedule.agents:
            if hasattr(agent, 'session_id') and agent.session_id == session_id:
                pet = agent
                break
        
        if not pet:
            return {
                'session_id': session_id,
                'memories': [],
                'total_count': 0,
                'timestamp': time.time()
            }
        
        memories = []
        if hasattr(pet, 'semantic_system') and pet.semantic_system:
            raw_memories = pet.semantic_system._get_recent_semantic_memories(limit=limit)
            
            for i, mem_data in enumerate(raw_memories):
                memory = {
                    'id': f"anon_mem_{i}_{int(time.time())}",
                    'timestamp': mem_data.get('timestamp', time.time() * 1000),
                    'interaction_type': mem_data.get('type', 'unknown'),
                    'content': mem_data.get('content', ''),
                    'semantic_tags': mem_data.get('semantic_tags', []),
                    'emotional_context': {
                        'valence': mem_data.get('emotional_context', {}).get('valence', 0),
                        'arousal': mem_data.get('emotional_context', {}).get('arousal', 0),
                        'dominance': mem_data.get('emotional_context', {}).get('dominance', 0)
                    },
                    'significance': mem_data.get('significance_score', 0.5),
                    'associations': mem_data.get('associations', []),
                    'cluster_id': mem_data.get('cluster_id')
                }
                memories.append(memory)
        
        return {
            'session_id': session_id,
            'memories': memories,
            'total_count': len(memories),
            'timestamp': time.time()
        }
        
    except Exception as e:
        logger.error(f"Error getting memories for anonymous pet {session_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get memories: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
