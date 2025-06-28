# DKS Agent System - Setup Guide

## Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for local frontend development)

## Quick Start with Docker

1. **Clone and navigate to the project directory:**
   ```bash
   cd /Users/gerardlynn/agents/dks
   ```

2. **Start all services:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Backend API docs: http://localhost:8000/docs

4. **Stop the services:**
   ```bash
   docker-compose down
   ```

## Service Details

### Backend (Python/FastAPI)
- **Port:** 8000
- **Framework:** FastAPI with Mesa agent framework
- **Features:** 
  - RESTful API endpoints
  - WebSocket for real-time updates
  - Agent-based simulation engine
  - Redis communication layer

### Frontend (React)
- **Port:** 3000
- **Framework:** React with D3.js visualization
- **Features:**
  - Real-time agent network visualization
  - Metrics dashboard
  - Simulation control panel

### Redis
- **Port:** 6379
- **Purpose:** Inter-agent message passing and caching
- **Data:** Persistent with volume mounting

### MySQL
- **Port:** 3306
- **Purpose:** State storage and analysis data
- **Database:** `dks_hospital`
- **Credentials:** 
  - User: `dks_user`
  - Password: `dks_password`

## Development Setup

### Backend Development

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables:**
   ```bash
   export REDIS_URL=redis://localhost:6379
   export MYSQL_HOST=localhost
   export MYSQL_DATABASE=dks_hospital
   export MYSQL_USER=dks_user
   export MYSQL_PASSWORD=dks_password
   ```

4. **Run the backend:**
   ```bash
   python -m backend.main
   ```

### Frontend Development

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm start
   ```

## Testing

### Run Backend Tests
```bash
# With virtual environment activated
pytest tests/ -v
```

### Run Frontend Tests
```bash
cd frontend
npm test
```

## Troubleshooting

### Common Issues

1. **Port conflicts:**
   - Check if ports 3000, 8000, 6379, or 3306 are in use
   - Modify `docker-compose.yml` port mappings if needed

2. **Docker build fails:**
   - Ensure Docker has sufficient memory allocated
   - Try rebuilding without cache: `docker-compose build --no-cache`

3. **Database connection issues:**
   - Wait for MySQL to fully initialize (can take 30-60 seconds)
   - Check logs: `docker-compose logs mysql`

4. **Frontend can't connect to backend:**
   - Verify `REACT_APP_BACKEND_URL` environment variable
   - Check CORS settings in backend configuration

### Logs and Debugging

**View all service logs:**
```bash
docker-compose logs -f
```

**View specific service logs:**
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f redis
docker-compose logs -f mysql
```

**Execute commands in running containers:**
```bash
# Backend container
docker-compose exec backend bash

# MySQL container
docker-compose exec mysql mysql -u dks_user -p dks_hospital
```

## Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │     Backend      │    │     Redis       │
│   (React)       │◄──►│   (FastAPI)      │◄──►│   (Messages)    │
│   Port: 3000    │    │   Port: 8000     │    │   Port: 6379    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                       ┌────────▼────────┐
                       │     MySQL       │
                       │   (Storage)     │
                       │   Port: 3306    │
                       └─────────────────┘
```

## Next Steps

After successful setup:

1. **Test the system:** Start simulation and observe agent behaviors
2. **Explore the code:** Review agent implementations and DKS principles
3. **Monitor metrics:** Watch for emergent patterns in the dashboard
4. **Prepare for Stage 2:** Ready to implement specialized agent types

## Support

For issues or questions:
- Check the logs using commands above
- Review the implementation plan in `IMPLEMENTATION_PLAN.md`
- Ensure all prerequisites are properly installed
