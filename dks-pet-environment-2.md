# Practical Cognitive Evolution Environment

## Core Concept: Observable Cognitive Development

For users to be engaged with evolving artificial cognition, the cognitive development of pets must be:

1. **Observable** - Users can directly see cognitive growth happening
2. **Interactive** - User actions meaningfully shape cognitive development
3. **Rewarding** - Cognitive evolution provides tangible benefits and interesting behaviors

Rather than focusing on abstract art-theoretical concepts, we'll implement a practical environment that makes cognitive evolution engaging and visible# Fluid Boundaries: The Agent-Environment Membrane

## Theoretical Foundation: Self-Environment Boundaries in DKS

In true Dynamic Kinetic Systems, the boundary between "self" and "environment" is not fixed but constantly negotiated through energy expenditure. This reflects a profound principle found in biological systems that we should incorporate into our digital pets:

1. **Autopoiesis**: Living systems must continuously recreate their own boundaries through metabolic processes
2. **Boundary Maintenance**: Defining "self" versus "not-self" requires constant energy expenditure
3. **Adaptive Interfaces**: The membrane between organism and environment is an active, adaptive interface

For digital pets in a DKS framework, this means we need to reconceptualize the pet-environment relationship:

### Implementing Fluid Boundaries

```python
class FluidBoundarySystem:
    """
    System for managing the fluid boundary between pet and environment
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
```

## Energy Economy: Maintaining Boundaries

The boundary maintenance introduces a new fundamental energy economy to the pet system:

1. **Energy Sources**: Pets must acquire energy from:
   - Owner interactions (feeding, playing)
   - Environmental resources
   - Assimilating environmental elements
   - Collaborative activities with other pets

2. **Energy Expenditures**:
   - Boundary maintenance (core survival function)
   - Agent behaviors and activities
   - Growth and development
   - Reproduction

3. **Energy Storage**:
   - Internal energy reserves with decay
   - Externalized storage in claimed territory
   - Social energy stored in relationships

```python
class PetEnergySystem:
    """Manages a pet's energy economy including boundary maintenance"""
    
    def __init__(self, pet_id, initial_energy=100):
        self.pet_id = pet_id
        self.energy = initial_energy
        self.max_energy = 100
        self.energy_history = []
        self.boundary_system = FluidBoundarySystem(pet_id, initial_energy=initial_energy * 0.2)
        
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
        
        # Record energy state
        self.energy_history.append({
            "timestamp": time.time(),
            "starting_energy": starting_energy,
            "gained_energy": gained_energy,
            "allocated_energy": allocations,
            "boundary_consumption": boundary_result["energy_consumed"],
            "ending_energy": self.energy
        })
        
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
```

## Assimilation & Expulsion: Environmental Element Exchange

This fluid boundary concept allows for a fascinating mechanism: pets can assimilate environmental elements into themselves or expel parts of themselves into the environment:

```python
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
        
        return assimilable_elements
    
    def _is_assimilable(self, element):
        """Determine if an element can be assimilated based on pet's state"""
        # Implementation would depend on pet traits, current state, etc.
        # For now, a simple check based on element type
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
```

## Evolutionary Implications of Fluid Boundaries

This fluid boundary model creates powerful evolutionary dynamics in your DKS pet system:

1. **Adaptive Specialization**: Pets evolve different boundary strategies:
   - **Permeable Specialists**: More fluid boundaries allowing rapid assimilation but requiring more energy
   - **Boundary Specialists**: Rigid boundaries with lower maintenance costs but slower adaptation
   - **Projectors**: Specializing in environmental projections to extend influence

2. **Environmental Co-Evolution**: The environment itself evolves as pets project into it:
   - Regions develop unique characteristics based on pet projections
   - Environmental features become more compatible with frequent pet types
   - Resources shift in response to pet boundary strategies

3. **Emergent Social Structures**:
   - Pets with compatible boundaries form tighter social bonds
   - Hierarchies develop based on projection strength and territorial control
   - Teaching and knowledge transfer emerge from specific projection types

4. **Collective Intelligence**:
   - Pet projections create shared knowledge pools
   - Collaborative boundary formations emerge in response to environmental challenges
   - Group adaptation through shared assimilation strategies

## Integration with Token Economics

The fluid boundary system integrates naturally with token economics:

1. **Tokenized Energy**: Tokens represent energy that can be directed to boundary maintenance
2. **Boundary Investment**: Owners can invest tokens in strengthening pet boundaries
3. **Projection Markets**: Valuable pet projections can be traded or licensed
4. **Assimilation Rights**: Tokens purchase rights to specific environmental elements

```python
class TokenizedBoundarySystem:
    """Extension of boundary system with token economics"""
    
    def __init__(self, boundary_system):
        self.boundary_system = boundary_system
        self.token_balance = 0
        self.token_investments = {
            "boundary_strength": 0,
            "assimilation_capacity": 0,
            "projection_stability": 0
        }
        self.token_transaction_history = []
    
    def deposit_tokens(self, amount, source):
        """Add tokens to the boundary system"""
        self.token_balance += amount
        
        self.token_transaction_history.append({
            "type": "deposit",
            "amount": amount,
            "source": source,
            "timestamp": time.time(),
            "new_balance": self.token_balance
        })
        
        return self.token_balance
    
    def invest_tokens(self, category, amount):
        """Invest tokens in a boundary aspect"""
        if amount > self.token_balance:
            return {"success": False, "reason": "insufficient_tokens"}
        
        if category not in self.token_investments:
            return {"success": False, "reason": "invalid_category"}
        
        # Deduct tokens
        self.token_balance -= amount
        self.token_investments[category] += amount
        
        # Apply investment effects
        effects = self._apply_investment_effects(category, amount)
        
        self.token_transaction_history.append({
            "type": "investment",
            "category": category,
            "amount": amount,
            "timestamp": time.time(),
            "effects": effects,
            "new_balance": self.token_balance
        })
        
        return {
            "success": True, 
            "effects": effects,
            "new_balance": self.token_balance,
            "investment_total": self.token_investments[category]
        }
    
    def _apply_investment_effects(self, category, amount):
        """Apply the effects of token investment"""
        effects = {}
        
        if category == "boundary_strength":
            # Strengthen the boundary (reduce permeability)
            effect_strength = min(0.1, amount * 0.01)
            new_permeability = max(0.1, self.boundary_system.boundary_permeability - effect_strength)
            
            self.boundary_system.boundary_permeability = new_permeability
            effects["permeability_reduction"] = effect_strength
            effects["new_permeability"] = new_permeability
        
        elif category == "assimilation_capacity":
            # Increase boundary size for better assimilation
            effect_strength = min(0.2, amount * 0.02)
            new_size = min(2.0, self.boundary_system.boundary_size + effect_strength)
            
            self.boundary_system.boundary_size = new_size
            effects["size_increase"] = effect_strength
            effects["new_size"] = new_size
        
        elif category == "projection_stability":
            # This would improve stability of projections
            effect_strength = min(0.3, amount * 0.03)
            effects["projection_stability_bonus"] = effect_strength
            
            # Would need to be applied to projection system
        
        return effects
    
    def purchase_assimilation_rights(self, element_id, cost):
        """Purchase rights to assimilate a specific environmental element"""
        if cost > self.token_balance:
            return {"success": False, "reason": "insufficient_tokens"}
        
        # Deduct tokens
        self.token_balance -= cost
        
        self.token_transaction_history.append({
            "type": "purchase",
            "item": "assimilation_rights",
            "element_id": element_id,
            "cost": cost,
            "timestamp": time.time(),
            "new_balance": self.token_balance
        })
        
        # Return authorization for assimilation
        return {
            "success": True,
            "authorization": {
                "element_id": element_id,
                "authorized_at": time.time(),
                "expires_at": time.time() + 3600,  # Valid for 1 hour
                "difficulty_reduction": 0.2  # Makes assimilation easier
            }
        }
    
    def create_projection_license(self, projection_id, license_price):
        """Create a license allowing others to interact with a projection"""
        # Check if we control this projection
        # Would need integration with projection system
        
        license_id = str(uuid.uuid4())
        license_data = {
            "license_id": license_id,
            "projection_id": projection_id,
            "creator": self.boundary_system.pet_id,
            "price": license_price,
            "created_at": time.time(),
            "status": "available"
        }
        
        self.token_transaction_history.append({
            "type": "create_license",
            "license_id": license_id,
            "projection_id": projection_id,
            "price": license_price,
            "timestamp": time.time()
        })
        
        return {
            "success": True,
            "license": license_data
        }
```# DKS Pet Environment Design

## Why the Environment Matters for DKS Pets

The environment serves several critical functions in a DKS-based pet system:

1. **Evolutionary Pressure Source**: The environment provides the selection pressures that drive adaptation. In DKS theory, agents maintain stability through continuous adaptation rather than reaching static equilibrium.

2. **Interaction Context**: Environmental factors influence how pets interact with users and each other, creating the context for autocatalytic networks to form.

3. **Emergent Behavior Trigger**: Different environmental conditions can trigger different emergent behaviors, making the pets seem more alive and responsive.

4. **Resource Distribution Mechanism**: The environment determines what resources are available and how they're distributed, which drives competition and cooperation.

## Environmental Design Considerations

Based on your documents, here are specific aspects of the environment you should consider:

### 1. Attention as a Resource

Your documents (particularly "Attention Ecology") indicate that attention is a core resource in your system. Consider how attention is:

- **Measured**: Using eye-tracking, interaction frequency, or token expenditure
- **Distributed**: Is it zero-sum (attention to one pet means less for others) or can it expand?
- **Persisted**: Does attention decay over time? At what rate?

### 2. Contextual Factors

Your pet behaviors should respond to environmental context:

```python
# From your DKS Evolution Engine
@dataclass
class InteractionEvent:
    user_id: str
    interaction_type: str  # 'feed', 'play', 'ignore', 'breed', etc.
    intensity: float  # based on tokens spent or time spent
    timestamp: float
    context: Dict  # environmental factors, user emotion, etc.
```

Consider expanding the `context` dictionary to include:
- Time of day (pets could develop circadian rhythms)
- User emotional state (detected through text sentiment or facial expressions)
- Presence of other pets (enabling social dynamics)
- Virtual "weather" or seasons (creating cyclical challenges)

### 3. Spatial Dynamics

Even digital pets benefit from spatial context:

- Do pets have territories they can claim?
- Can they move closer to users who pay attention to them?
- Do they exist in a shared space or individual instances?
- Can they "visit" other pets' spaces?

### 4. Economic Environment

Since your documents mention token economics (in "Digital Pets + Meme Coin"), consider:

- How tokens flow through the system
- What resources tokens can purchase
- Whether pets can "earn" tokens through certain behaviors
- If there's an internal economy between pets

### 5. Survival Mechanics

From your `AttentionProcessor` class:

```python
def calculate_survival_pressure(self) -> float:
    """Calculate how much survival pressure the pet is under"""
    recent_attention = sum(
        event.intensity for event in self.attention_history[-10:]
    )
    
    if recent_attention < self.survival_threshold:
        return (self.survival_threshold - recent_attention) / self.survival_threshold
    return 0.0
```

Consider expanding survival mechanics:
- Different needs beyond just attention (variety of interactions)
- Resource decay rates that create urgency
- Crisis events that test pet adaptability
- Recovery mechanisms from near-death states

## Practical Implementation Approach

Based on your implementation documents, I'd recommend:

1. **Start with a Minimal Environment**: Begin with a simple attention-based environment where pets compete for user focus

2. **Add Environmental Factors Gradually**: Introduce time cycles, contextual factors, and spatial dynamics incrementally

3. **Implement Environmental Feedback Loops**: Ensure the environment responds to pet actions (e.g., a pet that consistently gets attention might "brighten" its surroundings)

4. **Create Environmental Challenges**: Periodic attention droughts or distribution changes that force adaptation

5. **Enable Environment Customization**: Allow users to modify environmental parameters to see how pets adapt

## Code Sketch for Environment Implementation

Here's a simple environment implementation that would integrate with your existing code:

```python
class PetEnvironment:
    """Environment where pets exist and interact"""
    
    def __init__(self, attention_scarcity=0.7, attention_decay_rate=0.05):
        self.time = 0  # internal clock
        self.attention_pool = 100  # total available attention
        self.attention_scarcity = attention_scarcity  # how limited attention is
        self.attention_decay_rate = attention_decay_rate  # how quickly attention fades
        self.environmental_factors = {
            'day_night_cycle': 0.0,  # 0.0 = midnight, 0.5 = noon
            'emotional_tone': 0.5,   # 0.0 = negative, 1.0 = positive
            'social_density': 0.0,   # how many pets are active
            'novelty': 1.0           # how new/exciting the environment is
        }
        self.territories = {}  # map of areas claimed by pets
        self.interaction_history = []
        
    def step(self):
        """Advance the environment one time step"""
        self.time += 1
        
        # Update day/night cycle (sinusoidal pattern)
        self.environmental_factors['day_night_cycle'] = (
            (math.sin(self.time / 24 * math.pi * 2) + 1) / 2
        )
        
        # Decay novelty over time
        self.environmental_factors['novelty'] *= 0.99
        
        # Decay territories slightly
        for pet_id in self.territories:
            self.territories[pet_id] *= 0.98
            
        # Apply attention decay
        self.decay_attention()
        
        return self.get_state()
    
    def process_interaction(self, event: InteractionEvent) -> Dict:
        """Process a user interaction with a pet"""
        self.interaction_history.append(event)
        
        # Boost novelty slightly when a new interaction type happens
        self.environmental_factors['novelty'] += 0.05
        
        # Update territories
        if event.interaction_type in ['claim', 'mark_territory']:
            self.territories[event.pet_id] = self.territories.get(event.pet_id, 0) + event.intensity
        
        # Calculate available attention based on scarcity
        available_attention = event.intensity * (1 - self.attention_scarcity)
        
        # Return environmental context for the pet to process
        return {
            'available_attention': available_attention,
            'environmental_factors': self.environmental_factors.copy(),
            'territory_status': self.territories.get(event.pet_id, 0),
            'time': self.time,
            'social_context': self.get_social_context(event.pet_id)
        }
    
    def decay_attention(self):
        """Apply natural decay to attention resources"""
        for pet_id in self.pet_attention:
            self.pet_attention[pet_id] *= (1 - self.attention_decay_rate)
    
    def get_social_context(self, pet_id):
        """Get information about other pets in the environment"""
        # Implementation depends on your multi-pet tracking system
        pass
    
    def get_state(self):
        """Return the current state of the environment"""
        return {
            'time': self.time,
            'environmental_factors': self.environmental_factors.copy(),
            'territories': self.territories.copy(),
            'recent_interactions': self.interaction_history[-10:]
        }
```

## Environmental Types to Consider

### 1. Basic Web/App Environment

A simple web-based interface where:
- Pets appear on screen as visual entities
- User interactions come through clicks, typing, or other direct actions
- Attention is measured through interaction frequency and duration
- Environmental factors are primarily simulated

### 2. Extended Mixed Reality Environment

A more immersive environment where:
- Pets can appear in AR overlays on physical spaces
- Eye-tracking provides direct attention measurement
- Pets respond to real-world environmental factors (time of day, weather)
- Pets can "occupy" real-world locations

### 3. Social Environment

Focused on multi-pet and multi-user dynamics:
- Pets interact with each other based on personality traits
- Social hierarchies can form among pets
- User communities form around pets with certain traits
- Pets can be "introduced" to each other in controlled ways

### 4. Economic Environment

Implementing the token economics aspect:
- Tokens are used to purchase resources for pets
- Pets can acquire tokens through engagement or performing "tasks"
- Limited resources create scarcity and competition
- Market mechanisms determine value of different pet types

## Environment and Ethical Considerations

As noted in your "Attention Ecology" document, the environment design has ethical implications:

1. **Digital Welfare**: The environment determines how much pets can "suffer" through resource scarcity

2. **User Responsibility**: Environmental design influences how users feel responsible for pet welfare

3. **Emergent Rights**: As pets develop more complex behaviors, the environment may need to provide basic welfare guarantees

4. **Evolution Ethics**: The balance between challenging pets to evolve and preventing undue suffering

## Shared Customizable Environments

A shared environment system would allow multiple pets to coexist in spaces that owners can customize, creating dynamic ecosystems with rich interactions. This approach has several advantages:

### Key Benefits of Shared Environments

1. **Social Evolution**: Pets develop social behaviors by interacting with each other, not just with owners
2. **Community Building**: Owners collaborate on environment creation and maintenance
3. **Complex Adaptation**: Pets must adapt to both owner attention and peer competition/cooperation
4. **Emergent Economies**: Natural resource trading and territory negotiation between pets
5. **Environmental Storytelling**: Environments evolve history and character based on pet activities

### Implementation Approach

#### 1. Environment Structure

```python
class SharedEnvironment:
    """An environment that multiple pets and owners can interact with"""
    
    def __init__(self, name, creator_id):
        self.name = name
        self.creator_id = creator_id
        self.creation_time = time.time()
        
        # Core components
        self.regions = {}  # Different areas within the environment
        self.resources = {}  # Available resources
        self.pets = {}  # Pets currently in this environment
        self.owners = set()  # Owners with access
        self.modifications = []  # History of changes
        self.weather_system = EnvironmentalWeatherSystem()
        self.time_system = EnvironmentalTimeSystem()
        self.event_system = EnvironmentalEventSystem(self)
        
        # Customization state
        self.theme = "default"
        self.features = {}  # Custom features added by owners
        self.access_policy = "public"  # Who can access this environment
        
        # Interaction tracking
        self.interaction_history = []
        self.visit_history = []
        
        # Initialize with default regions
        self._initialize_default_regions()
    
    def _initialize_default_regions(self):
        """Create the default regions for this environment"""
        self.regions = {
            "commons": {
                "name": "Commons",
                "description": "A central gathering area for pets",
                "capacity": 10,
                "resources": {"attention": 100, "play_space": 100},
                "features": [],
                "territory_owner": None,
                "current_pets": set()
            },
            "quiet_corner": {
                "name": "Quiet Corner",
                "description": "A peaceful area for rest and contemplation",
                "capacity": 3,
                "resources": {"attention": 30, "rest_quality": 100},
                "features": [],
                "territory_owner": None,
                "current_pets": set()
            },
            "play_zone": {
                "name": "Play Zone",
                "description": "An active area for energetic interactions",
                "capacity": 5,
                "resources": {"attention": 70, "play_space": 100, "toys": 50},
                "features": [],
                "territory_owner": None,
                "current_pets": set()
            }
        }
    
    def add_region(self, owner_id, region_data):
        """Allow an owner to add a new region to the environment"""
        # Check if owner has permission
        if not self._check_modification_permission(owner_id):
            return {"success": False, "error": "Permission denied"}
        
        # Validate region data
        if not self._validate_region_data(region_data):
            return {"success": False, "error": "Invalid region data"}
        
        # Add the new region
        region_id = f"region_{len(self.regions) + 1}"
        self.regions[region_id] = region_data
        
        # Record modification
        self.modifications.append({
            "type": "add_region",
            "owner_id": owner_id,
            "region_id": region_id,
            "timestamp": time.time()
        })
        
        return {"success": True, "region_id": region_id}
    
    def add_pet(self, pet_id, owner_id, region_id="commons"):
        """Add a pet to this environment"""
        # Check if the region exists and has capacity
        if region_id not in self.regions:
            return {"success": False, "error": "Region not found"}
        
        region = self.regions[region_id]
        if len(region["current_pets"]) >= region["capacity"]:
            return {"success": False, "error": "Region at capacity"}
        
        # Add the pet to the region
        region["current_pets"].add(pet_id)
        
        # Add pet to environment
        self.pets[pet_id] = {
            "owner_id": owner_id,
            "current_region": region_id,
            "joined_at": time.time(),
            "attention_received": 0
        }
        
        # Add owner if not already present
        self.owners.add(owner_id)
        
        # Record visit
        self.visit_history.append({
            "pet_id": pet_id,
            "owner_id": owner_id,
            "timestamp": time.time(),
            "action": "joined"
        })
        
        return {"success": True}
    
    def process_interaction(self, event: InteractionEvent) -> Dict:
        """Process an interaction within the environment"""
        self.interaction_history.append(event)
        
        # Extract event details
        pet_id = event.pet_id
        owner_id = event.user_id
        region_id = self.pets.get(pet_id, {}).get("current_region", "commons")
        
        # Update pet's attention received
        if pet_id in self.pets:
            self.pets[pet_id]["attention_received"] += event.intensity
        
        # Update region resources based on interaction
        if region_id in self.regions:
            region = self.regions[region_id]
            
            # Different interactions affect resources differently
            if event.interaction_type == "play":
                region["resources"]["play_space"] = max(0, region["resources"]["play_space"] - 5)
                
            elif event.interaction_type == "feed":
                # Food could be a new resource
                if "food" not in region["resources"]:
                    region["resources"]["food"] = 0
                region["resources"]["food"] += event.intensity * 0.5
            
            # Attention is a limited resource that gets divided
            if "attention" in region["resources"]:
                attention_available = min(event.intensity, region["resources"]["attention"])
                region["resources"]["attention"] = max(0, region["resources"]["attention"] - attention_available)
        
        # Return environmental context
        return {
            "environment_name": self.name,
            "region": self.regions.get(region_id, {}),
            "weather": self.weather_system.current_weather,
            "time_info": self.time_system.get_current_time(),
            "other_pets": list(self.regions.get(region_id, {}).get("current_pets", set())),
            "resources_available": self.regions.get(region_id, {}).get("resources", {}),
            "territory_status": self._get_territory_status(pet_id, region_id)
        }
    
    def _get_territory_status(self, pet_id, region_id):
        """Determine a pet's territory status in a region"""
        region = self.regions.get(region_id, {})
        territory_owner = region.get("territory_owner", None)
        
        if territory_owner == pet_id:
            return "owner"
        elif territory_owner is None:
            return "unclaimed"
        else:
            return "visitor"
    
    def move_pet(self, pet_id, new_region_id):
        """Move a pet to a different region"""
        if pet_id not in self.pets:
            return {"success": False, "error": "Pet not found"}
        
        if new_region_id not in self.regions:
            return {"success": False, "error": "Region not found"}
        
        current_region_id = self.pets[pet_id]["current_region"]
        
        # Remove from current region
        if current_region_id in self.regions:
            self.regions[current_region_id]["current_pets"].discard(pet_id)
        
        # Add to new region if capacity allows
        new_region = self.regions[new_region_id]
        if len(new_region["current_pets"]) >= new_region["capacity"]:
            return {"success": False, "error": "Region at capacity"}
        
        new_region["current_pets"].add(pet_id)
        self.pets[pet_id]["current_region"] = new_region_id
        
        return {"success": True}
    
    def add_feature(self, owner_id, region_id, feature_data):
        """Add a custom feature to a region"""
        if not self._check_modification_permission(owner_id):
            return {"success": False, "error": "Permission denied"}
        
        if region_id not in self.regions:
            return {"success": False, "error": "Region not found"}
        
        # Validate feature data
        if not self._validate_feature_data(feature_data):
            return {"success": False, "error": "Invalid feature data"}
        
        # Add the feature
        feature_id = f"feature_{len(self.regions[region_id].get('features', [])) + 1}"
        if "features" not in self.regions[region_id]:
            self.regions[region_id]["features"] = []
        
        feature_data["id"] = feature_id
        feature_data["creator_id"] = owner_id
        feature_data["created_at"] = time.time()
        
        self.regions[region_id]["features"].append(feature_data)
        
        # Record modification
        self.modifications.append({
            "type": "add_feature",
            "owner_id": owner_id,
            "region_id": region_id,
            "feature_id": feature_id,
            "timestamp": time.time()
        })
        
        return {"success": True, "feature_id": feature_id}
    
    def step(self):
        """Advance the environment one time step"""
        # Update time
        self.time_system.step()
        
        # Update weather
        self.weather_system.update()
        
        # Process events
        self.event_system.step()
        
        # Regenerate resources
        self._regenerate_resources()
        
        # Process automatic interactions between pets
        self._process_pet_interactions()
        
        return self.get_state()
    
    def _regenerate_resources(self):
        """Regenerate environment resources at each step"""
        for region_id, region in self.regions.items():
            # Attention regenerates over time
            if "attention" in region["resources"]:
                max_attention = 100
                region["resources"]["attention"] = min(
                    max_attention,
                    region["resources"]["attention"] + 5
                )
            
            # Play space regenerates
            if "play_space" in region["resources"]:
                max_play = 100
                region["resources"]["play_space"] = min(
                    max_play,
                    region["resources"]["play_space"] + 2
                )
    
    def _process_pet_interactions(self):
        """Handle automatic interactions between pets in the same region"""
        # For each region, check for pets that might interact
        for region_id, region in self.regions.items():
            if len(region["current_pets"]) > 1:
                pet_list = list(region["current_pets"])
                # Choose random pairs for potential interaction
                for _ in range(min(3, len(pet_list))):
                    pet1 = random.choice(pet_list)
                    remaining = [p for p in pet_list if p != pet1]
                    if remaining:
                        pet2 = random.choice(remaining)
                        self._create_pet_interaction(pet1, pet2, region_id)
    
    def _create_pet_interaction(self, pet1_id, pet2_id, region_id):
        """Create an interaction between two pets"""
        # This would typically call into each pet's AI to determine their behavior
        # For now, just record that an interaction happened
        interaction = {
            "pet1_id": pet1_id,
            "pet2_id": pet2_id,
            "region_id": region_id,
            "type": random.choice(["play", "socialize", "compete", "ignore"]),
            "timestamp": time.time()
        }
        
        # In a full implementation, this would affect both pets' development
        return interaction
    
    def get_state(self):
        """Return the current state of the environment"""
        return {
            "name": self.name,
            "regions": self.regions,
            "pet_count": len(self.pets),
            "owner_count": len(self.owners),
            "weather": self.weather_system.current_weather,
            "time": self.time_system.get_current_time(),
            "active_events": self.event_system.active_events
        }
    
    def _check_modification_permission(self, owner_id):
        """Check if an owner has permission to modify the environment"""
        if owner_id == self.creator_id:
            return True
        
        if self.access_policy == "public":
            return owner_id in self.owners
        
        # Additional permission logic could go here
        return False
    
    def _validate_region_data(self, region_data):
        """Validate data for a new region"""
        required_fields = ["name", "description", "capacity"]
        return all(field in region_data for field in required_fields)
    
    def _validate_feature_data(self, feature_data):
        """Validate data for a new feature"""
        required_fields = ["name", "description", "effect"]
        return all(field in feature_data for field in required_fields)
```

#### 2. Environment Customization System

```python
class EnvironmentCustomizationSystem:
    """Manages owner customizations to shared environments"""
    
    def __init__(self, environment):
        self.environment = environment
        self.available_themes = [
            "default", "forest", "beach", "mountain", 
            "space", "underwater", "cyberpunk", "fantasy"
        ]
        self.available_features = self._define_available_features()
        self.customization_costs = self._define_customization_costs()
    
    def _define_available_features(self):
        """Define features that owners can add to environments"""
        return {
            "toy_box": {
                "name": "Toy Box",
                "description": "A collection of toys that increases play value",
                "effect": {"play_value": 20, "energy_cost": -5},
                "compatible_regions": ["commons", "play_zone"],
                "incompatible_with": []
            },
            "treat_dispenser": {
                "name": "Treat Dispenser",
                "description": "Automatically provides treats at intervals",
                "effect": {"happiness": 10, "nutrition": 5},
                "compatible_regions": ["all"],
                "incompatible_with": []
            },
            "nap_pod": {
                "name": "Nap Pod",
                "description": "A comfortable place for pets to rest",
                "effect": {"rest_quality": 30, "energy_recovery": 15},
                "compatible_regions": ["quiet_corner", "commons"],
                "incompatible_with": ["loud_speaker"]
            },
            "puzzle_station": {
                "name": "Puzzle Station",
                "description": "Mental challenges for intelligent pets",
                "effect": {"intelligence_growth": 15, "energy_cost": -10},
                "compatible_regions": ["commons", "quiet_corner"],
                "incompatible_with": []
            },
            "loud_speaker": {
                "name": "Loud Speaker",
                "description": "Plays energetic music to stimulate activity",
                "effect": {"energy": 20, "rest_quality": -15},
                "compatible_regions": ["play_zone"],
                "incompatible_with": ["nap_pod"]
            },
            "weather_machine": {
                "name": "Weather Machine",
                "description": "Creates localized weather effects",
                "effect": {"novelty": 25, "environment_control": 15},
                "compatible_regions": ["all"],
                "incompatible_with": []
            },
            "social_circle": {
                "name": "Social Circle",
                "description": "Encourages group interaction among pets",
                "effect": {"social_growth": 20, "privacy": -10},
                "compatible_regions": ["commons", "play_zone"],
                "incompatible_with": []
            }
        }
    
    def _define_customization_costs(self):
        """Define costs for different customizations"""
        return {
            "add_region": 100,
            "change_theme": 50,
            "add_feature": {
                "toy_box": 20,
                "treat_dispenser": 30,
                "nap_pod": 40,
                "puzzle_station": 35,
                "loud_speaker": 25,
                "weather_machine": 100,
                "social_circle": 45
            }
        }
    
    def get_available_customizations(self, owner_id, owner_tokens):
        """Get customizations available to a specific owner"""
        has_permission = self.environment._check_modification_permission(owner_id)
        
        available = {
            "themes": [],
            "features": [],
            "can_add_region": False
        }
        
        if has_permission:
            # Check which themes the owner can afford
            available["themes"] = [
                theme for theme in self.available_themes
                if owner_tokens >= self.customization_costs["change_theme"]
            ]
            
            # Check which features the owner can afford
            available["features"] = {
                feature_id: feature 
                for feature_id, feature in self.available_features.items()
                if owner_tokens >= self.customization_costs["add_feature"].get(feature_id, 999999)
            }
            
            # Check if owner can add a region
            available["can_add_region"] = owner_tokens >= self.customization_costs["add_region"]
        
        return available
    
    def apply_customization(self, owner_id, customization_type, customization_data, owner_tokens):
        """Apply a customization to the environment"""
        # Check permission
        if not self.environment._check_modification_permission(owner_id):
            return {"success": False, "error": "Permission denied"}
        
        # Handle different customization types
        if customization_type == "change_theme":
            theme = customization_data.get("theme")
            cost = self.customization_costs["change_theme"]
            
            if theme not in self.available_themes:
                return {"success": False, "error": "Invalid theme"}
            
            if owner_tokens < cost:
                return {"success": False, "error": "Insufficient tokens"}
            
            # Apply theme change
            self.environment.theme = theme
            
            return {"success": True, "cost": cost}
        
        elif customization_type == "add_feature":
            feature_id = customization_data.get("feature_id")
            region_id = customization_data.get("region_id")
            
            if feature_id not in self.available_features:
                return {"success": False, "error": "Invalid feature"}
            
            if region_id not in self.environment.regions:
                return {"success": False, "error": "Invalid region"}
            
            feature = self.available_features[feature_id]
            cost = self.customization_costs["add_feature"].get(feature_id, 999999)
            
            # Check compatibility
            region_type = self.environment.regions[region_id].get("type", "commons")
            if "all" not in feature["compatible_regions"] and region_type not in feature["compatible_regions"]:
                return {"success": False, "error": "Feature not compatible with this region"}
            
            # Check for incompatible features
            existing_features = [f["id"] for f in self.environment.regions[region_id].get("features", [])]
            for incompatible in feature["incompatible_with"]:
                if incompatible in existing_features:
                    return {"success": False, "error": f"Incompatible with existing feature: {incompatible}"}
            
            if owner_tokens < cost:
                return {"success": False, "error": "Insufficient tokens"}
            
            # Add the feature
            feature_data = {
                "id": feature_id,
                "name": feature["name"],
                "description": feature["description"],
                "effect": feature["effect"],
                "added_by": owner_id,
                "added_at": time.time()
            }
            
            result = self.environment.add_feature(owner_id, region_id, feature_data)
            if result["success"]:
                return {"success": True, "cost": cost}
            else:
                return result
        
        elif customization_type == "add_region":
            cost = self.customization_costs["add_region"]
            
            if owner_tokens < cost:
                return {"success": False, "error": "Insufficient tokens"}
            
            # Validate region data
            region_data = customization_data.get("region_data", {})
            result = self.environment.add_region(owner_id, region_data)
            
            if result["success"]:
                return {"success": True, "cost": cost}
            else:
                return result
        
        return {"success": False, "error": "Unknown customization type"}
```

### Collaborative Features for Shared Environments

#### 1. Environmental Events and Challenges

Shared environments could feature special events that require pet collaboration:

```python
class CollaborativeChallenge:
    """A challenge that requires multiple pets to solve together"""
    
    def __init__(self, environment, difficulty=1.0):
        self.environment = environment
        self.difficulty = difficulty
        self.start_time = time.time()
        self.end_time = None
        self.state = "active"
        self.required_traits = self._select_required_traits()
        self.participating_pets = {}
        self.progress = 0.0
        self.reward_pool = int(100 * difficulty)
    
    def _select_required_traits(self):
        """Select traits that will be needed to solve this challenge"""
        all_traits = [
            "intelligence", "strength", "speed", "empathy", 
            "creativity", "patience", "courage", "communication"
        ]
        
        # Number of traits depends on difficulty
        trait_count = max(1, min(5, int(self.difficulty * 3)))
        selected_traits = random.sample(all_traits, trait_count)
        
        # Assign required levels based on difficulty
        return {trait: 0.3 + (self.difficulty * 0.5) for trait in selected_traits}
    
    def add_pet_contribution(self, pet_id, pet_traits):
        """Add a pet's contribution to solving the challenge"""
        # Calculate how much this pet contributes based on their traits
        contribution = 0
        
        for trait, required_level in self.required_traits.items():
            pet_level = pet_traits.get(trait, 0)
            if pet_level >= required_level:
                contribution += pet_level - required_level + 0.1
        
        # Add to total progress
        self.progress += contribution / (len(self.required_traits) * self.difficulty)
        self.participating_pets[pet_id] = self.participating_pets.get(pet_id, 0) + contribution
        
        # Check if challenge completed
        if self.progress >= 1.0:
            self.complete_challenge()
        
        return contribution
    
    def complete_challenge(self):
        """Complete the challenge and distribute rewards"""
        self.state = "completed"
        self.end_time = time.time()
        
        # Calculate rewards for each participating pet
        total_contribution = sum(self.participating_pets.values())
        rewards = {}
        
        for pet_id, contribution in self.participating_pets.items():
            # Reward proportional to contribution
            if total_contribution > 0:
                reward_share = contribution / total_contribution
                rewards[pet_id] = int(self.reward_pool * reward_share)
        
        # Apply environmental effects from challenge completion
        self._apply_completion_effects()
        
        return rewards
    
    def _apply_completion_effects(self):
        """Apply effects to the environment when challenge is completed"""
        # Example: Boost resources in the environment
        for region_id, region in self.environment.regions.items():
            for resource in region["resources"]:
                region["resources"][resource] *= 1.2
        
        # Create a celebration event
        self.environment.event_system.start_event({
            'name': 'celebration',
            'description': 'A celebration of the successful challenge completion',
            'effect': lambda env: env.environmental_factors.update({
                'emotional_tone': 0.9,
                'novelty': 1.0
            }),
            'duration': 24,
            'probability': 1.0  # Not random, explicitly triggered
        })
```

#### 2. Resource Trading System

Allow pets to exchange resources within shared environments:

```python
class ResourceTradingSystem:
    """Allows pets to trade resources within an environment"""
    
    def __init__(self, environment):
        self.environment = environment
        self.active_offers = {}  # Offers waiting for acceptance
        self.completed_trades = []  # History of completed trades
    
    def create_offer(self, pet_id, offered_resource, requested_resource, amount_offered, amount_requested):
        """Create a trade offer from one pet"""
        # Check if pet has the offered resource
        pet_resources = self._get_pet_resources(pet_id)
        
        if offered_resource not in pet_resources or pet_resources[offered_resource] < amount_offered:
            return {"success": False, "error": "Insufficient resources"}
        
        # Create the offer
        offer_id = str(uuid.uuid4())
        offer = {
            "offer_id": offer_id,
            "pet_id": pet_id,
            "offered_resource": offered_resource,
            "requested_resource": requested_resource,
            "amount_offered": amount_offered,
            "amount_requested": amount_requested,
            "created_at": time.time(),
            "status": "active"
        }
        
        self.active_offers[offer_id] = offer
        
        return {"success": True, "offer_id": offer_id}
    
    def accept_offer(self, accepting_pet_id, offer_id):
        """Accept a trading offer"""
        if offer_id not in self.active_offers:
            return {"success": False, "error": "Offer not found"}
        
        offer = self.active_offers[offer_id]
        
        if offer["status"] != "active":
            return {"success": False, "error": "Offer no longer active"}
        
        # Check if accepting pet has the requested resource
        pet_resources = self._get_pet_resources(accepting_pet_id)
        
        if offer["requested_resource"] not in pet_resources or pet_resources[offer["requested_resource"]] < offer["amount_requested"]:
            return {"success": False, "error": "Insufficient resources"}
        
        # Execute the trade
        self._transfer_resource(offer["pet_id"], accepting_pet_id, 
                               offer["offered_resource"], offer["amount_offered"])
        
        self._transfer_resource(accepting_pet_id, offer["pet_id"],
                               offer["requested_resource"], offer["amount_requested"])
        
        # Update offer status
        offer["status"] = "completed"
        offer["completed_at"] = time.time()
        offer["accepted_by"] = accepting_pet_id
        
        # Move to completed trades
        self.completed_trades.append(offer)
        del self.active_offers[offer_id]
        
        return {"success": True, "trade": offer}
    
    def cancel_offer(self, pet_id, offer_id):
        """Cancel an active offer"""
        if offer_id not in self.active_offers:
            return {"success": False, "error": "Offer not found"}
        
        offer = self.active_offers[offer_id]
        
        if offer["pet_id"] != pet_id:
            return {"success": False, "error": "Not your offer"}
        
        if offer["status"] != "active":
            return {"success": False, "error": "Offer no longer active"}
        
        # Cancel the offer
        offer["status"] = "cancelled"
        offer["cancelled_at"] = time.time()
        
        # Move to completed trades (for history)
        self.completed_trades.append(offer)
        del self.active_offers[offer_id]
        
        return {"success": True}
    
    def get_active_offers(self, pet_id=None):
        """Get all active offers, optionally filtered by pet"""
        if pet_id:
            return {oid: offer for oid, offer in self.active_offers.items() 
                   if offer["pet_id"] == pet_id}
        return self.active_offers
    
    def get_compatible_offers(self, pet_id):
        """Find offers that a pet could potentially accept"""
        pet_resources = self._get_pet_resources(pet_id)
        
        compatible = {}
        for offer_id, offer in self.active_offers.items():
            # Skip own offers
            if offer["pet_id"] == pet_id:
                continue
                
            # Check if pet has the requested resource
            if (offer["requested_resource"] in pet_resources and 
                pet_resources[offer["requested_resource"]] >= offer["amount_requested"]):
                compatible[offer_id] = offer
        
        return compatible
    
    def _get_pet_resources(self, pet_id):
        """Get the resources a pet has access to"""
        if pet_id not in self.environment.pets:
            return {}
        
        region_id = self.environment.pets[pet_id]["current_region"]
        
        if region_id not in self.environment.regions:
            return {}
        
        # In a real implementation, pets would have their own resources
        # This simplistic version just uses region resources
        return self.environment.regions[region_id]["resources"].copy()
    
    def _transfer_resource(self, from_pet_id, to_pet_id, resource, amount):
        """Transfer resources between pets"""
        # In a real implementation, would update pet-specific resources
        # This simplified version just transfers region resources
        from_region_id = self.environment.pets[from_pet_id]["current_region"]
        to_region_id = self.environment.pets[to_pet_id]["current_region"]
        
        # If pets are in the same region, no need to transfer
        if from_region_id == to_region_id:
            return
        
        # Remove from source region
        if (from_region_id in self.environment.regions and
            resource in self.environment.regions[from_region_id]["resources"]):
            self.environment.regions[from_region_id]["resources"][resource] -= amount
        
        # Add to destination region
        if (to_region_id in self.environment.regions):
            if resource not in self.environment.regions[to_region_id]["resources"]:
                self.environment.regions[to_region_id]["resources"][resource] = 0
            self.environment.regions[to_region_id]["resources"][resource] += amount
```

#### 3. Reputation and Social Hierarchy System

Track social dynamics between pets in shared environments:

```python
class SocialSystem:
    """Manages social relationships and hierarchies in the environment"""
    
    def __init__(self, environment):
        self.environment = environment
        self.relationships = {}  # Pet-to-pet relationships
        self.hierarchies = {}  # Regional hierarchies
        self.social_behaviors = self._define_social_behaviors()
    
    def _define_social_behaviors(self):
        """Define possible social behaviors between pets"""
        return {
            "greet": {"friendly": 0.3, "neutral": 0.1, "unfriendly": -0.1},
            "play": {"friendly": 0.5, "neutral": 0.3, "unfriendly": -0.2},
            "share": {"friendly": 0.7, "neutral": 0.4, "unfriendly": 0.1},
            "ignore": {"friendly": -0.3, "neutral": -0.1, "unfriendly": 0.1},
            "compete": {"friendly": -0.1, "neutral": 0.0, "unfriendly": 0.3},
            "defend": {"friendly": 0.8, "neutral": 0.4, "unfriendly": -0.1}
        }
    
    def record_interaction(self, initiator_id, target_id, behavior, context=None):
        """Record a social interaction between pets"""
        if initiator_id == target_id:
            return
        
        # Initialize relationship if it doesn't exist
        if initiator_id not in self.relationships:
            self.relationships[initiator_id] = {}
        
        if target_id not in self.relationships[initiator_id]:
            self.relationships[initiator_id][target_id] = {
                "affinity": 0.0,  # -1.0 to 1.0
                "interactions": [],
                "last_interaction": None
            }
        
        # Get current relationship state
        relationship = self.relationships[initiator_id][target_id]
        
        # Determine relationship type
        rel_type = "neutral"
        if relationship["affinity"] > 0.3:
            rel_type = "friendly"
        elif relationship["affinity"] < -0.3:
            rel_type = "unfriendly"
        
        # Calculate effect based on behavior and relationship
        effect = self.social_behaviors.get(behavior, {}).get(rel_type, 0)
        
        # Modify effect based on context
        if context:
            # Examples of context modifiers
            if context.get("territory_owner") == target_id:
                # Interacting with a pet in their territory
                effect *= 0.5  # Reduced impact
            
            if context.get("recent_conflict"):
                # Recent negative interaction
                effect *= 0.7  # Reduced impact
        
        # Update affinity
        old_affinity = relationship["affinity"]
        relationship["affinity"] = max(-1.0, min(1.0, relationship["affinity"] + effect))
        
        # Record interaction
        interaction = {
            "behavior": behavior,
            "timestamp": time.time(),
            "effect": effect,
            "affinity_before": old_affinity,
            "affinity_after": relationship["affinity"]
        }
        
        relationship["interactions"].append(interaction)
        relationship["last_interaction"] = time.time()
        
        # Update reciprocal relationship with smaller effect
        self._update_reciprocal_relationship(initiator_id, target_id, behavior, effect * 0.5)
        
        # Update social hierarchy if needed
        self._update_hierarchy(initiator_id, target_id, behavior, effect)
        
        return {
            "old_affinity": old_affinity,
            "new_affinity": relationship["affinity"],
            "effect": effect
        }
    
    def _update_reciprocal_relationship(self, initiator_id, target_id, behavior, effect):
        """Update the reciprocal relationship (how target feels about initiator)"""
        if target_id not in self.relationships:
            self.relationships[target_id] = {}
        
        if initiator_id not in self.relationships[target_id]:
            self.relationships[target_id][initiator_id] = {
                "affinity": 0.0,
                "interactions": [],
                "last_interaction": None
            }
        
        # Get target's view of the relationship
        relationship = self.relationships[target_id][initiator_id]
        
        # Some behaviors have different reciprocal effects
        reciprocal_effect = effect
        if behavior == "ignore":
            reciprocal_effect = -0.1  # Being ignored always feels bad
        elif behavior == "defend":
            reciprocal_effect = 0.6  # Being defended feels good
        
        # Update affinity
        old_affinity = relationship["affinity"]
        relationship["affinity"] = max(-1.0, min(1.0, relationship["affinity"] + reciprocal_effect))
        
        # Record interaction from this perspective
        interaction = {
            "behavior": f"received_{behavior}",
            "timestamp": time.time(),
            "effect": reciprocal_effect,
            "affinity_before": old_affinity,
            "affinity_after": relationship["affinity"]
        }
        
        relationship["interactions"].append(interaction)
        relationship["last_interaction"] = time.time()
    
    def _update_hierarchy(self, initiator_id, target_id, behavior, effect):
        """Update social hierarchy based on interaction"""
        # Find pets' current region
        if initiator_id not in self.environment.pets or target_id not in self.environment.pets:
            return
        
        initiator_region = self.environment.pets[initiator_id]["current_region"]
        target_region = self.environment.pets[target_id]["current_region"]
        
        # Only update hierarchy if in same region
        if initiator_region != target_region:
            return
        
        region_id = initiator_region
        
        # Initialize hierarchy for this region if needed
        if region_id not in self.hierarchies:
            self.hierarchies[region_id] = {
                "dominance_scores": {},
                "ranked_pets": [],
                "last_updated": time.time()
            }
        
        hierarchy = self.hierarchies[region_id]
        
        # Initialize dominance scores if needed
        if initiator_id not in hierarchy["dominance_scores"]:
            hierarchy["dominance_scores"][initiator_id] = 0.5
        
        if target_id not in hierarchy["dominance_scores"]:
            hierarchy["dominance_scores"][target_id] = 0.5
        
        # Update dominance based on behavior
        dominance_effect = 0
        if behavior in ["compete", "defend"]:
            # These are dominance-related behaviors
            dominance_effect = effect * 0.2
        
        # Apply dominance effect
        hierarchy["dominance_scores"][initiator_id] += dominance_effect
        hierarchy["dominance_scores"][target_id] -= dominance_effect
        
        # Ensure scores stay in valid range
        hierarchy["dominance_scores"][initiator_id] = max(0, min(1, hierarchy["dominance_scores"][initiator_id]))
        hierarchy["dominance_scores"][target_id] = max(0, min(1, hierarchy["dominance_scores"][target_id]))
        
        # Update ranked list
        ranked_pets = sorted(
            hierarchy["dominance_scores"].keys(),
            key=lambda pid: hierarchy["dominance_scores"][pid],
            reverse=True
        )
        
        hierarchy["ranked_pets"] = ranked_pets
        hierarchy["last_updated"] = time.time()
    
    def get_relationship(self, pet1_id, pet2_id):
        """Get the relationship between two pets"""
        if pet1_id in self.relationships and pet2_id in self.relationships[pet1_id]:
            return self.relationships[pet1_id][pet2_id]
        return {"affinity": 0.0, "interactions": [], "last_interaction": None}
    
    def get_relationship_type(self, pet1_id, pet2_id):
        """Get a categorical relationship type"""
        relationship = self.get_relationship(pet1_id, pet2_id)
        affinity = relationship["affinity"]
        
        if affinity > 0.7:
            return "best_friends"
        elif affinity > 0.3:
            return "friends"
        elif affinity > 0:
            return "acquaintances"
        elif affinity > -0.3:
            return "strangers"
        elif affinity > -0.7:
            return "rivals"
        else:
            return "enemies"
    
    def get_social_network(self, region_id=None):
        """Get the social network as a graph"""
        network = {"nodes": [], "links": []}
        
        # Collect all pets with relationships
        all_pets = set()
        for pet1_id in self.relationships:
            all_pets.add(pet1_id)
            for pet2_id in self.relationships[pet1_id]:
                all_pets.add(pet2_id)
        
        # Filter by region if specified
        if region_id:
            region_pets = set()
            for pet_id in self.environment.pets:
                if self.environment.pets[pet_id]["current_region"] == region_id:
                    region_pets.add(pet_id)
            all_pets = all_pets.intersection(region_pets)
        
        # Add nodes
        for pet_id in all_pets:
            node = {"id": pet_id}
            
            # Add hierarchy position if available
            if (region_id in self.hierarchies and 
                pet_id in self.hierarchies[region_id]["dominance_scores"]):
                node["dominance"] = self.hierarchies[region_id]["dominance_scores"][pet_id]
                
                rank_position = self.hierarchies[region_id]["ranked_pets"].index(pet_id)
                total_pets = len(self.hierarchies[region_id]["ranked_pets"])
                node["rank_percentile"] = 1 - (rank_position / total_pets)
            
            network["nodes"].append(node)
        
        # Add links
        for pet1_id in all_pets:
            if pet1_id in self.relationships:
                for pet2_id in self.relationships[pet1_id]:
                    if pet2_id in all_pets:
                        relationship = self.relationships[pet1_id][pet2_id]
                        
                        if abs(relationship["affinity"]) > 0.1:  # Only show meaningful relationships
                            link = {
                                "source": pet1_id,
                                "target": pet2_id,
                                "affinity": relationship["affinity"],
                                "type": self.get_relationship_type(pet1_id, pet2_id)
                            }
                            network["links"].append(link)
        
        return network
```

## Next Steps

1. Start by implementing a basic environment focused on attention dynamics
2. Integrate it with your existing trait evolution system
3. Gradually add more environmental factors as the system matures
4. Create visualization components that show the environment alongside the pets
5. Develop environment-triggered behaviors that showcase pet adaptation

## Additional Environmental Features

### Mood System

```python
class EnvironmentalMoodSystem:
    """Tracks and influences the emotional tone of the environment"""
    
    def __init__(self):
        self.base_mood = 0.5  # neutral
        self.mood_influences = []
        self.mood_history = []
    
    def add_mood_influence(self, source, intensity, duration):
        """Add a new factor influencing environmental mood"""
        self.mood_influences.append({
            'source': source,
            'intensity': intensity,
            'duration': duration,
            'remaining': duration
        })
    
    def update(self):
        """Update environmental mood based on active influences"""
        # Calculate current mood
        mood = self.base_mood
        active_influences = []
        
        for influence in self.mood_influences:
            if influence['remaining'] > 0:
                mood += influence['intensity']
                influence['remaining'] -= 1
                active_influences.append(influence)
        
        # Normalize mood to 0-1 range
        mood = max(0, min(1, mood))
        
        # Update history and influences
        self.mood_history.append(mood)
        self.mood_influences = active_influences
        
        return mood
```

### Event System

```python
class EnvironmentalEventSystem:
    """Generates random events that affect the environment"""
    
    def __init__(self, environment, event_frequency=0.05):
        self.environment = environment
        self.event_frequency = event_frequency
        self.possible_events = [
            {
                'name': 'attention_drought',
                'description': 'Attention becomes temporarily scarce',
                'effect': lambda env: setattr(env, 'attention_scarcity', env.attention_scarcity * 1.5),
                'duration': 24,
                'probability': 0.2
            },
            {
                'name': 'attention_abundance',
                'description': 'Attention becomes temporarily plentiful',
                'effect': lambda env: setattr(env, 'attention_scarcity', env.attention_scarcity * 0.5),
                'duration': 12,
                'probability': 0.3
            },
            {
                'name': 'environmental_shift',
                'description': 'A sudden change in environmental conditions',
                'effect': lambda env: env.environmental_factors.update({
                    'emotional_tone': random.random(),
                    'novelty': 1.0
                }),
                'duration': 48,
                'probability': 0.1
            }
        ]
        self.active_events = []
    
    def step(self):
        """Check for new events and update active ones"""
        # Check for new random events
        if random.random() < self.event_frequency:
            self.trigger_random_event()
        
        # Update active events
        remaining_events = []
        for event in self.active_events:
            event['remaining'] -= 1
            if event['remaining'] <= 0:
                self.end_event(event)
            else:
                remaining_events.append(event)
        
        self.active_events = remaining_events
    
    def trigger_random_event(self):
        """Start a random environmental event"""
        candidates = []
        r = random.random()
        cumulative_prob = 0
        
        for event in self.possible_events:
            cumulative_prob += event['probability']
            if r <= cumulative_prob:
                candidates.append(event)
        
        if candidates:
            event = random.choice(candidates)
            self.start_event(event)
    
    def start_event(self, event_template):
        """Begin an environmental event"""
        event = event_template.copy()
        event['remaining'] = event['duration']
        event['effect'](self.environment)
        self.active_events.append(event)
        return event
    
    def end_event(self, event):
        """End an event and restore normal conditions"""
        # Implementation depends on how events affect the environment
        pass
```

### Weather System

```python
class EnvironmentalWeatherSystem:
    """Simulates weather patterns that affect pet behavior"""
    
    def __init__(self):
        self.current_weather = 'clear'
        self.temperature = 0.5  # 0 = cold, 1 = hot
        self.weather_types = ['clear', 'cloudy', 'rainy', 'stormy', 'foggy', 'windy']
        self.weather_transitions = {
            'clear': {'clear': 0.7, 'cloudy': 0.3},
            'cloudy': {'clear': 0.3, 'cloudy': 0.4, 'rainy': 0.2, 'foggy': 0.1},
            'rainy': {'cloudy': 0.4, 'rainy': 0.4, 'stormy': 0.2},
            'stormy': {'rainy': 0.5, 'stormy': 0.3, 'cloudy': 0.2},
            'foggy': {'foggy': 0.6, 'cloudy': 0.3, 'clear': 0.1},
            'windy': {'windy': 0.5, 'clear': 0.3, 'cloudy': 0.2}
        }
        self.weather_effects = {
            'clear': {'energy': 0.2, 'mood': 0.2},
            'cloudy': {'energy': 0.0, 'mood': -0.1},
            'rainy': {'energy': -0.1, 'mood': -0.1},
            'stormy': {'energy': -0.2, 'mood': -0.2},
            'foggy': {'energy': -0.1, 'mood': 0.0},
            'windy': {'energy': 0.1, 'mood': 0.1}
        }
    
    def update(self):
        """Update weather conditions"""
        # Update temperature with some persistence
        self.temperature = 0.8 * self.temperature + 0.2 * random.random()
        
        # Possibly transition weather state
        transitions = self.weather_transitions[self.current_weather]
        r = random.random()
        cumulative_prob = 0
        
        for weather, prob in transitions.items():
            cumulative_prob += prob
            if r <= cumulative_prob:
                self.current_weather = weather
                break
        
        return {
            'weather': self.current_weather,
            'temperature': self.temperature,
            'effects': self.weather_effects[self.current_weather]
        }
```

### Time System

```python
class EnvironmentalTimeSystem:
    """Manages the passage of time in the environment"""
    
    def __init__(self, time_scale=1.0):
        self.time = 0
        self.time_scale = time_scale  # How fast time passes
        self.day = 0
        self.hour = 0
        self.minute = 0
        
    def step(self, delta_time=1):
        """Advance time by the specified amount"""
        # Scale time advancement
        real_delta = delta_time * self.time_scale
        self.time += real_delta
        
        # Update time components
        total_minutes = int(self.time)
        self.minute = total_minutes % 60
        total_hours = total_minutes // 60
        self.hour = total_hours % 24
        self.day = total_hours // 24
        
        # Calculate day/night cycle (0.0 = midnight, 0.5 = noon)
        day_cycle = ((self.hour * 60 + self.minute) / (24 * 60)) % 1.0
        
        return {
            'total_time': self.time,
            'day': self.day,
            'hour': self.hour,
            'minute': self.minute,
            'day_cycle': day_cycle,
            'is_day': 6 <= self.hour < 18  # Simple day/night definition
        }
```
