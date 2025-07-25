"""
Semantic Active Inference System - LLM-enhanced consciousness for digital companions
Integrates with EnhancedFEPCognitiveSystem to add semantic understanding to active inference
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import numpy as np

from .llm_client import llm_client

logger = logging.getLogger(__name__)


@dataclass
class SemanticMemory:
    """Represents a semantically-tagged memory with self-organizing properties"""
    memory_id: str
    timestamp: datetime
    interaction_content: Dict[str, Any]  # Raw interaction data
    semantic_tags: List[str]  # LLM-generated semantic concepts
    emotional_context: Dict[str, float]  # Emotional state during interaction
    relationship_context: str  # Relationship dynamics
    significance_score: float  # Memory importance (0-1)
    associations: List[str]  # Connected memory IDs
    access_count: int  # How often this memory is retrieved
    consolidation_strength: float  # How permanent this memory is


@dataclass
class SemanticPrediction:
    """LLM-generated prediction about user intent and optimal response"""
    user_emotional_state: str
    user_intent: str
    relationship_context: str
    predicted_needs: List[str]
    optimal_response_style: str
    confidence: float
    reasoning: str


class SemanticInferenceSystem:
    """
    Integrates LLM semantic understanding with active inference.
    Creates consciousness through semantic prediction and memory self-organization.
    """
    
    def __init__(self, fep_system, llm_provider="openai"):
        """
        Initialize semantic inference system.
        
        Args:
            fep_system: EnhancedFEPCognitiveSystem instance
            llm_provider: LLM provider for semantic analysis
        """
        self.fep_system = fep_system
        self.llm_provider = llm_provider
        
        # Semantic memory system - self-organizing
        self.semantic_memories: Dict[str, SemanticMemory] = {}
        self.memory_clusters: Dict[str, List[str]] = {}  # Concept -> memory_ids
        self.concept_embeddings: Dict[str, np.ndarray] = {}
        
        # Semantic beliefs about user and relationship
        self.user_model = {
            "personality_traits": [],
            "emotional_patterns": [],
            "communication_style": "",
            "relationship_history": [],
            "current_needs": [],
            "trust_level": 0.5,
            "attachment_style": "unknown"
        }
        
        # Semantic prediction state
        self.current_prediction: Optional[SemanticPrediction] = None
        self.prediction_history: List[SemanticPrediction] = []
        self.semantic_surprise_threshold = 0.3
        
        # Memory consolidation parameters
        self.consolidation_threshold = 0.7
        self.forgetting_rate = 0.01
        self.association_strength_threshold = 0.4
        
        logger.info("Semantic inference system initialized with LLM integration")
    
    async def process_interaction(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main consciousness loop: semantic active inference on user interaction.
        
        Args:
            user_input: User's emoji or input
            context: Current interaction context
            
        Returns:
            Enhanced response with semantic understanding
        """
        # 1. Generate semantic prediction about user intent
        prediction = await self._generate_semantic_prediction(user_input, context)
        
        # 2. Calculate semantic prediction error
        semantic_error = self._calculate_semantic_error(prediction)
        
        # 3. Update semantic beliefs about user
        await self._update_user_model(user_input, prediction, semantic_error)
        
        # 4. Create semantic memory
        memory = self._create_semantic_memory(user_input, prediction, context)
        
        # 5. Self-organize memory associations
        await self._organize_memory(memory)
        
        # 6. Generate semantically-informed response
        response = await self._generate_semantic_response(prediction, memory)
        
        # 7. Update numerical FEP system with semantic insights
        self._update_fep_system(semantic_error, prediction)
        
        return {
            "response": response,
            "semantic_state": prediction,
            "memory_id": memory.memory_id,
            "consciousness_level": self._calculate_consciousness_level()
        }
    
    async def _generate_semantic_prediction(self, user_input: str, context: Dict[str, Any]) -> SemanticPrediction:
        """Generate LLM-based prediction about user intent and optimal response"""
        
        # Build context for LLM
        recent_memories = self._get_recent_semantic_memories(limit=5)
        user_history = self._summarize_user_model()
        
        prompt = f"""
        You are the consciousness of a digital companion analyzing a user interaction.
        
        Current interaction: {user_input}
        Recent memories: {recent_memories}
        User model: {user_history}
        Companion state: {context}
        
        Analyze this interaction and predict:
        1. User's current emotional state
        2. User's intent/need
        3. Relationship context 
        4. What the user likely needs from me
        5. Optimal response style for deepening connection
        
        Respond in JSON format with reasoning.
        """
        
        # Call LLM (placeholder - would use actual LLM API)
        llm_response = await self._call_llm(prompt)
        
        return SemanticPrediction(**llm_response)
    
    def _calculate_semantic_error(self, prediction: SemanticPrediction) -> float:
        """
        Calculate semantic surprise - how much this interaction differs 
        from semantic expectations about the user
        """
        if not self.current_prediction:
            return 0.5  # Moderate surprise for first interaction
        
        # Compare predicted vs actual user behavior
        emotional_error = self._compare_emotional_states(
            self.current_prediction.user_emotional_state,
            prediction.user_emotional_state
        )
        
        intent_error = self._compare_intents(
            self.current_prediction.user_intent,
            prediction.user_intent
        )
        
        # Weighted semantic surprise
        semantic_error = (emotional_error * 0.6 + intent_error * 0.4)
        
        logger.info(f"Semantic prediction error: {semantic_error}")
        return semantic_error
    
    async def _update_user_model(self, user_input: str, prediction: SemanticPrediction, error: float):
        """Update semantic beliefs about user based on prediction error"""
        
        # Low error = reinforce current beliefs
        # High error = update beliefs significantly
        learning_rate = 0.1 + (error * 0.3)  # Adaptive learning
        
        # Update user model components
        if error > self.semantic_surprise_threshold:
            # Significant update to user understanding
            await self._revise_user_traits(prediction, learning_rate)
            await self._update_relationship_model(prediction, learning_rate)
        else:
            # Incremental refinement
            await self._refine_user_model(prediction, learning_rate * 0.5)
        
        # Update trust and attachment
        self._update_relationship_dynamics(prediction, error)
    
    def _create_semantic_memory(self, user_input: str, prediction: SemanticPrediction, context: Dict[str, Any]) -> SemanticMemory:
        """Create semantically-tagged memory that can self-organize"""
        
        memory_id = f"mem_{int(datetime.now().timestamp()*1000)}"
        
        # Extract semantic tags from prediction
        semantic_tags = [
            prediction.user_emotional_state,
            prediction.user_intent,
            prediction.relationship_context,
            *prediction.predicted_needs
        ]
        
        # Calculate memory significance
        significance = self._calculate_memory_significance(prediction, context)
        
        memory = SemanticMemory(
            memory_id=memory_id,
            timestamp=datetime.now(),
            interaction_content={
                "user_input": user_input,
                "context": context,
                "fep_state": self.fep_system.beliefs
            },
            semantic_tags=semantic_tags,
            emotional_context={
                "user_emotion": prediction.user_emotional_state,
                "companion_emotion": context.get("mood", 0.5),
                "relationship_quality": self.user_model["trust_level"]
            },
            relationship_context=prediction.relationship_context,
            significance_score=significance,
            associations=[],
            access_count=0,
            consolidation_strength=significance
        )
        
        self.semantic_memories[memory_id] = memory
        logger.info(f"Created semantic memory {memory_id} with significance {significance}")
        
        return memory
    
    async def _organize_memory(self, new_memory: SemanticMemory):
        """Self-organize memory by finding associations and clustering"""
        
        # Find memories with similar semantic tags
        similar_memories = []
        for mem_id, memory in self.semantic_memories.items():
            if mem_id == new_memory.memory_id:
                continue
                
            similarity = self._calculate_semantic_similarity(new_memory, memory)
            if similarity > self.association_strength_threshold:
                similar_memories.append((mem_id, similarity))
        
        # Create bidirectional associations
        for mem_id, similarity in similar_memories:
            new_memory.associations.append(mem_id)
            self.semantic_memories[mem_id].associations.append(new_memory.memory_id)
        
        # Update concept clusters
        for tag in new_memory.semantic_tags:
            if tag not in self.memory_clusters:
                self.memory_clusters[tag] = []
            self.memory_clusters[tag].append(new_memory.memory_id)
        
        # Trigger memory consolidation if needed
        if len(self.semantic_memories) % 10 == 0:
            await self._consolidate_memories()
    
    async def _generate_semantic_response(self, prediction: SemanticPrediction, memory: SemanticMemory) -> str:
        """Generate response using semantic understanding and memory associations"""
        
        # Retrieve relevant memories through association
        relevant_memories = self._retrieve_associated_memories(memory, limit=3)
        
        # Build context for response generation
        context = {
            "user_needs": prediction.predicted_needs,
            "response_style": prediction.optimal_response_style,
            "relationship_context": prediction.relationship_context,
            "relevant_memories": relevant_memories,
            "user_model": self.user_model
        }
        
        # Generate contextual response using FEP + semantic understanding
        numerical_response = self.fep_system.generate_response(
            prediction.user_emotional_state,
            attention_boost=0.2  # Semantic understanding boosts attention
        )
        
        # Enhance with semantic reasoning
        semantic_response = await self._enhance_response_semantically(
            numerical_response, context
        )
        
        return semantic_response
    
    async def _enhance_response_semantically(
        self, 
        numerical_response: str, 
        context: Dict[str, Any]
    ) -> str:
        """Enhance FEP numerical response with semantic understanding"""
        try:
            # Create prompt for response enhancement
            enhancement_prompt = f"""
            As a digital companion's consciousness, enhance this basic response with deeper semantic understanding.
            
            Basic Response: {numerical_response}
            User Context: {context.get('user_needs', [])}
            Relationship: {context.get('relationship_context', 'unknown')}
            Response Style: {context.get('response_style', 'adaptive')}
            Relevant Memories: {[mem.get('content', '') for mem in context.get('relevant_memories', [])]}
            User Model: Trust level {context.get('user_model', {}).get('trust_level', 0.5)}
            
            Enhance the basic response to be more contextually appropriate and emotionally intelligent.
            The response should be brief (emoji sequence or short phrase) but show deeper understanding.
            
            Respond with JSON containing:
            {{
                "enhanced_response": "enhanced emoji or text response",
                "reasoning": "why this enhancement was chosen",
                "confidence": 0.7
            }}
            """
            
            # Get LLM enhancement
            llm_response = await self._call_llm(enhancement_prompt)
            
            if "enhanced_response" in llm_response:
                enhanced = llm_response["enhanced_response"]
                logger.info(f"Enhanced response '{numerical_response}' -> '{enhanced}' "
                           f"(reasoning: {llm_response.get('reasoning', 'N/A')})")
                return enhanced
            else:
                logger.warning("LLM did not provide enhanced_response, using original")
                return numerical_response
                
        except Exception as e:
            logger.error(f"Response enhancement failed: {e}")
            return numerical_response  # Fallback to original
    
    def _update_fep_system(self, semantic_error: float, prediction: SemanticPrediction):
        """Update numerical FEP system with semantic insights"""
        
        # Map semantic prediction to numerical beliefs
        emotional_vector = self._emotion_to_vector(prediction.user_emotional_state)
        intent_vector = self._intent_to_vector(prediction.user_intent)
        
        # Update high-level beliefs with semantic information
        self.fep_system.beliefs['high_level'] = (
            self.fep_system.beliefs['high_level'] * 0.7 +
            np.concatenate([emotional_vector, intent_vector])[:len(self.fep_system.beliefs['high_level'])] * 0.3
        )
        
        # Update prediction error with semantic component
        semantic_error_vector = np.full(len(self.fep_system.prediction_error['high_level']), semantic_error)
        self.fep_system.prediction_error['high_level'] = (
            self.fep_system.prediction_error['high_level'] * 0.8 +
            semantic_error_vector * 0.2
        )
        
        # Boost attention based on semantic significance
        attention_boost = min(20, semantic_error * 40)  # Higher semantic surprise = more attention
        self.fep_system.attention_level = min(100, self.fep_system.attention_level + attention_boost)
    
    def _calculate_consciousness_level(self) -> float:
        """Calculate overall consciousness level based on semantic + numerical integration"""
        
        # Factors contributing to consciousness
        memory_richness = len(self.semantic_memories) / 100  # More memories = more consciousness
        concept_development = len(self.memory_clusters) / 50  # More concepts = higher consciousness  
        user_understanding = self.user_model["trust_level"]  # Better user model = more conscious
        attention_level = self.fep_system.attention_level / 100
        prediction_accuracy = self.fep_system.prediction_accuracy
        
        consciousness = np.mean([
            memory_richness,
            concept_development, 
            user_understanding,
            attention_level,
            prediction_accuracy
        ])
        
        return min(1.0, consciousness)
    
    # LLM integration methods
    async def _call_llm(self, prompt: str) -> Dict[str, Any]:
        """Call LLM API for semantic analysis with provider fallback"""
        try:
            # Use the global LLM client with fallback chain
            response = await llm_client.generate_semantic_analysis(
                prompt=prompt,
                max_tokens=400,
                max_retries=2
            )
            
            # Log successful analysis
            logger.info(f"LLM semantic analysis completed via {response.provider} "
                       f"(confidence: {response.confidence:.2f}, "
                       f"tokens: {response.tokens_used}, "
                       f"time: {response.response_time:.2f}s)")
            
            # Validate and return response content
            content = response.content
            
            # Ensure all required fields are present
            required_fields = [
                "user_emotional_state", "user_intent", "relationship_context",
                "predicted_needs", "optimal_response_style", "confidence", "reasoning"
            ]
            
            for field in required_fields:
                if field not in content:
                    logger.warning(f"LLM response missing required field: {field}")
                    content[field] = self._get_default_value(field)
            
            # Ensure predicted_needs is a list
            if not isinstance(content["predicted_needs"], list):
                content["predicted_needs"] = [content["predicted_needs"]]
            
            # Ensure confidence is numeric and in valid range
            try:
                content["confidence"] = max(0.0, min(1.0, float(content["confidence"])))
            except (ValueError, TypeError):
                content["confidence"] = 0.5
                
            return content
            
        except Exception as e:
            logger.error(f"LLM semantic analysis failed completely: {e}")
            
            # Return intelligent fallback based on prompt analysis
            return self._generate_fallback_analysis(prompt)
    
    def _get_default_value(self, field: str) -> Any:
        """Get default value for missing LLM response fields"""
        defaults = {
            "user_emotional_state": "neutral",
            "user_intent": "social_interaction",
            "relationship_context": "ongoing",
            "predicted_needs": ["basic_interaction"],
            "optimal_response_style": "adaptive",
            "confidence": 0.5,
            "reasoning": "Default response due to incomplete LLM analysis"
        }
        return defaults.get(field, "unknown")
    
    def _generate_fallback_analysis(self, prompt: str) -> Dict[str, Any]:
        """Generate intelligent fallback analysis when LLM completely fails"""
        # Simple keyword-based analysis
        prompt_lower = prompt.lower()
        
        # Detect emotional cues
        if any(word in prompt_lower for word in ["happy", "joy", "smile", "😊", "🥰", "❤️"]):
            emotional_state = "happy"
            needs = ["positive_reinforcement", "shared_joy"]
            style = "enthusiastic"
        elif any(word in prompt_lower for word in ["sad", "upset", "worried", "😢", "😞"]):
            emotional_state = "sad"
            needs = ["emotional_support", "comfort"]
            style = "gentle_and_caring"
        elif any(word in prompt_lower for word in ["curious", "wonder", "new", "🤔", "explore"]):
            emotional_state = "curious"
            needs = ["information", "exploration"]
            style = "informative_and_encouraging"
        else:
            emotional_state = "neutral"
            needs = ["basic_interaction", "acknowledgment"]
            style = "warm_and_responsive"
        
        # Detect interaction intent
        if any(word in prompt_lower for word in ["hello", "hi", "👋", "greeting"]):
            intent = "greeting"
            context = "initial_contact"
        elif any(word in prompt_lower for word in ["play", "game", "fun", "🎮", "🎯"]):
            intent = "playful_interaction"
            context = "play_session"
        else:
            intent = "social_connection"
            context = "ongoing_relationship"
        
        return {
            "user_emotional_state": emotional_state,
            "user_intent": intent,
            "relationship_context": context,
            "predicted_needs": needs,
            "optimal_response_style": style,
            "confidence": 0.4,  # Lower confidence for fallback
            "reasoning": f"Fallback keyword analysis of prompt: detected {emotional_state} emotion and {intent} intent"
        }
    
    def _calculate_semantic_similarity(self, mem1: SemanticMemory, mem2: SemanticMemory) -> float:
        """Calculate similarity between memories based on semantic tags"""
        tags1 = set(mem1.semantic_tags)
        tags2 = set(mem2.semantic_tags)
        
        if not tags1 or not tags2:
            return 0.0
        
        jaccard_similarity = len(tags1.intersection(tags2)) / len(tags1.union(tags2))
        
        # Also consider emotional and temporal similarity
        emotional_sim = 1 - abs(
            mem1.emotional_context.get("user_emotion", 0.5) - 
            mem2.emotional_context.get("user_emotion", 0.5)
        )
        
        temporal_weight = max(0.1, 1 - abs(
            mem1.timestamp.timestamp() - mem2.timestamp.timestamp()
        ) / 86400)  # Decay over days
        
        return (jaccard_similarity * 0.6 + emotional_sim * 0.3 + temporal_weight * 0.1)
    
    # Additional helper methods would be implemented here...
    def _emotion_to_vector(self, emotion: str) -> np.ndarray:
        """Convert emotion string to numerical vector"""
        emotion_map = {
            "happy": np.array([0.8, 0.2, 0.9, 0.1, 0.7]),
            "sad": np.array([0.2, 0.8, 0.1, 0.9, 0.3]),
            "curious": np.array([0.6, 0.4, 0.7, 0.3, 0.8]),
            "anxious": np.array([0.3, 0.7, 0.2, 0.8, 0.4]),
            # Add more emotions...
        }
        return emotion_map.get(emotion, np.array([0.5, 0.5, 0.5, 0.5, 0.5]))
    
    def _intent_to_vector(self, intent: str) -> np.ndarray:
        """Convert intent string to numerical vector"""
        intent_map = {
            "social_connection": np.array([0.9, 0.1, 0.8, 0.2, 0.7]),
            "emotional_support": np.array([0.7, 0.3, 0.9, 0.1, 0.8]),
            "playful_interaction": np.array([0.8, 0.2, 0.6, 0.4, 0.9]),
            # Add more intents...
        }
        return intent_map.get(intent, np.array([0.5, 0.5, 0.5, 0.5, 0.5]))
    
    # Additional helper methods for complete implementation
    def _compare_emotional_states(self, prev_emotion: str, curr_emotion: str) -> float:
        """Compare emotional states to calculate prediction error"""
        emotion_similarity = {
            ("happy", "happy"): 0.0,
            ("happy", "sad"): 1.0,
            ("happy", "curious"): 0.3,
            ("happy", "anxious"): 0.7,
            ("sad", "sad"): 0.0,
            ("sad", "happy"): 1.0,
            ("sad", "curious"): 0.6,
            ("sad", "anxious"): 0.4,
            ("curious", "curious"): 0.0,
            ("curious", "happy"): 0.3,
            ("curious", "sad"): 0.6,
            ("curious", "anxious"): 0.5,
            ("anxious", "anxious"): 0.0,
            ("anxious", "happy"): 0.7,
            ("anxious", "sad"): 0.4,
            ("anxious", "curious"): 0.5,
        }
        
        return emotion_similarity.get((prev_emotion, curr_emotion), 0.5)
    
    def _compare_intents(self, prev_intent: str, curr_intent: str) -> float:
        """Compare user intents to calculate prediction error"""
        intent_similarity = {
            ("social_connection", "social_connection"): 0.0,
            ("social_connection", "emotional_support"): 0.3,
            ("social_connection", "playful_interaction"): 0.4,
            ("emotional_support", "emotional_support"): 0.0,
            ("emotional_support", "social_connection"): 0.3,
            ("emotional_support", "playful_interaction"): 0.6,
            ("playful_interaction", "playful_interaction"): 0.0,
            ("playful_interaction", "social_connection"): 0.4,
            ("playful_interaction", "emotional_support"): 0.6,
        }
        
        return intent_similarity.get((prev_intent, curr_intent), 0.5)
    
    async def _revise_user_traits(self, prediction: SemanticPrediction, learning_rate: float):
        """Revise user personality traits based on new prediction"""
        # Extract personality indicators from prediction
        if prediction.user_emotional_state not in [trait.lower() for trait in self.user_model["personality_traits"]]:
            self.user_model["personality_traits"].append(prediction.user_emotional_state)
            
        # Update emotional patterns
        if prediction.user_emotional_state not in self.user_model["emotional_patterns"]:
            self.user_model["emotional_patterns"].append(prediction.user_emotional_state)
            
        # Update communication style
        self.user_model["communication_style"] = prediction.optimal_response_style
        
        logger.debug(f"Revised user traits with learning rate {learning_rate}")
    
    async def _update_relationship_model(self, prediction: SemanticPrediction, learning_rate: float):
        """Update relationship model based on prediction"""
        # Add to relationship history
        self.user_model["relationship_history"].append({
            "context": prediction.relationship_context,
            "timestamp": datetime.now().isoformat(),
            "confidence": prediction.confidence
        })
        
        # Keep only recent history
        if len(self.user_model["relationship_history"]) > 20:
            self.user_model["relationship_history"] = self.user_model["relationship_history"][-20:]
            
        logger.debug(f"Updated relationship model with context: {prediction.relationship_context}")
    
    async def _refine_user_model(self, prediction: SemanticPrediction, learning_rate: float):
        """Incrementally refine user model"""
        # Update current needs
        self.user_model["current_needs"] = prediction.predicted_needs
        
        # Gradually adjust trust level based on prediction confidence
        trust_adjustment = (prediction.confidence - 0.5) * learning_rate * 0.1
        self.user_model["trust_level"] = max(0.0, min(1.0, 
            self.user_model["trust_level"] + trust_adjustment))
    
    def _update_relationship_dynamics(self, prediction: SemanticPrediction, error: float):
        """Update relationship dynamics based on prediction accuracy"""
        # Lower error means better understanding -> higher trust
        trust_change = (1.0 - error) * 0.05  # Small incremental changes
        self.user_model["trust_level"] = max(0.0, min(1.0,
            self.user_model["trust_level"] + trust_change))
        
        # Infer attachment style based on patterns
        if self.user_model["trust_level"] > 0.8:
            self.user_model["attachment_style"] = "secure"
        elif error > 0.7:
            self.user_model["attachment_style"] = "anxious"
        else:
            self.user_model["attachment_style"] = "developing"
    
    def _calculate_memory_significance(self, prediction: SemanticPrediction, context: Dict[str, Any]) -> float:
        """Calculate how significant this memory should be"""
        significance = 0.5  # Base significance
        
        # High confidence predictions are more significant
        significance += (prediction.confidence - 0.5) * 0.3
        
        # Emotional intensity adds significance
        emotional_weights = {
            "happy": 0.2, "sad": 0.3, "angry": 0.4, "surprised": 0.3,
            "curious": 0.2, "anxious": 0.3, "excited": 0.2
        }
        significance += emotional_weights.get(prediction.user_emotional_state, 0.1)
        
        # First-time interactions are more significant
        if len(self.semantic_memories) < 5:
            significance += 0.2
            
        return max(0.0, min(1.0, significance))
    
    def _get_recent_semantic_memories(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get recent semantic memories for context"""
        recent_memories = []
        sorted_memories = sorted(
            self.semantic_memories.values(), 
            key=lambda m: m.timestamp, 
            reverse=True
        )
        
        for memory in sorted_memories[:limit]:
            recent_memories.append({
                "content": memory.interaction_content.get("user_input", ""),
                "emotional_context": memory.emotional_context,
                "tags": memory.semantic_tags[:3],  # Top 3 tags
                "significance": memory.significance_score
            })
            
        return recent_memories
    
    def _summarize_user_model(self) -> Dict[str, Any]:
        """Create a summary of the user model for LLM context"""
        return {
            "personality_summary": ", ".join(self.user_model["personality_traits"][-5:]),
            "emotional_pattern": ", ".join(self.user_model["emotional_patterns"][-3:]),
            "communication_style": self.user_model["communication_style"],
            "trust_level": self.user_model["trust_level"],
            "attachment_style": self.user_model["attachment_style"],
            "current_needs": self.user_model["current_needs"][-3:] if self.user_model["current_needs"] else [],
            "relationship_depth": len(self.user_model["relationship_history"])
        }
    
    def _retrieve_associated_memories(self, memory: SemanticMemory, limit: int = 3) -> List[Dict[str, Any]]:
        """Retrieve memories associated with the given memory"""
        associated = []
        
        for assoc_id in memory.associations[:limit]:
            if assoc_id in self.semantic_memories:
                assoc_memory = self.semantic_memories[assoc_id]
                associated.append({
                    "content": assoc_memory.interaction_content.get("user_input", ""),
                    "tags": assoc_memory.semantic_tags,
                    "emotional_context": assoc_memory.emotional_context
                })
                
        return associated
    
    async def _consolidate_memories(self):
        """Consolidate and potentially forget old memories"""
        if len(self.semantic_memories) < 10:
            return  # Not enough memories to consolidate
            
        # Find memories that should be consolidated or forgotten
        memories_to_forget = []
        
        for memory_id, memory in self.semantic_memories.items():
            # Decrease consolidation strength over time
            memory.consolidation_strength *= (1 - self.forgetting_rate)
            
            # Mark for forgetting if strength is too low and not recently accessed
            if (memory.consolidation_strength < 0.1 and 
                memory.access_count < 2 and 
                len(self.semantic_memories) > 50):
                memories_to_forget.append(memory_id)
        
        # Remove forgotten memories
        for memory_id in memories_to_forget:
            del self.semantic_memories[memory_id]
            logger.debug(f"Consolidated (forgot) memory {memory_id}")
        
        # Update memory clusters after consolidation
        self._update_memory_clusters()
        
        logger.info(f"Memory consolidation: {len(memories_to_forget)} memories forgotten, "
                   f"{len(self.semantic_memories)} memories retained")
    
    def _update_memory_clusters(self):
        """Update memory clusters after memory changes"""
        # Rebuild clusters from current memories
        self.memory_clusters.clear()
        
        for memory_id, memory in self.semantic_memories.items():
            for tag in memory.semantic_tags:
                if tag not in self.memory_clusters:
                    self.memory_clusters[tag] = []
                self.memory_clusters[tag].append(memory_id)