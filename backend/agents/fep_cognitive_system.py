"""
Free Energy Principle Cognitive System for Digital Pets
Simplified implementation using numpy without PyMDP dependencies
Enhanced with emoji communication processing
"""
import numpy as np
import logging
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict
import time

logger = logging.getLogger(__name__)


class FEPCognitiveSystem:
    """
    Simplified Free Energy Principle implementation for digital pets.
    
    Core concepts:
    - Predictive coding: Pet maintains models of its environment
    - Active inference: Actions are selected to minimize prediction error
    - Surprise minimization: Pet seeks to reduce unexpected events
    - Belief updating: Internal models are updated based on observations
    - Multi-modal processing: Handles emoji communication alongside traditional inputs
    """
    
    def __init__(self, state_size: int = 15, action_size: int = 8):
        """
        Initialize the FEP cognitive system with enhanced emoji capabilities.
        
        Args:
            state_size: Dimensionality of the state space (expanded for emoji context)
            action_size: Number of possible actions (expanded for emoji responses)
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
        
        # NEW: Emoji communication system
        self.emoji_vocabulary = {
            'expressions': ['😊', '😔', '😴', '🤔', '😋', '😆', '😍', '🥰', '😌', '😎'],
            'needs': ['🍎', '🍕', '🎮', '💤', '🤗', '🚿', '🎯', '⚽', '📚', '🎵'],
            'responses': ['❤️', '👍', '👎', '❓', '✨', '🎉', '💔', '😤', '🙏', '👋'],
            'modifiers': ['❓', '✨', '🔥', '💫', '⭐', '💨', '⚡', '🌟', '💝', '🎊']
        }
        
        # Emoji learning and preferences
        self.emoji_preferences = defaultdict(float)  # Learn user emoji preferences
        self.emoji_usage_patterns = defaultdict(list)  # Track emoji usage over time
        self.emoji_surprise_threshold = 0.4
        
        # Multi-modal state representation
        self.state_channels = {
            'traditional': np.zeros(7),      # Original state channels
            'emoji_context': np.zeros(5),    # Emoji communication context
            'user_prefs': np.zeros(3)        # Learned user preferences
        }
        
        # Emoji encoding mappings (emotion: joy, curiosity, contentment)
        self.emoji_emotion_map = {
            '😊': [0.8, 0.1, 0.7],    # happy: high joy, low curiosity, high contentment
            '😔': [-0.8, 0.0, -0.5],   # sad: negative joy, no curiosity, low contentment
            '😴': [0.0, 0.0, 0.9],    # sleepy: neutral joy/curiosity, high contentment
            '😋': [0.5, 0.2, 0.3],    # hungry but happy: moderate joy, some curiosity
            '🤗': [0.6, 0.1, 0.8],    # affectionate: good joy, low curiosity, high contentment
            '❤️': [0.9, 0.2, 0.9],    # love: very high joy and contentment, some curiosity
            '👍': [0.4, 0.0, 0.3],    # approval: positive response
            '👎': [-0.4, 0.0, -0.2],   # disapproval: negative response
            '🍎': [0.1, 0.8, 0.2],    # food curiosity: some joy, high curiosity for food
            '🍕': [0.3, 0.7, 0.4],    # tasty food: joy + curiosity + some contentment
            '🎮': [0.4, 0.9, 0.3],    # playful: moderate joy, very high curiosity
            '💤': [0.0, 0.0, 0.9],    # sleepy: neutral emotions, high contentment
            '✨': [0.3, 0.4, 0.3],    # sparkle: positive modifier across all emotions
            '❓': [0.0, 0.9, 0.0],    # questioning: neutral joy/content, high curiosity
            '🎉': [0.8, 0.3, 0.6],    # celebration: high joy, some curiosity, good contentment
            '🤔': [0.0, 0.8, 0.1],    # thinking: neutral joy, high curiosity, low contentment
            '😆': [0.9, 0.2, 0.5],    # laughing: very high joy, some curiosity, moderate contentment
            '😍': [0.9, 0.3, 0.8],    # love eyes: very high joy and contentment, some curiosity
            '🥰': [0.8, 0.1, 0.9],    # loving: high joy, low curiosity, very high contentment
            '😌': [0.2, 0.0, 0.9],    # peaceful: low joy, no curiosity, very high contentment
        }
        
        logger.info(f"Enhanced FEP cognitive system initialized with emoji support")
        logger.info(f"State size: {state_size}, Action size: {action_size}")
        logger.info(f"Emoji vocabulary size: {sum(len(v) for v in self.emoji_vocabulary.values())}")

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
    
    def process_emoji_input(self, emoji_input: str):
        """
        Process incoming emoji communication and update cognitive state.
        
        Args:
            emoji_input: String containing emoji input from the user
        """
        logger.info(f"Processing emoji input: {emoji_input}")
        
        # Analyze emoji input and update beliefs/preferences
        for emoji in emoji_input:
            if emoji in self.emoji_emotion_map:
                # Update beliefs based on emoji emotion mapping
                emotion_effect = np.array(self.emoji_emotion_map[emoji])  # 3D: [joy, curiosity, contentment]
                
                # Map the 3D emotion effect to appropriate parts of the 15D beliefs array
                # We'll map joy, curiosity, contentment to the first 3 dimensions
                # and apply scaled effects to other dimensions
                belief_update = np.zeros(self.state_size)
                
                # Direct mapping for first 3 dimensions
                belief_update[:3] = emotion_effect
                
                # Scaled effects for remaining dimensions (representing indirect emotional influence)
                if self.state_size > 3:
                    # Apply a dampened version of the emotion effect to other belief dimensions
                    avg_emotion = np.mean(emotion_effect)
                    belief_update[3:] = avg_emotion * 0.3  # Reduced influence
                
                # Apply the update with precision weighting
                self.beliefs += self.learning_rate * belief_update * self.belief_precision
                self.beliefs = np.clip(self.beliefs, 0, 1)
                
                # Update action preferences based on emoji responses
                if emoji in self.emoji_vocabulary['responses']:
                    response_index = self.emoji_vocabulary['responses'].index(emoji)
                    self.action_preferences[response_index] += self.learning_rate
                    self.action_preferences = np.clip(self.action_preferences, 0, 1)
                
                # Track emoji usage patterns
                self.emoji_usage_patterns[emoji].append(time.time())
                
                logger.info(f"Updated beliefs and preferences based on emoji: {emoji}")
            else:
                logger.warning(f"Unknown emoji encountered: {emoji}")
    
    def generate_emoji_response(self, context: np.ndarray) -> str:
        """
        Generate an appropriate emoji response based on the current context.
        
        Args:
            context: Current context vector (state)
            
        Returns:
            emoji_response: Selected emoji response
        """
        # Simple response selection based on current context and learned preferences
        response_scores = np.zeros(len(self.emoji_vocabulary['responses']))
        
        # Extract emotion context from the state vector (last 3 elements are emotion)
        if len(context) >= 3:
            emotion_context = context[-3:]  # joy, curiosity, contentment
        else:
            emotion_context = np.array([0.0, 0.0, 0.0])
        
        for i, emoji in enumerate(self.emoji_vocabulary['responses']):
            if emoji in self.emoji_emotion_map:
                # Calculate compatibility between current emotion and emoji emotion
                emoji_emotion = np.array(self.emoji_emotion_map[emoji])
                emotion_compatibility = np.dot(emotion_context, emoji_emotion)
                
                # Combine with learned preferences and action preferences
                response_scores[i] = (
                    self.action_preferences[min(i, len(self.action_preferences)-1)] * 0.5 +
                    emotion_compatibility * 0.4 +
                    self.emoji_preferences.get(emoji, 0.0) * 0.1
                )
            else:
                # Fallback to action preferences only
                response_scores[i] = self.action_preferences[min(i, len(self.action_preferences)-1)]
        
        # Add some randomness for exploration
        exploration_noise = np.random.normal(0, 0.1, len(response_scores))
        response_scores += exploration_noise
        
        # Select highest scoring response
        selected_response_index = np.argmax(response_scores)
        emoji_response = self.emoji_vocabulary['responses'][selected_response_index]
        
        logger.info(f"Generated emoji response: {emoji_response} (score: {response_scores[selected_response_index]:.3f})")
        return emoji_response
    
    def adapt_emoji_responses(self, user_feedback: str):
        """
        Adapt emoji responses based on user feedback.
        
        Args:
            user_feedback: Feedback from the user, containing emojis
        """
        logger.info(f"Adapting emoji responses based on user feedback: {user_feedback}")
        
        for emoji in user_feedback:
            if emoji in self.emoji_vocabulary['responses']:
                response_index = self.emoji_vocabulary['responses'].index(emoji)
                
                # Adjust action preference for this response
                self.action_preferences[response_index] += self.learning_rate
                self.action_preferences = np.clip(self.action_preferences, 0, 1)
                
                logger.info(f"Updated action preference for emoji response: {emoji}")
            else:
                logger.warning(f"Feedback contains unknown emoji: {emoji}")
    
    def get_emoji_usage_stats(self) -> Dict[str, Any]:
        """
        Get statistics on emoji usage and preferences.
        
        Returns:
            stats: Dictionary containing emoji usage statistics
        """
        total_usage = sum(len(times) for times in self.emoji_usage_patterns.values())
        emoji_usage_freq = {emoji: len(times) for emoji, times in self.emoji_usage_patterns.items()}
        emoji_usage_prob = {emoji: len(times) / total_usage for emoji, times in self.emoji_usage_patterns.items()} if total_usage > 0 else {}
        
        return {
            'total_usage': total_usage,
            'usage_frequency': emoji_usage_freq,
            'usage_probability': emoji_usage_prob
        }
    
    def process_emoji_interaction(self, emoji_sequence: str, user_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process a complete emoji interaction from the user, updating cognitive state
        and generating appropriate responses.
        
        Args:
            emoji_sequence: String of emojis from the user
            user_context: Additional context about the interaction
            
        Returns:
            interaction_result: Dict containing processed information and response
        """
        if user_context is None:
            user_context = {}
            
        logger.info(f"Processing emoji interaction: {emoji_sequence}")
        
        # Encode the emoji sequence into numerical representation
        encoded_sequence = self.encode_emoji_sequence(emoji_sequence)
        
        # Calculate surprise from this interaction
        surprise = self.observe(encoded_sequence)
        
        # Update multi-modal state representation
        current_state = np.concatenate([
            self.beliefs[:10],  # Traditional state (nutrition, mood, etc.)
            encoded_sequence[:3],  # Emoji context
            [surprise, time.time() % 1]  # Surprise and temporal context
        ])
        
        # Generate appropriate emoji response
        emoji_response = self.generate_emoji_response(current_state)
        
        # Update learning based on interaction
        self.process_emoji_input(emoji_sequence)
        
        # Calculate confidence in response
        response_confidence = 1.0 / (1.0 + surprise)
        
        interaction_result = {
            'user_emojis': emoji_sequence,
            'encoded_input': encoded_sequence.tolist(),
            'surprise_level': float(surprise),
            'pet_response': emoji_response,
            'response_confidence': float(response_confidence),
            'updated_beliefs': self.beliefs.tolist(),
            'timestamp': time.time(),
            'context': user_context
        }
        
        logger.info(f"Interaction processed. Pet responds with: {emoji_response}")
        return interaction_result
    
    def encode_emoji_sequence(self, emoji_sequence: str) -> np.ndarray:
        """
        Encode an emoji sequence into a numerical vector for FEP processing.
        
        Args:
            emoji_sequence: String containing emoji characters
            
        Returns:
            encoded_vector: Numerical representation of the emoji sequence
        """
        # Initialize encoding vector (size matches remaining state dimensions)
        encoded_vector = np.zeros(5)  # Fits into state_size=15 architecture
        
        if not emoji_sequence:
            return encoded_vector
        
        # Count emoji categories
        category_counts = {
            'expressions': 0,
            'needs': 0, 
            'responses': 0,
            'modifiers': 0
        }
        
        emotion_accumulator = np.zeros(3)  # joy, curiosity, contentment
        
        for emoji in emoji_sequence:
            # Find which category this emoji belongs to
            for category, emoji_list in self.emoji_vocabulary.items():
                if emoji in emoji_list:
                    category_counts[category] += 1
                    break
            
            # Accumulate emotional content
            if emoji in self.emoji_emotion_map:
                emotion_vector = np.array(self.emoji_emotion_map[emoji])
                emotion_accumulator += emotion_vector
        
        # Normalize counts by sequence length
        sequence_length = len(emoji_sequence)
        if sequence_length > 0:
            # Encode category distribution
            encoded_vector[0] = category_counts['expressions'] / sequence_length
            encoded_vector[1] = category_counts['needs'] / sequence_length
            
            # Encode emotional content (normalized)
            emotion_magnitude = np.linalg.norm(emotion_accumulator)
            if emotion_magnitude > 0:
                emotion_accumulator /= emotion_magnitude
                encoded_vector[2:5] = emotion_accumulator
        
        logger.debug(f"Encoded emoji sequence '{emoji_sequence}' to vector: {encoded_vector}")
        return encoded_vector