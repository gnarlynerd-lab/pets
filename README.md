# DKS Digital Pet System Implementation

This project implements a Dynamic Kinetic Systems (DKS) framework for digital pets that evolve through human interaction. The system demonstrates genuine emergence of personality, behavior, and relationships between pets and their owners.

## Overview

The Digital Pet System is built on the following core principles:
- **Emergent Behavior**: Pet personalities develop organically through interaction patterns
- **Dynamic Adaptation**: Pets adapt their behavior based on experiences and attention
- **Self-Organization**: The system maintains stability while allowing for complex behavioral patterns
- **Memory and Learning**: Pets form memories and learn from interactions
- **Fluid Boundaries**: The interface between pets and environment is dynamic and permeable
- **Observable Cognitive Development**: Pets demonstrate visible growth in intelligence and abilities

## Architecture

The system is structured around several key components:

### Backend
- **Pet Model**: Environment where pets exist and interact
- **Digital Pet Agent**: Core entity with traits, behaviors, needs, and memory systems
- **Fluid Boundary System**: Manages the interface between pet and environment
- **Pet Environment**: Dynamic shared space with resources, regions, and features
- **Observable Cognition**: System for tracking pet cognitive development
- **Redis Communication Layer**: Messaging system for pet-user interactions
- **Database**: Storage for persistent pet data

### Frontend
- **Pet Network Visualization**: Visual representation of the pet environment
- **Pet Detail View**: Detailed information about pet traits and stats
- **Interaction Panel**: Interface for users to interact with pets
- **Environment Display**: Shows weather, time, and environmental conditions
- **Boundary Visualization**: Represents the fluid boundary between pet and environment
- **Cognitive Development Display**: Shows growth in pet intelligence
- **Metrics Dashboard**: System statistics and monitoring

## Key Features

- **Trait Network**: Interconnected personality traits that influence each other and evolve
- **Behavior Generation**: Dynamic behaviors based on traits, needs, and context
- **Attention System**: Tracks human attention and affects pet development
- **Relationship Formation**: Pets form relationships with users and other pets
- **Development Stages**: Pets progress through life stages (infant, child, adolescent, adult, elder)
- **Fluid Boundaries**: Dynamic interface between pet and environment requiring energy maintenance
- **Environmental Exchange**: Pets can assimilate elements from and project into the environment
- **Cognitive Development**: Observable growth in intelligence and problem-solving abilities
- **Dynamic Environment**: Weather, time of day, and regional features affect pet behavior

## Running the System

1. Start the system with Docker Compose:
```
docker-compose up
```

2. Access the frontend interface:
```
http://localhost:3000
```

3. Interact with pets through the web interface

## Key Interaction Types

- **Feed**: Provide food to your pet, reducing hunger
- **Play**: Engage in active play, reducing boredom
- **Pet**: Physical affection, improving mood and reducing social need
- **Train**: Teach new behaviors through training
- **Check**: Simply observe your pet (minimal interaction)
- **Explore**: Help your pet discover new environmental elements
- **Shelter**: Protect your pet from harsh environmental conditions
- **Challenge**: Create boundary challenges that promote cognitive growth

## Environment Features

- **Weather System**: Different weather conditions affect pet behavior and energy
- **Time System**: Day/night cycle influences pet activities and needs
- **Regions**: Different areas with unique resources and features
- **Resources**: Food, water, toys and knowledge for pets to consume
- **Pet Projections**: Extensions of pets into the environment (territorial markers, social signals)

## Development

The system is built with:
- **Backend**: Python + Mesa framework for agent simulation
- **Frontend**: React + D3.js for visualization
- **Database**: MySQL for data persistence
- **Communication**: Redis for messaging

## API Endpoints

### Pet Endpoints
- `GET /api/pets`: List all pets
- `GET /api/pets/{pet_id}`: Get detailed pet information
- `GET /api/pets/{pet_id}/boundary`: Get pet boundary information
- `GET /api/pets/{pet_id}/cognition`: Get pet cognitive development information
- `POST /api/pets/interact`: Interact with a pet

### Environment Endpoints
- `GET /api/environment`: Get current environment state

### WebSocket Endpoints
- `/ws`: Main WebSocket for pet interactions
- `/ws/environment`: WebSocket for environment updates

## Future Enhancements

- **Advanced Evolution**: More sophisticated trait evolution algorithms
- **Pet Breeding**: Allow pets to have offspring with inherited traits
- **Token Economy**: Integration with blockchain for digital pet ownership
- **Mobile App**: Native mobile interface for pets
- **Voice Interaction**: Add voice commands and responses
