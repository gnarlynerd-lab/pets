# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DKS (Digital Kinetic Systems) - A multi-agent simulation framework for digital pets that evolve through human interaction using the Free Energy Principle (FEP). The system consists of a Python backend with FastAPI/Mesa, and dual frontend implementations (React and Next.js).

## Architecture

### Backend (`/backend/`)
- **Framework**: FastAPI + Mesa (agent-based modeling)
- **Key agents**: `digital_pet.py`, `enhanced_fep_system.py`, `user_modeling.py`
- **Entry point**: `backend/main.py`
- **Dependencies**: mesa, fastapi, uvicorn, numpy, pandas, mysql-connector-python, redis

### Frontend Options
1. **React App** (`/frontend/`) - Traditional React 18 with D3.js visualization
2. **Next.js App** (`/next/`) - Modern Next.js 15 with TypeScript, Tailwind CSS, Radix UI (appears to be the newer implementation)

### Services
- MySQL (port 3306) - Persistence
- Redis (port 6379) - Message broker
- Backend API (port 8000)
- Frontend (port 3000)

## Common Commands

### Development
```bash
# Start all services
docker-compose up

# Backend only
python -m backend.main

# Next.js frontend (preferred)
cd next && npm run dev

# React frontend (legacy)
cd frontend && npm start
```

### Testing
```bash
# Python backend tests
python -m pytest tests/
python test_enhanced_fep.py
python test_user_modeling.py
python test_policy_optimization.py

# Frontend tests
cd frontend && npm test
```

### Code Quality
```bash
# Python
black .          # Format code
flake8          # Lint

# Next.js
cd next && npm run lint
```

### Build
```bash
# Next.js production build
cd next && npm run build

# React production build  
cd frontend && npm run build
```

## Key Implementation Details

### Agent System
The core simulation uses Mesa framework with custom agents implementing:
- Free Energy Principle (FEP) for cognitive modeling
- Active inference for decision making
- User modeling for personalization
- Policy optimization using MDP (Markov Decision Process)

### API Structure
- FastAPI backend with WebSocket support for real-time updates
- RESTful endpoints for pet management, user profiles, interactions
- WebSocket endpoints for live pet state updates

### Database Schema
- MySQL for user profiles, pet states, interaction history
- Redis for real-time messaging and caching

### Frontend Architecture
- Next.js app uses App Router with server components
- Component library: Radix UI with Tailwind CSS
- Key components: `blob-pet-display.tsx`, `user-insights-panel.tsx`
- Real-time updates via WebSocket connection to backend

## Current Development Focus

Active work is happening on:
- Enhanced FEP system implementation
- User modeling and personalization
- Policy optimization algorithms
- UI/UX improvements in Next.js app
- **Anonymous user support with session-based interactions**

When making changes, ensure compatibility between the backend agent system and frontend state management.

## Anonymous User Implementation Plan

### Philosophy (aligned with FUTURE_VISION.md)
- Anonymous users are **participants**, not owners
- Session-based interaction model that naturally evolves into the peer ecosystem vision
- No "limited version" - full FEP experience without authentication
- Authentication provides persistence and relationship continuity, not ownership

### Backend Changes

1. **Database Schema Updates**
   - Add `session_id` field to pets table (nullable)
   - Allow `owner_id` to be nullable
   - Consider renaming `owner_id` → `participant_id` in future migration

2. **New Anonymous Endpoints**
   ```python
   /api/anonymous/session/create  # Generate session, assign companion
   /api/anonymous/pets/{session_id}  # Get pet state
   /api/anonymous/pets/{session_id}/interact  # Full FEP interaction
   /api/anonymous/pets/{session_id}/emoji  # Emoji interaction
   ```

3. **Session Management**
   - Generate UUID session IDs in frontend
   - Store in localStorage
   - Pass `X-Session-ID` header for anonymous requests
   - Cleanup job for old anonymous pets (30 days?)

### Frontend Changes

1. **Update `useAuthenticatedPetState` hook**
   - Check for authentication status
   - Use session-based endpoints when not authenticated
   - Store session ID in localStorage
   - Seamless switch between anonymous/authenticated modes

2. **UI Updates**
   - Subtle "Sign up to save your companion" prompts
   - Show relationship benefits of authentication (history, multi-device)
   - Not "upgrade" messaging - just continuity options

### Migration Path

1. **Anonymous → Authenticated**
   - On signup, offer to claim session-based companion
   - Transfer pet from `session_id` to `user_id`
   - Preserve all interaction history and state
   - Multiple sessions can be merged if user had several

### Implementation Steps

1. **Phase 1**: Backend anonymous endpoints
2. **Phase 2**: Frontend session management
3. **Phase 3**: Migration flow
4. **Phase 4**: UI polish and prompts
5. **Phase 5**: Consider peer ecosystem refactoring