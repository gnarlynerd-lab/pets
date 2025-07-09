"""
Enhanced Free Energy Principle Cognitive System for Digital Pets
Incorporates active inference concepts and attention-based thriving
"""
import numpy as np
import logging
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict
import time
import re
import random

logger = logging.getLogger(__name__)


class EnhancedFEPCognitiveSystem:
    """
    Enhanced Free Energy Principle implementation for digital pets.
    
    Key enhancements:
    - Active inference: Pet actively seeks interactions to minimize surprise
    - Attention-based thriving: Interactions are viewed as positive attention
    - Hierarchical generative models: Multi-level belief updating
    - Contextual response generation: Responses based on pet's internal state
    - Adaptive precision: Learning rate adjusts based on prediction accuracy
    """
    
    def __init__(self, state_size: int = 20, action_size: int = 12):
        """
        Initialize the enhanced FEP cognitive system.
        
        Args:
            state_size: Dimensionality of the state space (expanded for richer context)
            action_size: Number of possible actions (expanded for varied responses)
        """
        self.state_size = state_size
        self.action_size = action_size
        
        # Hierarchical generative model (pet's beliefs about the world)
        self.beliefs = {
            'low_level': np.random.uniform(0, 1, state_size // 2),      # Sensory beliefs
            'high_level': np.random.uniform(0, 1, state_size // 2),     # Abstract beliefs
        }
        
        # Adaptive precision for each belief level
        self.belief_precision = {
            'low_level': np.ones(state_size // 2),
            'high_level': np.ones(state_size // 2),
        }
        
        # Predictive models for each level
        self.predictions = {
            'low_level': np.zeros(state_size // 2),
            'high_level': np.zeros(state_size // 2),
        }
        
        # Prediction errors
        self.prediction_error = {
            'low_level': np.zeros(state_size // 2),
            'high_level': np.zeros(state_size // 2),
        }
        
        # Learning parameters with adaptive rates
        self.learning_rate = {
            'low_level': 0.15,
            'high_level': 0.08,
        }
        self.precision_update_rate = 0.05
        
        # Attention and thriving system
        self.attention_level = 50.0  # 0-100 scale
        self.attention_history = []
        self.thriving_level = 50.0   # 0-100 scale, based on attention and interactions
        self.interaction_count = 0
        self.last_interaction_time = time.time()
        
        # History tracking
        self.surprise_history = []
        self.prediction_accuracy = 0.5
        self.free_energy_history = []
        
        # Enhanced emoji vocabulary with emotional context
        self.emoji_vocabulary = {
            'expressions': ['😊', '😔', '😴', '🤔', '😋', '😆', '😍', '🥰', '😌', '😎'],
            'needs': ['🍎', '🍕', '🎮', '💤', '🤗', '🚿', '🎯', '⚽', '📚', '🎵'],
            'responses': ['❤️', '👍', '👎', '❓', '✨', '🎉', '💔', '😤', '🙏', '👋', '🤗', '🥰'],
            'modifiers': ['❓', '✨', '🔥', '💫', '⭐', '💨', '⚡', '🌟', '💝', '🎊']
        }
        
        # Action preferences with attention-based modulation
        responses_size = len(self.emoji_vocabulary['responses'])
        self.action_preferences = np.random.uniform(0.2, 0.8, responses_size)
        
        # Emoji learning and preferences with attention context
        self.emoji_preferences = defaultdict(float)
        self.emoji_usage_patterns = defaultdict(list)
        self.emoji_surprise_threshold = 0.4
        
        # Multi-modal state representation
        self.state_channels = {
            'traditional': np.zeros(7),      # Original state channels
            'emoji_context': np.zeros(5),    # Emoji communication context
            'user_prefs': np.zeros(3),       # Learned user preferences
            'attention_state': np.zeros(3),  # Attention and thriving state
            'internal_state': np.zeros(2),   # Internal cognitive state
        }
        
        # Enhanced emoji emotion map with attention context
        self.emoji_emotion_map = {
            # Positive attention-seeking emojis (high thriving potential)
            '😊': [0.8, 0.1, 0.7, 0.9],    # happy: high joy, low curiosity, high contentment, high attention
            '😍': [0.9, 0.3, 0.8, 0.95],   # love eyes: very high joy and contentment, some curiosity, very high attention
            '🥰': [0.8, 0.1, 0.9, 0.9],    # loving: high joy, low curiosity, very high contentment, high attention
            '❤️': [0.9, 0.2, 0.9, 0.95],   # love: very high joy and contentment, some curiosity, very high attention
            '🤗': [0.6, 0.1, 0.8, 0.85],   # affectionate: good joy, low curiosity, high contentment, high attention
            
            # Attention-seeking emojis (moderate thriving potential)
            '😋': [0.5, 0.2, 0.3, 0.7],    # hungry but happy: moderate joy, some curiosity, moderate attention
            '😆': [0.9, 0.2, 0.5, 0.8],    # laughing: very high joy, some curiosity, high attention
            '🎉': [0.8, 0.3, 0.6, 0.85],   # celebration: high joy, some curiosity, high attention
            '✨': [0.3, 0.4, 0.3, 0.6],    # sparkle: positive modifier, moderate attention
            
            # Neutral/curious emojis (low-moderate thriving potential)
            '🤔': [0.0, 0.8, 0.1, 0.4],    # thinking: neutral joy, high curiosity, low attention
            '❓': [0.0, 0.9, 0.0, 0.3],    # questioning: neutral joy/content, high curiosity, low attention
            '👋': [0.5, 0.1, 0.4, 0.5],    # waving: moderate joy, low curiosity, moderate attention
            
            # Negative/low attention emojis (low thriving potential)
            '😔': [-0.8, 0.0, -0.5, 0.1],   # sad: negative joy, no curiosity, low contentment, very low attention
            '😴': [0.0, 0.0, 0.9, 0.2],    # sleepy: neutral joy/curiosity, high contentment, low attention
            '👎': [-0.4, 0.0, -0.2, 0.1],   # disapproval: negative response, very low attention
            '💔': [-0.8, 0.0, -0.8, 0.05],  # broken heart: negative joy and contentment, very low attention
            
            # Needs-based emojis (variable attention potential)
            '🍎': [0.1, 0.8, 0.2, 0.6],    # food curiosity: some joy, high curiosity for food, moderate attention
            '🍕': [0.3, 0.7, 0.4, 0.7],    # tasty food: joy + curiosity + some contentment, moderate attention
            '🎮': [0.4, 0.9, 0.3, 0.8],    # playful: moderate joy, very high curiosity, high attention
            '💤': [0.0, 0.0, 0.9, 0.2],    # sleepy: neutral emotions, high contentment, low attention
            
            # Additional response emojis
            '👍': [0.4, 0.0, 0.3, 0.6],    # approval: positive response, moderate attention
            '😤': [-0.3, 0.2, -0.4, 0.2],   # face with steam: slight negative, some curiosity, low attention
            '🙏': [0.3, 0.0, 0.8, 0.5],    # praying: moderate joy, no curiosity, high contentment, moderate attention
            
            # Additional needs emojis
            '🚿': [0.2, 0.1, 0.6, 0.4],    # shower: low joy, low curiosity, moderate contentment, low attention
            '⚽': [0.5, 0.8, 0.4, 0.7],    # soccer: moderate joy, high curiosity, moderate attention
            '📚': [0.2, 0.9, 0.3, 0.5],    # books: low joy, very high curiosity, low contentment, moderate attention
            '🎵': [0.6, 0.3, 0.5, 0.6],    # music: moderate joy, some curiosity, moderate attention
            
            # Additional modifier emojis
            '🔥': [0.7, 0.4, 0.2, 0.7],    # fire: high joy, some curiosity, low contentment, moderate attention
            '💫': [0.4, 0.5, 0.3, 0.5],    # dizzy: moderate joy, high curiosity, low contentment, moderate attention
            '⭐': [0.5, 0.3, 0.4, 0.6],    # star: moderate joy, some curiosity, moderate attention
            '💨': [0.2, 0.6, 0.1, 0.3],    # dashing away: low joy, high curiosity, low contentment, low attention
            '⚡': [0.6, 0.7, 0.2, 0.6],    # lightning: moderate joy, high curiosity, low contentment, moderate attention
            '🌟': [0.6, 0.4, 0.5, 0.7],    # glowing star: moderate joy, some curiosity, moderate attention
            '💝': [0.8, 0.2, 0.8, 0.9],    # heart with ribbon: high joy, low curiosity, high contentment, high attention
            '🎊': [0.8, 0.3, 0.6, 0.85],   # confetti: high joy, some curiosity, moderate contentment, high attention
        }
        
        # Active inference parameters
        self.exploration_rate = 0.3  # How much to explore vs exploit
        self.attention_decay_rate = 0.02  # How quickly attention decays
        self.thriving_growth_rate = 0.05  # How quickly thriving increases with attention
        self.thriving_decay_rate = 0.01   # How quickly thriving decays without attention
        
        logger.info(f"Enhanced FEP cognitive system initialized with attention-based thriving")
        logger.info(f"State size: {state_size}, Action size: {action_size}")
        logger.info(f"Emoji vocabulary size: {sum(len(v) for v in self.emoji_vocabulary.values())}")

    def observe(self, observation: np.ndarray) -> Dict[str, Any]:
        """
        Process an observation and calculate surprise with hierarchical processing.
        
        Args:
            observation: Current observation from the environment
            
        Returns:
            Dict containing surprise, free energy, and hierarchical updates
        """
        # Split observation into low and high level components
        low_level_obs = observation[:self.state_size // 2]
        high_level_obs = observation[self.state_size // 2:]
        
        # Process each level
        low_level_surprise = self._process_level('low_level', low_level_obs)
        high_level_surprise = self._process_level('high_level', high_level_obs)
        
        # Calculate overall surprise and free energy
        total_surprise = (low_level_surprise + high_level_surprise) / 2.0
        free_energy = self._calculate_free_energy()
        
        # Update attention and thriving based on observation
        self._update_attention_from_observation(observation)
        
        # Track history
        self.surprise_history.append(total_surprise)
        self.free_energy_history.append(free_energy)
        
        if len(self.surprise_history) > 100:
            self.surprise_history.pop(0)
        if len(self.free_energy_history) > 100:
            self.free_energy_history.pop(0)
        
        return {
            'surprise': total_surprise,
            'free_energy': free_energy,
            'low_level_surprise': low_level_surprise,
            'high_level_surprise': high_level_surprise,
            'attention_level': self.attention_level,
            'thriving_level': self.thriving_level
        }
    
    def _process_level(self, level: str, observation: np.ndarray) -> float:
        """Process observation at a specific hierarchical level."""
        # Calculate prediction error
        self.prediction_error[level] = observation - self.predictions[level]
        
        # Calculate surprise for this level
        raw_surprise = np.sum(np.square(self.prediction_error[level]) * self.belief_precision[level])
        surprise = 1.0 / (1.0 + np.exp(-raw_surprise + 2.0))
        
        # Update beliefs at this level
        self._update_beliefs_at_level(level, observation)
        
        return surprise
    
    def _update_beliefs_at_level(self, level: str, observation: np.ndarray):
        """Update beliefs at a specific hierarchical level."""
        prediction_error = observation - self.beliefs[level]
        
        # Adaptive learning rate based on prediction accuracy
        recent_accuracy = np.mean(self.surprise_history[-10:]) if self.surprise_history else 0.5
        adaptive_rate = self.learning_rate[level] * (1.0 + (1.0 - recent_accuracy))
        
        # Update beliefs
        self.beliefs[level] += adaptive_rate * prediction_error * self.belief_precision[level]
        self.beliefs[level] = np.clip(self.beliefs[level], 0, 1)
        
        # Update precision
        error_magnitude = np.abs(prediction_error)
        self.belief_precision[level] += self.precision_update_rate * (1.0 - error_magnitude)
        self.belief_precision[level] = np.clip(self.belief_precision[level], 0.1, 2.0)
    
    def _calculate_free_energy(self) -> float:
        """Calculate free energy as a measure of overall cognitive load."""
        total_error = 0
        total_precision = 0
        
        for level in ['low_level', 'high_level']:
            total_error += np.sum(np.square(self.prediction_error[level]))
            total_precision += np.sum(self.belief_precision[level])
        
        # Free energy is precision-weighted prediction error
        free_energy = float(total_error / (total_precision + 1e-6))
        return free_energy
    
    def _update_attention_from_observation(self, observation: np.ndarray):
        """Update attention and thriving based on observation."""
        # Decay attention over time
        time_since_interaction = time.time() - self.last_interaction_time
        attention_decay = self.attention_decay_rate * time_since_interaction / 3600  # Per hour
        self.attention_level = max(0, self.attention_level - attention_decay)
        
        # Update thriving based on attention level
        if self.attention_level > 30:
            # Positive attention increases thriving
            thriving_gain = self.thriving_growth_rate * (self.attention_level / 100.0)
            self.thriving_level = min(100, self.thriving_level + thriving_gain)
        else:
            # Low attention decreases thriving
            self.thriving_level = max(0, self.thriving_level - self.thriving_decay_rate)
        
        # Record attention history
        self.attention_history.append({
            'timestamp': time.time(),
            'attention_level': self.attention_level,
            'thriving_level': self.thriving_level
        })
        
        if len(self.attention_history) > 50:
            self.attention_history.pop(0)
    
    def receive_interaction(self, interaction_type: str, intensity: float = 1.0):
        """
        Process an interaction and update attention/thriving accordingly.
        
        Args:
            interaction_type: Type of interaction (emoji, petting, feeding, etc.)
            intensity: Intensity of the interaction (0-1)
        """
        # Update interaction count and time
        self.interaction_count += 1
        self.last_interaction_time = time.time()
        
        # Calculate attention boost based on interaction type and intensity
        base_attention_boost = 10.0 * intensity
        
        # Different interaction types have different attention values
        attention_multipliers = {
            'emoji': 1.0,
            'petting': 1.5,
            'feeding': 1.2,
            'playing': 1.8,
            'training': 1.3,
            'checking': 0.8,
        }
        
        multiplier = attention_multipliers.get(interaction_type, 1.0)
        attention_boost = base_attention_boost * multiplier
        
        # Apply attention boost with diminishing returns
        if self.attention_level > 80:
            effective_boost = attention_boost * (1.0 - (self.attention_level - 80) / 20)
        else:
            effective_boost = attention_boost
        
        self.attention_level = min(100.0, self.attention_level + effective_boost)
        
        # Thriving increases more with positive interactions
        thriving_boost = attention_boost * 0.5 * intensity
        self.thriving_level = min(100.0, self.thriving_level + thriving_boost)
        
        logger.info(f"Interaction received: {interaction_type} (intensity: {intensity:.2f})")
        logger.info(f"Attention: {self.attention_level:.1f}, Thriving: {self.thriving_level:.1f}")

    def select_action(self, current_state: np.ndarray, use_policy_optimization: bool = True) -> Tuple[int, float]:
        """
        Select action using active inference principles with optional policy optimization.
        
        Args:
            current_state: Current state of the environment
            use_policy_optimization: Whether to use multi-step policy optimization
            
        Returns:
            Tuple of (action_index, confidence)
        """
        if use_policy_optimization:
            return self._select_action_with_policy_optimization(current_state)
        else:
            return self._select_action_greedy(current_state)
    
    def _select_action_greedy(self, current_state: np.ndarray) -> Tuple[int, float]:
        """
        Greedy action selection (original method).
        
        Args:
            current_state: Current state of the environment
            
        Returns:
            Tuple of (action_index, confidence)
        """
        # Calculate expected free energy for each action
        expected_free_energies = []
        
        for action in range(self.action_size):
            # Predict next state for this action
            predicted_state = self._predict_next_state(current_state, action)
            
            # Calculate expected surprise
            expected_surprise = self._calculate_expected_surprise(predicted_state)
            
            # Calculate expected free energy
            expected_fe = expected_surprise - np.log(self.action_preferences[action] + 1e-6)
            expected_free_energies.append(expected_fe)
        
        # Convert to probabilities using softmax
        action_probs = self.softmax(-np.array(expected_free_energies), temperature=1.0)
        
        # Add exploration
        if random.random() < self.exploration_rate:
            # Random action for exploration
            action = random.randint(0, self.action_size - 1)
            confidence = 0.5
        else:
            # Exploit best action
            action = int(np.argmax(action_probs))
            confidence = float(action_probs[action])
        
        return action, confidence
    
    def _select_action_with_policy_optimization(self, current_state: np.ndarray, horizon: int = 3) -> Tuple[int, float]:
        """
        Select action using multi-step policy optimization.
        
        Args:
            current_state: Current state of the environment
            horizon: Planning horizon (number of steps to look ahead)
            
        Returns:
            Tuple of (action_index, confidence)
        """
        # Generate action sequences
        action_sequences = self._generate_action_sequences(horizon)
        
        # Evaluate each sequence
        sequence_evaluations = []
        for sequence in action_sequences:
            evaluation = self._evaluate_action_sequence(current_state, sequence)
            sequence_evaluations.append(evaluation)
        
        # Find best sequence
        best_sequence_idx = int(np.argmax(sequence_evaluations))
        best_sequence = action_sequences[best_sequence_idx]
        best_evaluation = float(sequence_evaluations[best_sequence_idx])
        
        # Return first action from best sequence
        first_action = int(best_sequence[0])
        
        # Calculate confidence based on evaluation quality and exploration
        if random.random() < self.exploration_rate:
            # Add some exploration
            if random.random() < 0.3:  # 30% chance to explore even with policy optimization
                first_action = random.randint(0, self.action_size - 1)
                confidence = 0.6
            else:
                confidence = min(0.9, best_evaluation / 10.0)  # Scale evaluation to confidence
        else:
            confidence = min(0.95, best_evaluation / 8.0)  # Higher confidence for exploitation
        
        return first_action, confidence
    
    def _generate_action_sequences(self, horizon: int, max_sequences: int = 20) -> List[List[int]]:
        """
        Generate possible action sequences for planning.
        
        Args:
            horizon: Planning horizon
            max_sequences: Maximum number of sequences to generate
            
        Returns:
            List of action sequences
        """
        sequences = []
        
        # Generate sequences using different strategies
        strategies = [
            self._generate_greedy_sequences,
            self._generate_exploratory_sequences,
            self._generate_balanced_sequences
        ]
        
        sequences_per_strategy = max_sequences // len(strategies)
        
        for strategy in strategies:
            strategy_sequences = strategy(horizon, sequences_per_strategy)
            sequences.extend(strategy_sequences)
        
        # Ensure we have some diversity
        if len(sequences) < max_sequences:
            additional_sequences = self._generate_random_sequences(horizon, max_sequences - len(sequences))
            sequences.extend(additional_sequences)
        
        return sequences[:max_sequences]
    
    def _generate_greedy_sequences(self, horizon: int, count: int) -> List[List[int]]:
        """Generate sequences focusing on immediate rewards."""
        sequences = []
        for _ in range(count):
            sequence = []
            for _ in range(horizon):
                # Prefer actions with high preferences
                action_probs = self.action_preferences / np.sum(self.action_preferences)
                action = np.random.choice(len(action_probs), p=action_probs)
                sequence.append(action)
            sequences.append(sequence)
        return sequences
    
    def _generate_exploratory_sequences(self, horizon: int, count: int) -> List[List[int]]:
        """Generate sequences with more exploration."""
        sequences = []
        for _ in range(count):
            sequence = []
            for _ in range(horizon):
                # Mix of random and preference-based actions
                if random.random() < 0.6:  # 60% random exploration
                    action = random.randint(0, self.action_size - 1)
                else:
                    action_probs = self.action_preferences / np.sum(self.action_preferences)
                    action = np.random.choice(len(action_probs), p=action_probs)
                sequence.append(action)
            sequences.append(sequence)
        return sequences
    
    def _generate_balanced_sequences(self, horizon: int, count: int) -> List[List[int]]:
        """Generate sequences balancing exploration and exploitation."""
        sequences = []
        for _ in range(count):
            sequence = []
            for _ in range(horizon):
                # Balanced approach
                if random.random() < 0.4:  # 40% random
                    action = random.randint(0, self.action_size - 1)
                else:
                    # Weighted by preferences but with some randomness
                    action_probs = self.action_preferences / np.sum(self.action_preferences)
                    action = np.random.choice(len(action_probs), p=action_probs)
                sequence.append(action)
            sequences.append(sequence)
        return sequences
    
    def _generate_random_sequences(self, horizon: int, count: int) -> List[List[int]]:
        """Generate completely random sequences."""
        sequences = []
        for _ in range(count):
            sequence = [random.randint(0, self.action_size - 1) for _ in range(horizon)]
            sequences.append(sequence)
        return sequences
    
    def _evaluate_action_sequence(self, current_state: np.ndarray, action_sequence: List[int]) -> float:
        """
        Evaluate an action sequence by simulating its execution.
        
        Args:
            current_state: Starting state
            action_sequence: Sequence of actions to evaluate
            
        Returns:
            Evaluation score (higher is better)
        """
        state = current_state.copy()
        total_reward = 0.0
        discount_factor = 0.9  # Future rewards are discounted
        
        for i, action in enumerate(action_sequence):
            # Predict next state
            next_state = self._predict_next_state(state, action)
            
            # Calculate immediate reward
            immediate_reward = self._calculate_immediate_reward(state, action, next_state)
            
            # Apply discount
            discounted_reward = immediate_reward * (discount_factor ** i)
            total_reward += discounted_reward
            
            # Update state for next iteration
            state = next_state
        
        return total_reward
    
    def _calculate_immediate_reward(self, current_state: np.ndarray, action: int, next_state: np.ndarray) -> float:
        """
        Calculate immediate reward for a state-action-state transition.
        
        Args:
            current_state: Current state
            action: Action taken
            next_state: Resulting state
            
        Returns:
            Reward value
        """
        reward = 0.0
        
        # Reward for reducing surprise (active inference principle)
        current_surprise = self._calculate_expected_surprise(current_state)
        next_surprise = self._calculate_expected_surprise(next_state)
        surprise_reduction = current_surprise - next_surprise
        reward += surprise_reduction * 2.0  # Weight surprise reduction heavily
        
        # Reward for attention-seeking behavior (thriving principle)
        if self.attention_level < 50.0:  # Low attention
            # Reward actions that might increase attention
            if action in [0, 1, 2]:  # Assuming these are attention-seeking actions
                reward += 1.0
        
        # Reward for maintaining thriving
        if self.thriving_level > 70.0:  # High thriving
            # Reward actions that maintain high thriving
            if action in [3, 4, 5]:  # Assuming these are thriving-maintaining actions
                reward += 0.5
        
        # Reward for action preference alignment
        if action < len(self.action_preferences):
            preference_bonus = self.action_preferences[action] * 0.3
            reward += preference_bonus
        
        # Penalty for very surprising states
        if next_surprise > 2.0:  # High surprise threshold
            reward -= 1.0
        
        return reward
    
    def _predict_next_state(self, current_state: np.ndarray, action: int) -> np.ndarray:
        """Predict next state given current state and action."""
        # Simple predictive model
        predicted_state = current_state.copy()
        
        # Action effects on different state components
        if action < len(predicted_state):
            predicted_state[action] += 0.1
        
        # Add some noise for uncertainty
        noise = np.random.normal(0, 0.05, len(predicted_state))
        predicted_state += noise
        
        return np.clip(predicted_state, 0, 1)
    
    def _calculate_expected_surprise(self, predicted_state: np.ndarray) -> float:
        """Calculate expected surprise for a predicted state."""
        # Calculate how surprising this state would be given current beliefs
        belief_error = predicted_state - np.concatenate([self.beliefs['low_level'], self.beliefs['high_level']])
        expected_surprise = np.sum(np.square(belief_error))
        return expected_surprise
    
    def process_emoji_interaction(self, emoji_sequence: str, user_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process emoji interaction with enhanced attention-based processing.
        
        Args:
            emoji_sequence: Sequence of emojis from user
            user_context: Additional context about the user
            
        Returns:
            Dict containing response and cognitive state
        """
        # Parse emoji sequence
        emojis = self._parse_emoji_sequence(emoji_sequence)
        
        # Calculate emotional context
        emotional_context = self._calculate_emotional_context(emojis)
        
        # Update attention and thriving based on interaction
        self.receive_interaction('emoji', intensity=emotional_context['attention_potential'])
        
        # Generate response based on current state and emotional context
        response_emoji = self._generate_contextual_response(emotional_context)
        
        # Calculate surprise and update beliefs
        observation = self._create_observation_from_interaction(emotional_context)
        cognitive_update = self.observe(observation)
        
        # Update emoji preferences
        self._update_emoji_preferences(emojis, emotional_context)
        
        return {
            'emoji_response': response_emoji,
            'surprise_level': cognitive_update['surprise'],
            'response_confidence': cognitive_update.get('confidence', 0.5),
            'attention_level': self.attention_level,
            'thriving_level': self.thriving_level,
            'emotional_context': emotional_context,
            'cognitive_state': cognitive_update
        }
    
    def _parse_emoji_sequence(self, emoji_sequence: str) -> List[str]:
        """Parse emoji sequence into individual emojis."""
        # Use regex to match emoji characters
        emoji_pattern = re.compile(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002600-\U000027BF]')
        emojis = emoji_pattern.findall(emoji_sequence)
        return emojis if emojis else [emoji_sequence]
    
    def _calculate_emotional_context(self, emojis: List[str]) -> Dict[str, Any]:
        """Calculate emotional context from emoji sequence."""
        if not emojis:
            return {
                'joy': 0.0,
                'curiosity': 0.0,
                'contentment': 0.0,
                'attention_potential': 0.3,
                'overall_sentiment': 0.0,
                'emoji_count': 0
            }
        
        # Calculate average emotional values
        total_joy = 0.0
        total_curiosity = 0.0
        total_contentment = 0.0
        total_attention = 0.0
        valid_emojis = 0
        
        for emoji in emojis:
            if emoji in self.emoji_emotion_map:
                emotion_vector = self.emoji_emotion_map[emoji]
                total_joy += emotion_vector[0]
                total_curiosity += emotion_vector[1]
                total_contentment += emotion_vector[2]
                total_attention += emotion_vector[3]
                valid_emojis += 1
        
        if valid_emojis == 0:
            return {
                'joy': 0.0,
                'curiosity': 0.0,
                'contentment': 0.0,
                'attention_potential': 0.3,
                'overall_sentiment': 0.0,
                'emoji_count': len(emojis)
            }
        
        avg_joy = total_joy / valid_emojis
        avg_curiosity = total_curiosity / valid_emojis
        avg_contentment = total_contentment / valid_emojis
        avg_attention = total_attention / valid_emojis
        
        # Calculate overall sentiment
        overall_sentiment = (avg_joy + avg_contentment) / 2.0
        
        return {
            'joy': avg_joy,
            'curiosity': avg_curiosity,
            'contentment': avg_contentment,
            'attention_potential': avg_attention,
            'overall_sentiment': overall_sentiment,
            'emoji_count': len(emojis)
        }
    
    def _generate_contextual_response(self, emotional_context: Dict[str, Any]) -> str:
        """Generate contextual multi-emoji response based on pet's state and emotional context."""
        # Get current state
        current_attention = self.attention_level / 100.0
        current_thriving = self.thriving_level / 100.0
        
        # Calculate response probabilities for each emoji category
        response_scores = []
        expression_scores = []
        modifier_scores = []
        
        # Score response emojis
        for i, emoji in enumerate(self.emoji_vocabulary['responses']):
            score = 0.0
            
            # Base preference
            score += self.action_preferences[i] * 0.3
            
            # Attention-based modulation
            if current_attention > 0.7:  # High attention
                if emoji in ['❤️', '🥰', '✨', '🎉']:  # Positive responses
                    score += 0.4
            elif current_attention < 0.3:  # Low attention
                if emoji in ['❓', '👋', '🤗']:  # Attention-seeking responses
                    score += 0.4
            
            # Thriving-based modulation
            if current_thriving > 0.7:  # High thriving
                if emoji in ['❤️', '✨', '🎉', '🥰']:  # Thriving responses
                    score += 0.3
            elif current_thriving < 0.3:  # Low thriving
                if emoji in ['😤', '💔', '👎']:  # Distress responses
                    score += 0.3
            
            # Emotional context modulation
            sentiment = emotional_context['overall_sentiment']
            if sentiment > 0.5:  # Positive user emotion
                if emoji in ['❤️', '🥰', '✨', '🎉']:  # Positive responses
                    score += 0.3
            elif sentiment < -0.3:  # Negative user emotion
                if emoji in ['🤗', '🙏', '👋']:  # Comforting responses
                    score += 0.3
            
            response_scores.append(score)
        
        # Score expression emojis
        for emoji in self.emoji_vocabulary['expressions']:
            score = 0.0
            
            # Match expression to emotional context
            if emotional_context['joy'] > 0.5 and emoji in ['😊', '😍', '🥰', '😆']:
                score += 0.6
            elif emotional_context['joy'] < -0.3 and emoji in ['😔', '💔']:
                score += 0.6
            elif emotional_context['curiosity'] > 0.5 and emoji in ['🤔', '😋']:
                score += 0.5
            elif emotional_context['contentment'] > 0.5 and emoji in ['😌', '😴']:
                score += 0.5
            
            expression_scores.append(score)
        
        # Score modifier emojis
        for emoji in self.emoji_vocabulary['modifiers']:
            score = 0.0
            
            # Add modifiers based on intensity
            if emotional_context['attention_potential'] > 0.7:
                if emoji in ['✨', '🔥', '⚡', '🌟']:  # High energy modifiers
                    score += 0.4
            elif emotional_context['overall_sentiment'] > 0.5:
                if emoji in ['💫', '⭐', '💝', '🎊']:  # Positive modifiers
                    score += 0.3
            
            modifier_scores.append(score)
        
        # Add randomness
        response_scores = np.array(response_scores) + np.random.normal(0, 0.1, len(response_scores))
        expression_scores = np.array(expression_scores) + np.random.normal(0, 0.1, len(expression_scores))
        modifier_scores = np.array(modifier_scores) + np.random.normal(0, 0.1, len(modifier_scores))
        
        # Build multi-emoji response
        response_parts = []
        
        # Add expression (50% chance)
        if random.random() < 0.5 and max(expression_scores) > 0.3:
            expression_index = np.argmax(expression_scores)
            response_parts.append(self.emoji_vocabulary['expressions'][expression_index])
        
        # Add main response
        response_index = np.argmax(response_scores)
        response_parts.append(self.emoji_vocabulary['responses'][response_index])
        
        # Add modifier (30% chance)
        if random.random() < 0.3 and max(modifier_scores) > 0.2:
            modifier_index = np.argmax(modifier_scores)
            response_parts.append(self.emoji_vocabulary['modifiers'][modifier_index])
        
        # Add need-based emoji (20% chance)
        if random.random() < 0.2:
            # Select based on current state
            if current_thriving < 0.4:  # Low thriving - show needs
                needs = ['🍎', '🍕', '🎮', '💤', '🤗']
                response_parts.append(random.choice(needs))
        
        return ''.join(response_parts)
    
    def _create_observation_from_interaction(self, emotional_context: Dict[str, Any]) -> np.ndarray:
        """Create observation vector from emotional context."""
        observation = np.zeros(self.state_size)
        
        # Map emotional context to state space
        observation[0] = emotional_context['joy']
        observation[1] = emotional_context['curiosity']
        observation[2] = emotional_context['contentment']
        observation[3] = emotional_context['attention_potential']
        observation[4] = self.attention_level / 100.0
        observation[5] = self.thriving_level / 100.0
        
        # Add some environmental context
        observation[6] = emotional_context['emoji_count'] / 10.0  # Normalize emoji count
        observation[7] = emotional_context['overall_sentiment']
        
        return observation
    
    def _update_emoji_preferences(self, emojis: List[str], emotional_context: Dict[str, Any]):
        """Update emoji preferences based on interaction."""
        for emoji in emojis:
            if emoji in self.emoji_emotion_map:
                # Update preference based on attention potential
                attention_potential = emotional_context['attention_potential']
                self.emoji_preferences[emoji] += 0.1 * attention_potential
                
                # Record usage pattern
                self.emoji_usage_patterns[emoji].append({
                    'timestamp': time.time(),
                    'attention_potential': attention_potential,
                    'sentiment': emotional_context['overall_sentiment']
                })
                
                # Keep only recent patterns
                if len(self.emoji_usage_patterns[emoji]) > 20:
                    self.emoji_usage_patterns[emoji].pop(0)
    
    @staticmethod
    def softmax(x: np.ndarray, temperature: float = 1.0) -> np.ndarray:
        """Compute softmax probabilities."""
        exp_x = np.exp(x / temperature)
        return exp_x / np.sum(exp_x)
    
    def get_cognitive_state(self) -> Dict[str, Any]:
        """Get current cognitive state."""
        return {
            'attention_level': self.attention_level,
            'thriving_level': self.thriving_level,
            'interaction_count': self.interaction_count,
            'surprise_history': self.surprise_history[-10:],
            'free_energy_history': self.free_energy_history[-10:],
            'prediction_accuracy': self.prediction_accuracy,
            'emoji_preferences': dict(self.emoji_preferences),
            'beliefs': {
                'low_level': self.beliefs['low_level'].tolist(),
                'high_level': self.beliefs['high_level'].tolist()
            }
        }
    
    def get_emoji_usage_stats(self) -> Dict[str, Any]:
        """Get statistics about emoji usage patterns."""
        stats = {
            'total_emojis_used': len(self.emoji_preferences),
            'most_used_emojis': [],
            'recent_usage_patterns': {},
            'preference_strength': {}
        }
        
        # Get most used emojis
        if self.emoji_preferences:
            sorted_emojis = sorted(self.emoji_preferences.items(), key=lambda x: x[1], reverse=True)
            stats['most_used_emojis'] = sorted_emojis[:5]
        
        # Get recent usage patterns
        current_time = time.time()
        for emoji, patterns in self.emoji_usage_patterns.items():
            recent_patterns = [p for p in patterns if current_time - p['timestamp'] < 3600]  # Last hour
            if recent_patterns:
                stats['recent_usage_patterns'][emoji] = len(recent_patterns)
        
        # Get preference strength
        for emoji, preference in self.emoji_preferences.items():
            stats['preference_strength'][emoji] = preference
        
        return stats
    
    def save_state(self) -> Dict[str, Any]:
        """Save current state."""
        return {
            'attention_level': self.attention_level,
            'thriving_level': self.thriving_level,
            'interaction_count': self.interaction_count,
            'last_interaction_time': self.last_interaction_time,
            'attention_history': self.attention_history,
            'surprise_history': self.surprise_history,
            'free_energy_history': self.free_energy_history,
            'prediction_accuracy': self.prediction_accuracy,
            'emoji_preferences': dict(self.emoji_preferences),
            'emoji_usage_patterns': dict(self.emoji_usage_patterns),
            'action_preferences': self.action_preferences.tolist(),
            'beliefs': {
                'low_level': self.beliefs['low_level'].tolist(),
                'high_level': self.beliefs['high_level'].tolist()
            },
            'belief_precision': {
                'low_level': self.belief_precision['low_level'].tolist(),
                'high_level': self.belief_precision['high_level'].tolist()
            }
        }
    
    def load_state(self, state: Dict[str, Any]):
        """Load state from saved data."""
        self.attention_level = state.get('attention_level', 50.0)
        self.thriving_level = state.get('thriving_level', 50.0)
        self.interaction_count = state.get('interaction_count', 0)
        self.last_interaction_time = state.get('last_interaction_time', time.time())
        self.attention_history = state.get('attention_history', [])
        self.surprise_history = state.get('surprise_history', [])
        self.free_energy_history = state.get('free_energy_history', [])
        self.prediction_accuracy = state.get('prediction_accuracy', 0.5)
        
        # Load emoji data
        self.emoji_preferences = defaultdict(float, state.get('emoji_preferences', {}))
        self.emoji_usage_patterns = defaultdict(list, state.get('emoji_usage_patterns', {}))
        
        # Load arrays
        if 'action_preferences' in state:
            self.action_preferences = np.array(state['action_preferences'])
        
        if 'beliefs' in state:
            self.beliefs['low_level'] = np.array(state['beliefs']['low_level'])
            self.beliefs['high_level'] = np.array(state['beliefs']['high_level'])
        
        if 'belief_precision' in state:
            self.belief_precision['low_level'] = np.array(state['belief_precision']['low_level'])
            self.belief_precision['high_level'] = np.array(state['belief_precision']['high_level'])
