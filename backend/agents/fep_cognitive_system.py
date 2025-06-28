"""
Free Energy Principle Cognitive System for Digital Pets
Simplified implementation using numpy without PyMDP dependencies
"""
import numpy as np
import logging
from typing import Dict, List, Any, Optional, Tuple

logger = logging.getLogger(__name__)


class FEPCognitiveSystem:
    """
    Simplified Free Energy Principle implementation for digital pets.
    
    Core concepts:
    - Predictive coding: Pet maintains models of its environment
    - Active inference: Actions are selected to minimize prediction error
    - Surprise minimization: Pet seeks to reduce unexpected events
    - Belief updating: Internal models are updated based on observations
    """
    
    def __init__(self, state_size: int = 10, action_size: int = 5):
        """
        Initialize the FEP cognitive system.
        
        Args:
            state_size: Dimensionality of the state space
            action_size: Number of possible actions
        """
        self.state_size = state_size
        self.action_size = action_size
        
        # Generative model (pet's beliefs about the world)
        self.beliefs = np.random.uniform(0, 1, state_size)
        self.belief_precision = np.ones(state_size)
        
        # Predictive model
        self.predictions = np.zeros(state_size)
        self.prediction_error = np.zeros(state_size)
        
        # Action preferences (prior preferences for actions)
        self.action_preferences = np.random.uniform(0, 1, action_size)
        
        # Learning parameters
        self.learning_rate = 0.1
        self.precision_update_rate = 0.05
        
        # History tracking
        self.surprise_history = []
        self.prediction_accuracy = 0.5
        
        logger.info(f"Initialized FEP cognitive system with {state_size} states and {action_size} actions")
    
    def observe(self, observation: np.ndarray) -> float:
        """
        Process an observation and calculate surprise.
        
        Args:
            observation: Current observation from the environment
            
        Returns:
            surprise: Level of surprise (prediction error)
        """
        # Ensure observation is the right size
        if len(observation) != self.state_size:
            observation = np.resize(observation, self.state_size)
        
        # Calculate prediction error
        self.prediction_error = observation - self.predictions
        
        # Calculate surprise (free energy proxy)
        surprise = np.sum(np.square(self.prediction_error) * self.belief_precision)
        
        # Update beliefs based on observation
        self.update_beliefs(observation)
        
        # Track surprise history
        self.surprise_history.append(surprise)
        if len(self.surprise_history) > 100:  # Keep only recent history
            self.surprise_history.pop(0)
        
        # Update prediction accuracy
        accuracy = 1.0 / (1.0 + surprise)
        self.prediction_accuracy = 0.9 * self.prediction_accuracy + 0.1 * accuracy
        
        return surprise
    
    def update_beliefs(self, observation: np.ndarray):
        """
        Update internal beliefs based on new observation.
        
        Args:
            observation: Current observation from the environment
        """
        # Weighted update of beliefs
        prediction_error = observation - self.beliefs
        self.beliefs += self.learning_rate * prediction_error * self.belief_precision
        
        # Clip beliefs to valid range
        self.beliefs = np.clip(self.beliefs, 0, 1)
        
        # Update precision based on prediction accuracy
        error_magnitude = np.abs(prediction_error)
        self.belief_precision += self.precision_update_rate * (1.0 - error_magnitude)
        self.belief_precision = np.clip(self.belief_precision, 0.1, 2.0)
    
    def predict_next_state(self, current_state: np.ndarray, action: int) -> np.ndarray:
        """
        Predict the next state given current state and action.
        
        Args:
            current_state: Current state
            action: Action to be taken
            
        Returns:
            predicted_state: Predicted next state
        """
        # Simple predictive model: weighted combination of current state and action effect
        action_effect = np.zeros(self.state_size)
        if action < self.state_size:
            action_effect[action] = 0.1
        
        predicted_state = 0.9 * current_state + 0.1 * action_effect + 0.05 * self.beliefs
        self.predictions = np.clip(predicted_state, 0, 1)
        
        return self.predictions
    
    def select_action(self, current_state: np.ndarray) -> Tuple[int, float]:
        """
        Select action using active inference principles.
        
        Args:
            current_state: Current state of the pet
            
        Returns:
            action: Selected action index
            confidence: Confidence in the action selection
        """
        action_values = np.zeros(self.action_size)
        
        for action in range(self.action_size):
            # Predict outcome of this action
            predicted_state = self.predict_next_state(current_state, action)
            
            # Calculate expected surprise for this action
            expected_error = np.sum(np.square(predicted_state - self.beliefs))
            
            # Action value = preference - expected surprise
            action_values[action] = self.action_preferences[action] - expected_error
        
        # Select action with highest value (softmax selection for exploration)
        action_probs = self.softmax(action_values)
        selected_action = np.random.choice(self.action_size, p=action_probs)
        confidence = action_probs[selected_action]
        
        return selected_action, confidence
    
    def update_action_preferences(self, action: int, outcome_surprise: float):
        """
        Update action preferences based on outcomes.
        
        Args:
            action: Action that was taken
            outcome_surprise: Surprise from the outcome
        """
        # Decrease preference for actions that led to high surprise
        preference_update = -self.learning_rate * outcome_surprise
        self.action_preferences[action] += preference_update
        
        # Normalize preferences
        self.action_preferences = np.clip(self.action_preferences, 0, 1)
    
    def get_cognitive_state(self) -> Dict[str, Any]:
        """
        Get current cognitive state for monitoring.
        
        Returns:
            state: Dictionary containing cognitive state information
        """
        return {
            'beliefs': self.beliefs.tolist(),
            'predictions': self.predictions.tolist(),
            'prediction_accuracy': self.prediction_accuracy,
            'recent_surprise': self.surprise_history[-10:] if self.surprise_history else [],
            'average_surprise': float(np.mean(self.surprise_history)) if self.surprise_history else 0,
            'belief_confidence': float(np.mean(self.belief_precision)),
            'action_preferences': self.action_preferences.tolist()
        }
    
    def adapt_to_environment(self, environment_complexity: float):
        """
        Adapt cognitive parameters based on environment complexity.
        
        Args:
            environment_complexity: Measure of how complex/unpredictable the environment is
        """
        # Adjust learning rate based on environment complexity
        base_learning_rate = 0.1
        self.learning_rate = base_learning_rate * (1.0 + environment_complexity)
        self.learning_rate = np.clip(self.learning_rate, 0.01, 0.5)
        
        # Adjust precision update rate
        self.precision_update_rate = 0.05 * (1.0 + 0.5 * environment_complexity)
        self.precision_update_rate = np.clip(self.precision_update_rate, 0.01, 0.2)
    
    @staticmethod
    def softmax(x: np.ndarray, temperature: float = 1.0) -> np.ndarray:
        """
        Compute softmax probabilities.
        
        Args:
            x: Input array
            temperature: Temperature parameter for exploration
            
        Returns:
            probabilities: Softmax probabilities
        """
        exp_x = np.exp((x - np.max(x)) / temperature)
        return exp_x / np.sum(exp_x)
    
    def save_state(self) -> Dict[str, Any]:
        """
        Save the current state of the FEP system.
        
        Returns:
            state: Dictionary containing the system state
        """
        return {
            'beliefs': self.beliefs.tolist(),
            'belief_precision': self.belief_precision.tolist(),
            'action_preferences': self.action_preferences.tolist(),
            'learning_rate': self.learning_rate,
            'precision_update_rate': self.precision_update_rate,
            'surprise_history': self.surprise_history[-50:],  # Keep recent history
            'prediction_accuracy': self.prediction_accuracy
        }
    
    def load_state(self, state: Dict[str, Any]):
        """
        Load the FEP system state.
        
        Args:
            state: Dictionary containing the system state
        """
        self.beliefs = np.array(state.get('beliefs', self.beliefs))
        self.belief_precision = np.array(state.get('belief_precision', self.belief_precision))
        self.action_preferences = np.array(state.get('action_preferences', self.action_preferences))
        self.learning_rate = state.get('learning_rate', self.learning_rate)
        self.precision_update_rate = state.get('precision_update_rate', self.precision_update_rate)
        self.surprise_history = state.get('surprise_history', [])
        self.prediction_accuracy = state.get('prediction_accuracy', 0.5)
        
        logger.info("Loaded FEP cognitive system state")