"""
Fluid Boundary System - Manages the boundary between digital pets and their environment
"""
import time
import random
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class FluidBoundarySystem:
    """
    System for managing the fluid boundary between pet and environment
    
    The boundary is a dynamic, energy-consuming interface that determines:
    - How permeable the pet is to environmental influences
    - How much energy the pet spends maintaining its identity
    - What environmental elements can be assimilated into the pet's self
    """
    
    def __init__(self, pet_id, initial_energy=100):
        self.pet_id = pet_id
        self.boundary_energy = initial_energy  # Energy available for boundary maintenance
        self.boundary_permeability = 0.5  # How easily environmental factors affect the pet
        self.boundary_size = 1.0  # Relative size/extent of boundary
        self.assimilated_elements = {}  # Environmental elements incorporated into self
        self.boundary_maintenance_cost = 0.1  # Base energy cost per tick
        self.boundary_history = []  # Track boundary changes over time
    
    def update(self, environment_state, available_energy):
        """Update boundary based on environment and available energy"""
        # Calculate base maintenance cost (proportional to boundary size)
        base_cost = self.boundary_maintenance_cost * self.boundary_size
        
        # Additional costs based on environmental pressure
        environmental_pressure = self._calculate_environmental_pressure(environment_state)
        total_cost = base_cost * (1 + environmental_pressure)
        
        # Check if we have enough energy
        if available_energy < total_cost:
            # Boundary failure - become more permeable
            self.boundary_permeability = min(1.0, self.boundary_permeability + 0.1)
            self.boundary_size = max(0.2, self.boundary_size - 0.05)
            boundary_status = "failing"
        else:
            # Successful maintenance
            self.boundary_permeability = max(0.1, self.boundary_permeability - 0.01)
            boundary_status = "maintained"
        
        # Record boundary state
        self.boundary_history.append({
            "timestamp": time.time(),
            "permeability": self.boundary_permeability,
            "size": self.boundary_size,
            "cost": total_cost,
            "status": boundary_status
        })
        
        # Limit history size
        if len(self.boundary_history) > 100:
            self.boundary_history = self.boundary_history[-100:]
        
        # Return energy consumed and boundary status
        return {
            "energy_consumed": min(total_cost, available_energy),
            "boundary_status": boundary_status,
            "permeability": self.boundary_permeability,
            "size": self.boundary_size
        }
    
    def _calculate_environmental_pressure(self, environment_state):
        """Calculate how much the environment is pressuring the boundary"""
        # Different environmental factors create different pressures
        pressure = 0
        
        if "weather" in environment_state:
            weather = environment_state["weather"]
            if weather in ["stormy", "extreme"]:
                pressure += 0.3
            elif weather in ["rainy", "windy"]:
                pressure += 0.1
        
        if "emotional_tone" in environment_state:
            # Extreme emotional environments require more boundary maintenance
            emotional_tone = environment_state["emotional_tone"]
            emotional_pressure = abs(emotional_tone - 0.5) * 0.4
            pressure += emotional_pressure
        
        if "competing_pets" in environment_state:
            # More competing pets = more boundary pressure
            num_competing = len(environment_state["competing_pets"])
            pressure += 0.05 * num_competing
            
        if "social_atmosphere" in environment_state:
            # Social environments can increase pressure for introverted pets
            social_atmosphere = environment_state["social_atmosphere"]
            pressure += social_atmosphere * 0.2
            
        if "novelty_level" in environment_state:
            # High novelty environments increase pressure
            novelty = environment_state["novelty_level"]
            pressure += novelty * 0.15
        
        return pressure
    
    def attempt_assimilation(self, environmental_element, difficulty=0.5):
        """Attempt to assimilate an environmental element into self"""
        # Check if we have a permeable enough boundary to assimilate
        if self.boundary_permeability < 0.2:
            return {"success": False, "reason": "boundary_too_rigid"}
        
        # Calculate success chance based on permeability and difficulty
        success_chance = self.boundary_permeability * (1 - difficulty)
        
        if random.random() < success_chance:
            # Successful assimilation
            element_id = f"element_{len(self.assimilated_elements) + 1}"
            self.assimilated_elements[element_id] = {
                "type": environmental_element["type"],
                "properties": environmental_element["properties"],
                "assimilated_at": time.time()
            }
            
            # Assimilation temporarily increases boundary size
            self.boundary_size = min(2.0, self.boundary_size + 0.1)
            
            return {
                "success": True, 
                "element_id": element_id,
                "boundary_growth": 0.1
            }
        else:
            return {"success": False, "reason": "assimilation_failed"}
    
    def release_element(self, element_id):
        """Release a previously assimilated element back to environment"""
        if element_id not in self.assimilated_elements:
            return {"success": False, "reason": "element_not_found"}
        
        element = self.assimilated_elements[element_id]
        del self.assimilated_elements[element_id]
        
        # Releasing elements reduces boundary size
        self.boundary_size = max(0.5, self.boundary_size - 0.05)
        
        return {
            "success": True,
            "released_element": element,
            "boundary_reduction": 0.05
        }
    
    def get_status(self):
        """Get the current status of the boundary system"""
        return {
            "pet_id": self.pet_id,
            "boundary_permeability": self.boundary_permeability,
            "boundary_size": self.boundary_size,
            "assimilated_elements_count": len(self.assimilated_elements),
            "boundary_stability": 1.0 - self.boundary_permeability,
            "recent_history": self.boundary_history[-5:] if self.boundary_history else []
        }


class EnvironmentalExchangeSystem:
    """Handles exchange of elements between pet and environment"""
    
    def __init__(self, pet_id, boundary_system):
        self.pet_id = pet_id
        self.boundary_system = boundary_system
        self.internal_elements = {}  # Elements that have become part of the pet
        self.external_projections = {}  # Parts of the pet projected into environment
        self.exchange_history = []
    
    def scan_environment(self, environment_state):
        """Scan environment for elements that could be assimilated"""
        assimilable_elements = []
        
        # Check each region for assimilable elements
        if "regions" in environment_state:
            for region_id, region in environment_state["regions"].items():
                # Features might be assimilable
                if "features" in region:
                    for feature in region["features"]:
                        # Determine if this feature can be assimilated
                        if self._is_assimilable(feature):
                            assimilable_elements.append({
                                "type": "feature",
                                "id": feature.get("id", "unknown"),
                                "properties": feature,
                                "location": region_id,
                                "difficulty": 0.6  # Features are harder to assimilate
                            })
                
                # Resources might be assimilable
                if "resources" in region:
                    for resource_name, amount in region["resources"].items():
                        if amount > 0 and self._is_assimilable({"type": "resource", "name": resource_name}):
                            assimilable_elements.append({
                                "type": "resource",
                                "id": resource_name,
                                "properties": {"name": resource_name, "amount": amount},
                                "location": region_id,
                                "difficulty": 0.3  # Resources are easier to assimilate
                            })
        
        # Other pets might have projections that can be assimilated
        if "other_pets" in environment_state:
            for pet_data in environment_state["other_pets"]:
                if "projections" in pet_data and pet_data["id"] != self.pet_id:
                    for proj_id, projection in pet_data["projections"].items():
                        if self._is_assimilable(projection):
                            assimilable_elements.append({
                                "type": "pet_projection",
                                "id": proj_id,
                                "source_pet": pet_data["id"],
                                "properties": projection,
                                "location": pet_data.get("location", "unknown"),
                                "difficulty": 0.7  # Pet projections are quite difficult to assimilate
                            })
        
        # Look for environmental resources that can be assimilated
        if "ambient_energy" in environment_state:
            assimilable_elements.append({
                "type": "ambient_energy",
                "id": "ambient_energy",
                "properties": {"amount": environment_state["ambient_energy"]},
                "difficulty": 0.2  # Ambient energy is easy to assimilate
            })
            
        return assimilable_elements
    
    def _is_assimilable(self, element):
        """Determine if an element can be assimilated based on pet's state"""
        # Implementation depends on pet traits, current state, etc.
        # For now, a simple check based on element type
        if isinstance(element, dict):
            if element.get("type") == "feature":
                # Can assimilate features if they're not too complex
                complexity = element.get("complexity", 0.5)
                return complexity < 0.8
            
            elif element.get("type") == "resource":
                # Can assimilate most resources
                return True
            
            elif element.get("type") == "pet_projection":
                # Can only assimilate compatible pet projections
                compatibility = self._check_projection_compatibility(element)
                return compatibility > 0.3
        
        return False
    
    def _check_projection_compatibility(self, projection):
        """Check if a pet projection is compatible with this pet"""
        # Implementation would compare pet traits with projection properties
        return 0.5  # Placeholder
    
    def assimilate_element(self, element):
        """Attempt to assimilate an environmental element"""
        # Check boundary permeability
        result = self.boundary_system.attempt_assimilation(element, difficulty=element["difficulty"])
        
        if not result["success"]:
            return result
        
        # Successfully assimilated - add to internal elements
        element_id = result["element_id"]
        self.internal_elements[element_id] = {
            "original": element,
            "assimilated_at": time.time(),
            "integration_level": 0.1,  # Starts barely integrated
            "effects": self._calculate_element_effects(element)
        }
        
        # Record the exchange
        self.exchange_history.append({
            "type": "assimilation",
            "element": element,
            "timestamp": time.time(),
            "result": "success",
            "internal_id": element_id
        })
        
        return {
            "success": True,
            "element_id": element_id,
            "integration_level": 0.1,
            "effects": self.internal_elements[element_id]["effects"]
        }
    
    def _calculate_element_effects(self, element):
        """Calculate the effects of an assimilated element"""
        effects = {}
        
        if element["type"] == "feature":
            # Features might affect traits or abilities
            properties = element["properties"]
            if "effect" in properties:
                effects = properties["effect"]
        
        elif element["type"] == "resource":
            # Resources might provide energy or materials
            resource_name = element["properties"]["name"]
            amount = element["properties"]["amount"]
            
            if resource_name == "food":
                effects["energy"] = amount * 2
            elif resource_name == "knowledge":
                effects["intelligence"] = amount * 0.1
            elif resource_name == "social":
                effects["charisma"] = amount * 0.1
        
        elif element["type"] == "pet_projection":
            # Pet projections might affect social abilities or provide traits
            effects["social_connection"] = 0.2
            # Could copy some traits from the source pet
        
        return effects
    
    def integrate_elements(self):
        """Further integrate assimilated elements into the pet"""
        integration_results = {}
        
        for element_id, element_data in self.internal_elements.items():
            # Elements become more integrated over time
            current_level = element_data["integration_level"]
            
            # Integration chance depends on current level
            integration_chance = 0.1 * (1 - current_level)
            
            if random.random() < integration_chance:
                # Integration progresses
                new_level = min(1.0, current_level + 0.1)
                element_data["integration_level"] = new_level
                
                # Effects become stronger with integration
                effect_scale = new_level / current_level if current_level > 0 else new_level
                for effect_name, effect_value in element_data["effects"].items():
                    element_data["effects"][effect_name] = effect_value * effect_scale
                
                integration_results[element_id] = {
                    "new_level": new_level,
                    "effect_scale": effect_scale,
                    "updated_effects": element_data["effects"]
                }
        
        return integration_results
    
    def project_to_environment(self, projection_type, properties, region_id):
        """Project part of the pet into the environment"""
        # Create the projection
        projection_id = f"proj_{len(self.external_projections) + 1}"
        
        projection = {
            "id": projection_id,
            "type": projection_type,
            "properties": properties,
            "source_pet": self.pet_id,
            "created_at": time.time(),
            "region_id": region_id,
            "stability": 0.5  # Initial stability
        }
        
        # Expend energy through boundary for projection
        boundary_status = self.boundary_system.get_status()
        
        # Projecting requires a somewhat permeable boundary
        if boundary_status["boundary_permeability"] < 0.3:
            return {
                "success": False, 
                "reason": "boundary_too_rigid",
                "required_permeability": 0.3
            }
        
        # Add to external projections
        self.external_projections[projection_id] = projection
        
        # Record the exchange
        self.exchange_history.append({
            "type": "projection",
            "projection": projection,
            "timestamp": time.time(),
            "result": "success"
        })
        
        return {
            "success": True,
            "projection_id": projection_id,
            "projection": projection
        }
    
    def maintain_projections(self, environment_state):
        """Maintain projections in the environment"""
        results = {}
        projections_to_remove = []
        
        for proj_id, projection in self.external_projections.items():
            # Check if the region still exists
            region_id = projection["region_id"]
            if "regions" not in environment_state or region_id not in environment_state["regions"]:
                # Region is gone, projection fails
                projections_to_remove.append(proj_id)
                results[proj_id] = {"status": "failed", "reason": "region_not_found"}
                continue
            
            # Calculate stability change
            stability_change = self._calculate_projection_stability(projection, environment_state)
            
            # Update stability
            new_stability = max(0, min(1, projection["stability"] + stability_change))
            projection["stability"] = new_stability
            
            if new_stability <= 0:
                # Projection has dissipated
                projections_to_remove.append(proj_id)
                results[proj_id] = {"status": "dissipated", "reason": "zero_stability"}
            else:
                # Projection continues
                results[proj_id] = {
                    "status": "maintained", 
                    "stability": new_stability,
                    "stability_change": stability_change
                }
        
        # Remove failed projections
        for proj_id in projections_to_remove:
            del self.external_projections[proj_id]
        
        return results
    
    def _calculate_projection_stability(self, projection, environment_state):
        """Calculate how a projection's stability changes"""
        # Base decay
        stability_change = -0.05
        
        # Environmental factors
        region_id = projection["region_id"]
        if "regions" in environment_state and region_id in environment_state["regions"]:
            region = environment_state["regions"][region_id]
            
            # Compatible features help stability
            if "features" in region:
                for feature in region["features"]:
                    if feature.get("type") == projection["type"]:
                        stability_change += 0.02
            
            # Other pets in region might affect stability
            if "current_pets" in region:
                pet_count = len(region["current_pets"])
                if self.pet_id in region["current_pets"]:
                    # Creator present helps stability
                    stability_change += 0.05
                elif pet_count > 0:
                    # Other pets might interfere
                    stability_change -= 0.01 * pet_count
        
        return stability_change
    
    def get_projection_effects(self, projection_id):
        """Get the effects of a projection on the environment"""
        if projection_id not in self.external_projections:
            return {}
        
        projection = self.external_projections[projection_id]
        effects = {}
        
        # Different projection types have different effects
        if projection["type"] == "territorial_marker":
            effects["territory_claim"] = 0.5 * projection["stability"]
            effects["pet_presence"] = 0.3 * projection["stability"]
        
        elif projection["type"] == "social_signal":
            effects["social_presence"] = 0.7 * projection["stability"]
            effects["communication"] = 0.5 * projection["stability"]
        
        elif projection["type"] == "knowledge_share":
            effects["shared_knowledge"] = 0.6 * projection["stability"]
            effects["teaching"] = 0.4 * projection["stability"]
        
        return effects


class PetEnergySystem:
    """Manages a pet's energy economy including boundary maintenance"""
    
    def __init__(self, pet_id, initial_energy=100):
        self.pet_id = pet_id
        self.energy = initial_energy
        self.max_energy = 100
        self.energy_history = []
        self.boundary_system = FluidBoundarySystem(pet_id, initial_energy=initial_energy * 0.2)
        self.exchange_system = EnvironmentalExchangeSystem(pet_id, self.boundary_system)
        
        # Energy allocation priorities (what gets energy first)
        self.allocation_priorities = {
            "boundary_maintenance": 1,  # Highest priority
            "critical_functions": 2,
            "growth": 3,
            "social_activities": 4,
            "exploration": 5,
            "reproduction": 6  # Lowest priority
        }
    
    def step(self, environment_state):
        """Process one energy cycle"""
        # Record energy at start of cycle
        starting_energy = self.energy
        
        # Collect energy from environment
        gained_energy = self._collect_energy(environment_state)
        self.energy = min(self.max_energy, self.energy + gained_energy)
        
        # Allocate energy according to priorities
        allocations = self._allocate_energy()
        
        # Maintain boundary (always first priority)
        boundary_allocation = allocations.get("boundary_maintenance", 0)
        boundary_result = self.boundary_system.update(environment_state, boundary_allocation)
        
        # Update energy based on consumption
        self.energy -= boundary_result["energy_consumed"]
        
        # Maintain any projections in the environment
        self.exchange_system.maintain_projections(environment_state)
        
        # Record energy state
        self.energy_history.append({
            "timestamp": time.time(),
            "starting_energy": starting_energy,
            "gained_energy": gained_energy,
            "allocated_energy": allocations,
            "boundary_consumption": boundary_result["energy_consumed"],
            "ending_energy": self.energy
        })
        
        # Limit history size
        if len(self.energy_history) > 100:
            self.energy_history = self.energy_history[-100:]
        
        return {
            "energy_level": self.energy,
            "energy_percent": (self.energy / self.max_energy) * 100,
            "boundary_status": boundary_result["boundary_status"],
            "allocations": allocations
        }
    
    def _collect_energy(self, environment_state):
        """Collect energy from the environment"""
        collected = 0
        
        # Energy from environmental resources
        if "resources" in environment_state:
            resources = environment_state["resources"]
            if "food" in resources:
                # Convert food to energy based on boundary permeability
                available_food = resources["food"]
                absorption_rate = 0.5 + (self.boundary_system.boundary_permeability * 0.5)
                food_energy = available_food * absorption_rate
                collected += food_energy
            
            if "ambient_energy" in resources:
                # Ambient energy collection scales with boundary size
                ambient = resources["ambient_energy"]
                collection_efficiency = self.boundary_system.boundary_size * 0.8
                ambient_energy = ambient * collection_efficiency
                collected += ambient_energy
        
        # Direct access to ambient energy
        if "ambient_energy" in environment_state:
            ambient = environment_state["ambient_energy"]
            collection_efficiency = self.boundary_system.boundary_size * 0.6
            ambient_energy = ambient * collection_efficiency * 0.1  # Scaled down to avoid double counting
            collected += ambient_energy
        
        # Energy from assimilated elements
        element_energy = sum(0.5 for _ in self.boundary_system.assimilated_elements)
        collected += element_energy
        
        return collected
    
    def _allocate_energy(self):
        """Allocate available energy according to priorities"""
        allocations = {}
        remaining_energy = self.energy
        
        # Sort functions by priority
        priority_order = sorted(self.allocation_priorities.items(), key=lambda x: x[1])
        
        for function_name, _ in priority_order:
            # Different allocation strategies for different functions
            if function_name == "boundary_maintenance":
                # Boundary gets 20-50% depending on its status
                boundary_status = self.boundary_system.get_status()
                allocation_percent = 0.2
                if boundary_status["boundary_permeability"] > 0.7:
                    allocation_percent = 0.5  # Failing boundary gets more energy
                
                allocation = remaining_energy * allocation_percent
                
            elif function_name == "critical_functions":
                # Critical functions get 20% of what remains
                allocation = remaining_energy * 0.2
                
            elif function_name == "growth":
                # Growth gets 30% of what remains if energy is above 50%
                if self.energy > (self.max_energy * 0.5):
                    allocation = remaining_energy * 0.3
                else:
                    allocation = 0  # No growth when energy is low
                    
            elif function_name == "social_activities":
                # Social activities get 20% of what remains if energy is above 30%
                if self.energy > (self.max_energy * 0.3):
                    allocation = remaining_energy * 0.2
                else:
                    allocation = 0
            
            elif function_name == "exploration":
                # Exploration gets 15% of what remains if energy is above 40%
                if self.energy > (self.max_energy * 0.4):
                    allocation = remaining_energy * 0.15
                else:
                    allocation = 0
            
            elif function_name == "reproduction":
                # Reproduction gets all remaining energy if above 80%
                if self.energy > (self.max_energy * 0.8):
                    allocation = remaining_energy
                else:
                    allocation = 0
            
            else:
                allocation = 0
            
            allocations[function_name] = allocation
            remaining_energy -= allocation
        
        return allocations
    
    def add_energy(self, amount, source="interaction"):
        """Add energy from an external source"""
        before = self.energy
        self.energy = min(self.max_energy, self.energy + amount)
        
        self.energy_history.append({
            "timestamp": time.time(),
            "source": source,
            "amount": amount,
            "before": before,
            "after": self.energy
        })
        
        return self.energy
    
    def consume_energy(self, amount, purpose):
        """Consume energy for a specific purpose"""
        if amount > self.energy:
            return {"success": False, "reason": "insufficient_energy"}
        
        self.energy -= amount
        
        self.energy_history.append({
            "timestamp": time.time(),
            "purpose": purpose,
            "amount": -amount,
            "before": self.energy + amount,
            "after": self.energy
        })
        
        return {"success": True, "remaining_energy": self.energy}
        
    def get_assimilated_elements_effects(self):
        """Get combined effects of all assimilated elements"""
        effects = {}
        
        for element_data in self.exchange_system.internal_elements.values():
            element_effects = element_data["effects"]
            integration_level = element_data["integration_level"]
            
            # Combine effects, weighted by integration level
            for effect_name, effect_value in element_effects.items():
                weighted_value = effect_value * integration_level
                if effect_name in effects:
                    effects[effect_name] += weighted_value
                else:
                    effects[effect_name] = weighted_value
        
        return effects
