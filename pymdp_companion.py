#!/usr/bin/env python3
"""
PyMDP-based Active Inference Companion for contextual emoji communication
"""
import numpy as np
import time
import json
from typing import Dict, Any, List, Optional, Tuple
from collections import defaultdict, deque

# Import pymdp components
try:
    from pymdp import agent, utils, maths
    PYMDP_AVAILABLE = True
except ImportError as e:
    print(f"PyMDP import failed: {e}")
    PYMDP_AVAILABLE = False

class PyMDPEmojiCompanion:
    """
    Active inference companion using pymdp for sophisticated emoji communication
    """
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.created_at = time.time()
        
        if not PYMDP_AVAILABLE:
            raise ImportError("PyMDP is required but not available")
        
        # Emoji vocabulary organized by semantic categories
        self.emoji_categories = {
            'positive_emotion': ['😊', '😄', '🥰', '😍', '🤗', '😌', '😎'],
            'negative_emotion': ['😔', '😤', '💔', '😢', '😞', '😖'],
            'love_affection': ['❤️', '💕', '💖', '💗', '💝', '💘', '🥰'],
            'excitement_celebration': ['🎉', '🥳', '🎊', '✨', '🌟', '💫', '🔥'],
            'curiosity_thinking': ['🤔', '💭', '❓', '🧐', '🔍', '💡'],
            'playful_fun': ['🎮', '⚽', '🎯', '🎵', '🎨', '🎭', '🎪'],
            'food_hunger': ['🍎', '🍕', '🍰', '🍔', '🥑', '🍓', '🥨'],
            'rest_sleep': ['😴', '💤', '🌙', '⭐', '🛌', '🌛'],
            'nature_beauty': ['🌸', '🦋', '🌈', '🌺', '🌹', '🌻', '🍃'],
            'social_greeting': ['👋', '🤝', '👏', '🙌', '👍', '👎', '🙏']
        }
        
        # Flatten for easy lookup
        self.all_emojis = []
        self.emoji_to_category = {}
        for category, emojis in self.emoji_categories.items():
            for emoji in emojis:
                self.all_emojis.append(emoji)
                self.emoji_to_category[emoji] = category
        
        # Active inference model setup
        self.setup_generative_model()
        
        # Conversation state
        self.conversation_history = deque(maxlen=20)
        self.user_preferences = defaultdict(float)
        self.context_memory = deque(maxlen=10)
        
        # Learning parameters
        self.learning_rate = 0.1
        self.surprise_threshold = 0.6
        
        print(f"Initialized PyMDP emoji companion with {len(self.all_emojis)} emojis across {len(self.emoji_categories)} categories")
    
    def setup_generative_model(self):
        """
        Set up the generative model for active inference
        """
        # State space dimensions
        self.num_emoji_states = len(self.all_emojis)  # Possible emoji responses
        self.num_context_states = len(self.emoji_categories)  # Conversation contexts
        self.num_relationship_states = 5  # relationship depth levels
        
        # Observation space
        self.num_user_emoji_obs = len(self.all_emojis)  # User can send any emoji
        self.num_timing_obs = 3  # fast, medium, slow response
        
        # Action space (companion's emoji responses)
        self.num_actions = len(self.all_emojis)
        
        # Initialize beliefs (prior preferences)
        self.init_beliefs()
        
        # Transition matrices (how states evolve)
        self.setup_transition_matrices()
        
        # Observation matrices (how observations relate to states)
        self.setup_observation_matrices()
        
        # Preferences (what outcomes the companion prefers)
        self.setup_preferences()
    
    @staticmethod
    def norm(x):
        """Normalize array to sum to 1"""
        return x / np.sum(x)
    
    @staticmethod
    def softmax(x, temperature=1.0):
        """Compute softmax probabilities"""
        exp_x = np.exp((x - np.max(x)) / temperature)
        return exp_x / np.sum(exp_x)
    
    def init_beliefs(self):
        """Initialize prior beliefs about states"""
        # Context beliefs - start neutral
        self.context_beliefs = self.norm(np.ones(self.num_context_states))
        
        # Relationship beliefs - start at low intimacy
        relationship_prior = np.array([0.6, 0.3, 0.1, 0.0, 0.0])  # Weighted toward casual interaction
        self.relationship_beliefs = self.norm(relationship_prior)
        
        # Emoji state beliefs - slight preference for positive emojis
        emoji_prior = np.ones(self.num_emoji_states)
        for i, emoji in enumerate(self.all_emojis):
            category = self.emoji_to_category[emoji]
            if category in ['positive_emotion', 'love_affection', 'social_greeting']:
                emoji_prior[i] *= 1.5
        self.emoji_beliefs = self.norm(emoji_prior)
    
    def setup_transition_matrices(self):
        """Setup state transition dynamics"""
        # Context transitions - contexts can shift based on conversation flow
        self.A_context = np.eye(self.num_context_states) * 0.8  # Tendency to stay in context
        # Add small probabilities for context shifts
        self.A_context += (np.ones((self.num_context_states, self.num_context_states)) - np.eye(self.num_context_states)) * 0.02
        
        # Relationship transitions - relationships can deepen over time
        self.A_relationship = np.eye(self.num_relationship_states) * 0.9
        # Allow progression to deeper relationship states
        for i in range(self.num_relationship_states - 1):
            self.A_relationship[i, i+1] = 0.1
    
    def setup_observation_matrices(self):
        """Setup observation model - how states generate observations"""
        # User emoji observations depend on context
        self.B_user_emoji = np.zeros((self.num_user_emoji_obs, self.num_context_states))
        
        for context_idx, (context, emojis) in enumerate(self.emoji_categories.items()):
            for emoji in emojis:
                if emoji in self.all_emojis:
                    emoji_idx = self.all_emojis.index(emoji)
                    self.B_user_emoji[emoji_idx, context_idx] = 1.0 / len(emojis)
        
        # Normalize
        for i in range(self.B_user_emoji.shape[1]):
            col_sum = np.sum(self.B_user_emoji[:, i])
            if col_sum > 0:
                self.B_user_emoji[:, i] /= col_sum
        
        # Timing observations - relationship affects response timing
        self.B_timing = np.array([
            [0.1, 0.3, 0.5, 0.7, 0.9],  # fast response probability by relationship level
            [0.6, 0.5, 0.4, 0.3, 0.1],  # medium response
            [0.3, 0.2, 0.1, 0.0, 0.0]   # slow response
        ])
        # Normalize columns
        for i in range(self.B_timing.shape[1]):
            col_sum = np.sum(self.B_timing[:, i])
            if col_sum > 0:
                self.B_timing[:, i] /= col_sum
    
    def setup_preferences(self):
        """Setup preferences - what the companion wants to achieve"""
        # Prefer contexts that indicate engagement
        self.C_context = np.array([0.8, 0.2, 1.0, 0.9, 0.7, 0.8, 0.5, 0.3, 0.6, 0.9])  # Excitement, love, play are preferred
        
        # Prefer deeper relationships over time
        self.C_relationship = np.array([0.2, 0.4, 0.6, 0.8, 1.0])
        
        # Slightly prefer positive emoji responses
        self.C_emoji = np.ones(self.num_emoji_states) * 0.5
        for i, emoji in enumerate(self.all_emojis):
            category = self.emoji_to_category[emoji]
            if category in ['positive_emotion', 'love_affection', 'excitement_celebration']:
                self.C_emoji[i] = 0.8
            elif category in ['playful_fun', 'social_greeting']:
                self.C_emoji[i] = 0.7
    
    def encode_user_input(self, user_emoji: str, response_time: float = None) -> Tuple[int, int]:
        """Encode user input into observation indices"""
        # Emoji observation
        if user_emoji in self.all_emojis:
            emoji_obs = self.all_emojis.index(user_emoji)
        else:
            # Default to first positive emoji if unknown
            emoji_obs = self.all_emojis.index('😊')
        
        # Timing observation
        if response_time is None:
            timing_obs = 1  # medium
        elif response_time < 5:
            timing_obs = 0  # fast
        elif response_time > 30:
            timing_obs = 2  # slow
        else:
            timing_obs = 1  # medium
            
        return emoji_obs, timing_obs
    
    def update_beliefs(self, user_emoji_obs: int, timing_obs: int) -> Dict[str, float]:
        """Update beliefs based on observations using active inference"""
        
        # Create observation vector
        obs_emoji = np.zeros(self.num_user_emoji_obs)
        obs_emoji[user_emoji_obs] = 1.0
        
        obs_timing = np.zeros(3)
        obs_timing[timing_obs] = 1.0
        
        # Update context beliefs using observation
        context_likelihood = self.B_user_emoji[user_emoji_obs, :]
        self.context_beliefs = self.norm(self.context_beliefs * context_likelihood)
        
        # Update relationship beliefs using timing observation
        relationship_likelihood = self.B_timing[timing_obs, :]
        self.relationship_beliefs = self.norm(self.relationship_beliefs * relationship_likelihood)
        
        # Calculate surprise (simple entropy-based measure)
        uniform_context = self.norm(np.ones(self.num_context_states))
        uniform_relationship = self.norm(np.ones(self.num_relationship_states))
        
        context_surprise = -np.sum(self.context_beliefs * np.log(self.context_beliefs + 1e-16)) + np.sum(uniform_context * np.log(uniform_context + 1e-16))
        relationship_surprise = -np.sum(self.relationship_beliefs * np.log(self.relationship_beliefs + 1e-16)) + np.sum(uniform_relationship * np.log(uniform_relationship + 1e-16))
        
        total_surprise = float(context_surprise + relationship_surprise)
        
        return {
            'context_surprise': float(context_surprise),
            'relationship_surprise': float(relationship_surprise),
            'total_surprise': total_surprise,
            'context_beliefs': self.context_beliefs.tolist(),
            'relationship_beliefs': self.relationship_beliefs.tolist()
        }
    
    def select_response_emoji(self) -> Tuple[str, float]:
        """Select emoji response using active inference action selection"""
        
        # Calculate expected free energy for each possible emoji response
        action_values = np.zeros(self.num_actions)
        
        for action_idx, emoji in enumerate(self.all_emojis):
            # Pragmatic value - how well does this emoji fit the current context?
            emoji_category = self.emoji_to_category[emoji]
            category_idx = list(self.emoji_categories.keys()).index(emoji_category)
            
            pragmatic_value = self.context_beliefs[category_idx]
            
            # Epistemic value - does this emoji help us learn about the user?
            # (For simplicity, use uniform epistemic value)
            epistemic_value = 0.1
            
            # Preference value - do we intrinsically prefer this emoji?
            preference_value = self.C_emoji[action_idx]
            
            # Combine values (expected free energy minimization)
            action_values[action_idx] = pragmatic_value + epistemic_value + preference_value
        
        # Add learned user preferences
        for i, emoji in enumerate(self.all_emojis):
            action_values[i] += self.user_preferences[emoji] * 0.5
        
        # Add exploration noise
        action_values += np.random.normal(0, 0.1, len(action_values))
        
        # Softmax selection for stochastic choice
        action_probs = self.softmax(action_values)
        selected_action = np.random.choice(self.num_actions, p=action_probs)
        confidence = action_probs[selected_action]
        
        selected_emoji = self.all_emojis[selected_action]
        
        return selected_emoji, float(confidence)
    
    def observe_interaction(self, user_emoji: str, response_time: float = None) -> Dict[str, Any]:
        """Process user interaction and generate response using active inference"""
        
        # Encode observations
        emoji_obs, timing_obs = self.encode_user_input(user_emoji, response_time)
        
        # Update beliefs
        belief_update = self.update_beliefs(emoji_obs, timing_obs)
        
        # Select response
        companion_emoji, confidence = self.select_response_emoji()
        
        # Update conversation history
        interaction = {
            'user_emoji': user_emoji,
            'companion_emoji': companion_emoji,
            'timestamp': time.time(),
            'surprise': belief_update['total_surprise'],
            'confidence': confidence
        }
        self.conversation_history.append(interaction)
        
        # Learn user preferences
        self.user_preferences[user_emoji] += self.learning_rate
        
        # Update context memory
        user_category = self.emoji_to_category.get(user_emoji, 'unknown')
        self.context_memory.append(user_category)
        
        return {
            'companion_response': companion_emoji,
            'surprise_level': belief_update['total_surprise'],
            'response_confidence': confidence,
            'engagement_belief': float(np.max(self.context_beliefs)),
            'relationship_depth': float(np.argmax(self.relationship_beliefs)),
            'context_distribution': belief_update['context_beliefs'],
            'relationship_distribution': belief_update['relationship_beliefs'],
            'active_inference_stats': {
                'context_surprise': belief_update['context_surprise'],
                'relationship_surprise': belief_update['relationship_surprise']
            }
        }
    
    def get_state(self) -> Dict[str, Any]:
        """Get current companion state for storage"""
        return {
            'session_id': self.session_id,
            'context_beliefs': self.context_beliefs.tolist(),
            'relationship_beliefs': self.relationship_beliefs.tolist(),
            'emoji_beliefs': self.emoji_beliefs.tolist(),
            'user_preferences': dict(self.user_preferences),
            'conversation_history': list(self.conversation_history),
            'context_memory': list(self.context_memory),
            'created_at': self.created_at,
            'last_interaction_time': time.time()
        }
    
    def load_state(self, state: Dict[str, Any]):
        """Load companion state from storage"""
        self.context_beliefs = np.array(state.get('context_beliefs', self.context_beliefs))
        self.relationship_beliefs = np.array(state.get('relationship_beliefs', self.relationship_beliefs))  
        self.emoji_beliefs = np.array(state.get('emoji_beliefs', self.emoji_beliefs))
        self.user_preferences.update(state.get('user_preferences', {}))
        self.conversation_history = deque(state.get('conversation_history', []), maxlen=20)
        self.context_memory = deque(state.get('context_memory', []), maxlen=10)
        self.created_at = state.get('created_at', time.time())

if __name__ == "__main__":
    # Test the system
    companion = PyMDPEmojiCompanion("test_session")
    
    # Test interaction
    result = companion.observe_interaction("❤️", 5.0)
    print(f"User sent ❤️, companion responds: {result['companion_response']}")
    print(f"Surprise level: {result['surprise_level']:.3f}")
    print(f"Confidence: {result['response_confidence']:.3f}")