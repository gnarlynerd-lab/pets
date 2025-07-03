# DKS Digital Pet System - Running Instructions

This document provides instructions for running and testing the DKS Digital Pet System.

## Prerequisites

- Python 3.8+
- Node.js 16+ 
- Redis running locally (or accessible via configured REDIS_URL)

## Starting the Backend Server

1. Navigate to the project root:

```bash
cd /Users/gerardlynn/agents/dks
```

2. Install Python dependencies:

```bash
# First install Mesa package directly (to avoid pkgutil.ImpImporter error)
pip install mesa

# Then install remaining requirements
pip install -r requirements.txt

# If you see the error "AttributeError: module 'pkgutil' has no attribute 'ImpImporter'", try:
pip install mesa --no-build-isolation
```

3. Start the backend server:

```bash
# From the project root directory:
python -m uvicorn backend.main:app --reload
```

The backend will be available at http://localhost:8000.

## Starting the Frontend Server

1. Navigate to the Next.js directory:

```bash
cd /Users/gerardlynn/agents/dks/next
```

2. Install Node.js dependencies:

```bash
npm install
```

3. Start the frontend development server:

```bash
npm run dev
```

The frontend will be available at http://localhost:3000.

## Testing the System

### API Testing

1. Check system status:

```bash
curl http://localhost:8000/api/status
```

2. Get all pets:

```bash
curl http://localhost:8000/api/pets
```

3. Get a specific pet (replace `<pet_id>` with an actual pet ID):

```bash
curl http://localhost:8000/api/pets/<pet_id>
```

4. Send emoji interaction (replace `<pet_id>` with an actual pet ID):

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"pet_id": "<pet_id>", "emojis": "👋😊", "user_id": "test_user"}' \
  http://localhost:8000/api/pets/emoji
```

### End-to-End Testing

1. Open the frontend at http://localhost:3000
2. Use the emoji input to send messages to your pet
3. Observe the pet's response and state changes

## Troubleshooting

### Package Installation Issues

If you encounter issues installing packages:

1. **Mesa Installation Issues** (AttributeError related to pkgutil.ImpImporter):

```bash
# Try installing with the --no-build-isolation flag
pip install mesa --no-build-isolation

# If still having issues, try installing dependencies manually
pip install numpy pandas tornado
pip install -e git+https://github.com/projectmesa/mesa.git#egg=mesa
```

2. **Conflicting Dependencies**:

```bash
# Create a virtual environment
python -m venv dks_env
source dks_env/bin/activate  # On Windows: dks_env\Scripts\activate

# Install packages in the clean environment
pip install -r requirements.txt
```

### Import Errors

If you encounter import errors like `ModuleNotFoundError: No module named 'backend'`, make sure:

1. You're running the backend from the project root directory
2. The project root is in your Python path:

```bash
export PYTHONPATH=$PYTHONPATH:/Users/gerardlynn/agents/dks
```

### Redis Connection Issues

If the system fails to connect to Redis:

1. Ensure Redis is running locally:

```bash
redis-cli ping
```

2. Check the Redis connection URL in your environment variables or set it explicitly:

```bash
export REDIS_URL=redis://localhost:6379
```

### Pet Not Found

If you receive "Pet not found" errors when interacting:

1. First get a list of available pets:

```bash
curl http://localhost:8000/api/pets
```

2. Use the `id` from the response in your subsequent requests

### FEP Cognitive System Issues

If you encounter errors related to the Free Energy Principle (FEP) implementation:

1. Check for NumPy or array shape mismatch errors:

```bash
# Install specific NumPy version compatible with FEP implementation
pip install numpy==1.24.3
```

2. For errors in the `fep_cognitive_system.py`:

```bash
# Debug with more logging:
cd /Users/gerardlynn/agents/dks
python -c "from backend.agents.fep_cognitive_system import FEPCognitiveSystem; print(FEPCognitiveSystem.__init__.__annotations__)"
```

3. For emoji interaction errors, try a basic test:

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"pet_id": "<pet_id>", "emojis": "👋", "user_id": "test_user"}' \
  http://localhost:8000/api/pets/emoji
```

## Verifying the Fixed Issues

The following issues have been fixed in the latest version:

1. **RedisManager Argument Error**: The emoji interaction endpoint now correctly calls `store_interaction()` with the required parameters.

2. **Frontend State Structure**: All frontend components use the flat pet state structure (not nested `vital_stats`).

To verify these fixes:

1. Start both backend and frontend servers
2. Send an emoji interaction via the frontend
3. Check the backend logs for any errors
4. Verify pet state updates correctly on the frontend
