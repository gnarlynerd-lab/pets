#!/bin/bash

# Start the complete MVP system

echo "🚀 Starting DKS Emoji Pet MVP System..."

# Set Python path
export PYTHONPATH=/Users/gerardlynn/agents/dks

# Start backend
echo "Starting backend server..."
cd /Users/gerardlynn/agents/dks
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Test backend
echo "Testing backend connection..."
curl -s http://localhost:8000/pets > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ Backend is running on http://localhost:8000"
else
    echo "❌ Backend failed to start"
    exit 1
fi

# Start frontend
echo "Starting frontend..."
cd /Users/gerardlynn/agents/dks/next
npm run dev &
FRONTEND_PID=$!

echo "✅ System started!"
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend: http://localhost:8000"
echo ""
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for interrupt
trap "echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
