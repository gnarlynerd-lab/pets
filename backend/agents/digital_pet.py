"""
Digital Pet Base Class - Core entity for evolving digital pets
"""
from mesa import Agent
import uuid
import time
import json
import logging
import random
from typing import Dict, List, Any, Optional
from collections import defaultdict

from backend.agents.fluid_boundary import PetEnergySystem
from backend.agents.pet_environment import ObservableCognitiveDevelopment
from backend.agents.fep_cognitive_system import FEPCognitiveSystem

logger = logging.getLogger(__name__)


class DigitalPet(Agent):
    """
    Digital Pet that evolves based on human interaction and attention patterns.
    
    Key components:
    - Trait network: Interconnected personality traits that evolve over time
    - Memory system: Stores and processes interactions and experiences
    - Behavior system: Generates behaviors based on traits and context
    - Attention system: Tracks and responds to human attention patterns
    - State manager: Handles health, mood, energy and other vital stats
    - Fluid boundary: Manages the interface between pet and environment
    - Cognitive development: Tracks observable growth in intelligence
    """
    
    def __init__(self, unique_id: str, model, initial_traits: Optional[Dict] = None):
        super().__init__(unique_id, model)
        
        # Core DKS attributes (from DKSAgent)
        self.pet_type = "base"  # Can be specialized later
        self.creation_time = time.time()
        self.last_interaction_time = time.time()
        
        # Evolution components
        self.trait_connections = defaultdict(float)  # How traits influence each other
        self.trait_evolution_rate = defaultdict(float)  # How quickly traits evolve
        self.traits = initial_traits or self._generate_default_traits()
        
        # Memory systems - multi-level memory for learning
        self.episodic_memory = []  # Individual experiences/interactions
        self.semantic_memory = {}  # Generalized knowledge from patterns
        self.user_memory = defaultdict(dict)  # Memory of specific users
        
        # Behavior system
        self.behavior_patterns = defaultdict(float)  # Behavior -> activation threshold
        self.active_behaviors = []  # Currently active behaviors
        self.behavior_history = []  # Recent behaviors
        self.behavior_mutations = []  # Newly developed behaviors
        
        # Attention tracking
        self.attention_level = 50.0  # 0-100 scale
        self.attention_history = []  # Recent attention patterns
        self.attention_threshold_low = 20.0  # Below this is neglect
        self.attention_threshold_high = 80.0  # Above this is overstimulation
        
        # Relationship formation
        self.human_relationships = defaultdict(float)  # User -> relationship strength
        self.pet_relationships = defaultdict(float)  # Pet -> relationship strength
        
        # Vital statistics
        self.health = 100.0  # 0-100 scale
        self.energy = 100.0  # 0-100 scale
        self.mood = 50.0  # 0-100 scale
        self.age = 0.0  # Age in days
        self.development_stage = "infant"  # infant, child, adolescent, adult, elder
        
        # Needs system
        self.needs = {
            "hunger": 0.0,  # 0-100, higher is more hungry
            "thirst": 0.0,  # 0-100, higher is more thirsty
            "social": 0.0,  # 0-100, higher is more lonely
            "play": 0.0,  # 0-100, higher is more bored
            "rest": 0.0,  # 0-100, higher is more tired
        }
        
        # Message handling
        self.message_queue = []
        self.pending_responses = {}
        
        # Performance tracking
        self.interaction_count = 0
        self.lifetime_attention = 0
        self.evolution_generation = 0
        
        # Fluid boundary system - NEW
        self.energy_system = PetEnergySystem(self.unique_id, initial_energy=self.energy)
        
        # Observable cognitive development - NEW
        self.cognitive_system = ObservableCognitiveDevelopment(self.unique_id)
        
        # Free Energy Principle cognitive system - NEW
        self.fep_system = FEPCognitiveSystem(state_size=15, action_size=8)
        
        # Current region in environment - NEW
        self.current_region_id = "central"  # Default starting region
        
        # Assimilated environmental elements - NEW
        self.assimilated_elements = []
        self.projections_to_environment = []
    
    def _generate_default_traits(self) -> Dict[str, float]:
        """Generate starting traits for a new pet"""
        # Base traits with random initial values (0.3-0.7 range for balance)
        # A trait value of 0.0 means the trait is not present
        # A trait value of 1.0 means the trait is extremely strong
        traits = {
            # Core personality dimensions (based on big five) 
            "openness": 0.3 + 0.4 * self.random.random(),
            "conscientiousness": 0.3 + 0.4 * self.random.random(),
            "extraversion": 0.3 + 0.4 * self.random.random(),
            "agreeableness": 0.3 + 0.4 * self.random.random(),
            "neuroticism": 0.3 + 0.4 * self.random.random(),
            
            # Secondary traits that make pets interesting
            "curiosity": 0.3 + 0.4 * self.random.random(),
            "playfulness": 0.3 + 0.4 * self.random.random(),
            "affection": 0.3 + 0.4 * self.random.random(),
            "stubbornness": 0.3 + 0.4 * self.random.random(),
        }
        
        # Initialize trait connections
        self._initialize_trait_connections(traits)
        
        return traits
    
    def _initialize_trait_connections(self, traits: Dict[str, float]):
        """Initialize how traits influence each other"""
        trait_keys = list(traits.keys())
        
        # Create some basic connections between related traits
        # These will evolve over time based on experiences
        self.trait_connections["extraversion:playfulness"] = 0.6
        self.trait_connections["extraversion:social"] = 0.7
        self.trait_connections["agreeableness:affection"] = 0.8
        self.trait_connections["neuroticism:stubbornness"] = 0.5
        self.trait_connections["openness:curiosity"] = 0.7
        
        # Add some random connections to create uniqueness
        for i in range(5):
            trait1 = self.random.choice(trait_keys)
            trait2 = self.random.choice(trait_keys)
            if trait1 != trait2:
                connection_key = f"{trait1}:{trait2}"
                self.trait_connections[connection_key] = 0.3 + 0.4 * self.random.random()
    
    def step(self):
        """
        Process one time step for the pet
        This is where pet behaviors emerge and needs change
        """
        try:
            # 1. Update age and development stage
            self._update_age()
            
            # 2. Process incoming messages (interactions)
            messages = self.get_messages()
            self.process_messages(messages)
            
            # 3. Get current environment state
            environment_state = self._get_environment_state()
            
            # 4. Update fluid boundary and energy system
            energy_result = self.energy_system.step(environment_state)
            self.energy = energy_result["energy_level"]  # Sync energy values
            
            # 5. Update needs based on time passing and environment
            self._update_needs(environment_state)
            
            # 5a. Use FEP system to process surprise and update boundary permeability
            if hasattr(self, "fep_system") and environment_state:
                observation = self._map_state_to_observation(environment_state)
                belief_update = self.fep_system.update_observation(observation)
                surprise_level = belief_update.get("surprise", 0)
                
                # Adjust boundary permeability based on surprise
                # High surprise = uncertain environment = decrease permeability for protection
                if surprise_level > 2.0:
                    current = self.energy_system.boundary_system.boundary_permeability
                    self.energy_system.boundary_system.boundary_permeability = max(
                        0.2, current - (surprise_level * 0.02)
                    )
            
            # 6. Adjust mood and health based on needs and boundary status
            self._update_vitals(energy_result["boundary_status"])
            
            # 7. Check attention level and update
            self._update_attention()
            
            # 8. Interact with environment (assimilate or project)
            self._interact_with_environment(environment_state)
            
            # 9. Generate behaviors based on traits, needs, and context
            behaviors = self.generate_behaviors(environment_state)
            self.perform_behaviors(behaviors)
            
            # 10. Update cognitive development based on experiences
            self._update_cognition(environment_state)
            
            # 11. Update traits based on recent experiences (slow evolution)
            if self.model.schedule.steps % 10 == 0:  # Every 10 steps
                self._evolve_traits()
            
            # 12. Update memory systems
            self._consolidate_memory()
            
        except Exception as e:
            logger.error(f"Error in pet {self.unique_id} step: {e}")
    
    def _update_age(self):
        """Update pet age and development stage"""
        # Assuming one step is 6 minutes in pet time
        time_increment = 0.004166  # 6/1440 = 0.004166 days
        self.age += time_increment
        
        # Update development stage based on age
        if self.age < 1.0:
            self.development_stage = "infant"
        elif self.age < 5.0:
            self.development_stage = "child"
        elif self.age < 10.0:
            self.development_stage = "adolescent"
        elif self.age < 25.0:
            self.development_stage = "adult"
        else:
            self.development_stage = "elder"
    
    def _get_environment_state(self):
        """Get the current environment state from the model"""
        # Use pet's boundary permeability to determine how much it can sense
        permeability = self.energy_system.boundary_system.boundary_permeability
        
        # Check if model has an environment
        if hasattr(self.model, "environment"):
            # Get pet-specific view of environment based on permeability
            return self.model.environment.get_pet_view(self.unique_id, permeability)
        else:
            # Fallback to basic environment state from model
            env_state = self.model.environment_state.copy()
            env_state["current_region"] = self.current_region_id
            return env_state
    
    def _update_needs(self, environment_state=None):
        """Update pet needs based on time passing and environment"""
        # Basic need increases over time
        self.needs["hunger"] += 0.5
        self.needs["thirst"] += 0.8
        self.needs["social"] += 0.3
        self.needs["play"] += 0.4
        self.needs["rest"] += 0.2
        
        # Environmental effects on needs
        if environment_state:
            # Weather effects
            if "weather" in environment_state and "weather_effects" in environment_state:
                effects = environment_state["weather_effects"]
                if "energy" in effects:
                    # Weather energy affects rest need
                    self.needs["rest"] += -effects["energy"] * 0.5  # Negative because energy reduces rest need
                
                if "mood" in effects and effects["mood"] < 0:
                    # Bad weather increases social need
                    self.needs["social"] += abs(effects["mood"]) * 0.3
            
            # Time of day effects
            if "time_of_day" in environment_state:
                hour = environment_state["time_of_day"]
                # Pets get hungrier during typical meal times
                if 7 <= hour < 9 or 12 <= hour < 14 or 18 <= hour < 20:
                    self.needs["hunger"] += 0.3
                
                # Pets get sleepier at night
                if 22 <= hour or hour < 6:
                    self.needs["rest"] += 0.4
            
            # Social atmosphere effects
            if "social_atmosphere" in environment_state:
                social = environment_state["social_atmosphere"]
                # High social atmosphere reduces social need
                self.needs["social"] -= social * 0.2
                
                # But increases rest need slightly (socializing is tiring)
                self.needs["rest"] += social * 0.1
        
        # Cap needs at 100
        for need in self.needs:
            self.needs[need] = max(0.0, min(100.0, self.needs[need]))
    
    def _update_vitals(self, boundary_status=None):
        """Update pet vitals based on current needs and boundary"""
        # Calculate average need level (higher is worse)
        avg_need = sum(self.needs.values()) / len(self.needs)
        
        # Base mood calculation
        mood_change = -0.02 * avg_need + 1.0  # +1 when needs are 0, -1 when needs are 100
        
        # Health calculation - health decreases when needs are high
        health_change = -0.01 * avg_need + 0.5  # +0.5 when needs are 0, -0.5 when needs are 100
        
        # Boundary effects on vitals
        if boundary_status:
            if boundary_status == "failing":
                # Failing boundary significantly impacts health and mood
                health_change -= 1.0
                mood_change -= 1.0
        
        # Update mood
        self.mood += mood_change
        self.mood = max(0.0, min(100.0, self.mood))
        
        # Update health
        self.health += health_change
        self.health = max(0.0, min(100.0, self.health))
            
        # Get effect of assimilated elements from energy system
        assimilated_effects = self.energy_system.get_assimilated_elements_effects()
        
        # Apply effects to vitals
        if "energy" in assimilated_effects:
            self.energy = min(100.0, self.energy + assimilated_effects["energy"])
        if "health" in assimilated_effects:
            self.health = min(100.0, self.health + assimilated_effects["health"])
        if "mood" in assimilated_effects:
            self.mood = min(100.0, self.mood + assimilated_effects["mood"])
    
    def _interact_with_environment(self, environment_state):
        """Interact with environment through assimilation or projection"""
        # Try to assimilate elements from environment
        if random.random() < 0.3:  # 30% chance each step
            self._try_assimilation(environment_state)
        
        # Try to project something into the environment
        if random.random() < 0.2:  # 20% chance each step
            self._try_projection(environment_state)
        
        # Move between regions occasionally
        if random.random() < 0.1:  # 10% chance each step
            self._consider_region_change(environment_state)
    
    def _try_assimilation(self, environment_state):
        """Try to assimilate something from the environment"""
        # Scan environment for assimilable elements
        assimilable_elements = self.energy_system.exchange_system.scan_environment(environment_state)
        
        if assimilable_elements:
            # Choose an element based on pet traits
            chosen_element = self._choose_assimilation_target(assimilable_elements)
            
            # Attempt to assimilate
            result = self.energy_system.exchange_system.assimilate_element(chosen_element)
            
            if result["success"]:
                # Record the assimilation success
                self.assimilated_elements.append({
                    "element_id": result["element_id"],
                    "type": chosen_element["type"],
                    "timestamp": time.time(),
                    "integration": result.get("integration_level", 0.1)
                })
                
                # Update cognitive development for successful assimilation
                self.cognitive_system.process_experience(
                    "assimilation", 
                    0.7,  # Medium-high intensity experience
                    self.traits
                )
                
                # Add to memory
                self.episodic_memory.append({
                    "type": "assimilation",
                    "element": chosen_element["type"],
                    "success": True,
                    "timestamp": time.time()
                })
    
    def _choose_assimilation_target(self, elements):
        """Choose which environmental element to attempt to assimilate"""
        if not elements:
            return None
        
        # For now, simple weighted random choice based on difficulty
        weighted_elements = []
        for element in elements:
            # Lower difficulty elements get higher weight
            weight = 1.0 - (element.get("difficulty", 0.5) * 0.8)
            
            # Boost weight based on traits
            if element["type"] == "resource" and "openness" in self.traits:
                weight *= (1.0 + (self.traits["openness"] - 0.5))
            
            if element["type"] == "pet_projection" and "social_intelligence" in self.cognitive_areas:
                weight *= (1.0 + self.cognitive_areas["social_intelligence"])
                
            weighted_elements.append((element, weight))
        
        # Normalize weights
        total_weight = sum(w for _, w in weighted_elements)
        if total_weight == 0:
            return random.choice(elements)
            
        r = random.random() * total_weight
        cumulative_weight = 0
        for element, weight in weighted_elements:
            cumulative_weight += weight
            if r <= cumulative_weight:
                return element
        
        return elements[0]  # Fallback
    
    def _try_projection(self, environment_state):
        """Try to project something into the environment"""
        # Get current region
        region_id = environment_state.get("current_region", self.current_region_id)
        
        # Determine what to project based on pet state and traits
        projection_type = self._choose_projection_type()
        
        # Generate projection properties
        properties = self._generate_projection_properties(projection_type)
        
        # Attempt projection
        if hasattr(self.energy_system.exchange_system, "project_to_environment"):
            result = self.energy_system.exchange_system.project_to_environment(
                projection_type, 
                properties, 
                region_id
            )
            
            if result["success"]:
                # Record projection
                self.projections_to_environment.append({
                    "projection_id": result["projection_id"],
                    "type": projection_type,
                    "region_id": region_id,
                    "timestamp": time.time()
                })
                
                # Update model's environment if possible
                if hasattr(self.model, "environment") and hasattr(self.model.environment, "add_pet_projection"):
                    self.model.environment.add_pet_projection(
                        self.unique_id,
                        result["projection"]
                    )
                
                # Update cognitive development
                self.cognitive_system.process_experience(
                    "boundary_challenge",
                    0.6,  # Medium intensity
                    self.traits
                )
                
                # Add to memory
                self.episodic_memory.append({
                    "type": "projection",
                    "projection_type": projection_type,
                    "timestamp": time.time()
                })
    
    def _choose_projection_type(self):
        """Choose what type of projection to create"""
        projection_types = ["territorial_marker", "social_signal", "knowledge_share"]
        weights = []
        
        # Weight by traits
        if "extraversion" in self.traits:
            weights.append((
                "social_signal", 
                0.4 + (self.traits["extraversion"] * 0.6)
            ))
        else:
            weights.append(("social_signal", 0.4))
            
        if "conscientiousness" in self.traits:
            weights.append((
                "knowledge_share", 
                0.3 + (self.traits["conscientiousness"] * 0.7)
            ))
        else:
            weights.append(("knowledge_share", 0.3))
            
        if "neuroticism" in self.traits:
            weights.append((
                "territorial_marker", 
                0.3 + (self.traits["neuroticism"] * 0.6)
            ))
        else:
            weights.append(("territorial_marker", 0.3))
        
        # Choose based on weights
        total_weight = sum(w for _, w in weights)
        r = random.random() * total_weight
        cumulative_weight = 0
        
        for proj_type, weight in weights:
            cumulative_weight += weight
            if r <= cumulative_weight:
                return proj_type
        
        return "social_signal"  # Default
    
    def _generate_projection_properties(self, projection_type):
        """Generate properties for a projection based on type and pet state"""
        properties = {
            "created_by": self.unique_id,
            "timestamp": time.time(),
        }
        
        if projection_type == "territorial_marker":
            properties.update({
                "strength": self.energy / 100.0 * 0.7,
                "description": f"{self.unique_id}'s territory",
                "duration": 5 + int(self.energy / 20),  # Energy affects duration
            })
        
        elif projection_type == "social_signal":
            properties.update({
                "intensity": self.mood / 100.0 * 0.8,
                "tone": "friendly" if self.mood > 50 else "cautious",
                "duration": 3 + int(self.mood / 25),  # Mood affects duration
            })
        
        elif projection_type == "knowledge_share":
            # Use cognitive development level to determine quality
            if hasattr(self, "cognitive_areas"):
                knowledge_quality = self.cognitive_areas.get("knowledge", 0.5)
            else:
                knowledge_quality = 0.5
                
            properties.update({
                "quality": knowledge_quality,
                "topic": random.choice(["environment", "social", "resources", "general"]),
                "duration": 4 + int(knowledge_quality * 10),  # Knowledge affects duration
            })
        
        return properties
    
    def _consider_region_change(self, environment_state):
        """Consider moving to a different region based on needs and traits"""
        # Current region
        current_region_id = environment_state.get("current_region", self.current_region_id)
        
        # Get all regions
        available_regions = []
        if "regions" in environment_state:
            available_regions = list(environment_state["regions"].keys())
        else:
            # Default regions if not found in environment
            available_regions = ["central", "quiet", "play"]
        
        if current_region_id in available_regions:
            available_regions.remove(current_region_id)
        
        if not available_regions:
            return  # No other regions available
        
        # Choose region based on needs
        chosen_region = None
        
        # If hungry/thirsty, go to central
        if self.needs["hunger"] > 60 or self.needs["thirst"] > 60:
            if "central" in available_regions:
                chosen_region = "central"
        
        # If need rest, go to quiet corner
        elif self.needs["rest"] > 70:
            if "quiet" in available_regions:
                chosen_region = "quiet"
        
        # If need play, go to play zone
        elif self.needs["play"] > 60:
            if "play" in available_regions:
                chosen_region = "play"
        
        # If need social, choose based on other pets
        elif self.needs["social"] > 60:
            for region_id in available_regions:
                if "regions" in environment_state and region_id in environment_state["regions"]:
                    region = environment_state["regions"][region_id]
                    if "current_pets" in region and len(region["current_pets"]) > 0:
                        chosen_region = region_id
                        break
        
        # Random choice if no specific need
        if not chosen_region and available_regions:
            chosen_region = random.choice(available_regions)
        
        # Move to new region
        if chosen_region:
            self.current_region_id = chosen_region
            
            # Update model's environment if possible
            if hasattr(self.model, "environment") and hasattr(self.model.environment, "update_pet_location"):
                self.model.environment.update_pet_location(self.unique_id, chosen_region)
            
            # Add to memory
            self.episodic_memory.append({
                "type": "region_change",
                "from": current_region_id,
                "to": chosen_region,
                "timestamp": time.time()
            })
    
    def _update_cognition(self, environment_state):
        """Update cognitive development based on experiences"""
        # Determine the type of cognitive experience
        if self.active_behaviors:
            recent_behavior = self.active_behaviors[0]
            
            if recent_behavior["type"] in ["play", "explore", "learn"]:
                # Direct experiences that boost cognition
                experience_type = recent_behavior["type"]
                intensity = 0.6 + (recent_behavior.get("intensity", 0) * 0.4)
                
                # Process this experience
                self.cognitive_system.process_experience(
                    experience_type,
                    intensity,
                    self.traits
                )
            
            elif "social" in recent_behavior["type"]:
                # Social interactions
                self.cognitive_system.process_experience(
                    "social_interaction",
                    0.7,
                    self.traits
                )
        
        # Environmental observation (always happens)
        self.cognitive_system.process_experience(
            "observation",
            0.3 + (self.energy_system.boundary_system.boundary_permeability * 0.5),
            self.traits
        )
        
        # Update cognitive areas based on pet traits
        self.cognitive_areas = self.cognitive_system.cognitive_areas
        
        # Update FEP-based cognition
        self._update_fep_cognition(environment_state)
    
    def get_messages(self) -> List[Dict[str, Any]]:
        """Get interaction messages from queue"""
        messages = self.message_queue.copy()
        self.message_queue.clear()
        return messages
    
    def process_messages(self, messages: List[Dict[str, Any]]):
        """Process received interaction messages"""
        for message in messages:
            try:
                msg_type = message.get("type")
                sender_id = message.get("sender")
                content = message.get("content", {})
                
                # Process different interaction types
                if msg_type == "feed":
                    self._handle_feeding(sender_id, content)
                elif msg_type == "play":
                    self._handle_play(sender_id, content)
                elif msg_type == "pet":
                    self._handle_petting(sender_id, content)
                elif msg_type == "train":
                    self._handle_training(sender_id, content)
                elif msg_type == "check":
                    self._handle_checking(sender_id, content)
                elif msg_type == "pet_interaction":
                    self._handle_pet_interaction(sender_id, content)
                
                # Update interaction metrics
                self.interaction_count += 1
                self.last_interaction_time = time.time()
                
                # Record interaction in memory
                self._record_interaction(sender_id, msg_type, content)
                
            except Exception as e:
                logger.error(f"Error processing message in pet {self.unique_id}: {e}")
    
    def _handle_feeding(self, user_id: str, content: Dict[str, Any]):
        """Handle feeding interactions"""
        food_type = content.get("food_type", "basic")
        amount = content.get("amount", 1.0)
        
        # Reduce hunger based on amount and food type
        base_reduction = amount * 20.0
        food_multiplier = 1.0
        if food_type == "premium":
            food_multiplier = 1.5
        elif food_type == "treat":
            food_multiplier = 0.5
        
        hunger_reduction = base_reduction * food_multiplier
        self.needs["hunger"] = max(0.0, self.needs["hunger"] - hunger_reduction)
        
        # Feeding also reduces thirst slightly
        self.needs["thirst"] = max(0.0, self.needs["thirst"] - (hunger_reduction * 0.3))
        
        # Update mood based on hunger satisfaction
        mood_boost = min(hunger_reduction / 10.0, 10.0)
        self.mood = min(100.0, self.mood + mood_boost)
        
        # Increase relationship with this user
        self._adjust_relationship(user_id, 0.5)
        
        # Attention boost from interaction
        self._receive_attention(user_id, amount)
    
    def _handle_play(self, user_id: str, content: Dict[str, Any]):
        """Handle play interactions"""
        play_type = content.get("play_type", "basic")
        intensity = content.get("intensity", 1.0)
        duration = content.get("duration", 1.0)
        
        # Reduce play need based on duration and intensity
        play_satisfaction = intensity * duration * 15.0
        self.needs["play"] = max(0.0, self.needs["play"] - play_satisfaction)
        
        # Playing also reduces social need
        self.needs["social"] = max(0.0, self.needs["social"] - (play_satisfaction * 0.5))
        
        # Increase mood significantly
        mood_boost = min(play_satisfaction / 5.0, 20.0)
        self.mood = min(100.0, self.mood + mood_boost)
        
        # Decrease energy based on intensity
        energy_cost = intensity * duration * 10.0
        self.energy = max(0.0, self.energy - energy_cost)
        
        # Increase relationship substantially
        self._adjust_relationship(user_id, 1.0 * intensity)
        
        # Significant attention boost
        self._receive_attention(user_id, intensity * 2.0)
        
        # Increase rest need from play
        self.needs["rest"] += intensity * duration * 5.0
    
    def _handle_petting(self, user_id: str, content: Dict[str, Any]):
        """Handle petting interactions"""
        duration = content.get("duration", 1.0)
        location = content.get("location", "head")  # head, back, belly
        
        # Reduce social need
        social_reduction = duration * 10.0
        self.needs["social"] = max(0.0, self.needs["social"] - social_reduction)
        
        # Mood boost depends on pet's personality and petting location
        base_mood_boost = duration * 5.0
        
        # Extraversion affects petting enjoyment
        extraversion_factor = 0.5 + self.traits.get("extraversion", 0.5)
        
        # Location preference depends on traits
        location_multiplier = 1.0
        if location == "belly" and self.traits.get("extraversion", 0.5) < 0.4:
            # Introverted pets may not like belly rubs
            location_multiplier = 0.5
        elif location == "head" and self.traits.get("affection", 0.5) > 0.7:
            # Affectionate pets love head pets
            location_multiplier = 1.5
        
        mood_boost = base_mood_boost * extraversion_factor * location_multiplier
        self.mood = min(100.0, self.mood + mood_boost)
        
        # Moderately increase relationship
        self._adjust_relationship(user_id, 0.3 * duration)
        
        # Moderate attention boost
        self._receive_attention(user_id, duration)
    
    def _handle_training(self, user_id: str, content: Dict[str, Any]):
        """Handle training interactions"""
        skill = content.get("skill", "basic")
        difficulty = content.get("difficulty", 1.0)
        duration = content.get("duration", 1.0)
        
        # Training effectiveness depends on pet's conscientiousness
        conscientiousness = self.traits.get("conscientiousness", 0.5)
        effectiveness = conscientiousness * duration
        
        # Harder skills require more conscientiousness
        if difficulty > conscientiousness * 1.5:
            effectiveness *= 0.5  # Reduced effectiveness for challenging skills
        
        # Possible new behavior based on training
        behavior_chance = effectiveness * 0.2
        if self.random.random() < behavior_chance:
            new_behavior = f"trained_{skill}"
            if new_behavior not in self.behavior_patterns:
                self.behavior_patterns[new_behavior] = 0.2  # Initial activation threshold
                self.behavior_mutations.append({
                    "behavior": new_behavior,
                    "timestamp": time.time(),
                    "source": "training",
                    "trainer": user_id
                })
        
        # Training increases energy and rest needs
        self.energy = max(0.0, self.energy - (difficulty * duration * 5.0))
        self.needs["rest"] += difficulty * duration * 3.0
        
        # Relationship change depends on effectiveness
        relationship_change = effectiveness * 0.5
        self._adjust_relationship(user_id, relationship_change)
        
        # High attention boost from focused training
        self._receive_attention(user_id, duration * 1.5)
    
    def _handle_checking(self, user_id: str, content: Dict[str, Any]):
        """Handle check-in interactions (just looking at pet)"""
        duration = content.get("duration", 0.5)  # Usually brief
        
        # Small social need reduction
        self.needs["social"] = max(0.0, self.needs["social"] - (duration * 5.0))
        
        # Small mood boost from attention
        self.mood = min(100.0, self.mood + (duration * 2.0))
        
        # Small relationship boost
        self._adjust_relationship(user_id, 0.1)
        
        # Small attention boost
        self._receive_attention(user_id, duration * 0.5)
    
    def _handle_pet_interaction(self, pet_id: str, content: Dict[str, Any]):
        """Handle interaction with another pet"""
        interaction_type = content.get("interaction_type", "meet")
        compatibility = content.get("compatibility", 0.5)
        
        # Update pet relationship based on compatibility
        relationship_change = (compatibility - 0.5) * 2.0  # Range: -1.0 to 1.0
        self.pet_relationships[pet_id] += relationship_change
        
        # Cap relationship strength
        self.pet_relationships[pet_id] = max(-10.0, min(10.0, self.pet_relationships[pet_id]))
        
        # Pet interactions affect social need
        if self.pet_relationships[pet_id] > 0:
            self.needs["social"] = max(0.0, self.needs["social"] - 10.0)
        
        # Possible behavior mimicry from other pets (learning)
        if interaction_type == "play" and self.random.random() < 0.2:
            other_behavior = content.get("behavior", None)
            if other_behavior and other_behavior not in self.behavior_patterns:
                self.behavior_patterns[other_behavior] = 0.3
                self.behavior_mutations.append({
                    "behavior": other_behavior,
                    "timestamp": time.time(),
                    "source": "mimicry",
                    "pet_id": pet_id
                })
    
    def _adjust_relationship(self, user_id: str, delta: float):
        """Adjust relationship strength with a user"""
        # Base relationship change
        base_change = delta
        
        # Personality affects relationship change
        if delta > 0:
            # Positive interactions affected by agreeableness
            agreeableness = self.traits.get("agreeableness", 0.5)
            base_change *= 0.5 + agreeableness
        else:
            # Negative interactions affected by neuroticism
            neuroticism = self.traits.get("neuroticism", 0.5)
            base_change *= 0.5 + neuroticism
        
        # Update relationship
        self.human_relationships[user_id] += base_change
        
        # Cap relationship strength
        self.human_relationships[user_id] = max(-10.0, min(10.0, self.human_relationships[user_id]))
    
    def _receive_attention(self, user_id: str, amount: float):
        """Process received attention and update attention state"""
        # Base attention boost
        base_boost = amount * 10.0
        
        # Cap attention boost based on current level to prevent oversaturation
        if self.attention_level > 80:
            # Diminishing returns at high attention
            effective_boost = base_boost * (1.0 - (self.attention_level - 80) / 20)
        else:
            effective_boost = base_boost
        
        # Update attention level
        self.attention_level = min(100.0, self.attention_level + effective_boost)
    
    def generate_behaviors(self, environment_state=None) -> List[Dict[str, Any]]:
        """Generate behaviors based on current state, traits, needs and environment"""
        behaviors = []
        
        # Get base behavior patterns
        available_behaviors = dict(self.behavior_patterns)
        
        # Check if we have sufficient energy for behaviors
        if self.energy < 10:
            # Only rest behaviors when energy is very low
            rest_behavior = {
                "type": "rest",
                "intensity": 1.0,
                "cause": "low_energy",
                "target": None
            }
            behaviors.append(rest_behavior)
            return behaviors
        
        # Check primary needs
        if self.needs["hunger"] > 70:
            hunger_behavior = {
                "type": "seek_food",
                "intensity": self.needs["hunger"] / 100.0,
                "cause": "hunger",
                "target": None
            }
            behaviors.append(hunger_behavior)
        
        if self.needs["thirst"] > 70:
            thirst_behavior = {
                "type": "seek_water",
                "intensity": self.needs["thirst"] / 100.0,
                "cause": "thirst",
                "target": None
            }
            behaviors.append(thirst_behavior)
        
        if self.needs["play"] > 70:
            play_behavior = {
                "type": "playful",
                "intensity": self.needs["play"] / 100.0,
                "cause": "boredom",
                "target": None
            }
            behaviors.append(play_behavior)
        
        # Mood-based behaviors
        if self.mood < 30:
            mood_behavior = {
                "type": "sad",
                "intensity": (30.0 - self.mood) / 30.0,
                "cause": "low_mood",
                "target": None
            }
            behaviors.append(mood_behavior)
        elif self.mood > 70:
            mood_behavior = {
                "type": "happy",
                "intensity": (self.mood - 70.0) / 30.0,
                "cause": "high_mood",
                "target": None
            }
            behaviors.append(mood_behavior)
        
        # Social behaviors if others are nearby
        nearby_entities = self._get_nearby_entities()
        if nearby_entities["pets"] and self.needs["social"] > 50:
            target_pet = nearby_entities["pets"][0]
            relationship = self.pet_relationships.get(target_pet, 0.0)
            
            if relationship > 3.0:
                # Friendly behavior toward liked pets
                social_behavior = {
                    "type": "social_friendly",
                    "intensity": 0.7,
                    "cause": "liked_pet",
                    "target": target_pet
                }
                behaviors.append(social_behavior)
            elif relationship < -3.0:
                # Avoidance behavior toward disliked pets
                social_behavior = {
                    "type": "social_avoid",
                    "intensity": 0.7,
                    "cause": "disliked_pet",
                    "target": target_pet
                }
                behaviors.append(social_behavior)
            else:
                # Curious behavior toward neutral pets
                social_behavior = {
                    "type": "social_curious",
                    "intensity": 0.5,
                    "cause": "neutral_pet",
                    "target": target_pet
                }
                behaviors.append(social_behavior)
        
        # User-directed behaviors
        if nearby_entities["users"]:
            target_user = nearby_entities["users"][0]
            relationship = self.human_relationships.get(target_user, 0.0)
            
            if relationship > 3.0:
                # Affectionate behavior toward liked users
                user_behavior = {
                    "type": "seek_attention",
                    "intensity": min(relationship / 10.0, 0.9),
                    "cause": "liked_user",
                    "target": target_user
                }
                behaviors.append(user_behavior)
        
        # Trait-influenced behaviors
        if self.traits.get("curiosity", 0.0) > 0.7:
            # Curious pets explore more
            explore_behavior = {
                "type": "explore",
                "intensity": self.traits["curiosity"] - 0.3,
                "cause": "curiosity",
                "target": None
            }
            behaviors.append(explore_behavior)
        
        # Random behaviors (less likely than need-based ones)
        if self.random.random() < 0.1:
            random_behaviors = ["groom", "stretch", "look_around", "yawn"]
            random_behavior = {
                "type": self.random.choice(random_behaviors),
                "intensity": self.random.random() * 0.5,
                "cause": "random",
                "target": None
            }
            behaviors.append(random_behavior)
        
        # Trained or evolved behaviors
        for behavior_name, activation in available_behaviors.items():
            if behavior_name.startswith("trained_") and self.random.random() < activation:
                behavior = {
                    "type": behavior_name,
                    "intensity": activation,
                    "cause": "training",
                    "target": None
                }
                behaviors.append(behavior)
        
        # Record active behaviors
        self.active_behaviors = [b["type"] for b in behaviors]
        
        # Environment-influenced behaviors
        if environment_state:
            # Weather-based behaviors
            if "weather" in environment_state:
                weather = environment_state["weather"]
                if weather == "rainy" or weather == "stormy":
                    # Seek shelter behavior in bad weather
                    if self.energy_system.boundary_system.boundary_permeability > 0.7:
                        # High permeability means more affected by weather
                        weather_behavior = {
                            "type": "seek_shelter",
                            "intensity": 0.7,
                            "cause": f"bad_weather_{weather}",
                            "target": None
                        }
                        behaviors.append(weather_behavior)
                        self.active_behaviors.append("seek_shelter")
                elif weather == "clear" and self.energy_system.boundary_system.boundary_permeability > 0.5:
                    # Sunbathe in clear weather
                    weather_behavior = {
                        "type": "sunbathe",
                        "intensity": 0.5,
                        "cause": "nice_weather",
                        "target": None
                    }
                    behaviors.append(weather_behavior)
                    self.active_behaviors.append("sunbathe")
            
            # Time of day behaviors
            if "time_of_day" in environment_state:
                hour = environment_state["time_of_day"]
                if 22 <= hour or hour < 6:
                    # Night time behaviors
                    if self.traits.get("neuroticism", 0.5) > 0.6:
                        # Nervous pets are more alert at night
                        night_behavior = {
                            "type": "night_alert",
                            "intensity": self.traits["neuroticism"] - 0.4,
                            "cause": "night_time",
                            "target": None
                        }
                        behaviors.append(night_behavior)
                        self.active_behaviors.append("night_alert")
                    elif self.needs["rest"] > 60:
                        # Tired pets sleep at night
                        night_behavior = {
                            "type": "deep_sleep",
                            "intensity": self.needs["rest"] / 100.0,
                            "cause": "night_time_tired",
                            "target": None
                        }
                        behaviors.append(night_behavior)
                        self.active_behaviors.append("deep_sleep")
            
            # Region-specific behaviors
            if "current_region" in environment_state:
                region = environment_state["current_region"]
                if region == "central":
                    # Social behaviors in central area
                    social_behavior = {
                        "type": "social_gather",
                        "intensity": 0.6,
                        "cause": "central_area",
                        "target": None
                    }
                    behaviors.append(social_behavior)
                    self.active_behaviors.append("social_gather")
                elif region == "quiet":
                    # Resting behaviors in quiet corner
                    rest_behavior = {
                        "type": "meditate",
                        "intensity": 0.7,
                        "cause": "quiet_corner",
                        "target": None
                    }
                    behaviors.append(rest_behavior)
                    self.active_behaviors.append("meditate")
                elif region == "play":
                    # Play behaviors in play zone
                    play_behavior = {
                        "type": "frolic",
                        "intensity": 0.8,
                        "cause": "play_zone",
                        "target": None
                    }
                    behaviors.append(play_behavior)
                    self.active_behaviors.append("frolic")
            
            # Novelty response behaviors
            if "novelty_level" in environment_state:
                novelty = environment_state["novelty_level"]
                if novelty > 0.7 and self.traits.get("openness", 0.5) > 0.5:
                    # High novelty and open-minded pets investigate
                    novelty_behavior = {
                        "type": "investigate",
                        "intensity": novelty * self.traits.get("openness", 0.5),
                        "cause": "high_novelty",
                        "target": None
                    }
                    behaviors.append(novelty_behavior)
                    self.active_behaviors.append("investigate")
                elif novelty > 0.8 and self.traits.get("neuroticism", 0.5) > 0.7:
                    # High novelty and neurotic pets get cautious
                    novelty_behavior = {
                        "type": "cautious",
                        "intensity": novelty * self.traits.get("neuroticism", 0.5),
                        "cause": "high_novelty_stress",
                        "target": None
                    }
                    behaviors.append(novelty_behavior)
                    self.active_behaviors.append("cautious")
            
            # Boundary-related behaviors
            boundary_status = self.energy_system.boundary_system.get_status()
            if boundary_status["boundary_permeability"] > 0.8:
                # Highly permeable boundary - vulnerable behavior
                boundary_behavior = {
                    "type": "boundary_restoration",
                    "intensity": boundary_status["boundary_permeability"] - 0.5,
                    "cause": "vulnerable_boundary",
                    "target": None
                }
                behaviors.append(boundary_behavior)
                self.active_behaviors.append("boundary_restoration")
            elif boundary_status["boundary_permeability"] < 0.3:
                # Very rigid boundary - isolated behavior
                boundary_behavior = {
                    "type": "boundary_stretching",
                    "intensity": 0.8 - boundary_status["boundary_permeability"],
                    "cause": "rigid_boundary",
                    "target": None
                }
                behaviors.append(boundary_behavior)
                self.active_behaviors.append("boundary_stretching")
        
        # Add to behavior history
        if behaviors:
            self.behavior_history.append({
                "timestamp": time.time(),
                "behaviors": self.active_behaviors.copy()
            })
            
            # Keep behavior history manageable
            if len(self.behavior_history) > 30:
                self.behavior_history = self.behavior_history[-30:]
        
        return behaviors
    
    def _get_nearby_entities(self) -> Dict[str, List]:
        """Get nearby entities (users and pets)"""
        nearby = {
            "users": [],
            "pets": []
        }
        
        # This would normally use spatial grid, but for now we'll simulate
        # by checking any entities the model knows about
        if hasattr(self.model, 'active_users'):
            nearby["users"] = list(self.model.active_users)[:2]  # Limit to 2
        
        if hasattr(self.model, 'schedule'):
            nearby_pets = []
            for agent in self.model.schedule.agents:
                if agent.unique_id != self.unique_id and isinstance(agent, DigitalPet):
                    nearby_pets.append(agent.unique_id)
            nearby["pets"] = nearby_pets[:3]  # Limit to 3
        
        return nearby
    
    def perform_behaviors(self, behaviors: List[Dict[str, Any]]):
        """Perform generated behaviors"""
        # This would have effects in visualization and potentially
        # trigger notifications, animations, etc.
        
        for behavior in behaviors:
            # Update internal state based on behavior
            behavior_type = behavior["type"]
            intensity = behavior["intensity"]
            
            # Behaviors consume energy
            self.energy = max(0.0, self.energy - (intensity * 2.0))
            
            # Some behaviors affect needs
            if behavior_type == "rest":
                self.needs["rest"] = max(0.0, self.needs["rest"] - (intensity * 20.0))
            elif behavior_type == "explore":
                self.needs["play"] = max(0.0, self.needs["play"] - (intensity * 10.0))
            elif behavior_type == "seek_food":
                # Try to consume food from environment
                if hasattr(self.model, "environment"):
                    self.model.environment.consume_resources(self.current_region_id, {"food": 10})
                    self.needs["hunger"] = max(0.0, self.needs["hunger"] - (intensity * 25.0))
            elif behavior_type == "seek_water":
                # Try to consume water from environment
                if hasattr(self.model, "environment"):
                    self.model.environment.consume_resources(self.current_region_id, {"water": 10})
                    self.needs["thirst"] = max(0.0, self.needs["thirst"] - (intensity * 25.0))
                    
            # Environment-related behaviors
            if behavior_type == "sunbathe":
                # Sunbathing increases energy and mood
                self.energy = min(100.0, self.energy + (intensity * 5.0))
                self.mood = min(100.0, self.mood + (intensity * 3.0))
                self.needs["rest"] = max(0.0, self.needs["rest"] - (intensity * 10.0))
            elif behavior_type == "seek_shelter":
                # Seeking shelter affects boundary permeability
                if hasattr(self, "energy_system"):
                    current_permeability = self.energy_system.boundary_system.boundary_permeability
                    # Make boundary less permeable for protection
                    self.energy_system.boundary_system.boundary_permeability = max(
                        0.3, current_permeability - (intensity * 0.1)
                    )
            elif behavior_type == "night_alert":
                # Being alert at night consumes energy but improves boundary
                self.energy = max(0.0, self.energy - (intensity * 3.0))
                if hasattr(self, "energy_system"):
                    # Strengthen boundary
                    self.energy_system.boundary_system.boundary_size = min(
                        1.5, self.energy_system.boundary_system.boundary_size + (intensity * 0.1)
                    )
            elif behavior_type == "deep_sleep":
                # Deep sleep restores energy and strengthens boundary
                self.energy = min(100.0, self.energy + (intensity * 10.0))
                self.needs["rest"] = max(0.0, self.needs["rest"] - (intensity * 30.0))
                if hasattr(self, "energy_system"):
                    # Healing time for boundary
                    self.energy_system.boundary_system.boundary_maintenance_cost *= 0.9
            elif behavior_type == "investigate":
                # Investigating novelty develops cognitive abilities
                if hasattr(self, "cognitive_system"):
                    self.cognitive_system.process_experience(
                        "exploration", 
                        intensity * 0.8,
                        self.traits
                    )
                self.needs["play"] = max(0.0, self.needs["play"] - (intensity * 15.0))
            elif behavior_type == "boundary_restoration":
                # Direct attempt to restore boundary integrity
                if hasattr(self, "energy_system"):
                    # Invest energy directly in boundary
                    energy_invested = min(self.energy * 0.2, intensity * 10.0)
                    self.energy -= energy_invested
                    result = self.energy_system.consume_energy(energy_invested, "boundary_repair")
                    
                    # Make boundary less permeable
                    self.energy_system.boundary_system.boundary_permeability = max(
                        0.3, self.energy_system.boundary_system.boundary_permeability - (intensity * 0.15)
                    )
            elif behavior_type == "boundary_stretching":
                # Attempt to make boundary more flexible
                if hasattr(self, "energy_system"):
                    # Increase permeability
                    self.energy_system.boundary_system.boundary_permeability = min(
                        0.8, self.energy_system.boundary_system.boundary_permeability + (intensity * 0.1)
                    )
                    # Process this as a cognitive development experience
                    if hasattr(self, "cognitive_system"):
                        self.cognitive_system.process_experience(
                            "boundary_challenge", 
                            intensity * 0.7,
                            self.traits
                        )
            
            # Optionally send message to target if there is one
            target = behavior.get("target")
            if target:
                self._send_behavior_to_target(behavior, target)
    
    def _send_behavior_to_target(self, behavior: Dict[str, Any], target: str):
        """Send behavior information to target entity"""
        # In a full implementation, this would use the message system
        # to notify other pets or users of this pet's behavior
        pass
    
    def _record_interaction(self, entity_id: str, interaction_type: str, content: Dict[str, Any]):
        """Record an interaction in memory"""
        memory_entry = {
            "timestamp": time.time(),
            "entity_id": entity_id,
            "type": interaction_type,
            "content": content,
            "mood_before": self.mood,
            "mood_after": self.mood
        }
        
        # Add to episodic memory
        self.episodic_memory.append(memory_entry)
        
        # Keep episodic memory manageable
        if len(self.episodic_memory) > 100:
            self.episodic_memory = self.episodic_memory[-100:]
        
        # Update user-specific memory
        if "user" in entity_id:
            if interaction_type not in self.user_memory[entity_id]:
                self.user_memory[entity_id][interaction_type] = 0
            self.user_memory[entity_id][interaction_type] += 1
            
            # Record last interaction time with this user
            self.user_memory[entity_id]["last_interaction"] = time.time()
            
            # Check for memory of favorite activities with this user
            interactions = [(k, v) for k, v in self.user_memory[entity_id].items()
                          if k not in ["last_interaction", "relationship"]]
            
            if interactions:
                favorite = max(interactions, key=lambda x: x[1])[0]
                self.user_memory[entity_id]["favorite_activity"] = favorite
    
    def _evolve_traits(self):
        """Evolve traits based on interactions and experiences"""
        # This happens slowly over time based on pet's experiences
        
        # Only evolve if we have sufficient experience
        if len(self.episodic_memory) < 5:
            return
        
        # Look at recent interactions (last 20)
        recent_memories = self.episodic_memory[-20:]
        
        # Analyze common interaction types
        interaction_counts = defaultdict(int)
        for memory in recent_memories:
            interaction_counts[memory["type"]] += 1
        
        # Evolve traits based on interaction patterns
        if interaction_counts["play"] > 8:
            # Lots of play increases extraversion and playfulness
            self._adjust_trait("extraversion", 0.02)
            self._adjust_trait("playfulness", 0.03)
        
        if interaction_counts["feed"] > 10:
            # Frequent feeding might increase dependence
            self._adjust_trait("agreeableness", 0.01)
        
        if interaction_counts["train"] > 5:
            # Training increases conscientiousness
            self._adjust_trait("conscientiousness", 0.03)
        
        # Neglect effects
        if self.attention_level < self.attention_threshold_low:
            # Prolonged neglect increases neuroticism and decreases extraversion
            self._adjust_trait("neuroticism", 0.03)
            self._adjust_trait("extraversion", -0.02)
        
        # Trait connections cause related traits to influence each other
        self._propagate_trait_influences()
        
        # Small chance for random trait mutation
        if self.random.random() < 0.05:
            trait = self.random.choice(list(self.traits.keys()))
            mutation = (self.random.random() - 0.5) * 0.1  # -0.05 to +0.05
            self._adjust_trait(trait, mutation)
        
        # Increment evolution generation
        self.evolution_generation += 1
    
    def _adjust_trait(self, trait: str, delta: float):
        """Adjust a trait by the given delta"""
        if trait in self.traits:
            self.traits[trait] = max(0.0, min(1.0, self.traits[trait] + delta))
    
    def _propagate_trait_influences(self):
        """Allow connected traits to influence each other"""
        trait_changes = defaultdict(float)
        
        # Check each trait connection
        for connection, strength in self.trait_connections.items():
            if strength > 0.1:  # Only significant connections matter
                source_trait, target_trait = connection.split(':')
                if source_trait in self.traits and target_trait in self.traits:
                    # Calculate influence (source trait pulls target trait toward it)
                    source_value = self.traits[source_trait]
                    target_value = self.traits[target_trait]
                    
                    # Direction of influence
                    direction = 1 if source_value > target_value else -1
                    
                    # Magnitude of influence
                    influence = direction * strength * 0.01
                    trait_changes[target_trait] += influence
        
        # Apply all changes at once
        for trait, change in trait_changes.items():
            self._adjust_trait(trait, change)
    
    def _consolidate_memory(self):
        """Convert episodic memories to semantic memory when patterns are found"""
        if len(self.episodic_memory) < 10:
            return
        
        # Look for patterns in recent memories
        recent_memories = self.episodic_memory[-20:]
        
        # Group by entity
        entity_memories = defaultdict(list)
        for memory in recent_memories:
            entity_memories[memory["entity_id"]].append(memory)
        
        # Look for patterns with each entity
        for entity_id, memories in entity_memories.items():
            if len(memories) < 3:
                continue
            
            # Common interaction type?
            interaction_counts = defaultdict(int)
            for memory in memories:
                interaction_counts[memory["type"]] += 1
            
            most_common = max(interaction_counts.items(), key=lambda x: x[1])
            interaction_type, count = most_common
            
            # If pattern is strong enough, add to semantic memory
            if count >= 3:
                pattern_key = f"{entity_id}:{interaction_type}"
                
                # Calculate outcome (average mood change)
                mood_changes = [m["mood_after"] - m["mood_before"] for m in memories]
                avg_mood_change = sum(mood_changes) / len(mood_changes)
                
                # Record pattern
                self.semantic_memory[pattern_key] = {
                    "entity_id": entity_id,
                    "interaction_type": interaction_type,
                    "frequency": count,
                    "avg_mood_effect": avg_mood_change,
                    "last_updated": time.time()
                }
    
    def get_status(self) -> Dict[str, Any]:
        """Get current pet status for display"""
        status_dict = {
            'pet_id': self.unique_id,
            'age': self.age,
            'development_stage': self.development_stage,
            'health': self.health,
            'mood': self.mood,
            'energy': self.energy,
            'needs': self.needs,
            'traits': self.traits,
            'active_behaviors': self.active_behaviors,
            'attention_level': self.attention_level
        }
        
        # Add FEP cognitive system status if available
        if hasattr(self, "fep_system"):
            status_dict['fep'] = {
                'surprise_level': self.fep_system.get_surprise_level(),
                'prediction_accuracy': self.fep_system.get_prediction_accuracy()
            }
            
            # Add current beliefs if available
            fep_state = self.fep_system.get_state()
            if 'beliefs' in fep_state:
                status_dict['fep']['beliefs'] = fep_state['beliefs']
            
        return status_dict
    
    def save_state(self) -> Dict[str, Any]:
        """Prepare complete pet state for database storage"""
        return {
            'pet_id': self.unique_id,
            'creation_time': self.creation_time,
            'last_interaction_time': self.last_interaction_time,
            
            'traits': self.traits,
            'trait_connections': dict(self.trait_connections),
            
            'episodic_memory': self.episodic_memory[-50:],  # Last 50 memories
            'semantic_memory': self.semantic_memory,
            'user_memory': dict(self.user_memory),
            
            'behavior_patterns': dict(self.behavior_patterns),
            'behavior_history': self.behavior_history[-10:],  # Last 10 behaviors
            'behavior_mutations': self.behavior_mutations[-5:],  # Last 5 mutations
            
            'attention_level': self.attention_level,
            'attention_history': self.attention_history[-20:],  # Last 20 attention records
            
            'human_relationships': dict(self.human_relationships),
            'pet_relationships': dict(self.pet_relationships),
            
            'health': self.health,
            'energy': self.energy,
            'mood': self.mood,
            'needs': self.needs,
            'age': self.age,
            'development_stage': self.development_stage,
            
            'interaction_count': self.interaction_count,
            'lifetime_attention': self.lifetime_attention,
            'evolution_generation': self.evolution_generation,
            
            # FEP cognitive system state
            'fep_system': {
                'surprise_history': getattr(self.fep_system, 'surprise_history', [])[-20:],
                'prediction_accuracy': getattr(self.fep_system, 'prediction_accuracy', [])[-20:],
                'learning_rate': getattr(self.fep_system, 'learning_rate', 0.1)
            } if hasattr(self, 'fep_system') else {}
        }
    
    @classmethod
    def load_from_state(cls, state_data: Dict[str, Any], model) -> 'DigitalPet':
        """Recreate pet from saved state"""
        pet = cls(state_data['pet_id'], model)
        
        # Restore basic properties
        pet.creation_time = state_data['creation_time']
        pet.last_interaction_time = state_data['last_interaction_time']
        
        # Restore traits
        pet.traits = state_data['traits']
        pet.trait_connections = defaultdict(float)
        for conn, strength in state_data['trait_connections'].items():
            pet.trait_connections[conn] = strength
        
        # Restore memory systems
        pet.episodic_memory = state_data.get('episodic_memory', [])
        pet.semantic_memory = state_data.get('semantic_memory', {})
        pet.user_memory = defaultdict(dict)
        for user_id, memory in state_data.get('user_memory', {}).items():
            pet.user_memory[user_id] = memory
        
        # Restore behavior systems
        pet.behavior_patterns = defaultdict(float)
        for behavior, activation in state_data.get('behavior_patterns', {}).items():
            pet.behavior_patterns[behavior] = activation
        pet.behavior_history = state_data.get('behavior_history', [])
        pet.behavior_mutations = state_data.get('behavior_mutations', [])
        
        # Restore attention
        pet.attention_level = state_data.get('attention_level', 50.0)
        pet.attention_history = state_data.get('attention_history', [])
        
        # Restore relationships
        pet.human_relationships = defaultdict(float)
        for human_id, rel in state_data.get('human_relationships', {}).items():
            pet.human_relationships[human_id] = rel
        
        pet.pet_relationships = defaultdict(float)
        for pet_id, rel in state_data.get('pet_relationships', {}).items():
            pet.pet_relationships[pet_id] = rel
        
        # Restore vital stats
        pet.health = state_data.get('health', 100.0)
        pet.energy = state_data.get('energy', 100.0)
        pet.mood = state_data.get('mood', 50.0)
        pet.needs = state_data.get('needs', {
            "hunger": 0.0,
            "thirst": 0.0,
            "social": 0.0,
            "play": 0.0,
            "rest": 0.0
        })
        pet.age = state_data.get('age', 0.0)
        pet.development_stage = state_data.get('development_stage', 'infant')
        
        # Restore metrics
        pet.interaction_count = state_data.get('interaction_count', 0)
        pet.lifetime_attention = state_data.get('lifetime_attention', 0.0)
        pet.evolution_generation = state_data.get('evolution_generation', 0)
        
        # Restore FEP cognitive system state if it exists
        if 'fep_system' in state_data and hasattr(pet, 'fep_system'):
            fep_data = state_data['fep_system']
            if 'surprise_history' in fep_data:
                pet.fep_system.surprise_history = fep_data['surprise_history']
            if 'prediction_accuracy' in fep_data:
                pet.fep_system.prediction_accuracy = fep_data['prediction_accuracy']
            if 'learning_rate' in fep_data:
                pet.fep_system.learning_rate = fep_data['learning_rate']
        
        return pet
    
    # ===== EMOJI COMMUNICATION METHODS =====
    
    def receive_emoji_message(self, emoji_sequence: str, user_id: str = "default") -> Dict[str, Any]:
        """
        Process an incoming emoji message from a user and generate a response.
        
        Args:
            emoji_sequence: String of emojis sent by the user
            user_id: Identifier for the user sending the message
            
        Returns:
            response_data: Dict containing the pet's emoji response and state changes
        """
        logger.info(f"Pet {self.unique_id} received emoji message: {emoji_sequence} from user {user_id}")
        
        # Update last interaction time
        self.last_interaction_time = time.time()
        
        # Store the interaction in memory
        interaction_memory = {
            'type': 'emoji_communication',
            'timestamp': time.time(),
            'user_id': user_id,
            'user_emojis': emoji_sequence,
            'context': self._get_current_context()
        }
        
        # Process through FEP cognitive system
        fep_result = self.fep_system.process_emoji_interaction(
            emoji_sequence, 
            user_context={'user_id': user_id, 'pet_state': self.get_state()}
        )
        
        # Update pet state based on FEP processing
        self._apply_fep_effects(fep_result)
        
        # Generate behavioral response based on emoji interaction
        behavioral_response = self._generate_emoji_behavioral_response(fep_result)
        
        # Update user memory
        self._update_user_emoji_memory(user_id, emoji_sequence, fep_result['pet_response'])
        
        # Store complete interaction in memory
        interaction_memory.update({
            'pet_response': fep_result['pet_response'],
            'surprise_level': fep_result['surprise_level'],
            'behavioral_response': behavioral_response
        })
        self.episodic_memory.append(interaction_memory)
        
        # Prepare response data
        response_data = {
            'pet_id': self.unique_id,
            'emoji_response': fep_result['pet_response'],
            'behavioral_response': behavioral_response,
            'mood_change': self._calculate_mood_change(fep_result),
            'surprise_level': fep_result['surprise_level'],
            'confidence': fep_result['response_confidence'],
            'updated_state': self.get_state(),
            'timestamp': time.time()
        }
        
        logger.info(f"Pet {self.unique_id} responds with: {fep_result['pet_response']}")
        return response_data
    
    def _get_current_context(self) -> Dict[str, Any]:
        """Get current context for emoji interaction processing."""
        return {
            'mood': self.mood / 100.0,  # Normalize to 0-1 scale
            'energy': self.energy / 100.0,
            'health': self.health / 100.0,
            'hunger': self.needs.get('hunger', 0.0) / 100.0,
            'social': self.needs.get('social', 0.0) / 100.0,
            'development_stage': self.development_stage,
            'recent_interactions': len([m for m in self.episodic_memory[-10:] if m.get('type') == 'emoji_communication']),
            'dominant_traits': self._get_dominant_traits()
        }
    
    def _apply_fep_effects(self, fep_result: Dict[str, Any]):
        """Apply effects from FEP processing to pet state."""
        surprise_level = fep_result.get('surprise_level', 0.0)
        
        # High surprise can affect mood and energy
        if surprise_level > 0.8:
            self.mood = max(0.0, self.mood - 10.0)  # Decrease mood by 10 points
            self.energy = max(0.0, self.energy - 5.0)  # Decrease energy by 5 points
        elif surprise_level < 0.2:
            # Low surprise (predictable, comforting interaction) improves mood
            self.mood = min(100.0, self.mood + 5.0)  # Increase mood by 5 points
        
        # Social interaction always helps social need
        self.needs['social'] = max(0.0, self.needs.get('social', 0.0) - 10.0)  # Reduce loneliness
        
        # Update traits based on interaction type
        self._update_traits_from_emoji_interaction(fep_result)
    
    def _generate_emoji_behavioral_response(self, fep_result: Dict[str, Any]) -> str:
        """Generate a behavioral response description based on emoji interaction."""
        emoji_response = fep_result['pet_response']
        surprise_level = fep_result['surprise_level']
        
        # Map emoji responses to behavioral descriptions
        behavior_map = {
            '❤️': "nuzzles affectionately and purrs contentedly",
            '😊': "wags tail happily and bounces around",
            '😔': "looks down sadly and seeks comfort",
            '🎉': "jumps excitedly and does a little dance",
            '😴': "yawns and curls up for a nap",
            '🤔': "tilts head curiously and investigates",
            '👍': "gives an approving chirp and stands proudly",
            '👎': "huffs disapprovingly and turns away briefly",
            '❓': "looks confused and tilts head from side to side",
            '✨': "sparkles with joy and spins in a circle"
        }
        
        base_behavior = behavior_map.get(emoji_response, "responds thoughtfully")
        
        # Modify behavior based on surprise level
        if surprise_level > 0.7:
            return f"looks startled, then {base_behavior}"
        elif surprise_level < 0.3:
            return f"calmly {base_behavior}"
        else:
            return base_behavior
    
    def _update_user_emoji_memory(self, user_id: str, user_emojis: str, pet_response: str):
        """Update memory of user's emoji communication patterns."""
        if 'emoji_patterns' not in self.user_memory[user_id]:
            self.user_memory[user_id]['emoji_patterns'] = {
                'favorite_emojis': defaultdict(int),
                'response_history': [],
                'successful_interactions': 0,
                'total_interactions': 0
            }
        
        patterns = self.user_memory[user_id]['emoji_patterns']
        
        # Track user's emoji usage
        for emoji in user_emojis:
            patterns['favorite_emojis'][emoji] += 1
        
        # Track interaction success (based on low surprise = good understanding)
        patterns['total_interactions'] += 1
        patterns['response_history'].append({
            'user_emojis': user_emojis,
            'pet_response': pet_response,
            'timestamp': time.time()
        })
        
        # Keep only recent history
        if len(patterns['response_history']) > 20:
            patterns['response_history'] = patterns['response_history'][-20:]
    
    def _calculate_mood_change(self, fep_result: Dict[str, Any]) -> float:
        """Calculate how much the mood changed from this interaction."""
        surprise_level = fep_result['surprise_level']
        confidence = fep_result['response_confidence']
        
        # Positive mood change for successful (low surprise, high confidence) interactions
        mood_change = (confidence - surprise_level) * 0.1
        return max(-0.2, min(0.2, mood_change))  # Clamp between -0.2 and +0.2
    
    def _update_traits_from_emoji_interaction(self, fep_result: Dict[str, Any]):
        """Update personality traits based on emoji interaction patterns."""
        user_emojis = fep_result.get('user_emojis', '')
        pet_response = fep_result.get('pet_response', '')
        
        # Analyze interaction type and update relevant traits
        if any(emoji in user_emojis for emoji in ['❤️', '🥰', '😍', '🤗']):
            # Affectionate interaction - increase sociability and affection
            self.traits['sociability'] = min(1.0, self.traits['sociability'] + 0.01)
            self.traits['affection'] = min(1.0, self.traits['affection'] + 0.01)
        
        if any(emoji in user_emojis for emoji in ['🎮', '⚽', '🎯']):
            # Playful interaction - increase playfulness and energy
            self.traits['playfulness'] = min(1.0, self.traits['playfulness'] + 0.01)
            self.traits['energy_level'] = min(1.0, self.traits['energy_level'] + 0.005)
        
        if any(emoji in user_emojis for emoji in ['🤔', '❓', '📚']):
            # Curious interaction - increase curiosity
            self.traits['curiosity'] = min(1.0, self.traits['curiosity'] + 0.01)
    
    def get_emoji_communication_stats(self) -> Dict[str, Any]:
        """Get statistics about emoji communication patterns."""
        emoji_interactions = [m for m in self.episodic_memory if m.get('type') == 'emoji_communication']
        
        if not emoji_interactions:
            return {'total_interactions': 0}
        
        # Analyze patterns
        user_emojis_used = []
        pet_responses_given = []
        surprise_levels = []
        
        for interaction in emoji_interactions:
            user_emojis_used.extend(list(interaction.get('user_emojis', '')))
            pet_responses_given.append(interaction.get('pet_response', ''))
            surprise_levels.append(interaction.get('surprise_level', 0.0))
        
        # Calculate statistics
        stats = {
            'total_interactions': len(emoji_interactions),
            'average_surprise': sum(surprise_levels) / len(surprise_levels) if surprise_levels else 0,
            'most_common_user_emoji': max(set(user_emojis_used), key=user_emojis_used.count) if user_emojis_used else None,
            'most_common_pet_response': max(set(pet_responses_given), key=pet_responses_given.count) if pet_responses_given else None,
            'recent_activity': len([i for i in emoji_interactions if time.time() - i.get('timestamp', 0) < 3600]),  # Last hour
            'communication_effectiveness': 1.0 - (sum(surprise_levels) / len(surprise_levels)) if surprise_levels else 0.5
        }
        
        return stats
    
    def interact_with_emoji(self, emoji_sequence: str, user_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process emoji interaction with the pet and return the pet's response.
        
        Args:
            emoji_sequence: String of emojis from the user
            user_context: Additional context about the interaction
            
        Returns:
            interaction_result: Dictionary containing the interaction result
        """
        if user_context is None:
            user_context = {}
            
        logger.info(f"Pet {self.unique_id} receiving emoji interaction: {emoji_sequence}")
        
        # Process through FEP cognitive system
        fep_result = self.fep_system.process_emoji_interaction(emoji_sequence, user_context)
        
        # Update pet's internal state based on emoji interaction
        self._update_state_from_emoji_interaction(fep_result)
        
        # Update last interaction time
        self.last_interaction_time = time.time()
        
        # Store interaction in memory
        interaction_memory = {
            'type': 'emoji_interaction',
            'user_input': emoji_sequence,
            'pet_response': fep_result['pet_response'],
            'surprise_level': fep_result['surprise_level'],
            'timestamp': fep_result['timestamp'],
            'context': user_context
        }
        self.episodic_memory.append(interaction_memory)
        
        # Limit memory size
        if len(self.episodic_memory) > 1000:
            self.episodic_memory = self.episodic_memory[-1000:]
        
        logger.info(f"Pet {self.unique_id} responds with: {fep_result['pet_response']}")
        
        return {
            'user_emojis': emoji_sequence,
            'pet_response': fep_result['pet_response'],
            'surprise_level': fep_result['surprise_level'],
            'response_confidence': fep_result['response_confidence'],
            'pet_state': self.get_state(),
            'timestamp': fep_result['timestamp']
        }
    
    def generate_emoji_message(self) -> str:
        """
        Generate an emoji message based on the pet's current state and needs.
        
        Returns:
            emoji_message: String of emojis expressing the pet's current state
        """
        # Get current state as context for emoji generation
        current_state = np.array([
            self.vital_stats['hunger'],
            self.vital_stats['energy'],
            self.vital_stats['mood'],
            self.vital_stats['health'],
            self.traits.get('playfulness', 0.5),
            self.traits.get('curiosity', 0.5),
            self.traits.get('affection', 0.5),
            self.traits.get('independence', 0.5),
            self.traits.get('energy_level', 0.5),
            time.time() % 1,  # Time component
            len(self.episodic_memory) / 1000.0,  # Experience component
            self.get_attention_level(),
            self.learning_adaptation_rate,
            random.random(),  # Random exploration
            random.random()   # Additional randomness
        ])
        
        # Generate emoji response using FEP system
        emoji_message = self.fep_system.generate_emoji_response(current_state)
        
        # Add context-based modifiers
        if self.vital_stats['hunger'] > 0.7:
            # Add food emojis when hungry
            food_emojis = ['🍎', '🍕', '🍪', '🥛']
            emoji_message += random.choice(food_emojis)
        
        if self.vital_stats['energy'] < 0.3:
            # Add sleep emojis when tired
            emoji_message += '😴'
        
        if self.traits.get('playfulness', 0.5) > 0.7 and self.vital_stats['energy'] > 0.5:
            # Add play emojis when energetic and playful
            play_emojis = ['🎮', '⚽', '🎯']
            emoji_message += random.choice(play_emojis)
        
        logger.info(f"Pet {self.unique_id} generated emoji message: {emoji_message}")
        return emoji_message
    
    def _update_state_from_emoji_interaction(self, fep_result: Dict[str, Any]):
        """
        Update pet's internal state based on emoji interaction results.
        
        Args:
            fep_result: Result from FEP cognitive system processing
        """
        surprise_level = fep_result.get('surprise_level', 0.0)
        confidence = fep_result.get('response_confidence', 0.5)
        
        # Low surprise (familiar interaction) increases contentment
        if surprise_level < 0.3:
            self.vital_stats['mood'] = min(1.0, self.vital_stats['mood'] + 0.1)
            self.traits['affection'] = min(1.0, self.traits.get('affection', 0.5) + 0.05)
        
        # High confidence interactions boost mood
        if confidence > 0.7:
            self.vital_stats['mood'] = min(1.0, self.vital_stats['mood'] + 0.05)
        
        # Update learning based on interaction quality
        learning_boost = confidence * 0.1
        self.learning_adaptation_rate = min(1.0, self.learning_adaptation_rate + learning_boost)
        
        # Evolve traits based on interaction patterns
        user_emojis = fep_result.get('user_emojis', '')
        if '🎮' in user_emojis or '⚽' in user_emojis:
            self.traits['playfulness'] = min(1.0, self.traits.get('playfulness', 0.5) + 0.02)
        if '❤️' in user_emojis or '🤗' in user_emojis:
            self.traits['affection'] = min(1.0, self.traits.get('affection', 0.5) + 0.02)
        if '🤔' in user_emojis or '❓' in user_emojis:
            self.traits['curiosity'] = min(1.0, self.traits.get('curiosity', 0.5) + 0.02)
    
    def _get_dominant_traits(self) -> List[str]:
        """Get the most prominent personality traits of the pet."""
        # Sort traits by value and return the top 3
        sorted_traits = sorted(self.traits.items(), key=lambda x: x[1], reverse=True)
        return [trait[0] for trait in sorted_traits[:3]]
    
    def get_state(self) -> Dict[str, Any]:
        """Get the current state of the pet for API responses."""
        return {
            'id': self.unique_id,
            'health': self.health,
            'mood': self.mood,
            'energy': self.energy,
            'attention': self.attention_level,
            'age': time.time() - self.creation_time,
            'stage': self.development_stage,
            'traits': self.traits,
            'needs': self.needs,
            'position': [self.pos[0], self.pos[1]] if hasattr(self, 'pos') else [0, 0]
        }
