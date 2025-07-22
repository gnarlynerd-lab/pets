"""
Pet Model - Main simulation environment for Digital Pet DKS system
"""
from mesa import Model
from mesa.time import RandomActivation
import mesa.space
import numpy as np
import random
import uuid
import time
import logging
from typing import Dict, List, Any, Optional
from collections import defaultdict

from backend.agents.digital_pet import DigitalPet
from backend.agents.pet_environment import PetEnvironment

logger = logging.getLogger(__name__)


class PetModel(Model):
    """
    Digital Pet model implementing DKS principles:
    - No centralized optimization
    - Pets self-organize through local interactions
    - Emergent behaviors develop from simple rules
    - System maintains dynamic stability through continuous activity
    
    This model simulates a virtual environment where digital pets live,
    evolve, and interact with users and other pets. The environment itself
    is an active component with fluid boundaries between pets and their
    surroundings.
    """
    
    def __init__(self, num_pets: int = 5, redis_manager=None, data_collector=None):
        super().__init__()
        
        # Initialize random number generator for Mesa framework
        self.random = random.Random()
        
        # Model parameters
        self.num_pets = num_pets
        
        # External managers
        self.redis_manager = redis_manager
        self.data_collector = data_collector
        
        # Model state
        self.running = False
        self.message_queue = []  # For inter-pet communication
        self.current_run_id = str(uuid.uuid4())
        
        # Create the environment
        self.environment = PetEnvironment()
        
        # Legacy environment state (for backwards compatibility)
        self.environment_state = {
            "time_of_day": self.environment.time_of_day,
            "day_of_week": self.environment.day_of_week,
            "ambient_energy": self.environment.ambient_energy,
            "social_atmosphere": self.environment.social_atmosphere,
            "novelty_level": self.environment.novelty_level
        }
        
        # User interaction tracking
        self.active_users = set()
        self.user_presence = defaultdict(float)  # User ID -> presence level (0-1)
        self.user_interaction_history = defaultdict(list)  # User ID -> list of interactions
        
        # Set up Mesa components
        self.grid = mesa.space.MultiGrid(20, 20, True)  # Smaller grid for pets
        self.schedule = RandomActivation(self)
        
        # Create pet agents
        self.create_pets()
        
        # Set up data collection
        self.setup_data_collection()
        
        logger.info(f"Pet model initialized with {len(self.schedule.agents)} pet agents")
    
    def create_pets(self):
        """Create pet agents"""
        for i in range(self.num_pets):
            # Create a unique ID for the pet
            pet_id = f"pet_{i}_{uuid.uuid4().hex[:8]}"
            
            # Create the pet with random initial traits
            pet = DigitalPet(
                unique_id=pet_id,
                model=self
            )
            self.schedule.add(pet)
            
            # Place on grid in random location
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(pet, (x, y))
            
            logger.debug(f"Created pet {pet_id} at position ({x}, {y})")
    
    def create_pet_for_user(self, owner_id: str, pet_name: str = None) -> Optional[DigitalPet]:
        """Create a new pet for a specific user"""
        try:
            # Create a unique ID for the pet
            pet_id = f"pet_{owner_id}_{uuid.uuid4().hex[:8]}"
            
            # Create the pet
            pet = DigitalPet(
                unique_id=pet_id,
                model=self,
                owner_id=owner_id,
                name=pet_name or f"Pet_{uuid.uuid4().hex[:4]}"
            )
            self.schedule.add(pet)
            
            # Place on grid in random location
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(pet, (x, y))
            
            logger.info(f"Created pet {pet_id} for user {owner_id} at position ({x}, {y})")
            
            # Save to database
            from backend.database import PetRepository
            pet_data = {
                "pet_id": pet.unique_id,
                "owner_id": owner_id,
                "pet_name": pet.name,
                "traits": pet.traits,
                "trait_connections": {str(k): v for k, v in pet.trait_connections.items()},
                "vital_stats": {
                    "health": pet.health,
                    "energy": pet.energy,
                    "mood": pet.mood
                },
                "needs": pet.needs,
                "memory": pet.episodic_memory if hasattr(pet, 'episodic_memory') else [],
                "behavior_patterns": pet.behavior_patterns if hasattr(pet, 'behavior_patterns') else {},
                "attention_level": pet.attention_level,
                "development_stage": pet.development_stage,
                "age": pet.age,
                "position_x": x,
                "position_y": y
            }
            PetRepository.create_pet(pet_data)
            
            return pet
            
        except Exception as e:
            logger.error(f"Error creating pet for user {owner_id}: {e}")
            return None
    
    def create_pet_for_session(self, session_id: str, pet_name: str = None) -> Optional[DigitalPet]:
        """Create a new pet for an anonymous session"""
        try:
            # Create a unique ID for the pet
            pet_id = f"pet_session_{session_id[:8]}_{uuid.uuid4().hex[:8]}"
            
            # Create the pet
            pet = DigitalPet(
                unique_id=pet_id,
                model=self,
                session_id=session_id,
                name=pet_name or f"Companion_{uuid.uuid4().hex[:4]}"
            )
            self.schedule.add(pet)
            
            # Place on grid in random location
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(pet, (x, y))
            
            logger.info(f"Created pet {pet_id} for session {session_id} at position ({x}, {y})")
            
            # Save to database
            from backend.database import PetRepository
            pet_data = {
                "pet_id": pet.unique_id,
                "session_id": session_id,
                "pet_name": pet.name,
                "traits": pet.traits,
                "trait_connections": {str(k): v for k, v in pet.trait_connections.items()},
                "vital_stats": {
                    "health": pet.health,
                    "energy": pet.energy,
                    "mood": pet.mood
                },
                "needs": pet.needs,
                "memory": pet.episodic_memory if hasattr(pet, 'episodic_memory') else [],
                "behavior_patterns": pet.behavior_patterns if hasattr(pet, 'behavior_patterns') else {},
                "attention_level": pet.attention_level,
                "development_stage": pet.development_stage,
                "age": pet.age,
                "position_x": x,
                "position_y": y
            }
            PetRepository.create_pet(pet_data)
            
            return pet
            
        except Exception as e:
            logger.error(f"Error creating pet for session {session_id}: {e}")
            return None
    
    def setup_data_collection(self):
        """Set up data collection for analysis and visualization"""
        if self.data_collector:
            # Define what data to collect from each pet
            model_reporters = {
                "Pet Count": lambda m: len(m.schedule.agents),
                "Average Attention": self.get_average_attention,
                "Average Health": self.get_average_health,
                "Average Mood": self.get_average_mood,
                "Average Boundary Permeability": self.get_average_boundary_permeability,
                "Average Cognitive Level": self.get_average_cognitive_level,
                "Active Users": lambda m: len(m.active_users),
                "Time of Day": lambda m: m.environment_state["time_of_day"],
                "Ambient Energy": lambda m: m.environment_state["ambient_energy"],
                "Weather": lambda m: m.environment_state.get("weather", "unknown"),
            }
            
            agent_reporters = {
                "Attention": lambda a: a.attention_level if hasattr(a, "attention_level") else 0,
                "Health": lambda a: a.health if hasattr(a, "health") else 0,
                "Mood": lambda a: a.mood if hasattr(a, "mood") else 0,
                "Energy": lambda a: a.energy if hasattr(a, "energy") else 0,
                "Age": lambda a: a.age if hasattr(a, "age") else 0,
                "Development Stage": lambda a: a.development_stage if hasattr(a, "development_stage") else "",
                "Traits": lambda a: a.traits if hasattr(a, "traits") else {},
                "Boundary Permeability": lambda a: a.energy_system.boundary_system.boundary_permeability if hasattr(a, "energy_system") else 0,
                "Boundary Size": lambda a: a.energy_system.boundary_system.boundary_size if hasattr(a, "energy_system") else 0,
                "Cognitive Stage": lambda a: a.cognitive_system.developmental_stage if hasattr(a, "cognitive_system") else "",
                "Assimilated Elements": lambda a: len(a.energy_system.boundary_system.assimilated_elements) if hasattr(a, "energy_system") else 0,
            }
            
            # Initialize data collection
            self.datacollector = mesa.DataCollector(
                model_reporters=model_reporters,
                agent_reporters=agent_reporters
            )
    
    def step(self):
        """Execute one step of the model"""
        try:
            # Step the environment first
            environment_state = self.environment.step()
            
            # Update legacy environment state
            self.environment_state = {
                "time_of_day": environment_state["time_of_day"],
                "day_of_week": environment_state["day_of_week"],
                "ambient_energy": environment_state["ambient_energy"],
                "social_atmosphere": environment_state["social_atmosphere"],
                "novelty_level": environment_state["novelty_level"],
                "weather": environment_state["weather"],
                "resources": environment_state["resources"]
            }
            
            # Process any external messages from Redis
            self.process_external_messages()
            
            # Update user presence (decay over time)
            self.update_user_presence()
            
            # Have pets interact with each other
            self.facilitate_pet_interactions()
            
            # Execute all agent steps
            self.schedule.step()
            
            # Collect data for visualization and analysis
            if self.data_collector:
                self.data_collector.collect_step_data(self)
            if hasattr(self, "datacollector"):
                self.datacollector.collect(self)
            
            # Update model metrics
            self.calculate_model_metrics()
            
            logger.debug(f"Completed model step {self.schedule.steps}")
        
        except Exception as e:
            logger.error(f"Error in model step: {e}")
    
    def update_environment(self):
        """
        Legacy method for updating environment state
        Now handled by the PetEnvironment class
        """
        # This method is kept for backward compatibility
        # Now the environment is updated in the step method by calling environment.step()
        pass
            
        # Novelty decays but occasionally spikes
        self.environment_state["novelty_level"] *= 0.995  # Slow decay
        if self.random.random() < 0.01:  # 1% chance of novelty spike
            self.environment_state["novelty_level"] = min(1.0, self.environment_state["novelty_level"] + 0.3)
    
    def process_external_messages(self):
        """Process messages from external sources (e.g., user interactions)"""
        # This would typically pull from Redis in a real implementation
        if self.redis_manager:
            # In async context, this would be awaited
            pass  # Placeholder for actual implementation
            
        # Process any messages in the queue
        for message in self.message_queue:
            try:
                msg_type = message.get("type")
                sender_id = message.get("sender")
                recipient_id = message.get("recipient")
                content = message.get("content", {})
                
                # Handle user interaction messages
                if msg_type == "user_interaction":
                    self.handle_user_interaction(sender_id, recipient_id, content)
                    
                # Update user presence
                if sender_id and sender_id.startswith("user_"):
                    self.active_users.add(sender_id)
                    self.user_presence[sender_id] = min(1.0, self.user_presence.get(sender_id, 0) + 0.1)
                
            except Exception as e:
                logger.error(f"Error processing external message: {e}")
        
        # Clear processed messages
        self.message_queue = []
    
    def handle_user_interaction(self, user_id: str, pet_id: str, content: Dict[str, Any]):
        """Process user interaction with a pet"""
        # Find the target pet
        target_pet = None
        for agent in self.schedule.agents:
            if agent.unique_id == pet_id:
                target_pet = agent
                break
        
        if not target_pet:
            logger.warning(f"Pet {pet_id} not found for interaction from {user_id}")
            return
        
        # Add the message to the pet's queue
        interaction_type = content.get("interaction_type", "check")
        target_pet.message_queue.append({
            "type": interaction_type,
            "sender": user_id,
            "content": content
        })
        
        # Record the interaction for analytics
        self.user_interaction_history[user_id].append({
            "timestamp": time.time(),
            "pet_id": pet_id,
            "interaction_type": interaction_type,
            "content": content
        })
        
        # Keep history manageable
        if len(self.user_interaction_history[user_id]) > 100:
            self.user_interaction_history[user_id] = self.user_interaction_history[user_id][-100:]
    
    def update_user_presence(self):
        """Update user presence levels (decay over time)"""
        for user_id in list(self.user_presence.keys()):
            # Decay presence by 1% each step
            self.user_presence[user_id] *= 0.99
            
            # Remove users with very low presence
            if self.user_presence[user_id] < 0.01:
                self.active_users.discard(user_id)
                del self.user_presence[user_id]
    
    def facilitate_pet_interactions(self):
        """Facilitate interactions between pets"""
        # This is a simplified approach - in a full implementation,
        # we'd use more sophisticated proximity and compatibility rules
        
        # For each pet, find potential interaction partners
        for pet in self.schedule.agents:
            # Skip if low energy
            if pet.energy < 20:
                continue
                
            # Get all pets in the same grid cell or adjacent cells
            x, y = self.grid.get_cell_list_contents([pet.pos])[0].pos
            neighbors = []
            
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue  # Skip self
                    
                    neighbor_pos = ((x + dx) % self.grid.width, (y + dy) % self.grid.height)
                    neighbors.extend(self.grid.get_cell_list_contents([neighbor_pos]))
            
            # Filter to only get other pets
            other_pets = [agent for agent in neighbors 
                         if isinstance(agent, DigitalPet) and agent.unique_id != pet.unique_id]
            
            # Randomly choose one pet to interact with (if any)
            if other_pets and self.random.random() < 0.3:  # 30% chance of interaction
                other_pet = self.random.choice(other_pets)
                
                # Calculate compatibility based on traits
                compatibility = self.calculate_pet_compatibility(pet, other_pet)
                
                # Create interaction content
                interaction_content = {
                    "interaction_type": "meet", 
                    "compatibility": compatibility,
                    "initiator_traits": {k: v for k, v in pet.traits.items() if self.random.random() < 0.3}
                }
                
                # Send message to other pet
                other_pet.message_queue.append({
                    "type": "pet_interaction",
                    "sender": pet.unique_id,
                    "content": interaction_content
                })
                
                # Also initiate a move to simulate pets moving together or apart
                if self.random.random() < 0.5:
                    self.move_pet_towards(pet, other_pet)
                else:
                    self.move_pet_randomly(pet)
            
            # Occasionally move randomly
            elif self.random.random() < 0.2:  # 20% chance to move randomly
                self.move_pet_randomly(pet)
    
    def calculate_pet_compatibility(self, pet1, pet2):
        """Calculate compatibility between two pets based on traits"""
        compatibility = 0.5  # Default neutral compatibility
        
        # Compare key traits
        key_traits = ["openness", "extraversion", "agreeableness"]
        trait_matches = 0
        trait_differences = 0
        
        for trait in key_traits:
            if trait in pet1.traits and trait in pet2.traits:
                difference = abs(pet1.traits[trait] - pet2.traits[trait])
                
                # Similar traits (within 0.2) increase compatibility
                if difference < 0.2:
                    trait_matches += 1
                # Very different traits (over 0.5) decrease compatibility
                elif difference > 0.5:
                    trait_differences += 1
        
        # Adjust compatibility based on matches and differences
        compatibility += trait_matches * 0.1
        compatibility -= trait_differences * 0.1
        
        # Consider existing relationship
        existing_relationship = pet1.pet_relationships.get(pet2.unique_id, 0)
        compatibility += existing_relationship * 0.05
        
        # Add some randomness
        compatibility += (self.random.random() * 0.2) - 0.1
        
        # Ensure in valid range
        return max(0.0, min(1.0, compatibility))
    
    def move_pet_towards(self, pet, target_pet):
        """Move pet towards another pet"""
        # Get current positions
        x1, y1 = pet.pos
        x2, y2 = target_pet.pos
        
        # Calculate direction
        dx = (x2 - x1 + self.grid.width // 2) % self.grid.width - self.grid.width // 2
        dy = (y2 - y1 + self.grid.height // 2) % self.grid.height - self.grid.height // 2
        
        # Move one step in the direction of the other pet
        new_x = (x1 + (1 if dx > 0 else -1 if dx < 0 else 0)) % self.grid.width
        new_y = (y1 + (1 if dy > 0 else -1 if dy < 0 else 0)) % self.grid.height
        
        # Move the pet
        self.grid.move_agent(pet, (new_x, new_y))
    
    def move_pet_randomly(self, pet):
        """Move pet to a random adjacent cell"""
        # Get current position
        x, y = pet.pos
        
        # Choose a random direction
        dx = self.random.randint(-1, 1)
        dy = self.random.randint(-1, 1)
        
        # Calculate new position (wrapping around grid edges)
        new_x = (x + dx) % self.grid.width
        new_y = (y + dy) % self.grid.height
        
        # Move the pet
        self.grid.move_agent(pet, (new_x, new_y))
    
    def calculate_model_metrics(self):
        """Calculate overall model metrics"""
        # These metrics would be used for system monitoring and analysis
        pass
    
    def get_average_attention(self):
        """Get average attention level across all pets"""
        if not self.schedule.agents:
            return 0
            
        total_attention = sum(agent.attention_level for agent in self.schedule.agents 
                              if hasattr(agent, "attention_level"))
        return total_attention / len(self.schedule.agents)
    
    def get_average_health(self):
        """Get average health across all pets"""
        if not self.schedule.agents:
            return 0
            
        total_health = sum(agent.health for agent in self.schedule.agents 
                           if hasattr(agent, "health"))
        return total_health / len(self.schedule.agents)
    
    def get_average_mood(self):
        """Get average mood across all pets"""
        if not self.schedule.agents:
            return 0
            
        total_mood = sum(agent.mood for agent in self.schedule.agents 
                         if hasattr(agent, "mood"))
        return total_mood / len(self.schedule.agents)
    
    def get_average_boundary_permeability(self):
        """Get the average boundary permeability of all pets"""
        permeabilities = []
        for agent in self.schedule.agents:
            if hasattr(agent, "energy_system") and hasattr(agent.energy_system, "boundary_system"):
                permeabilities.append(agent.energy_system.boundary_system.boundary_permeability)
        
        if permeabilities:
            return sum(permeabilities) / len(permeabilities)
        return 0.5  # Default if no pets with boundaries
    
    def get_average_cognitive_level(self):
        """Get the average cognitive level of all pets"""
        levels = []
        for agent in self.schedule.agents:
            if hasattr(agent, "cognitive_system") and hasattr(agent.cognitive_system, "cognitive_areas"):
                pet_avg = sum(agent.cognitive_system.cognitive_areas.values()) / len(agent.cognitive_system.cognitive_areas)
                levels.append(pet_avg)
        
        if levels:
            return sum(levels) / len(levels)
        return 0.1  # Default if no pets with cognitive systems
    
    def get_pet_by_id(self, pet_id):
        """Get a pet by ID"""
        for agent in self.schedule.agents:
            if agent.unique_id == pet_id:
                return agent
        return None
    
    def add_user_interaction(self, user_id, pet_id, interaction_type, content=None):
        """Add a user interaction to the model queue"""
        if content is None:
            content = {}
            
        # Add the interaction type to the content
        content["interaction_type"] = interaction_type
        
        # Create the message
        message = {
            "type": "user_interaction",
            "sender": user_id,
            "recipient": pet_id,
            "content": content
        }
        
        # Add to queue
        self.message_queue.append(message)
        
        # Register user as active
        self.active_users.add(user_id)
        self.user_presence[user_id] = min(1.0, self.user_presence.get(user_id, 0) + 0.1)
        
        return True
    
    def get_network_data(self):
        """Get network data for visualization"""
        nodes = []
        links = []
        
        # Add pet nodes
        for pet in self.schedule.agents:
            # Basic node data
            node = {
                "id": pet.unique_id,
                "type": "pet",
                "attributes": {
                    "health": pet.health,
                    "mood": pet.mood,
                    "attention": pet.attention_level,
                    "energy": pet.energy,
                    "age": pet.age,
                    "stage": pet.development_stage
                },
                "traits": pet.traits,
                "position": {"x": pet.pos[0], "y": pet.pos[1]}
            }
            nodes.append(node)
        
        # Add user nodes
        for user_id in self.active_users:
            node = {
                "id": user_id,
                "type": "user",
                "attributes": {
                    "presence": self.user_presence.get(user_id, 0)
                }
            }
            nodes.append(node)
        
        # Add links between pets and users
        for pet in self.schedule.agents:
            # Pet-user relationships
            for user_id, strength in pet.human_relationships.items():
                if strength != 0 and user_id in self.active_users:
                    links.append({
                        "source": pet.unique_id,
                        "target": user_id,
                        "type": "pet_user",
                        "strength": strength
                    })
            
            # Pet-pet relationships
            for other_pet_id, strength in pet.pet_relationships.items():
                if strength != 0:
                    # Check if other pet exists
                    other_pet = self.get_pet_by_id(other_pet_id)
                    if other_pet:
                        links.append({
                            "source": pet.unique_id,
                            "target": other_pet_id,
                            "type": "pet_pet",
                            "strength": strength
                        })
        
        return {"nodes": nodes, "links": links}
    
    def calculate_avg_wait_time(self):
        """This is a placeholder for compatibility with the original model API"""
        return 0.0
    
    def calculate_resource_utilization(self):
        """This is a placeholder for compatibility with the original model API"""
        return 0.0
    
    def calculate_patient_satisfaction(self):
        """This is a placeholder for compatibility with the original model API"""
        return 0.0
    
    def calculate_network_density(self):
        """Calculate network density of pet relationships"""
        pet_count = len(self.schedule.agents)
        if pet_count <= 1:
            return 0.0
            
        # Count actual relationships
        relationship_count = 0
        for pet in self.schedule.agents:
            relationship_count += sum(1 for strength in pet.pet_relationships.values() 
                                      if abs(strength) > 0.1)
        
        # Maximum possible directed relationships
        max_relationships = pet_count * (pet_count - 1)
        
        return relationship_count / max_relationships if max_relationships > 0 else 0
    
    def calculate_avg_adaptation_score(self):
        """This is a placeholder for compatibility with the original model API"""
        return 0.0
    
    def serialize(self):
        """Serialize model state for persistence"""
        # Basic model data
        model_data = {
            "id": self.current_run_id,
            "steps": self.schedule.steps,
            "environment_state": self.environment_state.copy(),
            "active_users": list(self.active_users),
            "user_presence": dict(self.user_presence),
            "grid_width": self.grid.width,
            "grid_height": self.grid.height,
        }
        
        # Pet data
        pet_data = []
        for pet in self.schedule.agents:
            pet_state = {
                "id": pet.unique_id,
                "traits": pet.traits.copy(),
                "health": pet.health,
                "mood": pet.mood,
                "energy": pet.energy,
                "age": pet.age,
                "development_stage": pet.development_stage,
                "needs": pet.needs.copy(),
                "attention_level": pet.attention_level,
                "position": pet.pos,
                "human_relationships": dict(pet.human_relationships),
                "pet_relationships": dict(pet.pet_relationships),
                "behavior_patterns": dict(pet.behavior_patterns),
            }
            pet_data.append(pet_state)
            
        model_data["pets"] = pet_data
        
        return model_data
    
    @classmethod
    def deserialize(cls, data, redis_manager=None, data_collector=None):
        """Create a model from serialized state"""
        # Create model instance
        model = cls(
            num_pets=0,  # Will add pets from serialized data
            redis_manager=redis_manager,
            data_collector=data_collector
        )
        
        # Restore model state
        model.current_run_id = data.get("id", str(uuid.uuid4()))
        model.schedule.steps = data.get("steps", 0)
        model.environment_state = data.get("environment_state", model.environment_state)
        model.active_users = set(data.get("active_users", []))
        model.user_presence = defaultdict(float, data.get("user_presence", {}))
        
        # Resize grid if needed
        grid_width = data.get("grid_width", 20)
        grid_height = data.get("grid_height", 20)
        if grid_width != model.grid.width or grid_height != model.grid.height:
            model.grid = mesa.space.MultiGrid(grid_width, grid_height, True)
        
        # Restore pets
        for pet_data in data.get("pets", []):
            # Create pet
            pet = DigitalPet(
                unique_id=pet_data.get("id"),
                model=model,
                initial_traits=pet_data.get("traits")
            )
            
            # Restore pet state
            pet.health = pet_data.get("health", 100.0)
            pet.mood = pet_data.get("mood", 50.0)
            pet.energy = pet_data.get("energy", 100.0)
            pet.age = pet_data.get("age", 0.0)
            pet.development_stage = pet_data.get("development_stage", "infant")
            pet.needs = pet_data.get("needs", pet.needs)
            pet.attention_level = pet_data.get("attention_level", 50.0)
            pet.human_relationships = defaultdict(float, pet_data.get("human_relationships", {}))
            pet.pet_relationships = defaultdict(float, pet_data.get("pet_relationships", {}))
            pet.behavior_patterns = defaultdict(float, pet_data.get("behavior_patterns", {}))
            
            # Add to model
            model.schedule.add(pet)
            
            # Place on grid
            position = pet_data.get("position", (0, 0))
            model.grid.place_agent(pet, position)
        
        return model
