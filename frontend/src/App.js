import React, { useState, useEffect } from 'react';
import './App.css';
import PetNetwork from './components/PetNetwork';
import MetricsDashboard from './components/MetricsDashboard';
import ControlPanel from './components/ControlPanel';
import PetDetail from './components/PetDetail';
import InteractionPanel from './components/InteractionPanel';
import { connectWebSocket, sendMessage } from './services/websocket';

function App() {
  const [isConnected, setIsConnected] = useState(false);
  const [simulationData, setSimulationData] = useState(null);
  const [systemStatus, setSystemStatus] = useState('initializing');
  const [selectedPet, setSelectedPet] = useState(null);
  const [pets, setPets] = useState([]);

  useEffect(() => {
    // Connect to WebSocket
    const ws = connectWebSocket(
      process.env.REACT_APP_BACKEND_URL?.replace('http', 'ws') + '/ws' || 'ws://localhost:8000/ws'
    );

    ws.onopen = () => {
      console.log('Connected to DKS Digital Pet System backend');
      setIsConnected(true);
      
      // Send ping to keep connection alive
      const pingInterval = setInterval(() => {
        sendMessage({ type: 'ping' });
      }, 30000);

      return () => clearInterval(pingInterval);
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        
        if (data.type === 'simulation_update') {
          setSimulationData(data);
          setSystemStatus('running');
        } else if (data.type === 'pong') {
          // Keep-alive response
          console.log('Connection alive');
        }
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };

    ws.onclose = () => {
      console.log('Disconnected from backend');
      setIsConnected(false);
      setSystemStatus('disconnected');
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      setIsConnected(false);
      setSystemStatus('error');
    };

    // Cleanup on unmount
    return () => {
      ws.close();
    };
  }, []);

  useEffect(() => {
    // Fetch initial pets data when connected
    if (isConnected) {
      fetchPets();
    }
  }, [isConnected]);

  const fetchPets = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000'}/api/pets`);
      if (response.ok) {
        const data = await response.json();
        setPets(data.pets);
      }
    } catch (error) {
      console.error('Error fetching pets:', error);
    }
  };

  const handlePetSelection = async (petId) => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000'}/api/pets/${petId}`);
      if (response.ok) {
        const petData = await response.json();
        setSelectedPet(petData);
      }
    } catch (error) {
      console.error('Error fetching pet details:', error);
    }
  };

  const handleInteraction = (interactionType, content) => {
    if (!selectedPet) return;
    
    const interaction = {
      type: interactionType,
      pet_id: selectedPet.id,
      user_id: 'user_' + Math.random().toString(36).substring(2, 10),
      content: content
    };
    
    // Send via websocket for real-time updates
    sendMessage({
      type: 'interact',
      pet_id: selectedPet.id,
      interaction_type: interactionType,
      content: content,
      request_id: Math.random().toString(36).substring(2, 10)
    });
    
    // Also call the REST API for confirmation
    fetch(`${process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000'}/api/pets/interact`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(interaction)
    }).catch(error => {
      console.error('Error sending interaction:', error);
    });
  };

  const handleStartSimulation = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000'}/api/simulation/start`, {
        method: 'POST',
      });
      
      if (response.ok) {
        setSystemStatus('starting');
      } else {
        console.error('Failed to start simulation');
      }
    } catch (error) {
      console.error('Error starting simulation:', error);
    }
  };

  const handleStopSimulation = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000'}/api/simulation/stop`, {
        method: 'POST',
      });
      
      if (response.ok) {
        setSystemStatus('stopped');
      } else {
        console.error('Failed to stop simulation');
      }
    } catch (error) {
      console.error('Error stopping simulation:', error);
    }
  };

  const handleResetSimulation = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000'}/api/simulation/reset`, {
        method: 'POST',
      });
      
      if (response.ok) {
        setSystemStatus('ready');
        setSimulationData(null);
      } else {
        console.error('Failed to reset simulation');
      }
    } catch (error) {
      console.error('Error resetting simulation:', error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>DKS Digital Pet System</h1>
        <div className="connection-status">
          <span className={`status-indicator ${isConnected ? 'connected' : 'disconnected'}`}>
            {isConnected ? '🟢' : '🔴'}
          </span>
          <span>
            {isConnected ? `Connected - ${systemStatus}` : 'Disconnected'}
          </span>
        </div>
      </header>

      <main className="App-main">
        <div className="control-section">
          <ControlPanel
            onStart={handleStartSimulation}
            onStop={handleStopSimulation}
            onReset={handleResetSimulation}
            systemStatus={systemStatus}
            isConnected={isConnected}
          />
        </div>

        <div className="visualization-section">
          <div className="network-container">
            <h2>Pet Environment</h2>
            <PetNetwork 
              networkData={simulationData?.network}
              isConnected={isConnected}
              onPetSelect={handlePetSelection}
              pets={pets}
              environment={simulationData?.environment}
            />
          </div>

          <div className="metrics-container">
            <h2>System Metrics</h2>
            <MetricsDashboard 
              metrics={simulationData?.metrics}
              isConnected={isConnected}
            />
          </div>
        </div>

        {selectedPet && (
          <div className="pet-detail-section">
            <div className="pet-detail-container">
              <h2>Pet Details: {selectedPet.id}</h2>
              <PetDetail 
                pet={selectedPet}
              />
            </div>
            <div className="interaction-container">
              <h2>Interact with Pet</h2>
              <InteractionPanel 
                onInteract={handleInteraction}
                petEnergy={selectedPet.energy}
                petMood={selectedPet.mood}
              />
            </div>
          </div>
        )}

        {!isConnected && (
          <div className="connection-message">
            <p>Connecting to DKS Digital Pet System backend...</p>
            <p>Make sure the backend is running on localhost:8000</p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
