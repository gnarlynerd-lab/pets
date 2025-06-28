# DKS Digital Pet System: Unified Implementation Document

## Overview

This document outlines the comprehensive implementation approach for the DKS (Dynamic Kinetic Systems) Digital Pet System. It serves as a unified development roadmap that integrates all existing concepts from multiple implementation documents, combining the core technical foundations of the original DKS framework with the digital pet concept pivot, emoji communication system, and fluid boundary mechanics.

## Core Architecture

### Technical Stack

- **Agent Framework**: Mesa (Python-based agent modeling framework)
- **Communication Layer**: Redis (for high-performance message passing between agents)
- **Frontend**: React + D3.js (for interactive visualization and user interface)
- **Persistence**: MySQL (for state storage and analysis)

### Key System Components

![DKS Digital Pet System Architecture](https://mermaid.ink/img/pako:eNqFk0tv2zAMgP_KQRcPKJDuVKDDslMPO2xYUfTQS6eDLCZx1cjyJDlNi8D_fXSc9Gk0O0Ri-FFk-FDPSJkSJIv2Pe6KG13QlZal2Zzp9cUw8-Kz3jilvTmZxpZrYcppG9fHmtEHzTXX4iCtCHwyiqZcWSbZhpVMG6UGmbbTT8IKrZlXuWicodNCGQOO9YfVLFfQ5OOnj6smqiw-LG-2VPF1tSD8PEd1rWoyfFhnbM9ysqxVOWPB9U1sZ4f1uoBn4Aofht-9Nh8-junXy-U_qEz4H7VcDP6Pm-vl5PKcnhGFr8_BYvOchynDw8Z65TBj3HCbZ0qXzDrjsgQCzbzudIYJ_8hK49qNbCwviH_qg5Qn5YTu5DaxUXlO7KRr0eBolbWOWtlIS4wmzDSdLvSAMfSZ4Ihg407ekDEyuvu9-j5dre9_rqarm7vp_euHzm14Ql-u73TbhtcTYVddVWXPcyPSaiZL2aecJc6l9vZpIie-vVjq37HLazLqlaVVyUivlwbtKl_5U8aKsaufVkrSGs859RuMvuAV5qWD0n3XTwl0g6cvuCJ2i47WplQa064KB4F0jdw04HTsQu9ADj-ALjTJshuDVRY6UUoYrJ8Cvohy35c0D0tc7ORymt_JuORl68aJxQNOnetG-F6WTONAe5EuD2okAUSuTJaZUPzDJnseYDT60Xm9SAsrONX-jaaCxFamDhLJ4ghOcHGLYuHPXyLZg98Oj4J7FLtE8q_hbVkeNwAZND_Y1S0OTfQCsuePoFeZxg?type=png)

1. **DigitalPet Base Class**: Core entity evolved from DKSAgent
   - Trait Network: Interconnected personality traits
   - Memory System: Multi-level memory for learning
   - Behavior System: Generates behaviors based on traits
   - Attention System: Tracks human interaction patterns

2. **Fluid Boundary System**: Manages pet-environment interactions
   - Boundary Permeability: Controls information/resource flow
   - Energy Management: Handles energy allocation for maintenance
   - Element Exchange: Facilitates assimilation and projection

3. **Environment System**: Creates interactive world
   - Weather System: Dynamic conditions affecting pets
   - Resources: Consumable and interactive elements
   - Regions: Different areas with unique properties

4. **Communication System**: Non-threatening emoji interface
   - Progressive complexity: Language development over time
   - Multi-modal expression: Visual, sound, and motion
   - Pattern-based communication: Unique to each pet

5. **Cognitive Development System**: Tracks learning and growth
   - Observable intelligence areas: Pattern recognition, problem-solving
   - Experience-based learning: Growth from interactions
   - Skill acquisition: Progressive capability development

## Implementation Strategy

### Phase 1: Foundation Development (Week 1-2)

#### Core Framework Setup
1. **Configure Mesa Agent Framework**
   ```python
   class HospitalModel(mesa.Model):
       # Transform into PetWorld model
       def __init__(self, num_pets, environment_config):
           self.num_pets = num_pets
           self.grid = mesa.space.MultiGrid(50, 50, True)
           self.schedule = mesa.time.RandomActivation(self)
           
           # Create environment
           self.environment = PetEnvironment(environment_config)
           
           # Create pets
           self.create_pets()
           
           # Set up data collection
           self.datacollector = mesa.DataCollector(
               model_reporters={
                   "Average Pet Health": self.calculate_avg_health,
                   "Environmental Complexity": self.calculate_env_complexity,
                   "Pet Happiness": self.calculate_pet_happiness
               },
               agent_reporters={
                   "Energy": "energy",
                   "Boundary Permeability": "boundary_permeability",
                   "Cognitive Development": "cognitive_level"
               }
           )
   ```

2. **Implement Redis Communication Layer**
   ```python
   def get_messages(self):
       """Retrieve messages from Redis queue"""
       message_key = f"pet:{self.unique_id}:messages"
       messages = self.redis.lrange(message_key, 0, -1)
       self.redis.delete(message_key)
       return [json.loads(m) for m in messages]
   
   def send_message(self, recipient_id, message_type, content):
       """Send message to another pet or to the environment"""
       message = {
           "sender": self.unique_id,
           "type": message_type,
           "content": content,
           "timestamp": time.time()
       }
       recipient_key = f"pet:{recipient_id}:messages"
       self.redis.rpush(recipient_key, json.dumps(message))
   ```

3. **Create MySQL Schema for Persistence**
   ```sql
   CREATE TABLE pet_states (
       id VARCHAR(36) PRIMARY KEY,
       pet_id VARCHAR(36) NOT NULL,
       timestamp DATETIME NOT NULL,
       traits JSON,
       needs JSON,
       health FLOAT,
       energy FLOAT,
       mood FLOAT,
       boundary_permeability FLOAT,
       cognitive_development JSON,
       environmental_elements JSON,
       FOREIGN KEY (pet_id) REFERENCES pets(id)
   );
   
   CREATE TABLE pet_interactions (
       id VARCHAR(36) PRIMARY KEY,
       pet_id VARCHAR(36) NOT NULL,
       user_id VARCHAR(36) NOT NULL,
       interaction_type VARCHAR(50) NOT NULL,
       content JSON,
       timestamp DATETIME NOT NULL,
       pet_response JSON,
       response_time FLOAT,
       FOREIGN KEY (pet_id) REFERENCES pets(id),
       FOREIGN KEY (user_id) REFERENCES users(id)
   );
   ```

#### Digital Pet Base Implementation

1. **Convert DKSAgent to DigitalPet**
   ```python
   class DigitalPet(mesa.Agent):
       """Digital Pet that evolves based on human interaction and attention patterns"""
       def __init__(self, unique_id, model, initial_traits=None):
           super().__init__(unique_id, model)
           
           # Core DKS attributes (from DKSAgent)
           self.pet_type = "base"  # Can be specialized later
           self.creation_time = time.time()
           self.last_interaction_time = time.time()
           
           # Evolution components
           self.traits = initial_traits or self._generate_default_traits()
           self.trait_connections = defaultdict(float)  # How traits influence each other
           self.trait_evolution_rate = defaultdict(float)  # How quickly traits evolve
           
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
           
           # Fluid boundary system
           self.energy_system = PetEnergySystem(self.unique_id, initial_energy=self.energy)
           self.cognitive_system = ObservableCognitiveDevelopment(self.unique_id)
           
           # Communication system - NEW
           self.communication_system = PetCommunicationSystem(self.unique_id)
   ```

2. **Implement Trait Evolution System**
   ```python
   def _evolve_traits(self):
       """Evolve traits based on recent experiences"""
       for trait, current_value in self.traits.items():
           # Get related traits based on connections
           related_traits = []
           for connection, strength in self.trait_connections.items():
               if connection.startswith(f"{trait}:"):
                   related_trait = connection.split(':')[1]
                   related_traits.append((related_trait, strength))
               elif connection.endswith(f":{trait}"):
                   related_trait = connection.split(':')[0]
                   related_traits.append((related_trait, strength))
           
           # Calculate evolution based on related trait values
           evolution_direction = 0
           total_influence = 0
           
           for related_trait, connection_strength in related_traits:
               if related_trait in self.traits:
                   # Direction is positive or negative based on relationship
                   influence = (self.traits[related_trait] - 0.5) * connection_strength
                   evolution_direction += influence
                   total_influence += abs(connection_strength)
           
           # More recent experiences have stronger influence
           for memory in self.episodic_memory[-5:]:
               if trait in memory.get("trait_impacts", {}):
                   impact = memory["trait_impacts"][trait]
                   evolution_direction += impact
                   total_influence += abs(impact)
           
           # Calculate normalized evolution
           if total_influence > 0:
               normalized_evolution = evolution_direction / total_influence
               # Scale by evolution rate (slow changes)
               evolution_amount = normalized_evolution * self.trait_evolution_rate.get(trait, 0.01)
               # Update trait value (clamped to 0-1)
               self.traits[trait] = max(0.0, min(1.0, current_value + evolution_amount))
   ```

### Phase 2: Core Systems Integration (Week 3-4)

#### Fluid Boundary Implementation

1. **Create Fluid Boundary Class**
   ```python
   class FluidBoundarySystem:
       """System for managing the fluid boundary between pet and environment"""
       def __init__(self, pet_id, initial_energy=100):
           self.pet_id = pet_id
           self.boundary_energy = initial_energy
           self.boundary_permeability = 0.5
           self.boundary_size = 1.0
           self.assimilated_elements = {}
           self.boundary_maintenance_cost = 0.1
           self.boundary_history = []
       
       def update(self, environment_state, available_energy):
           """Update boundary based on environment and available energy"""
           # Calculate maintenance cost
           base_cost = self.boundary_maintenance_cost * self.boundary_size
           environmental_pressure = self._calculate_environmental_pressure(environment_state)
           total_cost = base_cost * (1 + environmental_pressure)
           
           # Check energy availability
           if available_energy < total_cost:
               # Boundary failure - become more permeable
               self.boundary_permeability = min(1.0, self.boundary_permeability + 0.1)
               self.boundary_size = max(0.2, self.boundary_size - 0.05)
               boundary_status = "failing"
           else:
               # Successful maintenance
               self.boundary_permeability = max(0.1, self.boundary_permeability - 0.01)
               boundary_status = "maintained"
           
           # Return status and energy consumed
           return {
               "energy_consumed": min(total_cost, available_energy),
               "boundary_status": boundary_status,
               "permeability": self.boundary_permeability,
               "size": self.boundary_size
           }
   ```

2. **Implement Environmental Exchange System**
   ```python
   class EnvironmentalExchangeSystem:
       """Handles exchange of elements between pet and environment"""
       def __init__(self, pet_id, boundary_system):
           self.pet_id = pet_id
           self.boundary_system = boundary_system
           self.internal_elements = {}
           self.external_projections = {}
           
       def assimilate_element(self, element):
           """Attempt to assimilate an environmental element"""
           # Check boundary permeability
           result = self.boundary_system.attempt_assimilation(element)
           
           if result["success"]:
               # Successfully assimilated - add to internal elements
               element_id = result["element_id"]
               self.internal_elements[element_id] = {
                   "original": element,
                   "assimilated_at": time.time(),
                   "integration_level": 0.1,
                   "effects": self._calculate_element_effects(element)
               }
               
           return result
   ```

#### Environment System Development

1. **Create Pet Environment Class**
   ```python
   class PetEnvironment:
       """Environment system for pet world"""
       def __init__(self, config=None):
           self.config = config or {}
           self.weather = "clear"
           self.time_of_day = 12  # 24-hour format
           self.ambient_energy = 0.5  # 0-1 scale
           self.regions = self._create_regions()
           self.features = {}
           self.last_update = time.time()
       
       def _create_regions(self):
           """Create environment regions"""
           regions = {
               "central": {
                   "name": "Central Park",
                   "resources": {"food": 10, "water": 15, "toys": 5},
                   "features": [],
                   "ambient_mood": 0.7
               },
               "forest": {
                   "name": "Forest Grove",
                   "resources": {"food": 20, "water": 8, "hiding_spots": 12},
                   "features": [],
                   "ambient_mood": 0.5
               },
               "playground": {
                   "name": "Pet Playground",
                   "resources": {"toys": 15, "obstacles": 10, "food": 5},
                   "features": [],
                   "ambient_mood": 0.8
               }
           }
           return regions
       
       def step(self):
           """Update environment for one time step"""
           # Update time of day (1 hour per step)
           self.time_of_day = (self.time_of_day + 1) % 24
           
           # Update weather occasionally
           if random.random() < 0.1:
               self.weather = random.choice(["clear", "cloudy", "rainy", "stormy"])
           
           # Update ambient energy based on time of day and weather
           self._update_ambient_energy()
           
           # Replenish resources
           self._replenish_resources()
           
           # Return current state
           return self.get_state()
       
       def get_state(self):
           """Get the current environment state"""
           return {
               "weather": self.weather,
               "time_of_day": self.time_of_day,
               "ambient_energy": self.ambient_energy,
               "regions": self.regions,
               "features": self.features
           }
           
       def get_pet_view(self, pet_id, permeability):
           """Get a pet-specific view of the environment based on boundary permeability"""
           # Basic state always visible
           pet_view = {
               "weather": self.weather,
               "time_of_day": self.time_of_day
           }
           
           # Other elements visible based on permeability
           if permeability > 0.3:
               pet_view["ambient_energy"] = self.ambient_energy
               
           if permeability > 0.5:
               # Can see basic region info but not all details
               pet_view["regions"] = {
                   region_id: {
                       "name": region["name"],
                       "ambient_mood": region["ambient_mood"]
                   }
                   for region_id, region in self.regions.items()
               }
               
           if permeability > 0.7:
               # Can see resources and features
               pet_view["regions"] = self.regions.copy()
               
           return pet_view
   ```

#### Cognitive Development System

1. **Implement Observable Cognitive Development**
   ```python
   class ObservableCognitiveDevelopment:
       """Tracks and evolves pet cognitive capabilities"""
       def __init__(self, pet_id, base_level=0.1):
           self.pet_id = pet_id
           # Cognitive areas that develop through experience
           self.cognitive_areas = {
               "pattern_recognition": base_level,
               "environmental_awareness": base_level,
               "social_intelligence": base_level,
               "problem_solving": base_level,
               "memory_capacity": base_level,
               "communication": base_level,
               "creativity": base_level
           }
           self.developmental_history = []
           
       def process_experience(self, experience_type, intensity, relevant_traits):
           """Process an experience to potentially develop cognitive areas"""
           # Different experience types affect different cognitive areas
           affected_areas = {
               "exploration": ["environmental_awareness", "pattern_recognition"],
               "social": ["social_intelligence", "communication"],
               "problem": ["problem_solving", "creativity"],
               "memory": ["memory_capacity", "pattern_recognition"],
               "play": ["creativity", "problem_solving", "social_intelligence"]
           }
           
           # Get the areas affected by this experience
           areas = affected_areas.get(experience_type, ["pattern_recognition"])
           
           # Calculate development based on intensity and traits
           development = {}
           for area in areas:
               # Base development from experience intensity
               dev_amount = intensity * 0.01
               
               # Traits influence development rate
               trait_multiplier = 1.0
               for trait, value in relevant_traits.items():
                   if trait in ["curiosity", "openness"]:
                       trait_multiplier += (value - 0.5)
                   
               # Calculate final development amount
               final_dev = dev_amount * trait_multiplier
               
               # Apply development to cognitive area
               self.cognitive_areas[area] = min(1.0, self.cognitive_areas[area] + final_dev)
               development[area] = final_dev
           
           # Record development
           self.developmental_history.append({
               "timestamp": time.time(),
               "experience_type": experience_type,
               "intensity": intensity,
               "development": development
           })
           
           return development
   ```

### Phase 3: Cognitive & Communication Systems (Weeks 5-6)
1. **Cognitive Development**
   - Implement learning from experiences
   - Create cognitive area progression
   - Build skill acquisition mechanisms
   - Add pattern recognition capabilities

2. **Emoji Communication**
   - Implement base emoji vocabulary
   - Create complexity progression
   - Build personalization system
   - Add communication visualization

3. **Advanced Behaviors**
   - Implement behavior generation from traits
   - Create behavior mutation system
   - Add behavioral responses to stimuli
   - Build behavior history tracking

4. **Memory Systems**
   - Implement episodic memory
   - Create semantic pattern recognition
   - Add user-specific memories
   - Build memory visualization

```javascript
class PetCommunicationSystem {
    constructor() {
        this.vocabulary = {
            // Basic emotions
            happy: ['😊', '😄', '🥰', '✨'],
            sad: ['😢', '😞', '💔', '🌧️'],
            excited: ['🎉', '⚡', '🌟', '🚀'],
            confused: ['🤔', '❓', '😵‍💫', '🙃'],
            
            // Needs/wants
            hungry: ['🍎', '🥕', '🍪', '🍽️'],
            tired: ['😴', '💤', '🛏️', '🌙'],
            playful: ['🎾', '🎮', '🎪', '🎭'],
            attention: ['👋', '👀', '💕', '🫵'],
            
            // Relationship expressions
            bonding: ['💝', '🤗', '👥', '🔗'],
            trust: ['🤝', '💖', '🛡️', '🌈'],
            recognition: ['👁️', '💡', '📝', '🎯']
        };
        
        this.communicationEvolution = new CommunicationEvolution(petId);
        this.personalizedEmojis = new Map(); // Pet develops unique emoji preferences
        this.complexityLevel = 0.1;  // Starts simple, becomes more complex over time
    }
    
    generateMessage(petState, context) {
        // Determine pet's current state
        const mood = this._determineMood(petState);
        const need = this._identifyStrongestNeed(petState);
        const relationshipLevel = this._getRelationshipLevel(petState, context);
        
        // Get relationship emoji
        const relationshipEmoji = this._getRelationshipEmoji(relationshipLevel);
        
        // Generate message based on complexity level
        if (this.complexityLevel < 0.3) {
            // Simple pets use single emojis
            return this._selectEmoji(mood);
        } else if (this.complexityLevel < 0.7) {
            // More developed pets combine emojis
            return [
                this._selectEmoji(mood),
                this._selectEmoji(need)
            ];
        } else {
            // Advanced pets create "sentences"
            return [
                relationshipEmoji,
                this._selectEmoji(mood),
                this._selectEmoji(need),
                this._selectContextualEmoji(context)
            ];
        }
    }
    
    processInteractionFeedback(message, userResponse) {
        // Update communication evolution based on user response
        this.communicationEvolution.processInteractionFeedback({
            message: message,
            elements: Array.isArray(message) ? message : [message]
        }, userResponse);
        
        // Update complexity level
        this.complexityLevel = this.communicationEvolution.complexityLevel;
        
        // Update personalized emoji preferences
        this._updatePersonalizedStyle(message, userResponse);
    }
}

class CommunicationEvolution {
    constructor(petId) {
        this.petId = petId;
        this.vocabularySize = 5; // Start with 5 basic emojis
        this.complexityLevel = 0.1;
        this.personalStyle = {};
        this.successfulPatterns = [];
    }
    
    processInteractionFeedback(communication, userResponse) {
        if (userResponse.understood && userResponse.positive) {
            // Reinforce successful communication patterns
            this.successfulPatterns.push(communication);
            
            // Gradually increase complexity
            this.complexityLevel = Math.min(1.0, this.complexityLevel + 0.01);
            
            // Expand vocabulary when complexity threshold reached
            if (this.complexityLevel > (this.vocabularySize * 0.1)) {
                this.vocabularySize = Math.min(20, this.vocabularySize + 1);
            }
        }
        
        // Develop personal communication style
        this.updatePersonalStyle(communication, userResponse);
    }
    
    updatePersonalStyle(communication, userResponse) {
        // Track which emojis/patterns work best with this specific user
        communication.elements.forEach(element => {
            if (!this.personalStyle[element]) {
                this.personalStyle[element] = { success: 0, attempts: 0 };
            }
            
            this.personalStyle[element].attempts++;
            if (userResponse.understood && userResponse.positive) {
                this.personalStyle[element].success++;
            }
        });
    }
}
```

### Phase 4: Frontend & User Experience (Weeks 7-8)

1. **Pet Visualization**
   - Implement emoji display system
   - Create trait network visualization
   - Build pet state indicators
   - Add animation for behaviors

2. **Interactive Dashboard**
   - Create pet stats display
   - Implement interaction controls
   - Add history visualization
   - Build cognitive development tracking

3. **Pet Relationship UI**
   - Implement pet-to-pet interaction display
   - Create relationship visualization
   - Add communication interpretation helpers
   - Build user relationship tracking

4. **Environmental Display**
   - Implement environment visualization
   - Create resource indicators
   - Build weather display
   - Add region navigation controls

## Testing Strategy

### 4.1 Unit Testing

1. **Fluid Boundary Testing**
   - Test boundary permeability calculations
   - Verify resource exchange mechanics
   - Test energy costs for boundary maintenance
   - Verify assimilation logic

2. **Environment Testing**
   - Test environment state generation
   - Verify resource distribution
   - Test weather impact on pets
   - Verify region mechanics

3. **Trait Evolution Testing**
   - Test trait connection influences
   - Verify evolution based on experiences
   - Test trait mutation mechanisms
   - Verify trait stability over time

4. **Cognitive Development Testing**
   - Test learning rate calculations
   - Verify experience processing
   - Test skill acquisition thresholds
   - Verify cognitive development visualization

### 4.2 Integration Testing

1. **Pet-Environment Integration**
   - Test complete interaction cycles
   - Verify state propagation between systems
   - Test boundary adaptation to environmental changes
   - Verify environmental element effects on pets

2. **Communication Integration**
   - Test emoji generation based on pet state
   - Verify personalization over time
   - Test communication complexity progression
   - Verify communication affects relationships

3. **UI Integration**
   - Test visualization accuracy with actual data
   - Verify user interactions affect pet state
   - Test real-time updates via WebSockets
   - Verify data consistency between front and backend

### 4.3 System Testing

1. **Performance Testing**
   - Test system with multiple pets
   - Measure response times under load
   - Test environmental simulation performance
   - Verify Redis message handling at scale

2. **Longevity Testing**
   - Run extended simulations
   - Verify trait stability over long periods
   - Test memory system performance over time
   - Verify system remains responsive long-term

3. **User Acceptance Testing**
   - Test emotional connection to pets
   - Verify pet personality emergence
   - Test communication effectiveness
   - Verify engagement mechanisms

## 6. Conclusion

This implementation plan unifies the digital pet concept with the core DKS framework, integrating fluid boundaries, cognitive development, and emoji-based communication. The result is a sophisticated yet approachable digital pet system that demonstrates emergent intelligence while avoiding the uncanny valley through its non-threatening communication style.

The phased approach allows for incremental development and testing, with a strong focus on the mechanisms that enable genuine emergence of personality and behavior. By implementing proper energy management and fluid boundaries, we create pets that exist in a meaningful relationship with their environment, developing personalities and communication styles unique to each instance.

The core DKS principles of decentralized control, local interactions, and emergent behavior are preserved, while the pivot to digital pets provides a more engaging and approachable user experience. This implementation plan creates a roadmap for development that ensures all the key components work together harmoniously to create a compelling digital pet experience.

------------------

## Technical Appendix: Architecture Details

### Communication Flow Diagram

```
User Interface <--> API Layer <--> Redis Message Queue <--> Pet Agents <--> Environment
      |                |                                       |
      v                v                                       v
  React UI        Flask API                                Mesa Framework
```

### Key Classes and Methods

```
DigitalPet
  ├── step()
  ├── _update_age()
  ├── _evolve_traits()
  ├── _update_needs()
  ├── _update_vitals()
  ├── _update_attention()
  ├── generate_behaviors()
  └── process_messages()

FluidBoundarySystem
  ├── update()
  ├── attempt_assimilation()
  ├── release_element()
  └── get_status()

PetEnergySystem
  ├── step()
  ├── _collect_energy()
  ├── _allocate_energy()
  └── consume_energy()

PetEnvironment
  ├── step()
  ├── get_state()
  ├── get_pet_view()
  └── _replenish_resources()

ObservableCognitiveDevelopment
  ├── process_experience()
  ├── get_cognitive_level()
  └── can_perform_skill()

PetCommunicationSystem
  ├── generateMessage()
  ├── processInteractionFeedback()
  └── _selectEmoji()
```

### 5.2 Database Schema

```sql
-- Pet core data
CREATE TABLE pets (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    creation_time DATETIME NOT NULL,
    owner_id VARCHAR(36),
    pet_type VARCHAR(50) DEFAULT 'base',
    last_interaction DATETIME,
    FOREIGN KEY (owner_id) REFERENCES users(id)
);

-- Pet state snapshots
CREATE TABLE pet_states (
    id VARCHAR(36) PRIMARY KEY,
    pet_id VARCHAR(36) NOT NULL,
    timestamp DATETIME NOT NULL,
    traits JSON,
    needs JSON,
    health FLOAT,
    energy FLOAT,
    mood FLOAT,
    boundary_permeability FLOAT,
    cognitive_development JSON,
    environmental_elements JSON,
    FOREIGN KEY (pet_id) REFERENCES pets(id)
);

-- User interactions with pets
CREATE TABLE pet_interactions (
    id VARCHAR(36) PRIMARY KEY,
    pet_id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    interaction_type VARCHAR(50) NOT NULL,
    content JSON,
    timestamp DATETIME NOT NULL,
    pet_response JSON,
    response_time FLOAT,
    FOREIGN KEY (pet_id) REFERENCES pets(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Pet relationships
CREATE TABLE pet_relationships (
    id VARCHAR(36) PRIMARY KEY,
    pet_id VARCHAR(36) NOT NULL,
    target_id VARCHAR(36) NOT NULL,
    relationship_type ENUM('pet-pet', 'pet-human'),
    strength FLOAT DEFAULT 0,
    last_interaction DATETIME,
    relationship_data JSON,
    FOREIGN KEY (pet_id) REFERENCES pets(id)
);

-- Pet behaviors
CREATE TABLE pet_behaviors (
    id VARCHAR(36) PRIMARY KEY,
    pet_id VARCHAR(36) NOT NULL,
    behavior_name VARCHAR(100) NOT NULL,
    behavior_data JSON,
    first_observed DATETIME,
    last_observed DATETIME,
    frequency INT DEFAULT 1,
    FOREIGN KEY (pet_id) REFERENCES pets(id)
);
```
