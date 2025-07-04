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
import re

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
        
        # Action preferences (prior preferences for actions)
        # Size should match the responses vocabulary size
        responses_size = len(self.emoji_vocabulary['responses'])
        self.action_preferences = np.random.uniform(0.2, 0.8, responses_size)  # Start with more varied preferences
        
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
            '😎': [0.6, 0.1, 0.7],    # cool: moderate joy, low curiosity, good contentment
            # Add missing response emojis
            '💔': [-0.8, 0.0, -0.8],   # broken heart: negative joy and contentment
            '😤': [-0.3, 0.2, -0.4],   # face with steam: slight negative, some curiosity
            '🙏': [0.3, 0.0, 0.8],    # praying: moderate joy, no curiosity, high contentment
            '👋': [0.5, 0.1, 0.4],    # waving: moderate joy, low curiosity, moderate contentment
            # Add missing needs emojis
            '🚿': [0.2, 0.1, 0.6],    # shower: low joy, low curiosity, moderate contentment
            '⚽': [0.5, 0.8, 0.4],    # soccer: moderate joy, high curiosity, moderate contentment
            '📚': [0.2, 0.9, 0.3],    # books: low joy, very high curiosity, low contentment
            '🎵': [0.6, 0.3, 0.5],    # music: moderate joy, some curiosity, moderate contentment
            # Add missing modifier emojis
            '🔥': [0.7, 0.4, 0.2],    # fire: high joy, some curiosity, low contentment
            '💫': [0.4, 0.5, 0.3],    # dizzy: moderate joy, high curiosity, low contentment
            '⭐': [0.5, 0.3, 0.4],    # star: moderate joy, some curiosity, moderate contentment
            '💨': [0.2, 0.6, 0.1],    # dashing away: low joy, high curiosity, low contentment
            '⚡': [0.6, 0.7, 0.2],    # lightning: moderate joy, high curiosity, low contentment
            '🌟': [0.6, 0.4, 0.5],    # glowing star: moderate joy, some curiosity, moderate contentment
            '💝': [0.8, 0.2, 0.8],    # heart with ribbon: high joy, low curiosity, high contentment
            '🎊': [0.8, 0.3, 0.6],    # confetti: high joy, some curiosity, moderate contentment
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
        
        # Calculate surprise (free energy proxy) - normalize to reduce sensitivity
        raw_surprise = np.sum(np.square(self.prediction_error) * self.belief_precision)
        
        # Normalize surprise to a more reasonable range (0-1)
        # Use sigmoid function to bound the surprise
        surprise = 1.0 / (1.0 + np.exp(-raw_surprise + 2.0))  # Shift by 2.0 to center around 0.5
        
        # Update beliefs based on observation
        self.update_beliefs(observation)
        
        # Track surprise history
        self.surprise_history.append(surprise)
        if len(self.surprise_history) > 100:  # Keep only recent history
            self.surprise_history.pop(0)
        
        # Update prediction accuracy
        accuracy = 1.0 - surprise  # Invert so low surprise = high accuracy
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
        # Use the size of action_preferences (which matches responses vocabulary)
        action_size = len(self.action_preferences)
        action_values = np.zeros(action_size)
        
        for action in range(action_size):
            # Predict outcome of this action
            predicted_state = self.predict_next_state(current_state, action)
            
            # Calculate expected surprise for this action
            expected_error = np.sum(np.square(predicted_state - self.beliefs))
            
            # Action value = preference - expected surprise
            action_values[action] = self.action_preferences[action] - expected_error
        
        # Select action with highest value (softmax selection for exploration)
        action_probs = self.softmax(action_values)
        selected_action = np.random.choice(action_size, p=action_probs)
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
        Process emoji input and update cognitive state accordingly.
        
        Args:
            emoji_input: String containing emoji characters
        """
        logger.info(f"Processing emoji input: {emoji_input}")
        
        # Use regex to properly split emojis (handles multi-character emojis)
        emoji_pattern = re.compile(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U000024C2-\U0001F251]+')
        emojis = emoji_pattern.findall(emoji_input)
        
        for emoji in emojis:
            if emoji in self.emoji_emotion_map:
                # Update beliefs based on emoji emotion
                emotion_vector = np.array(self.emoji_emotion_map[emoji])
                
                # Update user preferences for this emoji
                self.emoji_preferences[emoji] += self.learning_rate
                self.emoji_preferences[emoji] = min(1.0, self.emoji_preferences[emoji])
                
                # Update action preferences based on emoji category
                if emoji in self.emoji_vocabulary['responses']:
                    response_index = self.emoji_vocabulary['responses'].index(emoji)
                    # Ensure index is within bounds
                    if response_index < len(self.action_preferences):
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
        
        logger.debug(f"Emotion context: {emotion_context}")
        logger.debug(f"Action preferences: {self.action_preferences}")
        
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
                logger.debug(f"Emoji {emoji}: action_pref={self.action_preferences[min(i, len(self.action_preferences)-1)]:.3f}, emotion_comp={emotion_compatibility:.3f}, final_score={response_scores[i]:.3f}")
            else:
                # Fallback to action preferences only
                response_scores[i] = self.action_preferences[min(i, len(self.action_preferences)-1)]
                logger.debug(f"Emoji {emoji}: no emotion map, using action_pref={response_scores[i]:.3f}")
        
        # Add some randomness for exploration
        exploration_noise = np.random.normal(0, 0.2, len(response_scores))
        response_scores += exploration_noise
        
        # Boost scores for non-thinking emojis to encourage variety
        for i, emoji in enumerate(self.emoji_vocabulary['responses']):
            if emoji != '❓':  # Boost non-thinking emojis
                response_scores[i] += 0.3
        
        logger.debug(f"Final response scores: {dict(zip(self.emoji_vocabulary['responses'], response_scores))}")
        
        # Use softmax selection instead of argmax for more variety
        response_probs = self.softmax(response_scores, temperature=1.5)  # Higher temperature = more exploration
        selected_response_index = np.random.choice(len(response_scores), p=response_probs)
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