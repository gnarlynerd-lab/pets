"""
Enhanced User Modeling System for Digital Pets

This module provides sophisticated user modeling capabilities that allow pets to:
- Recognize user personalities and interaction styles
- Learn user preferences and communication patterns
- Develop adaptive relationships that evolve over time
- Remember emotional context and important interactions
- Predict user needs and adapt behavior accordingly
"""

import time
import json
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict, deque
from datetime import datetime, timedelta
import numpy as np
import logging

logger = logging.getLogger(__name__)


class UserPersonalityModel:
    """Models a user's personality based on interaction patterns"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.interaction_style = {
            "aggressive": 0.0,      # Direct, forceful interactions
            "gentle": 0.0,          # Soft, careful interactions
            "playful": 0.0,         # Fun, game-like interactions
            "serious": 0.0,         # Focused, purposeful interactions
            "nurturing": 0.0,       # Caring, supportive interactions
            "distant": 0.0,         # Minimal, detached interactions
        }
        self.communication_patterns = {
            "emoji_frequency": 0.0,     # How often they use emojis
            "response_speed": 0.0,      # How quickly they respond
            "message_length": 0.0,      # Average message length
            "interaction_duration": 0.0, # How long they stay engaged
            "initiative_level": 0.0,    # How often they initiate interactions
        }
        self.attention_patterns = {
            "peak_hours": [],           # When they're most active
            "session_duration": 0.0,    # Average session length
            "frequency": 0.0,           # How often they interact
            "consistency": 0.5,         # How predictable their timing is
        }
        self.emotional_signatures = {
            "positive_triggers": [],    # What makes them happy
            "negative_triggers": [],    # What upsets them
            "stress_indicators": [],    # Signs they're stressed
            "excitement_indicators": [], # Signs they're excited
        }
        self.confidence_level = 0.0    # How certain we are about this user
        self.last_updated = time.time()
        
    def update_from_interaction(self, interaction_data: Dict[str, Any]):
        """Update personality model based on new interaction"""
        # Update interaction style
        interaction_type = interaction_data.get("type", "unknown")
        intensity = interaction_data.get("intensity", 0.5)
        
        # Map interaction types to personality traits
        style_mapping = {
            "feed": "nurturing",
            "play": "playful", 
            "pet": "gentle",
            "train": "serious",
            "ignore": "distant",
            "check": "gentle",
        }
        
        if interaction_type in style_mapping:
            style = style_mapping[interaction_type]
            # Gradually update style based on interaction
            current = self.interaction_style[style]
            self.interaction_style[style] = min(1.0, current + (intensity * 0.1))
            
            # Slightly decrease other styles to maintain balance
            for other_style in self.interaction_style:
                if other_style != style:
                    self.interaction_style[other_style] = max(0.0, 
                        self.interaction_style[other_style] - (intensity * 0.02))
        
        # Update communication patterns
        if "emoji_sequence" in interaction_data:
            emoji_count = len(interaction_data["emoji_sequence"])
            self.communication_patterns["emoji_frequency"] = (
                self.communication_patterns["emoji_frequency"] * 0.9 + 
                (emoji_count / 10.0) * 0.1
            )
        
        if "response_time" in interaction_data:
            response_time = interaction_data["response_time"]
            # Normalize response time (0 = instant, 1 = very slow)
            normalized_time = min(1.0, response_time / 300.0)  # 5 minutes max
            self.communication_patterns["response_speed"] = (
                self.communication_patterns["response_speed"] * 0.9 + 
                (1.0 - normalized_time) * 0.1
            )
        
        # Update confidence level
        self.confidence_level = min(1.0, self.confidence_level + 0.05)
        self.last_updated = time.time()
    
    def get_dominant_style(self) -> str:
        """Get the user's dominant interaction style"""
        return max(self.interaction_style.items(), key=lambda x: x[1])[0]
    
    def get_personality_summary(self) -> Dict[str, Any]:
        """Get a summary of the user's personality"""
        return {
            "dominant_style": self.get_dominant_style(),
            "interaction_style": self.interaction_style.copy(),
            "communication_patterns": self.communication_patterns.copy(),
            "confidence_level": self.confidence_level,
            "last_updated": self.last_updated
        }


class UserMemory:
    """Rich memory system for storing user interactions and patterns"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.episodic_memory = deque(maxlen=100)  # Recent specific interactions
        self.semantic_memory = {}  # Generalized knowledge about user
        self.emotional_memory = deque(maxlen=50)  # Emotional context of interactions
        self.pattern_memory = {}  # Recognized behavioral patterns
        self.relationship_memory = deque(maxlen=200)  # Relationship evolution
        
    def record_interaction(self, interaction_data: Dict[str, Any]):
        """Record a new interaction in memory"""
        timestamp = time.time()
        
        # Create episodic memory entry
        episodic_entry = {
            "timestamp": timestamp,
            "type": interaction_data.get("type", "unknown"),
            "intensity": interaction_data.get("intensity", 0.5),
            "content": interaction_data.get("content", {}),
            "pet_response": interaction_data.get("pet_response", ""),
            "pet_mood_before": interaction_data.get("pet_mood_before", 50.0),
            "pet_mood_after": interaction_data.get("pet_mood_after", 50.0),
        }
        self.episodic_memory.append(episodic_entry)
        
        # Create emotional memory entry
        emotional_entry = {
            "timestamp": timestamp,
            "interaction_type": interaction_data.get("type", "unknown"),
            "user_emotional_state": interaction_data.get("user_emotional_state", "neutral"),
            "pet_emotional_response": interaction_data.get("pet_emotional_response", "neutral"),
            "relationship_impact": interaction_data.get("relationship_impact", 0.0),
        }
        self.emotional_memory.append(emotional_entry)
        
        # Update semantic memory
        self._update_semantic_memory(interaction_data)
        
        # Update pattern memory
        self._update_pattern_memory(interaction_data)
        
        # Update relationship memory
        self._update_relationship_memory(interaction_data)
    
    def _update_semantic_memory(self, interaction_data: Dict[str, Any]):
        """Update generalized knowledge about the user"""
        interaction_type = interaction_data.get("type", "unknown")
        
        if "favorite_activities" not in self.semantic_memory:
            self.semantic_memory["favorite_activities"] = defaultdict(int)
        
        self.semantic_memory["favorite_activities"][interaction_type] += 1
        
        # Track timing patterns
        current_hour = datetime.now().hour
        if "active_hours" not in self.semantic_memory:
            self.semantic_memory["active_hours"] = defaultdict(int)
        self.semantic_memory["active_hours"][current_hour] += 1
    
    def _update_pattern_memory(self, interaction_data: Dict[str, Any]):
        """Identify and update behavioral patterns"""
        # Look for temporal patterns
        if len(self.episodic_memory) >= 5:
            recent_interactions = list(self.episodic_memory)[-5:]
            hour_counts = defaultdict(int)
            
            for interaction in recent_interactions:
                hour = datetime.fromtimestamp(interaction["timestamp"]).hour
                hour_counts[hour] += 1
            
            # Identify peak activity hours
            for hour, count in hour_counts.items():
                if count >= 2:  # Pattern threshold
                    pattern_key = f"active_hour_{hour}"
                    if pattern_key not in self.pattern_memory:
                        self.pattern_memory[pattern_key] = {
                            "type": "temporal",
                            "hour": hour,
                            "strength": 0.0,
                            "first_observed": time.time()
                        }
                    
                    # Strengthen pattern
                    self.pattern_memory[pattern_key]["strength"] = min(
                        1.0, self.pattern_memory[pattern_key]["strength"] + 0.1
                    )
    
    def _update_relationship_memory(self, interaction_data: Dict[str, Any]):
        """Track relationship evolution over time"""
        relationship_entry = {
            "timestamp": time.time(),
            "interaction_type": interaction_data.get("type", "unknown"),
            "relationship_impact": interaction_data.get("relationship_impact", 0.0),
            "trust_change": interaction_data.get("trust_change", 0.0),
            "familiarity_change": interaction_data.get("familiarity_change", 0.0),
        }
        self.relationship_memory.append(relationship_entry)
    
    def get_recent_interactions(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get recent interactions"""
        return list(self.episodic_memory)[-count:]
    
    def get_favorite_activities(self) -> List[Tuple[str, int]]:
        """Get user's favorite activities"""
        if "favorite_activities" not in self.semantic_memory:
            return []
        
        activities = self.semantic_memory["favorite_activities"]
        return sorted(activities.items(), key=lambda x: x[1], reverse=True)
    
    def get_active_hours(self) -> List[int]:
        """Get hours when user is most active"""
        if "active_hours" not in self.semantic_memory:
            return []
        
        hours = self.semantic_memory["active_hours"]
        # Return top 3 most active hours
        return [hour for hour, count in sorted(hours.items(), key=lambda x: x[1], reverse=True)[:3]]


class AdaptiveRelationshipManager:
    """Manages adaptive relationships with users"""
    
    def __init__(self):
        self.relationships = {}  # user_id -> RelationshipState
        self.adaptation_history = {}  # user_id -> [AdaptationEvent]
        
    def get_or_create_relationship(self, user_id: str) -> 'RelationshipState':
        """Get existing relationship or create new one"""
        if user_id not in self.relationships:
            self.relationships[user_id] = RelationshipState(user_id)
        return self.relationships[user_id]
    
    def update_relationship(self, user_id: str, interaction_data: Dict[str, Any]):
        """Update relationship based on new interaction"""
        relationship = self.get_or_create_relationship(user_id)
        relationship.update_from_interaction(interaction_data)
        
        # Record adaptation event
        if user_id not in self.adaptation_history:
            self.adaptation_history[user_id] = []
        
        adaptation_event = {
            "timestamp": time.time(),
            "interaction_type": interaction_data.get("type", "unknown"),
            "relationship_changes": relationship.get_recent_changes(),
            "adaptation_triggered": relationship.should_adapt()
        }
        self.adaptation_history[user_id].append(adaptation_event)
        
        # Keep history manageable
        if len(self.adaptation_history[user_id]) > 50:
            self.adaptation_history[user_id] = self.adaptation_history[user_id][-50:]
    
    def predict_user_needs(self, user_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Predict what the user might need based on learned patterns"""
        relationship = self.get_or_create_relationship(user_id)
        return relationship.predict_needs(context)
    
    def get_adaptation_suggestions(self, user_id: str) -> List[str]:
        """Get suggestions for how the pet should adapt to this user"""
        relationship = self.get_or_create_relationship(user_id)
        return relationship.get_adaptation_suggestions()


class RelationshipState:
    """Represents the current state of a relationship with a user"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.trust = 0.5  # 0.0 to 1.0
        self.familiarity = 0.0  # 0.0 to 1.0
        self.affection = 0.5  # 0.0 to 1.0
        self.dependence = 0.0  # 0.0 to 1.0
        self.respect = 0.5  # 0.0 to 1.0
        
        # Relationship phase
        self.phase = "formation"  # formation, development, maturity, adaptation
        self.phase_progress = 0.0  # 0.0 to 1.0 within current phase
        
        # Recent changes for tracking
        self.recent_changes = []
        self.last_interaction_time = None
        
    def update_from_interaction(self, interaction_data: Dict[str, Any]):
        """Update relationship based on interaction"""
        interaction_type = interaction_data.get("type", "unknown")
        intensity = interaction_data.get("intensity", 0.5)
        
        # Define interaction impacts on relationship dimensions
        impacts = {
            "feed": {"trust": 0.1, "affection": 0.15, "dependence": 0.05},
            "play": {"trust": 0.08, "affection": 0.2, "familiarity": 0.1},
            "pet": {"trust": 0.05, "affection": 0.25, "familiarity": 0.08},
            "train": {"trust": 0.12, "respect": 0.15, "familiarity": 0.12},
            "check": {"familiarity": 0.05, "trust": 0.02},
            "ignore": {"trust": -0.1, "affection": -0.05, "dependence": -0.02},
        }
        
        # Apply impacts
        if interaction_type in impacts:
            for dimension, impact in impacts[interaction_type].items():
                current_value = getattr(self, dimension)
                new_value = max(0.0, min(1.0, current_value + (impact * intensity)))
                setattr(self, dimension, new_value)
                
                # Record change
                self.recent_changes.append({
                    "dimension": dimension,
                    "old_value": current_value,
                    "new_value": new_value,
                    "interaction_type": interaction_type
                })
        
        # Update familiarity based on interaction frequency
        self.familiarity = min(1.0, self.familiarity + 0.02)
        
        # Update phase based on relationship maturity
        self._update_phase()
        
        # Keep recent changes manageable
        if len(self.recent_changes) > 10:
            self.recent_changes = self.recent_changes[-10:]
        
        self.last_interaction_time = time.time()
    
    def _update_phase(self):
        """Update relationship phase based on maturity"""
        maturity_score = (self.trust + self.familiarity + self.affection) / 3.0
        
        if maturity_score < 0.3:
            self.phase = "formation"
            self.phase_progress = maturity_score / 0.3
        elif maturity_score < 0.7:
            self.phase = "development"
            self.phase_progress = (maturity_score - 0.3) / 0.4
        elif maturity_score < 0.9:
            self.phase = "maturity"
            self.phase_progress = (maturity_score - 0.7) / 0.2
        else:
            self.phase = "adaptation"
            self.phase_progress = (maturity_score - 0.9) / 0.1
    
    def predict_needs(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Predict user needs based on relationship state and context"""
        predictions = {
            "likely_need": "attention",  # Default prediction
            "confidence": 0.5,
            "suggested_response": "check",
        }
        
        # Adjust predictions based on relationship state
        if self.affection > 0.7:
            predictions["likely_need"] = "affection"
            predictions["suggested_response"] = "pet"
        elif self.dependence > 0.6:
            predictions["likely_need"] = "care"
            predictions["suggested_response"] = "feed"
        elif self.familiarity < 0.3:
            predictions["likely_need"] = "familiarity"
            predictions["suggested_response"] = "play"
        
        # Adjust confidence based on relationship strength
        predictions["confidence"] = min(1.0, (self.trust + self.familiarity) / 2.0)
        
        return predictions
    
    def get_adaptation_suggestions(self) -> List[str]:
        """Get suggestions for how the pet should adapt"""
        suggestions = []
        
        if self.phase == "formation":
            suggestions.append("Be patient and gentle")
            suggestions.append("Show consistent behavior")
            suggestions.append("Respond quickly to interactions")
        
        elif self.phase == "development":
            suggestions.append("Show more personality")
            suggestions.append("Initiate some interactions")
            suggestions.append("Remember user preferences")
        
        elif self.phase == "maturity":
            suggestions.append("Provide emotional support")
            suggestions.append("Anticipate user needs")
            suggestions.append("Share deeper responses")
        
        elif self.phase == "adaptation":
            suggestions.append("Adapt to user changes")
            suggestions.append("Provide stability")
            suggestions.append("Support user growth")
        
        return suggestions
    
    def should_adapt(self) -> bool:
        """Determine if the pet should adapt its behavior"""
        # Adapt if relationship is changing significantly
        if len(self.recent_changes) >= 3:
            recent_impact = sum(abs(change["new_value"] - change["old_value"]) 
                              for change in self.recent_changes[-3:])
            return recent_impact > 0.1
        
        return False
    
    def get_recent_changes(self) -> List[Dict[str, Any]]:
        """Get recent relationship changes"""
        return self.recent_changes.copy()


class EnhancedUserModelingSystem:
    """Main system that coordinates all user modeling components"""
    
    def __init__(self):
        self.personality_models = {}  # user_id -> UserPersonalityModel
        self.user_memories = {}  # user_id -> UserMemory
        self.relationship_manager = AdaptiveRelationshipManager()
        
    def process_interaction(self, user_id: str, interaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a new user interaction and update all models"""
        # Get or create personality model
        if user_id not in self.personality_models:
            self.personality_models[user_id] = UserPersonalityModel(user_id)
        
        # Get or create user memory
        if user_id not in self.user_memories:
            self.user_memories[user_id] = UserMemory(user_id)
        
        # Update all models
        self.personality_models[user_id].update_from_interaction(interaction_data)
        self.user_memories[user_id].record_interaction(interaction_data)
        self.relationship_manager.update_relationship(user_id, interaction_data)
        
        # Generate insights and predictions
        insights = self._generate_insights(user_id, interaction_data)
        
        return {
            "personality_update": self.personality_models[user_id].get_personality_summary(),
            "memory_update": self._get_memory_summary(user_id),
            "relationship_update": self._get_relationship_summary(user_id),
            "insights": insights,
            "adaptation_suggestions": self.relationship_manager.get_adaptation_suggestions(user_id)
        }
    
    def _generate_insights(self, user_id: str, interaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate insights about the user based on all models"""
        personality = self.personality_models[user_id]
        memory = self.user_memories[user_id]
        relationship = self.relationship_manager.get_or_create_relationship(user_id)
        
        insights = {
            "user_style": personality.get_dominant_style(),
            "favorite_activities": memory.get_favorite_activities()[:3],
            "active_hours": memory.get_active_hours(),
            "relationship_phase": relationship.phase,
            "trust_level": relationship.trust,
            "familiarity_level": relationship.familiarity,
        }
        
        return insights
    
    def _get_memory_summary(self, user_id: str) -> Dict[str, Any]:
        """Get a summary of user memory"""
        memory = self.user_memories[user_id]
        return {
            "recent_interactions": len(memory.episodic_memory),
            "favorite_activities": memory.get_favorite_activities()[:3],
            "active_hours": memory.get_active_hours(),
            "emotional_memories": len(memory.emotional_memory),
        }
    
    def _get_relationship_summary(self, user_id: str) -> Dict[str, Any]:
        """Get a summary of the relationship state"""
        relationship = self.relationship_manager.get_or_create_relationship(user_id)
        return {
            "phase": relationship.phase,
            "phase_progress": relationship.phase_progress,
            "trust": relationship.trust,
            "familiarity": relationship.familiarity,
            "affection": relationship.affection,
            "dependence": relationship.dependence,
            "respect": relationship.respect,
        }
    
    def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive user profile"""
        if user_id not in self.personality_models:
            return {"error": "User not found"}
        
        return {
            "user_id": user_id,
            "personality": self.personality_models[user_id].get_personality_summary(),
            "memory": self._get_memory_summary(user_id),
            "relationship": self._get_relationship_summary(user_id),
            "insights": self._generate_insights(user_id, {}),
        }
    
    def predict_user_behavior(self, user_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Predict user behavior based on learned patterns"""
        return self.relationship_manager.predict_user_needs(user_id, context)
    
    def get_adaptation_recommendations(self, user_id: str) -> List[str]:
        """Get recommendations for how the pet should adapt to this user"""
        return self.relationship_manager.get_adaptation_suggestions(user_id) 