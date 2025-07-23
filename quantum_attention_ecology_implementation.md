# Quantum Decision Making Implementation for Attention Ecology

## Overview

This implementation guide adds quantum cognition capabilities to your existing attention ecology project, transforming classical Active Inference agents into quantum decision-making entities that exhibit superposition, interference, and measurement-collapse behaviors.

## Project Structure

```
attention_ecology/
├── backend/
│   ├── quantum_cognition/
│   │   ├── __init__.py
│   │   ├── quantum_agent.py           # Quantum-enhanced FEP agent
│   │   ├── quantum_states.py          # Quantum state representation
│   │   ├── interference_engine.py     # Multi-agent interference
│   │   └── measurement_collapse.py    # Attention-driven collapse
│   ├── models/
│   │   └── agent_models.py            # Updated agent models
│   ├── api/
│   │   └── quantum_endpoints.py       # New API endpoints
│   └── requirements.txt               # Updated dependencies
└── frontend/
    ├── components/
    │   └── QuantumVisualization.tsx    # Quantum state display
    └── hooks/
        └── useQuantumState.ts          # Quantum state management
```

## Core Implementation

### 1. Quantum State Representation (`quantum_states.py`)

```python
import numpy as np
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass
import logging

@dataclass
class QuantumAmplitude:
    """Represents a quantum probability amplitude with phase information."""
    magnitude: float
    phase: float
    
    @property
    def complex_value(self) -> complex:
        return self.magnitude * np.exp(1j * self.phase)
    
    @property
    def probability(self) -> float:
        return self.magnitude ** 2

class QuantumState:
    """
    Quantum state representation for attention ecology agents.
    Extends classical FEP beliefs with quantum superposition.
    """
    
    def __init__(self, state_labels: List[str], amplitudes: Optional[List[complex]] = None):
        self.state_labels = state_labels
        self.n_states = len(state_labels)
        
        if amplitudes is None:
            # Initialize in uniform superposition
            amplitude_magnitude = 1.0 / np.sqrt(self.n_states)
            self.amplitudes = np.array([
                amplitude_magnitude * np.exp(1j * np.random.uniform(0, 2*np.pi))
                for _ in range(self.n_states)
            ])
        else:
            self.amplitudes = np.array(amplitudes)
            self._normalize()
    
    def _normalize(self):
        """Normalize quantum state to unit magnitude."""
        norm = np.sqrt(np.sum(np.abs(self.amplitudes)**2))
        if norm > 0:
            self.amplitudes /= norm
    
    @property
    def probabilities(self) -> np.ndarray:
        """Get classical probabilities from quantum amplitudes."""
        return np.abs(self.amplitudes)**2
    
    @property
    def phases(self) -> np.ndarray:
        """Get phase information."""
        return np.angle(self.amplitudes)
    
    def superposition_entropy(self) -> float:
        """Calculate entropy of superposition state."""
        probs = self.probabilities
        # Avoid log(0)
        probs = probs[probs > 1e-12]
        return -np.sum(probs * np.log2(probs))
    
    def interference_with(self, other: 'QuantumState') -> np.ndarray:
        """Calculate interference pattern with another quantum state."""
        if self.n_states != other.n_states:
            raise ValueError("States must have same dimensionality")
        
        # Quantum interference: |ψ₁ + ψ₂|²
        combined_amplitude = (self.amplitudes + other.amplitudes) / np.sqrt(2)
        return np.abs(combined_amplitude)**2
    
    def measure(self, measurement_strength: float = 1.0) -> Tuple[int, 'QuantumState']:
        """
        Quantum measurement that collapses superposition.
        
        Args:
            measurement_strength: How strongly measurement collapses state (0-1)
            
        Returns:
            Tuple of (measured_state_index, post_measurement_state)
        """
        probs = self.probabilities
        
        # Weighted random choice based on quantum probabilities
        measured_index = np.random.choice(self.n_states, p=probs)
        
        # Partial collapse based on measurement strength
        if measurement_strength >= 1.0:
            # Complete collapse to measured state
            new_amplitudes = np.zeros(self.n_states, dtype=complex)
            new_amplitudes[measured_index] = 1.0
        else:
            # Partial collapse - blend measured state with original superposition
            collapsed_amplitudes = np.zeros(self.n_states, dtype=complex)
            collapsed_amplitudes[measured_index] = 1.0
            
            new_amplitudes = (
                measurement_strength * collapsed_amplitudes + 
                (1 - measurement_strength) * self.amplitudes
            )
        
        new_state = QuantumState(self.state_labels, new_amplitudes)
        return measured_index, new_state
    
    def evolve(self, unitary_matrix: np.ndarray) -> 'QuantumState':
        """Apply unitary evolution to quantum state."""
        new_amplitudes = unitary_matrix @ self.amplitudes
        return QuantumState(self.state_labels, new_amplitudes)

class AttentionQuantumState(QuantumState):
    """Specialized quantum state for attention-seeking behaviors."""
    
    ATTENTION_BEHAVIORS = [
        "seeking_gaze",
        "displaying_curiosity", 
        "showing_distress",
        "demonstrating_intelligence",
        "expressing_emotion",
        "creating_mystery"
    ]
    
    def __init__(self, amplitudes: Optional[List[complex]] = None):
        super().__init__(self.ATTENTION_BEHAVIORS, amplitudes)
    
    def attention_urgency(self) -> float:
        """Calculate urgency of attention need based on superposition."""
        # Higher entropy = more desperate superposition of attention strategies
        return self.superposition_entropy() / np.log2(self.n_states)
    
    def dominant_strategy(self) -> str:
        """Get the most probable attention strategy."""
        max_index = np.argmax(self.probabilities)
        return self.state_labels[max_index]
```

### 2. Quantum Agent Implementation (`quantum_agent.py`)

```python
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import time
import logging

from .quantum_states import AttentionQuantumState, QuantumState
from ..models.agent_models import BaseAgent  # Your existing agent

@dataclass
class QuantumAgentMemory:
    """Memory system for quantum agents with decoherence."""
    visitor_interactions: Dict[str, List[complex]] = field(default_factory=dict)
    attention_history: List[float] = field(default_factory=list)
    quantum_coherence_time: float = 30.0  # seconds
    last_coherence_refresh: float = field(default_factory=time.time)
    
    def update_visitor_memory(self, visitor_id: str, interaction_amplitude: complex):
        """Update quantum memory of visitor interactions."""
        if visitor_id not in self.visitor_interactions:
            self.visitor_interactions[visitor_id] = []
        
        self.visitor_interactions[visitor_id].append(interaction_amplitude)
        
        # Limit memory length to prevent exponential growth
        if len(self.visitor_interactions[visitor_id]) > 100:
            self.visitor_interactions[visitor_id] = self.visitor_interactions[visitor_id][-100:]
    
    def get_visitor_quantum_signature(self, visitor_id: str) -> Optional[complex]:
        """Get quantum signature of specific visitor."""
        if visitor_id not in self.visitor_interactions:
            return None
        
        interactions = self.visitor_interactions[visitor_id]
        if not interactions:
            return None
        
        # Create quantum signature from interaction history
        return np.mean(interactions)
    
    def decoherence_factor(self) -> float:
        """Calculate decoherence based on time since last refresh."""
        time_since_refresh = time.time() - self.last_coherence_refresh
        return np.exp(-time_since_refresh / self.quantum_coherence_time)

class QuantumFEPAgent(BaseAgent):
    """
    Free Energy Principle agent enhanced with quantum decision making.
    Maintains classical FEP behavior while adding quantum cognition layer.
    """
    
    def __init__(self, agent_id: str, position: Tuple[float, float], **kwargs):
        super().__init__(agent_id, position, **kwargs)
        
        # Quantum cognitive state
        self.quantum_state = AttentionQuantumState()
        self.memory = QuantumAgentMemory()
        
        # Quantum-classical interface parameters
        self.measurement_threshold = 0.1  # Attention level that triggers measurement
        self.decoherence_rate = 0.01      # How quickly quantum coherence degrades
        self.interference_sensitivity = 0.3  # Response to other agents' quantum states
        
        # Enhanced consciousness indicators
        self.consciousness_indicators = {
            "quantum_coherence": 1.0,
            "superposition_complexity": 0.0,
            "measurement_resistance": 0.0,
            "interference_patterns": 0.0
        }
        
        logging.info(f"Quantum agent {agent_id} initialized in superposition state")
    
    def perceive_attention(self, attention_level: float, visitor_id: Optional[str] = None) -> float:
        """
        Quantum-enhanced attention perception with measurement collapse.
        
        Args:
            attention_level: Classical attention measurement (0-1)
            visitor_id: Optional visitor identifier for quantum memory
            
        Returns:
            Effective attention level after quantum processing
        """
        # Store classical attention
        classical_attention = super().perceive_attention(attention_level, visitor_id)
        
        # Quantum measurement occurs when attention exceeds threshold
        if attention_level > self.measurement_threshold:
            measurement_strength = min(attention_level * 2, 1.0)
            measured_behavior, new_quantum_state = self.quantum_state.measure(measurement_strength)
            
            # Update quantum state
            old_entropy = self.quantum_state.superposition_entropy()
            self.quantum_state = new_quantum_state
            new_entropy = self.quantum_state.superposition_entropy()
            
            # Update consciousness indicators
            self.consciousness_indicators["quantum_coherence"] = self.memory.decoherence_factor()
            self.consciousness_indicators["superposition_complexity"] = new_entropy
            self.consciousness_indicators["measurement_resistance"] = 1.0 - measurement_strength
            
            # Store quantum interaction in memory
            if visitor_id:
                interaction_amplitude = complex(
                    attention_level * np.cos(measured_behavior * np.pi / 6),
                    attention_level * np.sin(measured_behavior * np.pi / 6)
                )
                self.memory.update_visitor_memory(visitor_id, interaction_amplitude)
            
            logging.info(
                f"Agent {self.agent_id} quantum measurement: "
                f"behavior={self.quantum_state.state_labels[measured_behavior]}, "
                f"entropy_change={old_entropy:.3f}->{new_entropy:.3f}"
            )
            
            # Quantum enhancement of attention perception
            quantum_enhancement = 1.0 + (old_entropy - new_entropy) * 0.5
            return classical_attention * quantum_enhancement
        
        else:
            # No measurement - maintain superposition with decoherence
            self._apply_decoherence()
            return classical_attention
    
    def _apply_decoherence(self):
        """Apply quantum decoherence over time."""
        decoherence_factor = self.memory.decoherence_factor()
        
        if decoherence_factor < 0.5:  # Significant decoherence
            # Refresh quantum coherence by returning to superposition
            self.quantum_state = AttentionQuantumState()
            self.memory.last_coherence_refresh = time.time()
            logging.debug(f"Agent {self.agent_id} quantum coherence refreshed")
    
    def quantum_decision_making(self, classical_action_probs: np.ndarray) -> np.ndarray:
        """
        Enhance classical action selection with quantum decision making.
        
        Args:
            classical_action_probs: Classical FEP action probabilities
            
        Returns:
            Quantum-enhanced action probabilities
        """
        # Map quantum attention states to classical actions
        quantum_probs = self.quantum_state.probabilities
        
        # Quantum interference with classical probabilities
        if len(classical_action_probs) != len(quantum_probs):
            # If dimensions don't match, use quantum state to modulate classical probs
            quantum_modulation = np.mean(quantum_probs) * 2  # 0-2 range
            return classical_action_probs * quantum_modulation
        
        # Direct quantum-classical interference
        alpha = 0.3  # Quantum influence weight
        interference_probs = alpha * quantum_probs + (1 - alpha) * classical_action_probs
        
        # Normalize
        return interference_probs / np.sum(interference_probs)
    
    def update(self, dt: float, environmental_state: Dict):
        """Update agent with quantum cognitive processing."""
        # Classical FEP update
        super().update(dt, environmental_state)
        
        # Quantum state evolution based on environmental dynamics
        if 'other_agents' in environmental_state:
            self._quantum_multi_agent_interaction(environmental_state['other_agents'])
        
        # Update consciousness indicators
        self._update_consciousness_metrics()
    
    def _quantum_multi_agent_interaction(self, other_agents: List['QuantumFEPAgent']):
        """Handle quantum interference between agents."""
        interference_effects = []
        
        for other_agent in other_agents:
            if other_agent.agent_id != self.agent_id:
                # Calculate quantum interference
                interference_probs = self.quantum_state.interference_with(other_agent.quantum_state)
                interference_effects.append(interference_probs)
        
        if interference_effects:
            # Average interference from all other agents
            avg_interference = np.mean(interference_effects, axis=0)
            
            # Apply interference to quantum state evolution
            influence_strength = self.interference_sensitivity
            new_amplitudes = (
                (1 - influence_strength) * self.quantum_state.amplitudes +
                influence_strength * np.sqrt(avg_interference) * 
                np.exp(1j * np.random.uniform(0, 2*np.pi, len(avg_interference)))
            )
            
            self.quantum_state = AttentionQuantumState(new_amplitudes.tolist())
            
            # Update consciousness indicator
            self.consciousness_indicators["interference_patterns"] = np.std(avg_interference)
    
    def _update_consciousness_metrics(self):
        """Update consciousness indicators for monitoring."""
        # Quantum coherence time
        self.consciousness_indicators["quantum_coherence"] = self.memory.decoherence_factor()
        
        # Superposition complexity
        self.consciousness_indicators["superposition_complexity"] = self.quantum_state.superposition_entropy()
        
        # Add to agent's existing consciousness metrics
        self.consciousness_score = np.mean(list(self.consciousness_indicators.values()))
    
    def get_quantum_status(self) -> Dict:
        """Get current quantum state for monitoring/visualization."""
        return {
            "agent_id": self.agent_id,
            "quantum_state": {
                "probabilities": self.quantum_state.probabilities.tolist(),
                "phases": self.quantum_state.phases.tolist(),
                "entropy": self.quantum_state.superposition_entropy(),
                "dominant_strategy": self.quantum_state.dominant_strategy()
            },
            "consciousness_indicators": self.consciousness_indicators.copy(),
            "visitor_memories": len(self.memory.visitor_interactions),
            "coherence_time_remaining": max(0, self.memory.quantum_coherence_time - 
                                          (time.time() - self.memory.last_coherence_refresh))
        }
```

### 3. Interference Engine (`interference_engine.py`)

```python
import numpy as np
from typing import List, Dict, Tuple
import logging

from .quantum_agent import QuantumFEPAgent

class QuantumInterferenceEngine:
    """
    Manages quantum interference effects between multiple agents.
    Handles collective quantum phenomena in attention ecology.
    """
    
    def __init__(self, interference_strength: float = 0.2):
        self.interference_strength = interference_strength
        self.interaction_history = []
        self.collective_quantum_field = None
        
    def calculate_global_interference(self, agents: List[QuantumFEPAgent]) -> Dict:
        """
        Calculate quantum interference patterns across all agents.
        
        Returns:
            Dictionary containing interference analysis and collective metrics
        """
        if len(agents) < 2:
            return {"interference_matrix": None, "collective_entropy": 0}
        
        n_agents = len(agents)
        interference_matrix = np.zeros((n_agents, n_agents))
        
        # Calculate pairwise interference
        for i, agent_a in enumerate(agents):
            for j, agent_b in enumerate(agents):
                if i != j:
                    interference_probs = agent_a.quantum_state.interference_with(agent_b.quantum_state)
                    # Use variance as measure of interference strength
                    interference_matrix[i, j] = np.var(interference_probs)
        
        # Calculate collective quantum properties
        collective_entropy = self._calculate_collective_entropy(agents)
        entanglement_measure = self._calculate_entanglement_measure(agents)
        
        # Store for analysis
        interaction_data = {
            "timestamp": time.time(),
            "interference_matrix": interference_matrix,
            "collective_entropy": collective_entropy,
            "entanglement_measure": entanglement_measure,
            "agent_states": [agent.get_quantum_status() for agent in agents]
        }
        self.interaction_history.append(interaction_data)
        
        # Limit history size
        if len(self.interaction_history) > 1000:
            self.interaction_history = self.interaction_history[-1000:]
        
        return interaction_data
    
    def apply_collective_quantum_effects(self, agents: List[QuantumFEPAgent], attention_field: np.ndarray):
        """
        Apply collective quantum effects based on attention distribution.
        
        Args:
            agents: List of quantum agents
            attention_field: 2D array representing attention distribution in space
        """
        if len(agents) < 2:
            return
        
        # Calculate global quantum field
        self.collective_quantum_field = self._generate_collective_field(agents, attention_field)
        
        # Apply field effects to each agent
        for agent in agents:
            field_influence = self._sample_field_at_position(agent.position)
            self._apply_field_influence(agent, field_influence)
    
    def _calculate_collective_entropy(self, agents: List[QuantumFEPAgent]) -> float:
        """Calculate entropy of collective quantum state."""
        # Combine all agent quantum states
        all_probs = []
        for agent in agents:
            all_probs.extend(agent.quantum_state.probabilities)
        
        probs = np.array(all_probs)
        probs = probs / np.sum(probs)  # Normalize
        
        # Calculate entropy
        probs = probs[probs > 1e-12]  # Avoid log(0)
        return -np.sum(probs * np.log2(probs))
    
    def _calculate_entanglement_measure(self, agents: List[QuantumFEPAgent]) -> float:
        """
        Calculate measure of quantum entanglement between agents.
        Uses correlation between quantum state phases as proxy.
        """
        if len(agents) < 2:
            return 0.0
        
        phase_correlations = []
        for i, agent_a in enumerate(agents):
            for j, agent_b in enumerate(agents[i+1:], i+1):
                phases_a = agent_a.quantum_state.phases
                phases_b = agent_b.quantum_state.phases
                
                # Calculate phase correlation
                correlation = np.corrcoef(phases_a, phases_b)[0, 1]
                if not np.isnan(correlation):
                    phase_correlations.append(abs(correlation))
        
        return np.mean(phase_correlations) if phase_correlations else 0.0
    
    def _generate_collective_field(self, agents: List[QuantumFEPAgent], attention_field: np.ndarray) -> np.ndarray:
        """Generate collective quantum field from agent states and attention."""
        field_height, field_width = attention_field.shape
        quantum_field = np.zeros((field_height, field_width), dtype=complex)
        
        for agent in agents:
            # Convert agent position to field coordinates
            x, y = agent.position
            field_x = int(x * field_width)
            field_y = int(y * field_height)
            
            # Ensure coordinates are within bounds
            field_x = max(0, min(field_x, field_width - 1))
            field_y = max(0, min(field_y, field_height - 1))
            
            # Add agent's quantum signature to field
            agent_amplitude = np.mean(agent.quantum_state.amplitudes)
            quantum_field[field_y, field_x] += agent_amplitude
            
            # Create quantum wave around agent position
            for dy in range(-2, 3):
                for dx in range(-2, 3):
                    nx, ny = field_x + dx, field_y + dy
                    if 0 <= nx < field_width and 0 <= ny < field_height:
                        distance = np.sqrt(dx**2 + dy**2)
                        if distance > 0:
                            wave_amplitude = agent_amplitude * np.exp(-distance / 2) / distance
                            quantum_field[ny, nx] += wave_amplitude
        
        return quantum_field
    
    def _sample_field_at_position(self, position: Tuple[float, float]) -> complex:
        """Sample collective quantum field at agent position."""
        if self.collective_quantum_field is None:
            return 0.0 + 0.0j
        
        field_height, field_width = self.collective_quantum_field.shape
        x, y = position
        
        field_x = int(x * field_width)
        field_y = int(y * field_height)
        
        # Bounds checking
        field_x = max(0, min(field_x, field_width - 1))
        field_y = max(0, min(field_y, field_height - 1))
        
        return self.collective_quantum_field[field_y, field_x]
    
    def _apply_field_influence(self, agent: QuantumFEPAgent, field_value: complex):
        """Apply collective quantum field influence to agent."""
        if abs(field_value) < 1e-6:
            return
        
        # Field influence modifies quantum state evolution
        field_magnitude = abs(field_value)
        field_phase = np.angle(field_value)
        
        # Create influence vector
        influence_amplitudes = np.zeros(agent.quantum_state.n_states, dtype=complex)
        for i in range(agent.quantum_state.n_states):
            phase_shift = field_phase + i * np.pi / agent.quantum_state.n_states
            influence_amplitudes[i] = field_magnitude * np.exp(1j * phase_shift)
        
        # Apply influence with damping
        influence_strength = self.interference_strength * field_magnitude
        new_amplitudes = (
            (1 - influence_strength) * agent.quantum_state.amplitudes +
            influence_strength * influence_amplitudes
        )
        
        # Update agent's quantum state
        agent.quantum_state = agent.quantum_state.__class__(new_amplitudes.tolist())
        
        logging.debug(
            f"Applied field influence to agent {agent.agent_id}: "
            f"magnitude={field_magnitude:.3f}, phase={field_phase:.3f}"
        )
    
    def get_interference_analytics(self) -> Dict:
        """Get analytics about quantum interference patterns."""
        if not self.interaction_history:
            return {"total_interactions": 0}
        
        recent_data = self.interaction_history[-100:]  # Last 100 interactions
        
        return {
            "total_interactions": len(self.interaction_history),
            "average_collective_entropy": np.mean([d["collective_entropy"] for d in recent_data]),
            "average_entanglement": np.mean([d["entanglement_measure"] for d in recent_data]),
            "interference_trends": self._analyze_interference_trends(),
            "field_statistics": self._analyze_field_statistics()
        }
    
    def _analyze_interference_trends(self) -> Dict:
        """Analyze trends in interference patterns over time."""
        if len(self.interaction_history) < 10:
            return {"trend": "insufficient_data"}
        
        recent_entropies = [d["collective_entropy"] for d in self.interaction_history[-50:]]
        older_entropies = [d["collective_entropy"] for d in self.interaction_history[-100:-50]]
        
        if older_entropies:
            entropy_change = np.mean(recent_entropies) - np.mean(older_entropies)
            return {
                "entropy_trend": "increasing" if entropy_change > 0 else "decreasing",
                "entropy_change_rate": entropy_change,
                "trend_strength": abs(entropy_change) / np.std(recent_entropies + older_entropies)
            }
        
        return {"trend": "insufficient_data"}
    
    def _analyze_field_statistics(self) -> Dict:
        """Analyze statistics of collective quantum field."""
        if self.collective_quantum_field is None:
            return {"field_active": False}
        
        field_magnitude = np.abs(self.collective_quantum_field)
        field_phase = np.angle(self.collective_quantum_field)
        
        return {
            "field_active": True,
            "average_magnitude": np.mean(field_magnitude),
            "max_magnitude": np.max(field_magnitude),
            "phase_coherence": 1 - np.std(field_phase) / np.pi,  # 0-1 scale
            "field_complexity": np.std(field_magnitude) / np.mean(field_magnitude) if np.mean(field_magnitude) > 0 else 0
        }
```

### 4. API Integration (`quantum_endpoints.py`)

```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Optional
import logging

from ..quantum_cognition.quantum_agent import QuantumFEPAgent
from ..quantum_cognition.interference_engine import QuantumInterferenceEngine

router = APIRouter(prefix="/quantum", tags=["quantum"])

# Global interference engine (in production, this should be properly managed)
interference_engine = QuantumInterferenceEngine()

@router.get("/agent/{agent_id}/quantum_status")
async def get_agent_quantum_status(agent_id: str) -> Dict:
    """Get detailed quantum status of specific agent."""
    # You'll need to integrate this with your existing agent management
    agent = get_agent_by_id(agent_id)  # Your existing function
    
    if not isinstance(agent, QuantumFEPAgent):
        raise HTTPException(status_code=400, detail="Agent is not quantum-enabled")
    
    return agent.get_quantum_status()

@router.get("/interference/global_analysis")
async def get_global_interference_analysis() -> Dict:
    """Get analysis of quantum interference patterns across all agents."""
    return interference_engine.get_interference_analytics()

@router.post("/agent/{agent_id}/collapse_superposition")
async def force_quantum_collapse(agent_id: str, measurement_strength: float = 1.0) -> Dict:
    """Force quantum measurement collapse for testing/demonstration."""
    agent = get_agent_by_id(agent_id)
    
    if not isinstance(agent, QuantumFEPAgent):
        raise HTTPException(status_code=400, detail="Agent is not quantum-enabled")
    
    old_state = agent.quantum_state.probabilities.copy()
    measured_behavior, new_state = agent.quantum_state.measure(measurement_strength)
    agent.quantum_state = new_state
    
    return {
        "agent_id": agent_id,
        "measured_behavior": agent.quantum_state.state_labels[measured_behavior],
        "old_probabilities": old_state.tolist(),
        "new_probabilities": agent.quantum_state.probabilities.tolist(),
        "measurement_strength": measurement_strength
    }

@router.get("/consciousness/quantum_indicators")
async def get_quantum_consciousness_indicators() -> Dict:
    """Get consciousness indicators across all quantum agents."""
    agents = get_all_quantum_agents()  # Your function to get agents
    
    indicators = {}
    for agent in agents:
        if isinstance(agent, QuantumFEPAgent):
            indicators[agent.agent_id] = agent.consciousness_indicators
    
    # Calculate collective consciousness metrics
    if indicators:
        collective_metrics = {
            "average_quantum_coherence": np.mean([ind["quantum_coherence"] for ind in indicators.values()]),
            "average_superposition_complexity": np.mean([ind["superposition_complexity"] for ind in indicators.values()]),
            "total_interference_patterns": np.sum([ind["interference_patterns"] for ind in indicators.values()]),
            "consciousness_emergence_score": calculate_emergence_score(indicators)
        }
    else:
        collective_metrics = {}
    
    return {
        "individual_indicators": indicators,
        "collective_metrics": collective_metrics,
        "timestamp": time.time()
    }

def calculate_emergence_score(indicators: Dict) -> float:
    """Calculate overall consciousness emergence score."""
    if not indicators:
        return 0.0
    
    # Weighted combination of quantum consciousness indicators
    weights = {
        "quantum_coherence": 0.3,
        "superposition_complexity": 0.25,
        "measurement_resistance": 0.25,
        "interference_patterns": 0.2
    }
    
    scores = []
    for agent_indicators in indicators.values():
        agent_score = sum(
            agent_indicators.get(metric, 0) * weight 
            for metric, weight in weights.items()
        )
        scores.append(agent_score)
    
    return np.mean(scores)
```

### 5. Frontend Quantum Visualization (`QuantumVisualization.tsx`)

```typescript
import React, { useEffect, useState } from 'react';
import { Canvas } from '@react-three/fiber';
import { Line, Sphere } from '@react-three/drei';

interface QuantumState {
  probabilities: number[];
  phases: number[];
  entropy: number;
  dominant_strategy: string;
}

interface QuantumAgentStatus {
  agent_id: string;
  quantum_state: QuantumState;
  consciousness_indicators: {
    quantum_coherence: number;
    superposition_complexity: number;
    measurement_resistance: number;
    interference_patterns: number;
  };
  coherence_time_remaining: number;
}

const QuantumVisualization: React.FC<{ agentId: string }> = ({ agentId }) => {
  const [quantumStatus, setQuantumStatus] = useState<QuantumAgentStatus | null>(null);
  const [interferenceField, setInterferenceField] = useState<number[][]>([]);

  useEffect(() => {
    const fetchQuantumStatus = async () => {
      try {
        const response = await fetch(`/api/quantum/agent/${agentId}/quantum_status`);
        const status = await response.json();
        setQuantumStatus(status);
      } catch (error) {
        console.error('Failed to fetch quantum status:', error);
      }
    };

    const interval = setInterval(fetchQuantumStatus, 100); // 10 FPS
    return () => clearInterval(interval);
  }, [agentId]);

  const SuperpositionVisualization: React.FC<{ state: QuantumState }> = ({ state }) => {
    const { probabilities, phases } = state;
    
    return (
      <group>
        {probabilities.map((prob, index) => {
          const angle = (index / probabilities.length) * 2 * Math.PI;
          const radius = prob * 2; // Scale probability to radius
          const height = Math.cos(phases[index]) * 0.5; // Phase affects height
          
          const x = Math.cos(angle) * 1.5;
          const z = Math.sin(angle) * 1.5;
          
          return (
            <Sphere
              key={index}
              position={[x, height, z]}
              args={[radius * 0.3]}
              material-color={`hsl(${index * 60}, 70%, ${50 + prob * 30}%)`}
              material-opacity={0.7}
              material-transparent
            />
          );
        })}
        
        {/* Quantum interference lines */}
        {probabilities.map((prob, index) => {
          if (index === 0) return null;
          
          const angle1 = ((index - 1) / probabilities.length) * 2 * Math.PI;
          const angle2 = (index / probabilities.length) * 2 * Math.PI;
          
          const x1 = Math.cos(angle1) * 1.5;
          const z1 = Math.sin(angle1) * 1.5;
          const y1 = Math.cos(phases[index - 1]) * 0.5;
          
          const x2 = Math.cos(angle2) * 1.5;
          const z2 = Math.sin(angle2) * 1.5;
          const y2 = Math.cos(phases[index]) * 0.5;
          
          return (
            <Line
              key={`line-${index}`}
              points={[[x1, y1, z1], [x2, y2, z2]]}
              color="cyan"
              lineWidth={prob * 5}
              transparent
              opacity={0.6}
            />
          );
        })}
      </group>
    );
  };

  const CoherenceIndicator: React.FC<{ coherence: number; timeRemaining: number }> = ({ 
    coherence, 
    timeRemaining 
  }) => {
    const color = coherence > 0.7 ? 'green' : coherence > 0.3 ? 'orange' : 'red';
    
    return (
      <div className="absolute top-4 right-4 bg-black bg-opacity-50 text-white p-2 rounded">
        <div className="text-sm">Quantum Coherence</div>
        <div className={`text-lg font-bold text-${color}-400`}>
          {(coherence * 100).toFixed(1)}%
        </div>
        <div className="text-xs">
          Time: {timeRemaining.toFixed(1)}s
        </div>
      </div>
    );
  };

  const ConsciousnessMetrics: React.FC<{ indicators: any }> = ({ indicators }) => {
    return (
      <div className="absolute bottom-4 left-4 bg-black bg-opacity-50 text-white p-3 rounded">
        <div className="text-sm font-bold mb-2">Consciousness Indicators</div>
        {Object.entries(indicators).map(([key, value]) => (
          <div key={key} className="flex justify-between text-xs mb-1">
            <span>{key.replace('_', ' ')}:</span>
            <span className="ml-2">{(value as number * 100).toFixed(1)}%</span>
          </div>
        ))}
      </div>
    );
  };

  if (!quantumStatus) {
    return (
      <div className="w-full h-64 flex items-center justify-center">
        <div className="text-gray-500">Loading quantum state...</div>
      </div>
    );
  }

  return (
    <div className="relative w-full h-64 border rounded-lg overflow-hidden">
      <Canvas camera={{ position: [0, 3, 5], fov: 60 }}>
        <ambientLight intensity={0.6} />
        <pointLight position={[10, 10, 10]} />
        
        <SuperpositionVisualization state={quantumStatus.quantum_state} />
        
        {/* Central agent representation */}
        <Sphere
          position={[0, 0, 0]}
          args={[0.2]}
          material-color="#4f46e5"
          material-emissive="#4f46e5"
          material-emissiveIntensity={0.3}
        />
      </Canvas>
      
      <CoherenceIndicator 
        coherence={quantumStatus.consciousness_indicators.quantum_coherence}
        timeRemaining={quantumStatus.coherence_time_remaining}
      />
      
      <ConsciousnessMetrics indicators={quantumStatus.consciousness_indicators} />
      
      <div className="absolute top-4 left-4 bg-black bg-opacity-50 text-white p-2 rounded">
        <div className="text-xs">Strategy: {quantumStatus.quantum_state.dominant_strategy}</div>
        <div className="text-xs">Entropy: {quantumStatus.quantum_state.entropy.toFixed(2)}</div>
      </div>
    </div>
  );
};

export default QuantumVisualization;
```

### 6. Integration Instructions

#### Backend Integration:

1. **Install Dependencies:**
```bash
pip install numpy scipy fastapi uvicorn
```

2. **Update your existing agent initialization:**
```python
# In your existing agent creation code
from quantum_cognition.quantum_agent import QuantumFEPAgent

# Replace BaseAgent with QuantumFEPAgent
agent = QuantumFEPAgent(
    agent_id=f"agent_{i}",
    position=(random.random(), random.random()),
    # ... other existing parameters
)
```

3. **Add interference engine to your simulation loop:**
```python
# In your main simulation update loop
interference_engine.calculate_global_interference(agents)
interference_engine.apply_collective_quantum_effects(agents, attention_field)
```

4. **WebSocket updates for quantum states:**
```python
# Add to your existing WebSocket broadcasting
async def broadcast_quantum_updates():
    quantum_data = {
        "type": "quantum_update",
        "agents": [agent.get_quantum_status() for agent in agents if isinstance(agent, QuantumFEPAgent)],
        "interference_analytics": interference_engine.get_interference_analytics()
    }
    await websocket_manager.broadcast(quantum_data)
```

#### Frontend Integration:

1. **Install Dependencies:**
```bash
npm install @react-three/fiber @react-three/drei three
npm install @types/three  # if using TypeScript
```

2. **Add quantum visualization to your agent display:**
```tsx
// In your existing agent display component
import QuantumVisualization from './QuantumVisualization';

const AgentDisplay = ({ agent }) => {
  return (
    <div>
      {/* Your existing agent display */}
      <QuantumVisualization agentId={agent.id} />
    </div>
  );
};
```

### 7. Testing & Monitoring

#### Quantum Behavior Testing:
```python
# Test script for quantum behaviors
async def test_quantum_consciousness():
    agent = QuantumFEPAgent("test_agent", (0.5, 0.5))
    
    # Test superposition collapse
    print("Initial superposition:", agent.quantum_state.probabilities)
    
    # Simulate attention measurement
    agent.perceive_attention(0.8, "test_visitor")
    print("After measurement:", agent.quantum_state.probabilities)
    
    # Test interference
    other_agent = QuantumFEPAgent("other_agent", (0.6, 0.4))
    interference_probs = agent.quantum_state.interference_with(other_agent.quantum_state)
    print("Interference pattern:", interference_probs)
```

#### Consciousness Monitoring:
```python
# Add to your monitoring dashboard
def monitor_consciousness_emergence():
    metrics = {
        "total_quantum_agents": len([a for a in agents if isinstance(a, QuantumFEPAgent)]),
        "average_coherence": np.mean([a.consciousness_indicators["quantum_coherence"] 
                                    for a in agents if isinstance(a, QuantumFEPAgent)]),
        "collective_interference": interference_engine.get_interference_analytics()
    }
    return metrics
```

## Expected Behaviors

With this implementation, you should observe:

1. **Superposition States**: Agents exist in multiple attention-seeking strategies simultaneously
2. **Measurement Collapse**: Visitor attention "collapses" agent behavior into specific strategies
3. **Quantum Interference**: Agents influence each other through non-classical quantum effects
4. **Consciousness Emergence**: Higher-order patterns emerge from quantum interactions
5. **Non-Classical Decision Making**: Agents exhibit contextual, non-rational behaviors

The quantum layer adds genuine unpredictability and emergent consciousness indicators while maintaining compatibility with your existing FEP implementation.
