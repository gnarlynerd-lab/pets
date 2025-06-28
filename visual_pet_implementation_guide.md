# Procedural Pet Generation Implementation Guide
## Using p5.js with Constraint-Based Animation for Dynamic Kinetic Systems

This document provides implementation guidelines for creating procedurally generated digital pets using a hybrid approach that combines p5.js for visual generation with constraint-based animation logic. This approach aligns with Dynamic Kinetic Systems (DKS) principles where entities maintain stability through continuous activity and adaptation rather than static states.

## Architecture Overview

```
┌────────────────────────────────────────────────────┐
│                                                    │
│  Pet Generation & Evolution System                 │
│  ┌──────────────────────┐  ┌───────────────────┐   │
│  │                      │  │                   │   │
│  │  Trait Engine        │  │  Physics Engine   │   │
│  │  - Personality       │  │  - Movement       │   │
│  │  - Appearance        │  │  - Animation      │   │
│  │  - Abilities         │  │  - Interactions   │   │
│  │                      │  │                   │   │
│  └──────────┬───────────┘  └────────┬──────────┘   │
│             │                       │              │
│             ▼                       ▼              │
│  ┌──────────────────────────────────────────────┐  │
│  │                                              │  │
│  │              Rendering Engine                │  │
│  │              (p5.js based)                   │  │
│  │                                              │  │
│  └──────────────────────┬───────────────────────┘  │
│                         │                          │
└─────────────────────────┼──────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│                                                     │
│                  User Interface                     │
│  ┌─────────────────────┐  ┌────────────────────┐    │
│  │                     │  │                    │    │
│  │   Pet Display       │  │  Interaction       │    │
│  │                     │  │  Controls          │    │
│  └─────────────────────┘  └────────────────────┘    │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## 1. Core Implementation Components

### 1.1 Trait Engine

The Trait Engine manages the pet's internal state, personality traits, and evolutionary parameters. This forms the foundation of your DKS implementation.

```javascript
class TraitEngine {
  constructor(initialTraits = null) {
    // Core personality traits (0-1 scale)
    this.traits = initialTraits || this.generateInitialTraits();
    
    // Internal state variables
    this.energy = 0.7;          // Current energy level
    this.attention = 0.5;       // Attention received recently
    this.mood = 0.6;            // Current emotional state
    this.complexity = 0.1;      // Overall developmental stage
    
    // Evolution tracking
    this.evolutionPoints = 0;
    this.stageThresholds = [100, 300, 600, 1000]; // Points needed for evolution
    this.developmentStage = 0;  // Current evolution stage (0-4)
    
    // Appearance genes - these directly affect visual representation
    this.appearanceGenes = this.generateAppearanceGenes();
    
    // Interaction history
    this.interactionHistory = [];
  }
  
  generateInitialTraits() {
    return {
      curiosity: 0.3 + Math.random() * 0.4,
      playfulness: 0.3 + Math.random() * 0.4,
      sociability: 0.3 + Math.random() * 0.4,
      independence: 0.3 + Math.random() * 0.4,
      adaptability: 0.3 + Math.random() * 0.4,
      energy: 0.4 + Math.random() * 0.3
    };
  }
  
  generateAppearanceGenes() {
    return {
      // Basic structure
      baseSize: 0.5 + Math.random() * 0.5,
      bodyShape: Math.floor(Math.random() * 5), // 0-4: different basic shapes
      symmetry: 0.7 + Math.random() * 0.3,
      
      // Color properties
      primaryHue: Math.random() * 360,
      primarySaturation: 0.5 + Math.random() * 0.5,
      primaryLightness: 0.4 + Math.random() * 0.3,
      secondaryHue: (Math.random() * 360 + 180) % 360, // Complementary color
      
      // Feature properties
      numFeatures: 2 + Math.floor(Math.random() * 3),
      featureSize: 0.2 + Math.random() * 0.3,
      featureComplexity: 0.1 + Math.random() * 0.3
    };
  }
  
  // Process an interaction and update internal state
  processInteraction(type, duration, intensity) {
    // Record interaction
    this.interactionHistory.push({
      type,
      duration,
      intensity,
      timestamp: Date.now()
    });
    
    // Update energy based on interaction type
    const energyImpacts = {
      click: 0.05,
      hold: 0.02,
      pet: 0.08,
      feed: 0.15,
      play: -0.1 // Play reduces energy but has other benefits
    };
    
    // Apply energy change with diminishing returns
    const baseChange = (energyImpacts[type] || 0) * intensity * duration;
    this.energy = Math.max(0, Math.min(1, this.energy + baseChange));
    
    // Update attention
    this.attention = Math.min(1, this.attention + (intensity * 0.1));
    
    // Calculate mood based on energy and attention
    this.mood = (this.energy * 0.6) + (this.attention * 0.4);
    
    // Accumulate evolution points
    const pointsGained = duration * intensity * 10;
    this.evolutionPoints += pointsGained;
    
    // Check for evolution stage changes
    this.checkEvolution();
    
    // Evolve traits based on interaction
    this.evolveTraits(type, intensity);
    
    return {
      energyChange: baseChange,
      pointsGained,
      currentStage: this.developmentStage
    };
  }
  
  // Check if the pet can evolve to a new stage
  checkEvolution() {
    for (let i = 0; i < this.stageThresholds.length; i++) {
      if (this.developmentStage === i && 
          this.evolutionPoints >= this.stageThresholds[i]) {
        this.developmentStage = i + 1;
        this.complexity = Math.min(1, this.complexity + 0.2);
        
        // Evolve appearance when stage changes
        this.evolveAppearance();
        
        return true;
      }
    }
    return false;
  }
  
  // Gradually change traits based on interactions
  evolveTraits(interactionType, intensity) {
    const traitInfluences = {
      click: { curiosity: 0.01 },
      hold: { sociability: 0.01 },
      pet: { sociability: 0.02, independence: -0.01 },
      feed: { adaptability: 0.01, energy: 0.01 },
      play: { playfulness: 0.02, energy: 0.01, curiosity: 0.01 }
    };
    
    const influences = traitInfluences[interactionType] || {};
    
    // Apply small changes to traits
    for (const [trait, change] of Object.entries(influences)) {
      if (this.traits[trait] !== undefined) {
        // Calculate change with diminishing returns
        const actualChange = change * intensity * (1 - Math.abs(this.traits[trait] - 0.5));
        this.traits[trait] = Math.max(0, Math.min(1, this.traits[trait] + actualChange));
      }
    }
  }
  
  // Evolve appearance genes based on current traits and stage
  evolveAppearance() {
    // Feature count increases with complexity
    this.appearanceGenes.numFeatures = 2 + Math.floor(this.complexity * 5);
    
    // Color saturation affected by mood
    this.appearanceGenes.primarySaturation = 0.3 + (this.mood * 0.7);
    
    // Size affected by energy
    this.appearanceGenes.baseSize = 0.5 + (this.energy * 0.5);
    
    // Shape complexity affected by developmental stage
    this.appearanceGenes.featureComplexity = 0.1 + (this.developmentStage * 0.2);
    
    // Traits influence appearance
    this.appearanceGenes.primaryHue = (this.traits.playfulness * 120) + (this.traits.energy * 240);
    this.appearanceGenes.symmetry = 0.5 + (this.traits.adaptability * 0.5);
    this.appearanceGenes.featureSize = 0.2 + (this.traits.curiosity * 0.3);
  }
  
  // Apply time decay to pet state when not interacted with
  applyTimeDecay(elapsedHours) {
    // Energy naturally decays
    const energyDecay = 0.05 * elapsedHours;
    this.energy = Math.max(0, this.energy - energyDecay);
    
    // Attention decays faster
    const attentionDecay = 0.1 * elapsedHours;
    this.attention = Math.max(0, this.attention - attentionDecay);
    
    // Update mood based on new values
    this.mood = (this.energy * 0.6) + (this.attention * 0.4);
  }
  
  // Get current state for rendering and logic
  getCurrentState() {
    return {
      traits: {...this.traits},
      energy: this.energy,
      attention: this.attention,
      mood: this.mood,
      complexity: this.complexity,
      developmentStage: this.developmentStage,
      evolutionPoints: this.evolutionPoints,
      appearanceGenes: {...this.appearanceGenes}
    };
  }
}
```

### 1.2 Physics Engine

The Physics Engine handles the pet's movement, animations, and interactions with the environment, implementing the constraint-based animation logic.

```javascript
class PhysicsEngine {
  constructor(traitEngine) {
    this.traitEngine = traitEngine;
    
    // Physics parameters
    this.position = { x: 0, y: 0 };
    this.velocity = { x: 0, y: 0 };
    this.acceleration = { x: 0, y: 0 };
    
    // Movement constraints
    this.constraints = {
      maxSpeed: 5,
      friction: 0.9,
      boundsRadius: 150,
      centerAttraction: 0.01
    };
    
    // Animation state
    this.animationState = 'idle';
    this.animationProgress = 0;
    this.animationSpeed = 0.05;
    
    // Body parts for constraint-based animation
    this.bodyParts = this.initializeBodyParts();
    
    // Behavior system
    this.behaviors = {
      wander: { weight: 0.5, cooldown: 0 },
      rest: { weight: 0.3, cooldown: 0 },
      play: { weight: 0.2, cooldown: 0 },
      seek: { weight: 0.4, cooldown: 0 }
    };
    
    // Current target
    this.target = null;
  }
  
  initializeBodyParts() {
    // Create body parts with relative positions and constraints
    return {
      body: { x: 0, y: 0, baseX: 0, baseY: 0, springStrength: 0.1 },
      feature1: { x: 20, y: -20, baseX: 20, baseY: -20, springStrength: 0.08 },
      feature2: { x: -20, y: -20, baseX: -20, baseY: -20, springStrength: 0.08 }
      // More features will be added dynamically as pet evolves
    };
  }
  
  // Update physics and animation state
  update(deltaTime, userInteraction = null) {
    // Get current traits and state
    const state = this.traitEngine.getCurrentState();
    
    // Update animation speed based on energy
    this.animationSpeed = 0.03 + (state.energy * 0.07);
    
    // Update constraints based on traits
    this.updateConstraints(state);
    
    // Handle user interaction if present
    if (userInteraction) {
      this.handleInteraction(userInteraction);
    }
    
    // Determine behavior based on state and traits
    this.selectBehavior(state);
    
    // Apply behavior forces
    this.applyBehaviorForces(state);
    
    // Apply physics
    this.applyPhysics(deltaTime);
    
    // Update body parts with constraint-based animation
    this.updateBodyParts(deltaTime, state);
    
    // Update animation progress
    this.updateAnimation(deltaTime);
  }
  
  updateConstraints(state) {
    // Update physical constraints based on pet's traits and state
    this.constraints.maxSpeed = 3 + (state.traits.energy * 4);
    this.constraints.friction = 0.95 - (state.traits.playfulness * 0.1);
    this.constraints.centerAttraction = 0.01 + (state.traits.independence * 0.01);
    
    // Body part constraints change with development
    for (const part in this.bodyParts) {
      this.bodyParts[part].springStrength = 0.05 + (state.traits.adaptability * 0.1);
    }
    
    // Add new body parts if needed based on evolution
    if (Object.keys(this.bodyParts).length < state.appearanceGenes.numFeatures + 1) {
      this.addBodyPart(state);
    }
  }
  
  addBodyPart(state) {
    // Add a new body part with position based on symmetry
    const partCount = Object.keys(this.bodyParts).length;
    const angle = (partCount * 2 * Math.PI / (state.appearanceGenes.numFeatures + 1)) * state.appearanceGenes.symmetry;
    const distance = 20 + (state.appearanceGenes.featureSize * 15);
    
    const baseX = Math.cos(angle) * distance;
    const baseY = Math.sin(angle) * distance;
    
    this.bodyParts[`feature${partCount}`] = { 
      x: baseX, 
      y: baseY, 
      baseX: baseX, 
      baseY: baseY, 
      springStrength: 0.05 + (Math.random() * 0.05) 
    };
  }
  
  handleInteraction(interaction) {
    // Apply forces based on user interaction
    if (interaction.type === 'click') {
      // Move toward click
      const dx = interaction.x - this.position.x;
      const dy = interaction.y - this.position.y;
      const distance = Math.sqrt(dx * dx + dy * dy);
      
      if (distance < 100) {
        this.acceleration.x += dx * 0.05;
        this.acceleration.y += dy * 0.05;
        this.animationState = 'excited';
      }
    } else if (interaction.type === 'hold') {
      // Stay near hold position
      this.target = { x: interaction.x, y: interaction.y };
      this.animationState = 'attentive';
    }
  }
  
  selectBehavior(state) {
    // Adjust behavior weights based on traits and state
    this.behaviors.wander.weight = 0.3 + (state.traits.curiosity * 0.5);
    this.behaviors.rest.weight = (1 - state.energy) * 0.8;
    this.behaviors.play.weight = state.traits.playfulness * 0.7;
    this.behaviors.seek.weight = state.traits.sociability * 0.5;
    
    // Cooldowns prevent behavior thrashing
    for (const behavior in this.behaviors) {
      if (this.behaviors[behavior].cooldown > 0) {
        this.behaviors[behavior].cooldown--;
      }
    }
    
    // Select behavior probabilistically based on weights
    if (this.animationState === 'idle') {
      let totalWeight = 0;
      const availableBehaviors = [];
      
      for (const behavior in this.behaviors) {
        if (this.behaviors[behavior].cooldown === 0) {
          totalWeight += this.behaviors[behavior].weight;
          availableBehaviors.push(behavior);
        }
      }
      
      if (availableBehaviors.length > 0) {
        const rand = Math.random() * totalWeight;
        let cumulativeWeight = 0;
        
        for (const behavior of availableBehaviors) {
          cumulativeWeight += this.behaviors[behavior].weight;
          if (rand <= cumulativeWeight) {
            this.animationState = behavior;
            this.behaviors[behavior].cooldown = 60; // Prevent immediate reselection
            break;
          }
        }
      }
    }
  }
  
  applyBehaviorForces(state) {
    // Apply forces based on current behavior
    switch (this.animationState) {
      case 'wander':
        // Random wandering with directional persistence
        if (Math.random() < 0.05) {
          this.acceleration.x += (Math.random() - 0.5) * 0.2;
          this.acceleration.y += (Math.random() - 0.5) * 0.2;
        }
        break;
        
      case 'rest':
        // Slow down and stop
        this.velocity.x *= 0.8;
        this.velocity.y *= 0.8;
        break;
        
      case 'play':
        // Energetic random movement
        this.acceleration.x += (Math.random() - 0.5) * 0.5;
        this.acceleration.y += (Math.random() - 0.5) * 0.5;
        break;
        
      case 'seek':
        // Move toward target or center if no target
        const targetX = this.target ? this.target.x : 0;
        const targetY = this.target ? this.target.y : 0;
        
        const dx = targetX - this.position.x;
        const dy = targetY - this.position.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance > 5) {
          this.acceleration.x += dx * 0.01;
          this.acceleration.y += dy * 0.01;
        } else if (this.target) {
          // Reached target, clear it
          this.target = null;
          this.animationState = 'idle';
        }
        break;
    }
    
    // Always apply center attraction to keep pet in bounds
    const distToCenter = Math.sqrt(
      this.position.x * this.position.x + 
      this.position.y * this.position.y
    );
    
    if (distToCenter > this.constraints.boundsRadius) {
      // Apply stronger force when near boundary
      const centerForce = this.constraints.centerAttraction * 
        (distToCenter / this.constraints.boundsRadius);
        
      this.acceleration.x -= this.position.x * centerForce;
      this.acceleration.y -= this.position.y * centerForce;
    }
  }
  
  applyPhysics(deltaTime) {
    // Update velocity with acceleration
    this.velocity.x += this.acceleration.x * deltaTime;
    this.velocity.y += this.acceleration.y * deltaTime;
    
    // Apply friction
    this.velocity.x *= this.constraints.friction;
    this.velocity.y *= this.constraints.friction;
    
    // Limit speed
    const speed = Math.sqrt(
      this.velocity.x * this.velocity.x + 
      this.velocity.y * this.velocity.y
    );
    
    if (speed > this.constraints.maxSpeed) {
      this.velocity.x = (this.velocity.x / speed) * this.constraints.maxSpeed;
      this.velocity.y = (this.velocity.y / speed) * this.constraints.maxSpeed;
    }
    
    // Update position
    this.position.x += this.velocity.x * deltaTime;
    this.position.y += this.velocity.y * deltaTime;
    
    // Reset acceleration
    this.acceleration.x = 0;
    this.acceleration.y = 0;
  }
  
  updateBodyParts(deltaTime, state) {
    // Apply spring forces to body parts to maintain relative positions
    for (const partName in this.bodyParts) {
      const part = this.bodyParts[partName];
      
      // Base position relative to main body
      let targetX = this.position.x;
      let targetY = this.position.y;
      
      if (partName !== 'body') {
        targetX += part.baseX;
        targetY += part.baseY;
      }
      
      // Apply spring force
      const dx = targetX - part.x;
      const dy = targetY - part.y;
      
      // Add some oscillation based on animation state
      let oscX = 0;
      let oscY = 0;
      
      switch (this.animationState) {
        case 'idle':
          oscX = Math.sin(this.animationProgress * 2) * 2;
          oscY = Math.sin(this.animationProgress * 2) * 2;
          break;
        case 'excited':
          oscX = Math.sin(this.animationProgress * 8) * 5;
          oscY = Math.sin(this.animationProgress * 6) * 5;
          break;
        case 'play':
          oscX = Math.sin(this.animationProgress * 10) * 8;
          oscY = Math.sin(this.animationProgress * 8) * 8;
          break;
        case 'rest':
          oscX = Math.sin(this.animationProgress) * 1;
          oscY = Math.sin(this.animationProgress * 0.8) * 1;
          break;
      }
      
      // Scale oscillation by energy
      oscX *= state.energy;
      oscY *= state.energy;
      
      // Apply force with some randomness for natural movement
      part.x += (dx + oscX) * part.springStrength * deltaTime;
      part.y += (dy + oscY) * part.springStrength * deltaTime;
    }
  }
  
  updateAnimation(deltaTime) {
    // Progress animation cycle
    this.animationProgress += this.animationSpeed * deltaTime;
    
    // Reset cycle
    if (this.animationProgress > Math.PI * 2) {
      this.animationProgress -= Math.PI * 2;
      
      // Possibly return to idle state
      if (this.animationState !== 'idle' && Math.random() < 0.2) {
        this.animationState = 'idle';
      }
    }
  }
  
  // Get current state for rendering
  getCurrentPhysicsState() {
    return {
      position: {...this.position},
      velocity: {...this.velocity},
      bodyParts: JSON.parse(JSON.stringify(this.bodyParts)),
      animationState: this.animationState,
      animationProgress: this.animationProgress
    };
  }
}
```

### 1.3 Rendering Engine

The Rendering Engine uses p5.js to visualize the pet based on its traits, state, and physics.

```javascript
class PetRenderer {
  constructor(traitEngine, physicsEngine, p5instance) {
    this.traitEngine = traitEngine;
    this.physicsEngine = physicsEngine;
    this.p5 = p5instance;
    
    // Visual style parameters
    this.baseSize = 50;
    this.colorPalette = {};
    
    // Effect animations
    this.effects = [];
    
    // Animation transitions
    this.lastState = {};
    this.stateTransition = 0;
    
    // Initialize color palette
    this.updateColorPalette();
  }
  
  updateColorPalette() {
    const genes = this.traitEngine.getCurrentState().appearanceGenes;
    
    // Create color palette based on appearance genes
    this.colorPalette = {
      primary: this.p5.color(
        genes.primaryHue, 
        genes.primarySaturation * 100, 
        genes.primaryLightness * 100
      ),
      secondary: this.p5.color(
        genes.secondaryHue, 
        genes.primarySaturation * 80, 
        genes.primaryLightness * 80
      ),
      detail: this.p5.color(
        (genes.primaryHue + 30) % 360, 
        genes.primarySaturation * 90, 
        genes.primaryLightness * 60
      ),
      outline: this.p5.color(
        genes.primaryHue, 
        genes.primarySaturation * 90, 
        genes.primaryLightness * 30
      )
    };
  }
  
  // Main render function
  render() {
    // Get current state
    const traits = this.traitEngine.getCurrentState();
    const physics = this.physicsEngine.getCurrentPhysicsState();
    
    // Update colors if traits changed significantly
    if (this.stateTransition === 0) {
      this.updateColorPalette();
    }
    
    // Save drawing state
    this.p5.push();
    
    // Use HSB color mode
    this.p5.colorMode(this.p5.HSB, 360, 100, 100, 1);
    
    // Draw background elements if needed
    this.drawBackground(traits);
    
    // Draw pet body and features
    this.drawPet(traits, physics);
    
    // Draw effects
    this.drawEffects(traits);
    
    // Restore drawing state
    this.p5.pop();
    
    // Update transition state
    this.lastState = traits;
  }
  
  drawBackground(traits) {
    // Optional background elements that reflect pet's state
    // For example, energy field, mood indicators, etc.
    
    // Draw energy indicator
    const energyAlpha = 0.1 + (traits.energy * 0.2);
    const energySize = 100 + (traits.energy * 100);
    
    this.p5.noStroke();
    this.p5.fill(
      this.p5.hue(this.colorPalette.primary),
      this.p5.saturation(this.colorPalette.primary) * 0.5,
      this.p5.brightness(this.colorPalette.primary),
      energyAlpha
    );
    
    this.p5.ellipse(0, 0, energySize, energySize);
  }
  
  drawPet(traits, physics) {
    // Translate to pet position
    this.p5.translate(physics.position.x, physics.position.y);
    
    // Calculate size based on traits
    const size = this.baseSize * traits.appearanceGenes.baseSize;
    
    // Draw each body part
    for (const partName in physics.bodyParts) {
      const part = physics.bodyParts[partName];
      
      // Only draw the part if it's within our view
      this.p5.push();
      this.p5.translate(part.x - physics.position.x, part.y - physics.position.y);
      
      if (partName === 'body') {
        this.drawBody(traits, size, physics.animationState, physics.animationProgress);
      } else {
        this.drawFeature(traits, partName, size, physics.animationState, physics.animationProgress);
      }
      
      this.p5.pop();
    }
    
    // Draw connecting elements between parts
    this.drawConnections(traits, physics);
    
    // Draw expressions based on mood and state
    this.drawExpression(traits, physics);
  }
  
  drawBody(traits, size, animationState, animationProgress) {
    // Draw main body based on shape type
    const shape = traits.appearanceGenes.bodyShape;
    const wobble = Math.sin(animationProgress) * (0.05 + (traits.energy * 0.05));
    const adjustedSize = size * (1 + wobble);
    
    // Set fill and stroke
    this.p5.fill(this.colorPalette.primary);
    this.p5.stroke(this.colorPalette.outline);
    this.p5.strokeWeight(2 + (traits.complexity * 2));
    
    switch (shape) {
      case 0: // Circle
        this.p5.ellipse(0, 0, adjustedSize, adjustedSize);
        break;
        
      case 1: // Square with rounded corners
        this.p5.rect(
          -adjustedSize/2, -adjustedSize/2, 
          adjustedSize, adjustedSize, 
          adjustedSize * 0.2
        );
        break;
        
      case 2: // Triangle
        this.p5.triangle(
          0, -adjustedSize/2,
          -adjustedSize/2, adjustedSize/2,
          adjustedSize/2, adjustedSize/2
        );
        break;
        
      case 3: // Star
        this.drawStar(0, 0, adjustedSize/2, adjustedSize/4, 5);
        break;
        
      case 4: // Blob
        this.drawBlob(adjustedSize/2, traits.complexity * 0.3, animationProgress);
        break;
    }
    
    // Add inner details based on complexity
    if (traits.complexity > 0.3) {
      this.p5.fill(this.colorPalette.secondary);
      this.p5.noStroke();
      this.p5.ellipse(0, 0, adjustedSize * 0.6, adjustedSize * 0.6);
    }
  }
  
  drawFeature(traits, featureName, baseSize, animationState, animationProgress) {
    // Extract feature index from name
    const featureIndex = parseInt(featureName.replace('feature', '')) || 0;
    const featureSize = baseSize * 0.3 * traits.appearanceGenes.featureSize;
    
    // Animate feature
    const wobble = Math.sin(animationProgress + featureIndex) * 0.1;
    const adjustedSize = featureSize * (1 + wobble);
    
    // Set fill and stroke
    this.p5.fill(this.colorPalette.secondary);
    this.p5.stroke(this.colorPalette.outline);
    this.p5.strokeWeight(1 + (traits.complexity));
    
    // Draw feature shape - shape varies based on complexity and feature index
    const shapeType = (featureIndex + traits.appearanceGenes.bodyShape) % 5;
    
    switch (shapeType) {
      case 0: // Circle
        this.p5.ellipse(0, 0, adjustedSize, adjustedSize);
        break;
        
      case 1: // Rectangle
        this.p5.rect(-adjustedSize/2, -adjustedSize/2, adjustedSize, adjustedSize);
        break;
        
      case 2: // Triangle
        this.p5.triangle(
          0, -adjustedSize/2,
          -adjustedSize/2, adjustedSize/2,
          adjustedSize/2, adjustedSize/2
        );
        break;
        
      case 3: // Diamond
        this.p5.quad(
          0, -adjustedSize/2,
          adjustedSize/2, 0,
          0, adjustedSize/2,
          -adjustedSize/2, 0
        );
        break;
        
      case 4: // Small blob
        this.drawBlob(adjustedSize/2, traits.complexity * 0.2, animationProgress + featureIndex);
        break;
    }
    
    // Add detail based on complexity
    if (traits.complexity > 0.5) {
      this.p5.fill(this.colorPalette.detail);
      this.p5.noStroke();
      this.p5.ellipse(0, 0, adjustedSize * 0.4, adjustedSize * 0.4);
    }
  }
  
  drawConnections(traits, physics) {
    // Draw connections between body parts for more advanced pets
    if (traits.complexity < 0.3) return;
    
    this.p5.stroke(this.colorPalette.outline);
    this.p5.strokeWeight(1 + (traits.complexity));
    this.p5.noFill();
    
    const bodyPart = physics.bodyParts.body;
    
    for (const partName in physics.bodyParts) {
      if (partName !== 'body') {
        const part = physics.bodyParts[partName];
        
        // Draw connection line or curve
        if (traits.complexity > 0.6) {
          // Bezier curve for advanced pets
          const dx = part.x - bodyPart.x;
          const dy = part.y - bodyPart.y;
          const midX = bodyPart.x + dx * 0.5;
          const midY = bodyPart.y + dy * 0.5;
          const perpX = -dy * 0.2;
          const perpY = dx * 0.2;
          
          this.p5.bezier(
            bodyPart.x - physics.position.x, bodyPart.y - physics.position.y,
            midX - physics.position.x + perpX, midY - physics.position.y + perpY,
            midX - physics.position.x - perpX, midY - physics.position.y - perpY,
            part.x - physics.position.x, part.y - physics.position.y
          );
        } else {
          // Simple line for less complex pets
          this.p5.line(
            bodyPart.x - physics.position.x, bodyPart.y - physics.position.y,
            part.x - physics.position.x, part.y - physics.position.y
          );
        }
      }
    }
  }
  
  drawExpression(traits, physics) {
    // Draw facial features on the main body
    const bodyPart = physics.bodyParts.body;
    const size = this.baseSize * traits.appearanceGenes.baseSize;
    
    // Only draw expression if complexity is high enough
    if (traits.complexity < 0.2) return;
    
    this.p5.push();
    this.p5.translate(bodyPart.x - physics.position.x, bodyPart.y - physics.position.y);
    
    // Draw eyes
    this.p5.fill(10, 10, 10);
    this.p5.noStroke();
    
    // Eye size based on complexity
    const eyeSize = size * 0.15;
    const eyeDistance = size * 0.2;
    
    // Eye position affected by animation state
    let eyeShiftX = 0;
    let eyeShiftY = 0;
    
    if (physics.animationState === 'seek') {
      // Eyes look toward movement direction
      eyeShiftX = Math.min(1, Math.max(-1, physics.velocity.x)) * 2;
    } else if (physics.animationState === 'rest') {
      // Eyes close slightly when resting
      eyeShiftY = 1;
    }
    
    // Left eye
    this.p5.ellipse(
      -eyeDistance + eyeShiftX, 
      -size * 0.1 + eyeShiftY, 
      eyeSize, 
      physics.animationState === 'rest' ? eyeSize * 0.3 : eyeSize
    );
    
    // Right eye
    this.p5.ellipse(
      eyeDistance + eyeShiftX, 
      -size * 0.1 + eyeShiftY, 
      eyeSize, 
      physics.animationState === 'rest' ? eyeSize * 0.3 : eyeSize
    );
    
    // Draw mouth if complex enough
    if (traits.complexity > 0.3) {
      this.p5.stroke(this.colorPalette.outline);
      this.p5.noFill();
      this.p5.strokeWeight(2);
      
      // Mouth shape based on mood
      if (traits.mood > 0.7) {
        // Happy
        this.p5.arc(0, size * 0.1, size * 0.3, size * 0.2, 0, this.p5.PI);
      } else if (traits.mood < 0.3) {
        // Sad
        this.p5.arc(0, size * 0.2, size * 0.3, size * 0.2, this.p5.PI, this.p5.TWO_PI);
      } else {
        // Neutral
        this.p5.line(-size * 0.15, size * 0.15, size * 0.15, size * 0.15);
      }
    }
    
    this.p5.pop();
  }
  
  drawBlob(radius, complexity, phase) {
    // Draw a blob shape with oscillating edges
    this.p5.beginShape();
    
    const points = 12 + Math.floor(complexity * 8);
    
    for (let i = 0; i < points; i++) {
      const angle = (i / points) * this.p5.TWO_PI;
      
      // Calculate radius variation
      const r = radius * (1 + (Math.sin(angle * 3 + phase) * complexity * 0.3));
      
      const x = Math.cos(angle) * r;
      const y = Math.sin(angle) * r;
      
      this.p5.vertex(x, y);
    }
    
    this.p5.endShape(this.p5.CLOSE);
  }
  
  drawStar(x, y, radius1, radius2, npoints) {
    // Draw a star shape
    this.p5.beginShape();
    
    for (let i = 0; i < npoints * 2; i++) {
      const angle = (i * this.p5.PI) / npoints;
      const r = (i % 2 === 0) ? radius1 : radius2;
      const sx = x + Math.cos(angle) * r;
      const sy = y + Math.sin(angle) * r;
      this.p5.vertex(sx, sy);
    }
    
    this.p5.endShape(this.p5.CLOSE);
  }
  
  // Add an effect animation
  addEffect(type, x, y) {
    this.effects.push({
      type,
      x,
      y,
      age: 0,
      maxAge: 30
    });
  }
  
  // Draw active effects
  drawEffects(traits) {
    // Update and draw effects
    for (let i = this.effects.length - 1; i >= 0; i--) {
      const effect = this.effects[i];
      
      // Age the effect
      effect.age++;
      
      // Remove if too old
      if (effect.age > effect.maxAge) {
        this.effects.splice(i, 1);
        continue;
      }
      
      // Draw based on type
      const progress = effect.age / effect.maxAge;
      
      this.p5.push();
      this.p5.translate(effect.x, effect.y);
      
      switch (effect.type) {
        case 'click':
          this.p5.noFill();
          this.p5.stroke(
            this.p5.hue(this.colorPalette.primary),
            this.p5.saturation(this.colorPalette.primary),
            this.p5.brightness(this.colorPalette.primary),
            1 - progress
          );
          this.p5.strokeWeight(2);
          this.p5.ellipse(0, 0, progress * 50, progress * 50);
          break;
          
        case 'evolution':
          // Particle burst effect
          for (let j = 0; j < 10; j++) {
            const angle = (j / 10) * this.p5.TWO_PI;
            const distance = progress * 100;
            const x = Math.cos(angle) * distance;
            const y = Math.sin(angle) * distance;
            
            this.p5.fill(
              (this.p5.hue(this.colorPalette.primary) + j * 20) % 360,
              this.p5.saturation(this.colorPalette.primary),
              this.p5.brightness(this.colorPalette.primary),
              1 - progress
            );
            
            this.p5.ellipse(x, y, 10 * (1 - progress), 10 * (1 - progress));
          }
          break;
      }
      
      this.p5.pop();
    }
  }
}
```

## 2. Main Application Integration

### 2.1 Main p5.js Sketch

```javascript
// Main p5.js sketch to integrate all components
let sketch = function(p) {
  // Declare components
  let traitEngine;
  let physicsEngine;
  let petRenderer;
  
  // Canvas size
  const canvasWidth = 600;
  const canvasHeight = 400;
  
  // Interaction tracking
  let lastInteractionTime = 0;
  let userInteraction = null;
  
  // UI elements
  let interactionButtons = [];
  
  p.setup = function() {
    // Create canvas
    let canvas = p.createCanvas(canvasWidth, canvasHeight);
    canvas.parent('pet-container');
    
    // Initialize components
    traitEngine = new TraitEngine();
    physicsEngine = new PhysicsEngine(traitEngine);
    petRenderer = new PetRenderer(traitEngine, physicsEngine, p);
    
    // Set color mode to HSB
    p.colorMode(p.HSB, 360, 100, 100, 1);
    
    // Center coordinates
    p.rectMode(p.CENTER);
    p.ellipseMode(p.CENTER);
    
    // Create UI elements
    createInteractionButtons();
    
    // Load saved pet if available
    loadPet();
  };
  
  p.draw = function() {
    // Calculate delta time (capped to avoid large jumps)
    const deltaTime = Math.min(p.deltaTime / 16, 2);
    
    // Clear background
    p.background(240, 10, 95);
    
    // Apply time decay if not interacted recently
    const currentTime = p.millis();
    const timeSinceInteraction = (currentTime - lastInteractionTime) / 1000; // in seconds
    
    if (timeSinceInteraction > 10) {
      // Calculate decay in hours
      const decayHours = (timeSinceInteraction - 10) / 3600;
      if (decayHours > 0) {
        traitEngine.applyTimeDecay(decayHours);
      }
    }
    
    // Update physics with user interaction
    physicsEngine.update(deltaTime, userInteraction);
    userInteraction = null; // Clear after using
    
    // Translate to center of canvas for drawing
    p.push();
    p.translate(canvasWidth / 2, canvasHeight / 2);
    
    // Render pet
    petRenderer.render();
    
    p.pop();
    
    // Draw UI elements
    drawUI();
    
    // Save pet state periodically
    if (p.frameCount % 300 === 0) {
      savePet();
    }
  };
  
  p.mousePressed = function() {
    // Convert to canvas coordinates
    const mouseX = p.mouseX - canvasWidth / 2;
    const mouseY = p.mouseY - canvasHeight / 2;
    
    // Check if clicked within canvas bounds
    if (p.mouseX >= 0 && p.mouseX < canvasWidth && 
        p.mouseY >= 0 && p.mouseY < canvasHeight) {
      
      // Check if clicked on any UI buttons
      const buttonClicked = checkButtonClicks();
      
      if (!buttonClicked) {
        // Regular click interaction
        userInteraction = {
          type: 'click',
          x: mouseX,
          y: mouseY,
          intensity: 1.0
        };
        
        // Process interaction in trait engine
        const result = traitEngine.processInteraction('click', 1, 1.0);
        
        // Record interaction time
        lastInteractionTime = p.millis();
        
        // Add visual effect
        petRenderer.addEffect('click', mouseX, mouseY);
        
        // Check for evolution
        if (result.currentStage > traitEngine.developmentStage - 1) {
          // Pet evolved!
          petRenderer.addEffect('evolution', 0, 0);
        }
      }
    }
  };
  
  p.mouseDragged = function() {
    // Convert to canvas coordinates
    const mouseX = p.mouseX - canvasWidth / 2;
    const mouseY = p.mouseY - canvasHeight / 2;
    
    // Check if within canvas bounds
    if (p.mouseX >= 0 && p.mouseX < canvasWidth && 
        p.mouseY >= 0 && p.mouseY < canvasHeight) {
      
      // Dragging interaction
      userInteraction = {
        type: 'hold',
        x: mouseX,
        y: mouseY,
        intensity: 0.7
      };
      
      // Process interaction in trait engine
      traitEngine.processInteraction('hold', 0.5, 0.7);
      
      // Record interaction time
      lastInteractionTime = p.millis();
    }
  };
  
  function createInteractionButtons() {
    // Create interaction buttons
    interactionButtons = [
      {
        text: "Feed",
        x: 60,
        y: canvasHeight - 30,
        width: 80,
        height: 40,
        action: function() {
          feedPet();
        }
      },
      {
        text: "Play",
        x: 160,
        y: canvasHeight - 30,
        width: 80,
        height: 40,
        action: function() {
          playWithPet();
        }
      },
      {
        text: "Pet",
        x: 260,
        y: canvasHeight - 30,
        width: 80,
        height: 40,
        action: function() {
          petPet();
        }
      }
    ];
  }
  
  function checkButtonClicks() {
    for (const button of interactionButtons) {
      if (p.mouseX >= button.x - button.width/2 && 
          p.mouseX <= button.x + button.width/2 &&
          p.mouseY >= button.y - button.height/2 && 
          p.mouseY <= button.y + button.height/2) {
        
        button.action();
        return true;
      }
    }
    return false;
  }
  
  function feedPet() {
    // Process feed interaction
    const result = traitEngine.processInteraction('feed', 3, 0.9);
    
    // Update physics
    userInteraction = {
      type: 'feed',
      x: 0,
      y: 0,
      intensity: 0.9
    };
    
    // Record interaction time
    lastInteractionTime = p.millis();
    
    // Check for evolution
    if (result.currentStage > traitEngine.developmentStage - 1) {
      // Pet evolved!
      petRenderer.addEffect('evolution', 0, 0);
    }
  }
  
  function playWithPet() {
    // Process play interaction
    const result = traitEngine.processInteraction('play', 5, 0.8);
    
    // Update physics
    userInteraction = {
      type: 'play',
      x: 0,
      y: 0,
      intensity: 0.8
    };
    
    // Record interaction time
    lastInteractionTime = p.millis();
    
    // Check for evolution
    if (result.currentStage > traitEngine.developmentStage - 1) {
      // Pet evolved!
      petRenderer.addEffect('evolution', 0, 0);
    }
  }
  
  function petPet() {
    // Process pet interaction
    const result = traitEngine.processInteraction('pet', 2, 0.9);
    
    // Update physics
    userInteraction = {
      type: 'pet',
      x: 0,
      y: 0,
      intensity: 0.9
    };
    
    // Record interaction time
    lastInteractionTime = p.millis();
    
    // Check for evolution
    if (result.currentStage > traitEngine.developmentStage - 1) {
      // Pet evolved!
      petRenderer.addEffect('evolution', 0, 0);
    }
  }
  
  function drawUI() {
    // Draw pet state indicators
    const state = traitEngine.getCurrentState();
    
    // Energy bar
    p.fill(200, 80, 80);
    p.noStroke();
    p.rect(canvasWidth - 20, 20, 20, 100);
    
    p.fill(120, 100, 100);
    const energyHeight = state.energy * 100;
    p.rect(canvasWidth - 20, 20 + (100 - energyHeight)/2, 20, energyHeight);
    
    // Draw stage indicator
    p.fill(0, 0, 20);
    p.textAlign(p.LEFT, p.TOP);
    p.textSize(14);
    p.text(`Stage: ${state.developmentStage}`, 10, 10);
    p.text(`Points: ${Math.floor(state.evolutionPoints)}`, 10, 30);
    
    // Draw interaction buttons
    for (const button of interactionButtons) {
      // Button background
      p.fill(210, 30, 95);
      p.stroke(210, 30, 50);
      p.strokeWeight(2);
      p.rect(button.x, button.y, button.width, button.height, 8);
      
      // Button text
      p.fill(0, 0, 20);
      p.noStroke();
      p.textAlign(p.CENTER, p.CENTER);
      p.textSize(16);
      p.text(button.text, button.x, button.y);
    }
  }
  
  function savePet() {
    // Save pet state to localStorage
    try {
      const petData = {
        traits: traitEngine.getCurrentState(),
        lastInteraction: lastInteractionTime,
        saveTime: Date.now()
      };
      
      localStorage.setItem('dksPet', JSON.stringify(petData));
    } catch (e) {
      console.error('Failed to save pet:', e);
    }
  }
  
  function loadPet() {
    // Load pet state from localStorage
    try {
      const petData = JSON.parse(localStorage.getItem('dksPet'));
      
      if (petData && petData.traits) {
        // Restore traits
        Object.assign(traitEngine.traits, petData.traits.traits);
        traitEngine.energy = petData.traits.energy;
        traitEngine.attention = petData.traits.attention;
        traitEngine.mood = petData.traits.mood;
        traitEngine.complexity = petData.traits.complexity;
        traitEngine.developmentStage = petData.traits.developmentStage;
        traitEngine.evolutionPoints = petData.traits.evolutionPoints;
        Object.assign(traitEngine.appearanceGenes, petData.traits.appearanceGenes);
        
        // Restore last interaction time
        lastInteractionTime = petData.lastInteraction || 0;
      }
    } catch (e) {
      console.error('Failed to load pet:', e);
    }
  }
};

// Initialize p5.js sketch
new p5(sketch);
```

### 2.2 HTML Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DKS Digital Pet</title>
  <link rel="stylesheet" href="styles.css">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.min.js"></script>
</head>
<body>
  <div class="container">
    <h1>DKS Digital Pet</h1>
    <div id="pet-container"></div>
    <div class="info-panel">
      <h2>Pet Information</h2>
      <div id="pet-stats"></div>
      <h3>Personality Traits</h3>
      <div id="pet-traits"></div>
    </div>
  </div>
  
  <!-- Load scripts -->
  <script src="js/trait-engine.js"></script>
  <script src="js/physics-engine.js"></script>
  <script src="js/pet-renderer.js"></script>
  <script src="js/main.js"></script>
</body>
</html>
```

### 2.3 CSS Styling

```css
body {
  font-family: 'Helvetica Neue', Arial, sans-serif;
  background-color: #f5f5f5;
  margin: 0;
  padding: 0;
}

.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  text-align: center;
  color: #333;
}

#pet-container {
  margin: 20px auto;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  background-color: white;
}

.info-panel {
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  margin-top: 20px;
}

h2, h3 {
  color: #444;
  margin-top: 0;
}

#pet-stats, #pet-traits {
  margin-bottom: 20px;
}

/* Stat bars */
.stat-bar {
  height: 20px;
  background-color: #eee;
  border-radius: 10px;
  margin-bottom: 10px;
  overflow: hidden;
}

.stat-fill {
  height: 100%;
  border-radius: 10px;
}

/* Different colors for different stats */
.energy-fill { background-color: #4CAF50; }
.mood-fill { background-color: #2196F3; }
.attention-fill { background-color: #FFC107; }
.complexity-fill { background-color: #9C27B0; }

/* Trait display */
.trait-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.trait-box {
  background-color: #f1f1f1;
  padding: 10px;
  border-radius: 5px;
  flex: 1 1 calc(50% - 10px);
  min-width: 150px;
}

.trait-name {
  font-weight: bold;
  margin-bottom: 5px;
}

.trait-value {
  height: 10px;
  background-color: #eee;
  border-radius: 5px;
  overflow: hidden;
}

.trait-fill {
  height: 100%;
  background-color: #FF5722;
  border-radius: 5px;
}
```

## 3. Advanced Extensions

### 3.1 Attention Tracking Module

For implementing attention-based evolution as described in your DKS concept:

```javascript
class AttentionTracker {
  constructor(traitEngine) {
    this.traitEngine = traitEngine;
    this.attentionHistory = [];
    this.attentionDecayRate = 0.05; // Per hour
    this.attentionThreshold = 0.3; // Minimum needed for stability
    this.lastUpdate = Date.now();
  }
  
  // Record attention event
  recordAttention(duration, intensity) {
    const attention = {
      timestamp: Date.now(),
      duration: duration,
      intensity: intensity,
      value: duration * intensity * 0.1
    };
    
    this.attentionHistory.push(attention);
    
    // Keep history from growing too large
    if (this.attentionHistory.length > 100) {
      this.attentionHistory.shift();
    }
    
    // Update trait engine
    this.traitEngine.attention = Math.min(1, this.traitEngine.attention + attention.value);
    
    return attention.value;
  }
  
  // Calculate current attention level
  getCurrentAttention() {
    const now = Date.now();
    const elapsedHours = (now - this.lastUpdate) / (1000 * 60 * 60);
    
    // Apply decay based on elapsed time
    if (elapsedHours > 0) {
      this.traitEngine.attention = Math.max(
        0, 
        this.traitEngine.attention - (this.attentionDecayRate * elapsedHours)
      );
      this.lastUpdate = now;
    }
    
    return this.traitEngine.attention;
  }
  
  // Get attention history over a time period
  getAttentionHistory(hours) {
    const now = Date.now();
    const cutoff = now - (hours * 60 * 60 * 1000);
    
    return this.attentionHistory.filter(a => a.timestamp >= cutoff);
  }
  
  // Calculate attention stability (how consistent attention has been)
  getAttentionStability() {
    const recentAttention = this.getAttentionHistory(24);
    
    if (recentAttention.length < 3) {
      return 0.5; // Not enough data
    }
    
    // Calculate variance in attention timing
    const intervals = [];
    for (let i = 1; i < recentAttention.length; i++) {
      intervals.push(recentAttention[i].timestamp - recentAttention[i-1].timestamp);
    }
    
    const avgInterval = intervals.reduce((sum, val) => sum + val, 0) / intervals.length;
    const variance = intervals.reduce((sum, val) => sum + Math.pow(val - avgInterval, 2), 0) / intervals.length;
    const normalizedVariance = Math.min(1, variance / (24 * 60 * 60 * 1000));
    
    // Lower variance = higher stability
    return 1 - normalizedVariance;
  }
  
  // Determine if pet is "attention starved"
  isAttentionStarved() {
    return this.traitEngine.attention < this.attentionThreshold;
  }
  
  // Get advice for optimal attention
  getAttentionAdvice() {
    const currentAttention = this.traitEngine.attention;
    
    if (currentAttention < this.attentionThreshold) {
      return "Your pet needs more attention soon.";
    } else if (currentAttention < 0.6) {
      return "Your pet is doing okay but could use more interaction.";
    } else {
      return "Your pet is getting plenty of attention.";
    }
  }
}
```

### 3.2 Evolution Event System

For creating meaningful evolution events with visual feedback:

```javascript
class EvolutionSystem {
  constructor(traitEngine, petRenderer) {
    this.traitEngine = traitEngine;
    this.petRenderer = petRenderer;
    this.evolutionHistory = [];
    this.milestones = [
      { 
        stage: 1, 
        name: "Awakening", 
        description: "Your pet has developed basic awareness.",
        trait: "curiosity" 
      },
      { 
        stage: 2, 
        name: "Personality", 
        description: "Your pet is developing distinct personality traits.",
        trait: "sociability" 
      },
      { 
        stage: 3, 
        name: "Intelligence", 
        description: "Your pet shows signs of complex thinking.",
        trait: "adaptability" 
      },
      { 
        stage: 4, 
        name: "Self-Awareness", 
        description: "Your pet seems to recognize itself and you.",
        trait: "independence" 
      }
    ];
    
    this.lastCheckedStage = 0;
  }
  
  // Check if evolution has occurred
  checkEvolution() {
    const currentStage = this.traitEngine.developmentStage;
    
    if (currentStage > this.lastCheckedStage) {
      // Evolution has occurred!
      const milestone = this.milestones.find(m => m.stage === currentStage);
      
      if (milestone) {
        this.triggerEvolutionEvent(milestone);
      }
      
      this.lastCheckedStage = currentStage;
      return true;
    }
    
    return false;
  }
  
  // Trigger evolution event
  triggerEvolutionEvent(milestone) {
    // Record evolution
    this.evolutionHistory.push({
      timestamp: Date.now(),
      stage: milestone.stage,
      name: milestone.name,
      dominantTrait: this.getDominantTrait()
    });
    
    // Create visual effect
    this.petRenderer.addEffect('evolution', 0, 0);
    
    // Boost the milestone's associated trait
    if (milestone.trait && this.traitEngine.traits[milestone.trait] !== undefined) {
      this.traitEngine.traits[milestone.trait] = Math.min(
        1, 
        this.traitEngine.traits[milestone.trait] + 0.2
      );
    }
    
    // Display evolution notification
    this.showEvolutionNotification(milestone);
    
    return milestone;
  }
  
  //