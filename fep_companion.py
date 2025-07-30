#!/usr/bin/env python3
"""
FEP-based Companion with attention-seeking for anonymous sessions
"""
import numpy as np
import time
import json
from typing import Dict, Any, Optional
from collections import defaultdict, deque

class FEPAttentionCompanion:
    """
    FEP-based companion that actively seeks to maintain user engagement
    """
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.created_at = time.time()
        
        # FEP Core Components
        self.beliefs = np.random.uniform(0.3, 0.7, 10)  # Beliefs about user state
        self.predictions = np.zeros(10)
        self.prediction_errors = deque(maxlen=20)
        self.surprise_history = deque(maxlen=50)
        
        # Engagement-specific beliefs  
        self.user_engagement_belief = 0.6  # 0=disengaged, 1=highly engaged (start optimistic)
        self.user_response_pattern = deque(maxlen=10)  # Recent response times
        self.successful_attention_strategies = defaultdict(float)
        
        # Attention-seeking parameters
        self.attention_threshold = 0.7  # When to escalate attention-seeking
        self.last_interaction_time = time.time()
        self.interaction_count = 0
        
        # Expanded learned preferences with emoji categories
        self.emoji_effectiveness = {
            # Greetings & Social
            "👋": 0.7, "🤝": 0.6, "👏": 0.7, "🙌": 0.8,
            # Love & Hearts  
            "❤️": 0.9, "💕": 0.8, "💖": 0.8, "🥰": 0.9, "😍": 0.8,
            # Happy & Positive
            "😊": 0.7, "😄": 0.8, "😁": 0.7, "🥳": 0.9, "🎉": 0.8,
            # Thinking & Curious
            "🤔": 0.5, "🧐": 0.5, "💭": 0.4, "❓": 0.6,
            # Food & Fun
            "🍕": 0.6, "🍎": 0.5, "🍰": 0.7, "🎮": 0.7, "🎯": 0.6,
            # Magic & Wonder
            "✨": 0.9, "💫": 0.9, "🌟": 0.8, "🔮": 0.7, "🌈": 0.8,
            # Animals
            "🐱": 0.7, "🐶": 0.8, "🦋": 0.6, "🐨": 0.7,
            # Sleep & Rest
            "😴": 0.3, "💤": 0.2, "🌙": 0.4,
            # Default effectiveness for unknown emojis
            "_default": 0.5
        }
        
        # Expanded response templates for different engagement levels
        self.engagement_responses = {
            "high": ["😊", "❤️", "🎉", "✨", "🥰", "🙌", "😄", "💖", "🌟", "🥳"],
            "medium": ["👋", "😄", "💫", "🌟", "🤗", "😁", "👏", "🎯", "🌈", "💕"],
            "low": ["💫✨", "👋🔔", "❤️", "🌈", "😍", "🥺", "💖", "🌟", "👀", "🦋"],
            "critical": ["🥺👋", "💖", "🌟✨💫", "👀💕", "💔", "🥰", "✨", "🙌", "❤️"]
        }
        
        # Contextual response patterns based on user input
        self.contextual_responses = {
            # If user sends hearts, respond with hearts
            "❤️": ["💖", "💕", "🥰", "😍", "❤️"],
            "💕": ["❤️", "💖", "🥰", "😘", "💗"],
            # If user sends party/celebration, match energy
            "🎉": ["🥳", "🎊", "✨", "🙌", "😄"],
            "🥳": ["🎉", "🎊", "🥰", "😄", "✨"],
            # If user sends greetings, respond warmly
            "👋": ["👋", "😊", "🤗", "😄", "🙌"],
            # Animals get cute responses
            "🐱": ["🥰", "💕", "🐶", "😍", "❤️"],
            "🐶": ["🥰", "💖", "🐱", "😊", "✨"],
            # Food gets playful responses
            "🍕": ["😋", "🤤", "🍎", "😄", "👌"],
            "🍎": ["😊", "💚", "🍕", "😋", "✨"],
            # Magic/wonder gets magical responses
            "✨": ["💫", "🌟", "🔮", "😍", "🥰"],
            "💫": ["✨", "🌟", "🔮", "😊", "💖"],
            "🌟": ["✨", "💫", "🥰", "😍", "🎉"]
        }
    
    def observe_interaction(self, user_emoji: str, response_time: float = None) -> Dict[str, Any]:
        """
        Process user interaction and update FEP beliefs
        """
        current_time = time.time()
        time_since_last = current_time - self.last_interaction_time
        
        # Update interaction tracking
        self.interaction_count += 1
        if response_time:
            self.user_response_pattern.append(response_time)
        
        # Calculate engagement indicators
        engagement_indicators = self._calculate_engagement_indicators(
            user_emoji, time_since_last, response_time
        )
        
        # Update FEP beliefs about user engagement
        surprise = self._update_engagement_beliefs(engagement_indicators)
        
        # Select response based on predicted engagement level and user input
        companion_response = self._select_attention_response(surprise, user_emoji)
        
        # Learn from this interaction
        self._learn_from_interaction(user_emoji, companion_response, surprise)
        
        self.last_interaction_time = current_time
        
        return {
            "companion_response": companion_response,
            "surprise_level": float(surprise),
            "engagement_belief": float(self.user_engagement_belief),
            "attention_strategy": self._get_current_strategy(),
            "response_confidence": 1.0 / (1.0 + surprise)
        }
    
    def _calculate_engagement_indicators(self, user_emoji: str, time_gap: float, response_time: float = None) -> np.ndarray:
        """Calculate features indicating user engagement"""
        indicators = np.zeros(10)
        
        # Time-based indicators
        indicators[0] = 1.0 / (1.0 + time_gap)  # Recent interaction = higher engagement
        indicators[1] = 1.0 if time_gap < 30 else 0.0  # Quick follow-up
        
        # Emoji-based indicators
        positive_emojis = ["👋", "❤️", "😊", "🎉"]
        indicators[2] = 1.0 if user_emoji in positive_emojis else 0.0
        indicators[3] = len(user_emoji) / 5.0  # Length of emoji sequence
        
        # Response pattern indicators
        if self.user_response_pattern:
            avg_response_time = np.mean(self.user_response_pattern)
            indicators[4] = 1.0 / (1.0 + avg_response_time)  # Faster = more engaged
            indicators[5] = 1.0 if len(self.user_response_pattern) >= 3 else 0.0  # Consistent interaction
        
        # Session indicators
        session_duration = time.time() - self.created_at
        indicators[6] = min(session_duration / 300, 1.0)  # Up to 5 minutes
        indicators[7] = min(self.interaction_count / 10, 1.0)  # Interaction frequency
        
        # Trend indicators
        if len(self.surprise_history) >= 3:
            recent_surprise = list(self.surprise_history)[-3:]
            indicators[8] = 1.0 if recent_surprise[-1] < recent_surprise[0] else 0.0  # Decreasing surprise
            indicators[9] = np.std(recent_surprise)  # Surprise variability
        
        return indicators
    
    def _update_engagement_beliefs(self, indicators: np.ndarray) -> float:
        """Update beliefs about user engagement using FEP"""
        # Predict engagement level
        predicted_engagement = np.dot(self.beliefs, indicators)
        
        # Current engagement estimate (simple heuristic)
        current_engagement = np.mean(indicators[:5])  # Focus on key indicators
        
        # Calculate prediction error (surprise)
        prediction_error = current_engagement - predicted_engagement
        surprise = abs(prediction_error)
        
        # Update beliefs (minimize prediction error)
        learning_rate = 0.1
        self.beliefs += learning_rate * prediction_error * indicators
        self.beliefs = np.clip(self.beliefs, 0, 1)  # Keep beliefs bounded
        
        # Update engagement belief
        self.user_engagement_belief = 0.9 * self.user_engagement_belief + 0.1 * current_engagement
        
        # Track surprise
        self.surprise_history.append(surprise)
        
        return surprise
    
    def _select_attention_response(self, surprise: float, user_emoji: str = "") -> str:
        """Select response based on engagement level, surprise, and user input"""
        
        # First, check for contextual responses to user's emoji
        if user_emoji in self.contextual_responses:
            contextual_options = self.contextual_responses[user_emoji]
            # Mix contextual with engagement-based for variety
            responses = contextual_options + self.engagement_responses.get("medium", ["😊"])
        else:
            # Determine engagement level
            if self.user_engagement_belief > 0.7:
                level = "high"
            elif self.user_engagement_belief > 0.4:
                level = "medium" 
            elif self.user_engagement_belief > 0.2:
                level = "low"
            else:
                level = "critical"
            
            # Add surprise-based modulation (reduce threshold)
            if surprise > 0.8:  # Very high surprise - user did something really unexpected
                # Respond with curiosity/attention
                responses = ["👀✨", "😮💫", "🤨", "❓", "🧐"]
            else:
                responses = self.engagement_responses[level]
        
        # Select best response based on learned effectiveness
        response_scores = {}
        for response in responses:
            base_score = self.emoji_effectiveness.get(response, self.emoji_effectiveness.get("_default", 0.5))
            attention_score = self.successful_attention_strategies.get(response, 0.0)
            # Add small random factor for variety
            random_factor = np.random.uniform(-0.1, 0.1)
            response_scores[response] = base_score + attention_score + random_factor
        
        # Select highest scoring response
        best_response = max(response_scores.keys(), key=lambda x: response_scores[x])
        return best_response
    
    def _learn_from_interaction(self, user_emoji: str, companion_response: str, surprise: float):
        """Learn from interaction outcomes"""
        # If user responded quickly after our response, it was effective
        effectiveness = 1.0 / (1.0 + surprise)  # Low surprise = effective
        
        # Update emoji effectiveness
        if companion_response in self.emoji_effectiveness:
            self.emoji_effectiveness[companion_response] = (
                0.9 * self.emoji_effectiveness[companion_response] + 
                0.1 * effectiveness
            )
        
        # Update attention strategies
        strategy = self._get_current_strategy()
        self.successful_attention_strategies[companion_response] += effectiveness * 0.1
    
    def _get_current_strategy(self) -> str:
        """Get current attention-seeking strategy"""
        if self.user_engagement_belief > 0.6:
            return "maintain"
        elif self.user_engagement_belief > 0.3:
            return "gentle_attention"
        else:
            return "active_attention_seeking"
    
    def check_needs_attention(self) -> bool:
        """Check if companion should proactively seek attention"""
        time_since_last = time.time() - self.last_interaction_time
        
        # Need attention if:
        # - User hasn't interacted recently AND engagement is dropping
        # - Or engagement is critically low
        return (
            (time_since_last > 60 and self.user_engagement_belief < 0.5) or
            self.user_engagement_belief < 0.2
        )
    
    def get_proactive_message(self) -> str:
        """Generate proactive attention-seeking message"""
        if self.user_engagement_belief < 0.2:
            return "🥺👋"  # Desperate for attention
        elif self.user_engagement_belief < 0.4:
            return "💫✨"  # Gentle attention seeking
        else:
            return "😊"   # Friendly check-in
    
    def get_state(self) -> Dict[str, Any]:
        """Get current companion state for storage"""
        return {
            "session_id": self.session_id,
            "beliefs": self.beliefs.tolist(),
            "user_engagement_belief": float(self.user_engagement_belief),
            "interaction_count": self.interaction_count,
            "emoji_effectiveness": dict(self.emoji_effectiveness),
            "successful_attention_strategies": dict(self.successful_attention_strategies),
            "surprise_history": list(self.surprise_history),
            "user_response_pattern": list(self.user_response_pattern),
            "last_interaction_time": self.last_interaction_time,
            "created_at": self.created_at
        }
    
    def load_state(self, state: Dict[str, Any]):
        """Load companion state from storage"""
        self.beliefs = np.array(state.get("beliefs", self.beliefs.tolist()))
        self.user_engagement_belief = state.get("user_engagement_belief", 0.5)
        self.interaction_count = state.get("interaction_count", 0)
        self.emoji_effectiveness.update(state.get("emoji_effectiveness", {}))
        self.successful_attention_strategies.update(state.get("successful_attention_strategies", {}))
        self.surprise_history = deque(state.get("surprise_history", []), maxlen=50)
        self.user_response_pattern = deque(state.get("user_response_pattern", []), maxlen=10)
        self.last_interaction_time = state.get("last_interaction_time", time.time())
        self.created_at = state.get("created_at", time.time())