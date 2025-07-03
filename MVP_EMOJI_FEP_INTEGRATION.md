# DKS Digital Pet MVP - Emoji-Enhanced FEP System

## Revised MVP Strategy: Enhance Existing Backend + New Frontend

### Core Philosophy
**Keep the sophisticated Redis/Mesa/FEP backend** we've built (it's valuable for multi-agent future) but add emoji communication as a **new input channel** to the existing FEP cognitive system.

## Technical Approach

### Backend: Enhance Existing FEP System
Instead of rebuilding, **extend** the current FEP cognitive system to handle emoji interactions alongside traditional inputs.

#### 1. Enhanced FEP Input Channels
```python
# backend/agents/fep_cognitive_system.py - EXTEND existing system

class FEPCognitiveSystem:
    def __init__(self, state_size: int = 15, action_size: int = 8):  # Expanded
        # ...existing code...
        
        # NEW: Emoji communication system
        self.emoji_vocabulary = {
            'expressions': ['😊', '😔', '😴', '🤔', '😋'],
            'needs': ['🍎', '🎮', '💤', '🤗', '🚿'],
            'responses': ['❤️', '👍', '👎', '❓', '✨']
        }
        self.emoji_preferences = defaultdict(float)  # Learn user emoji preferences
        self.emoji_usage_patterns = defaultdict(list)  # Track emoji usage over time
        
        # NEW: Multi-modal state representation
        self.state_channels = {
            'nutrition': np.zeros(3),      # Traditional input
            'stimulation': np.zeros(3),    # Traditional input  
            'emoji_context': np.zeros(5),  # NEW: Emoji communication context
            'user_emoji_prefs': np.zeros(4) # NEW: Learned user preferences
        }
    
    def process_emoji_interaction(self, user_emojis: List[str], pet_context: Dict) -> Dict:
        """Process emoji interaction through FEP learning"""
        # Convert emoji to numerical representation for FEP
        emoji_vector = self.encode_emoji_sequence(user_emojis)
        
        # Update state with emoji context
        self.state_channels['emoji_context'] = emoji_vector
        
        # FEP prediction: what did we expect user to send?
        expected_emoji = self.predict_user_emoji_response(pet_context)
        
        # Calculate surprise: how different was actual vs expected?
        surprise = self.calculate_emoji_surprise(expected_emoji, emoji_vector)
        
        # Update beliefs about user emoji preferences
        self.update_emoji_beliefs(user_emojis, surprise, pet_context)
        
        # Generate pet's emoji response based on updated beliefs
        pet_emoji_response = self.generate_emoji_response(user_emojis, surprise)
        
        return {
            'pet_emojis': pet_emoji_response,
            'surprise_level': surprise,
            'learning_occurred': surprise > self.surprise_threshold,
            'updated_preferences': self.emoji_preferences
        }
    
    def encode_emoji_sequence(self, emojis: List[str]) -> np.ndarray:
        """Convert emoji sequence to numerical vector for FEP processing"""
        # Map emojis to emotional/need dimensions
        emotion_map = {
            '😊': [1.0, 0.0, 0.0],      # happy
            '😔': [-1.0, 0.0, 0.0],     # sad  
            '❤️': [0.8, 0.8, 0.0],      # love
            '🍎': [0.0, 1.0, 0.0],      # nutrition need
            '🎮': [0.0, 0.0, 1.0],      # stimulation need
            # ... expand vocabulary
        }
        
        # Aggregate emoji meanings into state vector
        vector = np.zeros(5)
        for emoji in emojis:
            if emoji in emotion_map:
                vector += np.array(emotion_map[emoji] + [0.0, 0.0])
        
        return np.clip(vector, -1, 1)
    
    def generate_emoji_response(self, user_emojis: List[str], surprise: float) -> List[str]:
        """Generate pet's emoji response using FEP active inference"""
        # Use FEP to minimize future surprise by selecting appropriate emoji response
        
        # High surprise = more exploratory emoji response
        if surprise > 0.7:
            # Try new emoji combinations to learn user preferences
            response = self.explore_new_emoji_combination()
        else:
            # Use learned preferences to generate expected response
            response = self.generate_preferred_emoji_response(user_emojis)
        
        # Update emoji usage patterns for learning
        self.emoji_usage_patterns[tuple(user_emojis)].append(response)
        
        return response
```

#### 2. Enhanced Digital Pet with Emoji Communication
```python
# backend/agents/digital_pet.py - EXTEND existing pet

class DigitalPet(Agent):
    def __init__(self, unique_id, model, initial_traits=None):
        # ...existing initialization...
        
        # Enhanced FEP system with emoji support
        self.fep_system = FEPCognitiveSystem(state_size=15, action_size=8)
        
        # NEW: Emoji communication state
        self.emoji_communication = {
            'current_message': [],
            'complexity_level': 1,  # Starts simple, grows over time
            'learned_user_patterns': {},
            'communication_history': []
        }
    
    def receive_emoji_interaction(self, user_id: str, user_emojis: List[str]) -> Dict:
        """Process user emoji input through FEP system"""
        # Get current pet context for FEP processing
        pet_context = {
            'needs': self.needs,
            'mood': self.mood,
            'energy': self.energy,
            'attention_level': self.attention_level
        }
        
        # Process through FEP system
        fep_result = self.fep_system.process_emoji_interaction(user_emojis, pet_context)
        
        # Traditional attention processing (existing code)
        self.receive_attention(user_id, amount=5)
        
        # Update pet state based on emoji interaction
        self.update_from_emoji_interaction(user_emojis, fep_result)
        
        # Generate response
        response = {
            'pet_emojis': fep_result['pet_emojis'],
            'pet_state': self.get_simple_state(),
            'learning_feedback': {
                'surprise_level': fep_result['surprise_level'],
                'learning_occurred': fep_result['learning_occurred']
            }
        }
        
        # Store interaction history
        self.emoji_communication['communication_history'].append({
            'timestamp': time.time(),
            'user_emojis': user_emojis,
            'pet_response': fep_result['pet_emojis'],
            'surprise': fep_result['surprise_level']
        })
        
        return response
    
    def generate_spontaneous_emoji_message(self) -> List[str]:
        """Pet generates emoji message based on current needs/state"""
        # Use FEP to generate emoji message that minimizes expected surprise
        current_state = np.array([
            self.needs['hunger'],
            self.needs['energy'], 
            self.mood,
            self.attention_level,
            self.health
        ])
        
        # FEP active inference: what emoji will get desired user response?
        emoji_message = self.fep_system.select_communication_action(current_state)
        
        self.emoji_communication['current_message'] = emoji_message
        return emoji_message
```

#### 3. Enhanced API Endpoints
```python
# backend/main.py - ADD to existing WebSocket endpoint

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # ...existing WebSocket code...
    
    # NEW: Handle emoji interactions
    elif message.get("type") == "emoji_interaction":
        user_emojis = message.get("user_emojis", [])
        pet_id = message.get("pet_id")
        
        if pet_model and pet_id:
            pet = pet_model.get_pet_by_id(pet_id)
            if pet:
                # Process emoji interaction through FEP system
                response = pet.receive_emoji_interaction("websocket_user", user_emojis)
                
                await websocket.send_text(json.dumps({
                    "type": "emoji_response",
                    "pet_id": pet_id,
                    "response": response,
                    "timestamp": str(asyncio.get_event_loop().time())
                }))
    
    elif message.get("type") == "get_pet_emoji_message":
        # Get pet's spontaneous emoji message
        pet_id = message.get("pet_id")
        if pet_model and pet_id:
            pet = pet_model.get_pet_by_id(pet_id)
            if pet:
                emoji_message = pet.generate_spontaneous_emoji_message()
                
                await websocket.send_text(json.dumps({
                    "type": "pet_emoji_message", 
                    "pet_id": pet_id,
                    "emojis": emoji_message,
                    "timestamp": str(asyncio.get_event_loop().time())
                }))

# NEW: Emoji-specific REST endpoints
@app.post("/api/pets/{pet_id}/emoji")
async def emoji_interaction(pet_id: str, emoji_data: dict):
    """Handle emoji interaction with specific pet"""
    user_emojis = emoji_data.get("emojis", [])
    
    if pet_model:
        pet = pet_model.get_pet_by_id(pet_id)
        if pet:
            response = pet.receive_emoji_interaction("rest_user", user_emojis)
            return {"success": True, "response": response}
    
    return {"success": False, "error": "Pet not found"}

@app.get("/api/pets/{pet_id}/emoji_state")
async def get_emoji_state(pet_id: str):
    """Get pet's current emoji communication state"""
    if pet_model:
        pet = pet_model.get_pet_by_id(pet_id)
        if pet:
            return {
                "current_message": pet.emoji_communication['current_message'],
                "complexity_level": pet.emoji_communication['complexity_level'], 
                "vocabulary": pet.fep_system.emoji_vocabulary,
                "learned_preferences": dict(pet.fep_system.emoji_preferences)
            }
    
    return {"error": "Pet not found"}
```

### Frontend: New Emoji-Focused Interface

#### Use Existing Backend, New Frontend Experience
```typescript
// frontend/emoji-mvp/hooks/use-emoji-pet.ts

export function useEmojiPet(petId: string) {
  const [petState, setPetState] = useState(null);
  const [currentEmojiMessage, setCurrentEmojiMessage] = useState([]);
  const [ws, setWs] = useState<WebSocket | null>(null);

  useEffect(() => {
    // Connect to existing WebSocket endpoint
    const websocket = new WebSocket('ws://localhost:8000/ws');
    
    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      if (data.type === 'pet_emoji_message') {
        setCurrentEmojiMessage(data.emojis);
      } else if (data.type === 'emoji_response') {
        // Handle pet's emoji response
        setCurrentEmojiMessage(data.response.pet_emojis);
        setPetState(data.response.pet_state);
      }
    };
    
    setWs(websocket);
    
    // Request initial pet emoji message
    websocket.onopen = () => {
      websocket.send(JSON.stringify({
        type: 'get_pet_emoji_message',
        pet_id: petId
      }));
    };
    
    return () => websocket.close();
  }, [petId]);

  const sendEmojiToP pet = useCallback((userEmojis: string[]) => {
    if (ws) {
      ws.send(JSON.stringify({
        type: 'emoji_interaction',
        pet_id: petId,
        user_emojis: userEmojis
      }));
    }
  }, [ws, petId]);

  return {
    petState,
    currentEmojiMessage,
    sendEmojiToPet,
    isConnected: ws?.readyState === WebSocket.OPEN
  };
}
```

## Implementation Strategy

### Phase 1: Enhance Existing Backend (Day 1)
- ✅ Extend existing FEP system with emoji processing
- ✅ Add emoji communication to existing DigitalPet class  
- ✅ Add emoji endpoints to existing WebSocket/REST API
- ✅ **Keep all existing functionality** (Redis, Mesa, multi-pet support)

### Phase 2: Emoji Frontend (Day 2)
- ✅ Build new Next.js frontend focused on single-pet emoji interaction
- ✅ Connect to existing backend via existing WebSocket
- ✅ Emoji selection interface
- ✅ Pet emoji display with animations

### Phase 3: FEP Integration Testing (Day 3)
- ✅ Test emoji learning through FEP system
- ✅ Verify pet personality changes based on emoji interactions
- ✅ Ensure traditional inputs (nutrition, stimulation) still work
- ✅ Multi-modal FEP processing (emoji + traditional inputs)

## Key Benefits of This Approach

### 1. **Preserves Investment**
- Keep sophisticated Redis/Mesa/FEP backend
- Multi-agent capability remains for future
- All existing functionality preserved

### 2. **Enhances FEP System**
- Emoji becomes new input channel to existing FEP
- FEP handles multi-modal inputs (nutrition + stimulation + emoji)
- True cognitive integration, not separate system

### 3. **Clear MVP Path**
- Simple emoji-focused frontend
- Complex backend supports advanced features
- Easy to scale to multiple pets later

### 4. **Real FEP Learning**
- Pet learns emoji preferences through surprise minimization
- Personality evolution through emoji interaction patterns
- Progressive communication complexity

## Example Multi-Modal FEP Processing

```python
# Pet's FEP system processes ALL inputs together:

current_observation = {
    'nutrition': 0.3,        # Low food
    'stimulation': 0.8,      # High play  
    'user_emoji': [😊, 🍎],  # Happy + food emoji
    'context': 'user_interaction'
}

# FEP predicts: "User is happy and offering food"
# Surprise: Low (makes sense given nutrition need)
# Action: Accept food, show gratitude emoji
# Learning: User prefers 🍎 over other food emojis
```

This approach gives us the **best of both worlds**: sophisticated multi-agent backend ready for scaling + simple, engaging emoji communication MVP that demonstrates the FEP principles clearly.

Would you like me to start implementing the FEP emoji enhancements to the existing backend?
