"""
Pet Environment - Manages the shared environment for digital pets
"""
import time
import random
import logging
from typing import Dict, List, Any, Optional
from collections import defaultdict

logger = logging.getLogger(__name__)


class PetEnvironment:
    """
    Environment system for digital pets with fluid boundaries
    
    The environment is a shared space that:
    - Contains resources, features, and regions
    - Has its own dynamic properties like weather and time
    - Allows for pet projections to persist
    - Evolves based on pet interactions and external events
    """
    
    def __init__(self):
        # Core environmental factors
        self.time_of_day = 8.0  # 24-hour clock
        self.day_of_week = 1  # 1-7 (Monday-Sunday)
        self.day_count = 0  # Days since environment created
        self.ambient_energy = 1.0  # Base ambient energy level
        self.social_atmosphere = 0.7  # How social the environment feels
        self.novelty_level = 0.5  # How new/changing the environment is
        self.emotional_tone = 0.5  # 0=negative, 1=positive
        self.attention_scarcity = 1.0  # Multiplier for attention value
        
        # Weather system
        self.weather = "clear"
        self.temperature = 0.5  # 0=cold, 1=hot
        self.weather_effects = {
            "clear": {"energy": 0.2, "mood": 0.2},
            "cloudy": {"energy": 0.0, "mood": -0.1},
            "rainy": {"energy": -0.1, "mood": -0.1},
            "stormy": {"energy": -0.2, "mood": -0.2},
            "foggy": {"energy": -0.1, "mood": 0.0},
            "windy": {"energy": 0.1, "mood": 0.1}
        }
        
        # Resources
        self.resources = {
            "food": 100,
            "water": 100,
            "toys": 50,
            "knowledge": 100,
            "ambient_energy": self.ambient_energy
        }
        
        # Regions within the environment
        self.regions = {
            "central": {
                "name": "Central Area",
                "features": [
                    {"type": "social_hub", "strength": 0.8, "description": "A gathering place"},
                    {"type": "resource_node", "resource": "food", "amount": 50}
                ],
                "current_pets": [],
                "resources": {"food": 50, "water": 50, "ambient_energy": 1.2}
            },
            "quiet": {
                "name": "Quiet Corner",
                "features": [
                    {"type": "rest_spot", "quality": 0.9, "description": "A peaceful resting area"},
                    {"type": "knowledge_source", "topic": "general", "quality": 0.7}
                ],
                "current_pets": [],
                "resources": {"knowledge": 30, "ambient_energy": 0.8}
            },
            "play": {
                "name": "Play Zone",
                "features": [
                    {"type": "playground", "fun_level": 0.9, "description": "An exciting play area"},
                    {"type": "toy_collection", "variety": 0.8, "count": 20}
                ],
                "current_pets": [],
                "resources": {"toys": 30, "food": 10, "ambient_energy": 1.5}
            }
        }
        
        # Pet projections in environment
        self.pet_projections = defaultdict(dict)  # pet_id -> {projection_id: projection}
        
        # Active events affecting the environment
        self.active_events = []
        
        # Environment history
        self.history = []
        
    def step(self, time_increment=0.25):
        """Update environment state for one time step"""
        # Update time (increment in hours)
        self.time_of_day += time_increment
        if self.time_of_day >= 24:
            self.time_of_day -= 24
            self.day_of_week = (self.day_of_week % 7) + 1
            self.day_count += 1
        
        # Update weather
        self._update_weather()
        
        # Update resources
        self._update_resources()
        
        # Decay novelty level (gradually becomes less novel)
        self.novelty_level = max(0.1, self.novelty_level * 0.99)
        
        # Process active events
        self._process_events()
        
        # Record history
        self._record_state()
        
        return self.get_state()
    
    def _update_weather(self):
        """Update weather conditions"""
        # Simple weather transitions
        weather_transitions = {
            "clear": {"clear": 0.7, "cloudy": 0.25, "windy": 0.05},
            "cloudy": {"clear": 0.2, "cloudy": 0.5, "rainy": 0.25, "foggy": 0.05},
            "rainy": {"cloudy": 0.3, "rainy": 0.5, "stormy": 0.2},
            "stormy": {"rainy": 0.3, "stormy": 0.5, "cloudy": 0.2},
            "foggy": {"foggy": 0.6, "cloudy": 0.3, "clear": 0.1},
            "windy": {"windy": 0.5, "clear": 0.3, "cloudy": 0.2}
        }
        
        # Get possible transitions
        if self.weather in weather_transitions:
            transitions = weather_transitions[self.weather]
            
            # Random transition based on probabilities
            r = random.random()
            cumulative_prob = 0
            for weather, prob in transitions.items():
                cumulative_prob += prob
                if r <= cumulative_prob:
                    self.weather = weather
                    break
        
        # Update temperature with some persistence
        self.temperature = 0.8 * self.temperature + 0.2 * random.random()
        
        # Time of day affects ambient energy
        hour = self.time_of_day
        if 6 <= hour < 18:  # Daytime
            day_energy = 0.6 + 0.4 * (1 - abs((hour - 12) / 6))  # Peak at noon
            self.ambient_energy = day_energy * (0.8 + 0.4 * random.random())
        else:  # Nighttime
            night_energy = 0.2 + 0.1 * random.random()
            self.ambient_energy = night_energy
        
        # Weather effects
        if self.weather == "stormy":
            self.ambient_energy *= 0.7
        elif self.weather == "clear" and 10 <= hour < 14:  # Sunny midday
            self.ambient_energy *= 1.3
    
    def _update_resources(self):
        """Update resource levels"""
        # Base resource regeneration
        self.resources["food"] = min(100, self.resources["food"] + 0.5)
        self.resources["water"] = min(100, self.resources["water"] + 0.8)
        self.resources["toys"] = min(50, self.resources["toys"] + 0.2)
        self.resources["knowledge"] = min(100, self.resources["knowledge"] + 0.3)
        
        # Update ambient energy in resources
        self.resources["ambient_energy"] = self.ambient_energy
        
        # Update region resources
        for region_id, region in self.regions.items():
            # Each region regenerates resources at different rates
            if "resources" in region:
                if "food" in region["resources"]:
                    region["resources"]["food"] = min(50, region["resources"]["food"] + 0.3)
                if "water" in region["resources"]:
                    region["resources"]["water"] = min(50, region["resources"]["water"] + 0.5)
                if "toys" in region["resources"]:
                    region["resources"]["toys"] = min(30, region["resources"]["toys"] + 0.1)
                
                # Region ambient energy follows global but with local variations
                if "ambient_energy" in region["resources"]:
                    local_factor = 1.0
                    if region_id == "central":
                        local_factor = 1.2
                    elif region_id == "quiet":
                        local_factor = 0.8
                    elif region_id == "play":
                        local_factor = 1.5
                    
                    region["resources"]["ambient_energy"] = self.ambient_energy * local_factor
    
    def _process_events(self):
        """Process active environmental events"""
        # Remove expired events
        self.active_events = [event for event in self.active_events if event["duration"] > 0]
        
        # Apply event effects
        for event in self.active_events:
            event["duration"] -= 1
            
            # Apply different effects based on event type
            if event["type"] == "weather_event":
                self.weather = event["weather_type"]
            elif event["type"] == "resource_boost":
                resource = event["resource"]
                if resource in self.resources:
                    self.resources[resource] += event["amount"]
            elif event["type"] == "novelty_spike":
                self.novelty_level = min(1.0, self.novelty_level + event["intensity"])
    
    def _record_state(self):
        """Record current environment state to history"""
        state = {
            "timestamp": time.time(),
            "time_of_day": self.time_of_day,
            "day_count": self.day_count,
            "weather": self.weather,
            "ambient_energy": self.ambient_energy,
            "novelty_level": self.novelty_level,
            "active_events": len(self.active_events),
            "pet_projections": sum(len(projs) for projs in self.pet_projections.values()),
            "total_resources": sum(amount for res, amount in self.resources.items() if res != "ambient_energy")
        }
        
        self.history.append(state)
        if len(self.history) > 1000:  # Limit history size
            self.history = self.history[-1000:]
    
    def get_state(self):
        """Get the current state of the environment"""
        return {
            "time_of_day": self.time_of_day,
            "day_of_week": self.day_of_week,
            "day_count": self.day_count,
            "weather": self.weather,
            "temperature": self.temperature,
            "weather_effects": self.weather_effects[self.weather],
            "ambient_energy": self.ambient_energy,
            "social_atmosphere": self.social_atmosphere,
            "novelty_level": self.novelty_level,
            "emotional_tone": self.emotional_tone,
            "attention_scarcity": self.attention_scarcity,
            "resources": self.resources,
            "regions": self.regions,
            "active_events": [{"type": e["type"], "remaining": e["duration"]} for e in self.active_events]
        }
    
    def add_pet_projection(self, pet_id, projection):
        """Add a pet projection to the environment"""
        projection_id = projection.get("id", f"proj_{random.randint(1000, 9999)}")
        self.pet_projections[pet_id][projection_id] = projection
        
        # Update region if specified
        if "region_id" in projection:
            region_id = projection["region_id"]
            if region_id in self.regions:
                # Region is affected by projection
                if "projections" not in self.regions[region_id]:
                    self.regions[region_id]["projections"] = {}
                
                self.regions[region_id]["projections"][projection_id] = {
                    "pet_id": pet_id,
                    "type": projection["type"],
                    "effects": self._calculate_projection_effects(projection)
                }
        
        # New projections increase novelty
        self.novelty_level = min(1.0, self.novelty_level + 0.1)
        
        return {"success": True, "projection_id": projection_id}
    
    def remove_pet_projection(self, pet_id, projection_id):
        """Remove a pet projection from the environment"""
        if pet_id in self.pet_projections and projection_id in self.pet_projections[pet_id]:
            projection = self.pet_projections[pet_id][projection_id]
            
            # Remove from region if necessary
            if "region_id" in projection:
                region_id = projection["region_id"]
                if region_id in self.regions and "projections" in self.regions[region_id]:
                    if projection_id in self.regions[region_id]["projections"]:
                        del self.regions[region_id]["projections"][projection_id]
            
            # Remove from pet projections
            del self.pet_projections[pet_id][projection_id]
            
            return {"success": True}
        
        return {"success": False, "reason": "projection_not_found"}
    
    def _calculate_projection_effects(self, projection):
        """Calculate effects of a pet projection on the environment"""
        effects = {}
        
        if projection["type"] == "territorial_marker":
            effects["territory_claim"] = 0.5 * projection.get("stability", 0.5)
            effects["pet_presence"] = 0.3 * projection.get("stability", 0.5)
        
        elif projection["type"] == "social_signal":
            effects["social_presence"] = 0.7 * projection.get("stability", 0.5)
            effects["communication"] = 0.5 * projection.get("stability", 0.5)
            
            # Social signals affect the social atmosphere
            self.social_atmosphere = min(1.0, self.social_atmosphere + 0.05)
        
        elif projection["type"] == "knowledge_share":
            effects["shared_knowledge"] = 0.6 * projection.get("stability", 0.5)
            effects["teaching"] = 0.4 * projection.get("stability", 0.5)
            
            # Knowledge sharing increases resource
            if "knowledge" in self.resources:
                self.resources["knowledge"] = min(100, self.resources["knowledge"] + 2)
        
        return effects
    
    def update_pet_location(self, pet_id, region_id):
        """Update which region a pet is in"""
        # Remove pet from previous regions
        for region in self.regions.values():
            if "current_pets" in region and pet_id in region["current_pets"]:
                region["current_pets"].remove(pet_id)
        
        # Add pet to new region
        if region_id in self.regions:
            if "current_pets" not in self.regions[region_id]:
                self.regions[region_id]["current_pets"] = []
            
            self.regions[region_id]["current_pets"].append(pet_id)
            return {"success": True, "region": self.regions[region_id]["name"]}
        
        return {"success": False, "reason": "region_not_found"}
    
    def consume_resources(self, region_id, resources_to_consume):
        """Consume resources from a specific region"""
        if region_id not in self.regions:
            return {"success": False, "reason": "region_not_found"}
        
        region = self.regions[region_id]
        if "resources" not in region:
            return {"success": False, "reason": "no_resources_in_region"}
        
        consumed = {}
        for resource, amount in resources_to_consume.items():
            if resource in region["resources"] and region["resources"][resource] >= amount:
                region["resources"][resource] -= amount
                consumed[resource] = amount
            else:
                consumed[resource] = 0  # Couldn't consume any
        
        return {"success": True, "consumed": consumed}
    
    def add_event(self, event_type, duration, **params):
        """Add an event to the environment"""
        event = {
            "type": event_type,
            "duration": duration,
            "created_at": time.time(),
            **params
        }
        
        self.active_events.append(event)
        
        # Events increase novelty
        self.novelty_level = min(1.0, self.novelty_level + 0.15)
        
        return {"success": True, "event_id": len(self.active_events) - 1}
    
    def get_pet_view(self, pet_id, permeability=0.5):
        """
        Get a pet-specific view of the environment
        
        The permeability affects how much environmental detail the pet perceives
        """
        base_state = self.get_state()
        
        # Adjust perception based on permeability
        if permeability < 0.3:
            # Low permeability - limited perception
            return {
                "time_of_day": base_state["time_of_day"],
                "weather": base_state["weather"],
                "ambient_energy": base_state["ambient_energy"] * permeability * 2,  # Still get some energy
                "current_region": self._get_pet_region(pet_id)
            }
        elif permeability < 0.7:
            # Medium permeability - moderate perception
            pet_view = {
                "time_of_day": base_state["time_of_day"],
                "day_of_week": base_state["day_of_week"],
                "weather": base_state["weather"],
                "weather_effects": base_state["weather_effects"],
                "ambient_energy": base_state["ambient_energy"],
                "social_atmosphere": base_state["social_atmosphere"],
                "current_region": self._get_pet_region(pet_id),
                "regions": {r_id: r for r_id, r in base_state["regions"].items() if "current_pets" in r and pet_id in r["current_pets"]}
            }
            
            # Add partial info about other regions
            for r_id, region in base_state["regions"].items():
                if r_id not in pet_view["regions"]:
                    pet_view["regions"][r_id] = {
                        "name": region["name"],
                        "features": [f for f in region.get("features", []) if random.random() < permeability]
                    }
            
            return pet_view
        else:
            # High permeability - full perception
            pet_view = base_state.copy()
            
            # Add info about competing pets
            other_pets = []
            for r_id, region in base_state["regions"].items():
                if "current_pets" in region:
                    for other_pet_id in region["current_pets"]:
                        if other_pet_id != pet_id:
                            other_pets.append({"id": other_pet_id, "location": r_id})
            
            pet_view["competing_pets"] = other_pets
            pet_view["current_region"] = self._get_pet_region(pet_id)
            
            return pet_view
    
    def _get_pet_region(self, pet_id):
        """Get the current region of a pet"""
        for region_id, region in self.regions.items():
            if "current_pets" in region and pet_id in region["current_pets"]:
                return region_id
        return None


class ObservableCognitiveDevelopment:
    """
    System for making cognitive development observable and interactive
    
    This connects pet boundary systems with their observable cognitive growth,
    making the evolution of their intelligence visible to users.
    """
    
    def __init__(self, pet_id):
        self.pet_id = pet_id
        self.cognitive_areas = {
            "pattern_recognition": 0.1,  # Starting values
            "memory_capacity": 0.1,
            "social_intelligence": 0.1,
            "problem_solving": 0.1,
            "language_processing": 0.1,
            "environmental_awareness": 0.1,
            "creativity": 0.1
        }
        self.recent_developments = []  # Observable cognitive achievements
        self.learning_rate = 0.01  # Base learning rate
        self.last_interaction_type = None  # What type of interaction last occurred
        self.developmental_stage = "basic"  # cognitive development stage
    
    def process_experience(self, experience_type, intensity, traits):
        """Process an experience and potentially develop cognitive abilities"""
        # Different experiences develop different cognitive areas
        affected_areas = self._map_experience_to_areas(experience_type)
        
        # Calculate learning amount based on intensity and traits
        base_learning = intensity * self.learning_rate
        trait_modifier = 1.0
        
        if "openness" in traits:
            trait_modifier += (traits["openness"] - 0.5) * 0.5
        if "curiosity" in traits:
            trait_modifier += (traits["curiosity"] - 0.5) * 0.8
            
        # Apply learning to relevant cognitive areas
        developments = []
        for area, influence in affected_areas.items():
            if area in self.cognitive_areas:
                old_value = self.cognitive_areas[area]
                learning = base_learning * influence * trait_modifier
                
                # Learning becomes harder as cognitive ability increases
                difficulty_factor = 1.0 - (old_value ** 2)
                adjusted_learning = learning * difficulty_factor
                
                self.cognitive_areas[area] = min(1.0, old_value + adjusted_learning)
                
                # Check for notable developments
                if self._check_for_development(area, old_value, self.cognitive_areas[area]):
                    development = self._generate_development_description(area, self.cognitive_areas[area])
                    developments.append(development)
                    self.recent_developments.append(development)
        
        # Update development stage if needed
        self._update_developmental_stage()
        
        # Keep only recent developments
        if len(self.recent_developments) > 10:
            self.recent_developments = self.recent_developments[-10:]
            
        return {
            "cognitive_areas": self.cognitive_areas,
            "new_developments": developments,
            "developmental_stage": self.developmental_stage
        }
    
    def _map_experience_to_areas(self, experience_type):
        """Map different types of experiences to cognitive areas they develop"""
        mappings = {
            "play": {
                "pattern_recognition": 0.7,
                "problem_solving": 0.5,
                "creativity": 0.8
            },
            "social_interaction": {
                "social_intelligence": 0.9,
                "language_processing": 0.6,
                "memory_capacity": 0.3
            },
            "exploration": {
                "environmental_awareness": 0.8,
                "pattern_recognition": 0.5,
                "problem_solving": 0.4
            },
            "learning": {
                "language_processing": 0.7,
                "memory_capacity": 0.6,
                "problem_solving": 0.5
            },
            "observation": {
                "pattern_recognition": 0.6,
                "environmental_awareness": 0.7,
                "social_intelligence": 0.3
            },
            "boundary_challenge": {  # When boundary is tested
                "environmental_awareness": 0.8,
                "pattern_recognition": 0.4,
                "problem_solving": 0.6
            },
            "assimilation": {  # When assimilating environmental elements
                "memory_capacity": 0.7,
                "pattern_recognition": 0.5,
                "creativity": 0.4
            }
        }
        
        # Default if experience type not found
        if experience_type not in mappings:
            return {
                "pattern_recognition": 0.3,
                "memory_capacity": 0.3,
                "problem_solving": 0.3
            }
            
        return mappings[experience_type]
    
    def _check_for_development(self, area, old_value, new_value):
        """Check if there's been a significant cognitive development"""
        # Development thresholds - passing these is significant
        thresholds = [0.2, 0.4, 0.6, 0.8, 0.95]
        
        for threshold in thresholds:
            if old_value < threshold and new_value >= threshold:
                return True
                
        return False
    
    def _generate_development_description(self, area, level):
        """Generate a description of cognitive development"""
        descriptions = {
            "pattern_recognition": [
                "is beginning to recognize simple patterns",
                "can now identify complex recurring patterns",
                "has developed advanced pattern recognition",
                "shows remarkable ability to identify subtle patterns",
                "demonstrates exceptional pattern recognition abilities"
            ],
            "memory_capacity": [
                "can remember recent interactions",
                "has developed short-term memory for complex events",
                "shows significant memory retention capabilities",
                "demonstrates impressive long-term memory",
                "has exceptional memory recall and storage"
            ],
            "social_intelligence": [
                "is beginning to recognize other pets",
                "understands basic social interactions",
                "can interpret social dynamics effectively",
                "demonstrates advanced empathy and social awareness",
                "shows remarkable ability to navigate complex social situations"
            ],
            "problem_solving": [
                "attempts to solve simple problems",
                "can solve straightforward problems consistently",
                "tackles moderately complex challenges",
                "shows advanced problem-solving strategies",
                "demonstrates exceptional creative problem-solving"
            ],
            "language_processing": [
                "understands basic commands",
                "processes complex instructions",
                "has developed nuanced communication understanding",
                "shows sophisticated language comprehension",
                "demonstrates exceptional linguistic intelligence"
            ],
            "environmental_awareness": [
                "notices immediate surroundings",
                "understands how to navigate different regions",
                "can predict environmental changes",
                "shows detailed awareness of the environment",
                "demonstrates exceptional environmental intelligence"
            ],
            "creativity": [
                "shows basic creative responses",
                "demonstrates creative approaches to play",
                "develops unique interaction patterns",
                "shows impressive creative problem-solving",
                "demonstrates exceptional creative intelligence"
            ]
        }
        
        # Select appropriate description based on level
        index = min(4, int(level * 5))
        description = descriptions[area][index]
        
        return {
            "area": area,
            "level": level,
            "description": f"{self.pet_id} {description}",
            "timestamp": time.time()
        }
    
    def _update_developmental_stage(self):
        """Update the overall developmental stage based on cognitive areas"""
        avg_cognitive = sum(self.cognitive_areas.values()) / len(self.cognitive_areas)
        
        if avg_cognitive < 0.2:
            self.developmental_stage = "basic"
        elif avg_cognitive < 0.4:
            self.developmental_stage = "developing"
        elif avg_cognitive < 0.6:
            self.developmental_stage = "intermediate"
        elif avg_cognitive < 0.8:
            self.developmental_stage = "advanced"
        else:
            self.developmental_stage = "exceptional"
    
    def get_status(self):
        """Get the current status of cognitive development"""
        return {
            "pet_id": self.pet_id,
            "cognitive_areas": self.cognitive_areas,
            "avg_cognitive_level": sum(self.cognitive_areas.values()) / len(self.cognitive_areas),
            "developmental_stage": self.developmental_stage,
            "recent_developments": self.recent_developments
        }
