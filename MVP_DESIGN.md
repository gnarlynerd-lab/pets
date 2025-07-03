# DKS Digital Pet MVP - Emoji Communication System

## MVP Scope: Single Pet, Single User, Emoji Communication

### Core Vision
A single digital pet that communicates through emojis and evolves its personality based on user interactions. No complex multi-agent systems - just one charming pet that learns and grows.

### MVP Features

#### 1. Single Pet with Emoji Communication
- **Pet communicates only through emojis** (like 😊🍎 for "happy and hungry")
- **User responds with emoji reactions** (👍❤️😴 etc.)
- **Pet develops unique emoji preferences** based on positive user responses
- **Progressive complexity**: starts with single emojis, develops to "emoji sentences"

#### 2. Simple Personality Evolution
- **3-5 core traits**: Happy, Curious, Playful, Sleepy, Hungry
- **Traits evolve based on interactions**: more play → more playful
- **Visible personality changes** in emoji usage patterns
- **FEP-driven learning**: pet minimizes "surprise" by learning user preferences

#### 3. Clean, Simple UI
- **Large emoji display** showing pet's current communication
- **Emoji reaction buttons** for user to respond
- **Simple pet visualization** (could be just a cute emoji-based character)
- **Basic needs indicators** (hunger, energy, mood as simple bars)

#### 4. Core Interaction Loop
1. Pet shows emoji message based on current state/needs
2. User responds with emoji reaction
3. Pet learns from response (positive/negative feedback)
4. Pet's personality and communication style evolve
5. Over time, pet develops unique "emoji vocabulary"

### Technical Architecture (Simplified)

```
┌─────────────────────────────────────────┐
│ MVP DKS Digital Pet System              │
│                                         │
│  ┌─────────────────┐  ┌───────────────┐ │
│  │   Single Pet    │  │   Simple UI   │ │
│  │                 │  │               │ │
│  │ ┌─────────────┐ │  │ ┌───────────┐ │ │
│  │ │ Emoji       │ │  │ │ Emoji     │ │ │
│  │ │ Communication│◄─┼──┼►│ Reactions │ │ │
│  │ └─────────────┘ │  │ └───────────┘ │ │
│  │                 │  │               │ │
│  │ ┌─────────────┐ │  │ ┌───────────┐ │ │
│  │ │ FEP Learning│ │  │ │ Pet       │ │ │
│  │ │ System      │ │  │ │ Display   │ │ │
│  │ └─────────────┘ │  │ └───────────┘ │ │
│  │                 │  │               │ │
│  │ ┌─────────────┐ │  │ ┌───────────┐ │ │
│  │ │ 5 Core      │ │  │ │ Needs     │ │ │
│  │ │ Traits      │ │  │ │ Bars      │ │ │
│  │ └─────────────┘ │  │ └───────────┘ │ │
│  └─────────────────┘  └───────────────┘ │
│                                         │
│  ┌─────────────────────────────────────┐ │
│  │ Simple JSON State Storage           │ │
│  └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### Implementation Plan

#### Phase 1: Core Pet (1-2 days)
- Single pet with 5 basic traits
- Simple emoji communication system
- Basic needs (hunger, energy, mood)
- FEP learning for emoji preference development

#### Phase 2: User Interface (1 day)
- Clean React frontend
- Emoji display for pet communication
- Emoji reaction buttons for user
- Simple pet visualization
- Basic needs indicators

#### Phase 3: Learning & Evolution (1 day)
- Pet learns user emoji preferences
- Personality traits evolve based on interactions
- Progressive communication complexity
- Save/load pet state

### Example User Experience

```
[Pet appears as cute emoji character: 🐾]

Pet: 😊🍎 (happy + hungry)
User clicks: 🍕 (feed reaction)
Pet: 😍✨ (loves it!)

[After several feeding interactions...]

Pet: 😊🍕❓ (happy + remembers pizza + asking)
User clicks: 👍 (yes)
Pet: 🎉🍕🤗 (excited + pizza + grateful)

[Pet has learned user prefers pizza, develops food preferences]
```

### Core Files to Create/Modify

1. **`mvp_pet.py`** - Single pet class with emoji communication
2. **`emoji_system.py`** - Emoji vocabulary and learning system  
3. **`fep_simple.py`** - Simplified FEP learning for emoji preferences
4. **`mvp_frontend/`** - Clean React app focused on emoji interaction
5. **`mvp_main.py`** - Simple FastAPI backend

### Success Metrics for MVP
- [ ] Pet communicates clearly through emojis
- [ ] User can easily respond with emoji reactions
- [ ] Pet's emoji usage changes based on user feedback
- [ ] Personality traits visibly evolve over time
- [ ] System feels responsive and engaging
- [ ] No confusion about consciousness - clearly a pet toy

This MVP strips away complexity while keeping the core DKS principles: evolution through interaction, emergent behavior, and genuine personality development - all through the safe, playful medium of emoji communication.
