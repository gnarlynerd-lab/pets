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

from backend.models.pet_model import PetModel
from backend.communication.redis_manager import RedisManager
from backend.visualization.data_collector import DataCollector

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app for web API and WebSocket connections
app = FastAPI(title="DKS Agent System", version="1.0.0")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
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


@app.get("/api/pets")
async def get_all_pets():
    """Get all pets in the system"""
    if not pet_model:
        return {"error": "Model not initialized"}
    
    pets_data = []
    for agent in pet_model.schedule.agents:
        pet_data = {
            "id": agent.unique_id,
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
    
    return pet_data


@app.post("/api/pets/interact")
async def interact_with_pet(interaction: Dict[str, Any]):
    """Endpoint for user interactions with pets"""
    if not pet_model:
        return {"error": "Model not initialized"}
    
    user_id = interaction.get("user_id", f"user_{uuid.uuid4().hex[:8]}")
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
async def emoji_interact_with_pet(interaction: Dict[str, Any]):
    """Dedicated endpoint for emoji-based communication with pets"""
    if not pet_model:
        raise HTTPException(status_code=500, detail="Model not initialized")
    
    # Extract and validate parameters
    user_id = interaction.get("user_id", f"user_{uuid.uuid4().hex[:8]}")
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
        # Process emoji interaction directly through the pet
        response_data = pet.receive_emoji_message(emoji_message, user_id)
        
        # Store interaction data in Redis for persistence
        if redis_manager:
            await redis_manager.store_interaction(
                sender_id=user_id,
                receiver_id=pet_id,
                message_type='emoji_communication',
                content={
                    'user_emojis': emoji_message,
                    'pet_response': response_data['emoji_response'],
                    'timestamp': response_data['timestamp'],
                    'surprise_level': response_data['surprise_level']
                }
            )
        
        # Add to model's interaction tracking
        pet_model.add_user_interaction(user_id, pet_id, "emoji_communication", {
            'user_emojis': emoji_message,
            'pet_response': response_data['emoji_response']
        })
        
        logger.info(f"Emoji interaction processed: {user_id} -> {pet_id} | {emoji_message} -> {response_data['emoji_response']}")
        
        return response_data
        
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
    
    while pet_model.running:
        try:
            # Step the model
            pet_model.step()
            
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
    """Get details about a pet's cognitive development"""
    if not pet_model:
        return {"error": "Model not initialized"}
    
    pet = pet_model.get_pet_by_id(pet_id)
    if not pet:
        return {"error": f"Pet {pet_id} not found"}
    
    if not hasattr(pet, "cognitive_system"):
        return {"error": "Pet doesn't have cognitive system"}
    
    cognitive = pet.cognitive_system
    
    return {
        "pet_id": pet_id,
        "cognitive_areas": cognitive.cognitive_areas,
        "developmental_stage": cognitive.developmental_stage,
        "avg_cognitive_level": sum(cognitive.cognitive_areas.values()) / len(cognitive.cognitive_areas),
        "recent_developments": cognitive.recent_developments
    }
