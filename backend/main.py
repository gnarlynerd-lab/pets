"""
DKS Digital Pet System Main Application Entry Point
"""
import asyncio
import logging
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


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await websocket.accept()
    connected_clients.add(websocket)
    
    try:
        while True:
            # Keep connection alive and handle any client messages
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "ping":
                await websocket.send_text(json.dumps({"type": "pong"}))
            elif message.get("type") == "interact":
                # Handle interaction requests via websocket
                user_id = message.get("user_id", f"user_{uuid.uuid4().hex[:8]}")
                pet_id = message.get("pet_id")
                interaction_type = message.get("interaction_type")
                content = message.get("content", {})
                
                if pet_id and interaction_type and pet_model:
                    pet_model.add_user_interaction(user_id, pet_id, interaction_type, content)
                    await websocket.send_text(json.dumps({
                        "type": "interaction_response",
                        "status": "success",
                        "request_id": message.get("request_id")
                    }))
                else:
                    await websocket.send_text(json.dumps({
                        "type": "interaction_response",
                        "status": "error",
                        "message": "Invalid interaction request",
                        "request_id": message.get("request_id")
                    }))
                
    except WebSocketDisconnect:
        connected_clients.remove(websocket)


@app.websocket("/ws/environment")
async def environment_websocket(websocket: WebSocket):
    """WebSocket endpoint for real-time environment updates"""
    await websocket.accept()
    
    try:
        # Send initial environment state
        if pet_model and hasattr(pet_model, "environment"):
            env_state = pet_model.environment.get_state()
            await websocket.send_text(json.dumps({
                "type": "environment_update",
                "data": {
                    "time_of_day": env_state["time_of_day"],
                    "day_of_week": env_state["day_of_week"],
                    "weather": env_state["weather"],
                    "ambient_energy": env_state["ambient_energy"],
                    "social_atmosphere": env_state["social_atmosphere"],
                    "novelty_level": env_state["novelty_level"]
                }
            }))
        
        while True:
            # Wait for client to request updates
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "get_environment":
                if pet_model and hasattr(pet_model, "environment"):
                    env_state = pet_model.environment.get_state()
                    await websocket.send_text(json.dumps({
                        "type": "environment_update",
                        "data": {
                            "time_of_day": env_state["time_of_day"],
                            "day_of_week": env_state["day_of_week"],
                            "weather": env_state["weather"],
                            "ambient_energy": env_state["ambient_energy"],
                            "social_atmosphere": env_state["social_atmosphere"],
                            "novelty_level": env_state["novelty_level"],
                            "regions": {
                                k: {
                                    "name": v["name"], 
                                    "pet_count": len(v.get("current_pets", [])),
                                    "resources": v.get("resources", {})
                                } for k, v in env_state["regions"].items()
                            },
                            "active_events": env_state["active_events"]
                        }
                    }))
            elif message.get("type") == "add_event":
                # Allow clients to trigger events in the environment
                event_type = message.get("event_type")
                duration = message.get("duration", 10)
                params = message.get("params", {})
                
                if event_type and pet_model and hasattr(pet_model, "environment"):
                    result = pet_model.environment.add_event(event_type, duration, **params)
                    await websocket.send_text(json.dumps({
                        "type": "event_response",
                        "status": "success" if result.get("success") else "error",
                        "event_id": result.get("event_id"),
                        "request_id": message.get("request_id")
                    }))
    
    except WebSocketDisconnect:
        # Client disconnected
        pass


async def broadcast_to_clients(data: dict):
    """Broadcast data to all connected WebSocket clients"""
    if not connected_clients:
        return
    
    message = json.dumps(data)
    disconnected = set()
    
    for client in connected_clients:
        try:
            await client.send_text(message)
        except:
            disconnected.add(client)
    
    # Remove disconnected clients
    connected_clients -= disconnected


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
