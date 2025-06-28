"""
Base DKS Agent Class with Core Dynamic Kinetic Systems Principles
"""
import mesa
import uuid
import time
import json
import asyncio
import logging
from typing import Dict, List, Any, Optional
from collections import defaultdict

logger = logging.getLogger(__name__)


class DKSAgent(mesa.Agent):
    """
    Base agent class implementing Dynamic Kinetic Systems principles:
    - Persistent self-organization through continuous activity
    - Memory systems for adaptation and pattern recognition  
    - Autocatalytic network formation through interaction success
    - Emergence from simple local interactions
    """
    
    def __init__(self, unique_id: str, model, agent_type: str, initial_state: Optional[Dict] = None):
        super().__init__(unique_id, model)
        
        # Core DKS attributes
        self.agent_type = agent_type
        self.state = initial_state or {}
        self.resources = 0
        self.energy = 100  # Energy for maintaining dynamic stability
        
        # Memory systems - multi-level memory as per DKS theory
        self.episodic_memory = []  # Individual experiences
        self.semantic_memory = {}  # Generalized knowledge from patterns
        self.working_memory = {}   # Current context and active goals
        
        # Interaction patterns and adaptation
        self.interaction_patterns = defaultdict(float)  # Pattern -> success rate
        self.interaction_history = []  # Recent interactions
        self.strategy_weights = {}  # Strategy -> weight mapping
        self.adaptation_score = 0.5  # How well adapted to environment
        
        # Network formation (autocatalytic networks)
        self.connection_strengths = defaultdict(float)  # Agent -> strength
        self.preferred_partners = set()  # Agents with strong connections
        
        # Message handling
        self.message_queue = []
        self.pending_responses = {}
        
        # Performance tracking
        self.success_rate = 0.5
        self.interaction_count = 0
        self.last_adaptation = time.time()
        
    def step(self):
        """
        Core DKS agent step implementing persistent self-organization
        No centralized coordination - only local rules and interactions
        """
        try:
            # 1. Maintain dynamic stability (continuous activity vs. equilibrium)
            self.maintain_dynamic_stability()
            
            # 2. Process incoming messages (local information only)
            messages = self.get_messages()
            self.process_messages(messages)
            
            # 3. Assess current situation using local information
            self.assess_situation()
            
            # 4. Make decisions based on learned patterns and current state
            actions = self.decide_actions()
            
            # 5. Perform actions and send messages
            self.perform_actions(actions)
            
            # 6. Update internal state and adapt strategies
            self.update_state()
            self.adapt_strategies()
            
            # 7. Update memory systems
            self.consolidate_memory()
            
        except Exception as e:
            logger.error(f"Error in agent {self.unique_id} step: {e}")
    
    def maintain_dynamic_stability(self):
        """
        Maintain dynamic kinetic stability through continuous activity
        This is key to DKS - stability through ongoing processes, not equilibrium
        """
        # Consume energy for maintaining activity
        self.energy = max(0, self.energy - 1)
        
        # Generate energy through successful interactions (autocatalytic)
        if self.success_rate > 0.6:
            self.energy = min(100, self.energy + 2)
        
        # If energy is low, become more exploratory to find new resources
        if self.energy < 30:
            self.increase_exploration()
    
    def get_messages(self) -> List[Dict[str, Any]]:
        """Get messages from Redis via the model's redis manager"""
        if not self.model.redis_manager:
            return []
        
        try:
            # This will be an async call in practice, but Mesa requires sync
            # In the full implementation, we'll handle this with async queues
            messages = self.message_queue.copy()
            self.message_queue.clear()
            return messages
        except Exception as e:
            logger.error(f"Error getting messages for {self.unique_id}: {e}")
            return []
    
    def send_message(self, recipient_id: str, message_type: str, content: Dict[str, Any]):
        """Send message to another agent"""
        message = {
            "sender": self.unique_id,
            "recipient": recipient_id,
            "type": message_type,
            "content": content,
            "timestamp": time.time()
        }
        
        try:
            # Add to model's message queue for processing
            if hasattr(self.model, 'message_queue'):
                self.model.message_queue.append(message)
            
            # Record interaction for pattern learning
            self.record_interaction(recipient_id, message_type, "sent")
            
        except Exception as e:
            logger.error(f"Error sending message from {self.unique_id}: {e}")
    
    def process_messages(self, messages: List[Dict[str, Any]]):
        """Process received messages based on type"""
        for message in messages:
            try:
                msg_type = message.get("type")
                sender = message.get("sender")
                content = message.get("content", {})
                
                # Route message to appropriate handler
                if msg_type == "resource_request":
                    self.handle_resource_request(sender, content)
                elif msg_type == "resource_offer":
                    self.handle_resource_offer(sender, content)
                elif msg_type == "resource_response":
                    self.handle_resource_response(sender, content)
                elif msg_type == "status_update":
                    self.handle_status_update(sender, content)
                elif msg_type == "collaboration_request":
                    self.handle_collaboration_request(sender, content)
                else:
                    self.handle_unknown_message(sender, msg_type, content)
                
                # Record interaction
                self.record_interaction(sender, msg_type, "received")
                
            except Exception as e:
                logger.error(f"Error processing message in {self.unique_id}: {e}")
    
    def assess_situation(self):
        """Assess current state and environment using only local information"""
        # Update working memory with current context
        self.working_memory.update({
            "current_resources": self.resources,
            "energy_level": self.energy,
            "recent_success_rate": self.calculate_recent_success_rate(),
            "preferred_partners_available": self.check_preferred_partners(),
            "time_since_last_adaptation": time.time() - self.last_adaptation
        })
    
    def decide_actions(self) -> List[Dict[str, Any]]:
        """
        Make decisions based on learned patterns and current state
        This is where emergent intelligence appears through pattern matching
        """
        actions = []
        
        # Use strategy weights to decide actions
        for strategy, weight in self.strategy_weights.items():
            if weight > 0.3:  # Only consider strategies with reasonable weight
                action = self.generate_action_for_strategy(strategy)
                if action:
                    actions.append(action)
        
        # If no strategies are strong, explore new options
        if not actions or max(self.strategy_weights.values(), default=0) < 0.4:
            actions.append(self.generate_exploratory_action())
        
        return actions
    
    def perform_actions(self, actions: List[Dict[str, Any]]):
        """Perform decided actions"""
        for action in actions:
            try:
                action_type = action.get("type")
                
                if action_type == "send_request":
                    self.send_resource_request(action)
                elif action_type == "send_offer":
                    self.send_resource_offer(action)
                elif action_type == "seek_collaboration":
                    self.seek_collaboration(action)
                elif action_type == "explore":
                    self.explore_environment(action)
                else:
                    logger.warning(f"Unknown action type: {action_type}")
                    
            except Exception as e:
                logger.error(f"Error performing action {action}: {e}")
    
    def update_state(self):
        """Update internal state based on recent outcomes"""
        # Calculate current performance metrics
        recent_interactions = self.interaction_history[-10:]  # Last 10 interactions
        if recent_interactions:
            recent_successes = sum(1 for i in recent_interactions if i.get("outcome") == "success")
            self.success_rate = recent_successes / len(recent_interactions)
        
        # Update adaptation score based on performance
        if self.success_rate > 0.7:
            self.adaptation_score = min(1.0, self.adaptation_score + 0.05)
        elif self.success_rate < 0.3:
            self.adaptation_score = max(0.0, self.adaptation_score - 0.05)
    
    def adapt_strategies(self):
        """
        Adapt strategies based on interaction outcomes
        This implements the DKS principle of learning from successful patterns
        """
        # Only adapt if enough time has passed
        if time.time() - self.last_adaptation < 5:  # 5 seconds minimum
            return
        
        # Identify successful patterns in recent history
        successful_patterns = self.identify_successful_patterns()
        
        # Update strategy weights based on successful patterns
        for pattern, success_rate in successful_patterns.items():
            current_weight = self.strategy_weights.get(pattern, 0.5)
            # Weighted update: 80% current, 20% new evidence
            self.strategy_weights[pattern] = 0.8 * current_weight + 0.2 * success_rate
        
        # Normalize strategy weights
        total_weight = sum(self.strategy_weights.values())
        if total_weight > 0:
            self.strategy_weights = {
                k: v / total_weight 
                for k, v in self.strategy_weights.items()
            }
        
        self.last_adaptation = time.time()
    
    def consolidate_memory(self):
        """
        Convert episodic memories to semantic memory when patterns repeat
        This creates the learned behaviors that enable emergent intelligence
        """
        if len(self.episodic_memory) < 5:
            return
        
        # Look for patterns in recent episodic memories
        recent_memories = self.episodic_memory[-20:]  # Last 20 experiences
        patterns = self.identify_patterns_in_memories(recent_memories)
        
        # Consolidate repeated patterns to semantic memory
        for pattern, frequency in patterns.items():
            if frequency >= 3:  # Pattern occurs multiple times
                if pattern in self.semantic_memory:
                    # Strengthen existing pattern
                    self.semantic_memory[pattern] = min(1.0, 
                        0.9 * self.semantic_memory[pattern] + 0.1 * (frequency / 20)
                    )
                else:
                    # Add new pattern
                    self.semantic_memory[pattern] = frequency / 20
    
    # --- Helper Methods ---
    
    def record_interaction(self, other_agent: str, interaction_type: str, direction: str):
        """Record an interaction for learning and adaptation"""
        interaction = {
            "agent": other_agent,
            "type": interaction_type,
            "direction": direction,  # "sent" or "received"
            "timestamp": time.time(),
            "outcome": None  # Will be updated when outcome is known
        }
        
        self.interaction_history.append(interaction)
        
        # Keep only recent history
        if len(self.interaction_history) > 100:
            self.interaction_history = self.interaction_history[-50:]
        
        self.interaction_count += 1
    
    def calculate_recent_success_rate(self) -> float:
        """Calculate success rate for recent interactions"""
        recent = [i for i in self.interaction_history[-20:] if i.get("outcome")]
        if not recent:
            return 0.5  # Neutral assumption
        
        successes = sum(1 for i in recent if i["outcome"] == "success")
        return successes / len(recent)
    
    def identify_successful_patterns(self) -> Dict[str, float]:
        """Identify patterns that correlate with successful outcomes"""
        patterns = {}
        successful_interactions = [
            i for i in self.interaction_history[-50:] 
            if i.get("outcome") == "success"
        ]
        
        if not successful_interactions:
            return patterns
        
        # Analyze patterns in successful interactions
        for interaction in successful_interactions:
            pattern_key = f"{interaction['type']}_{interaction['direction']}"
            patterns[pattern_key] = patterns.get(pattern_key, 0) + 1
        
        # Convert counts to rates
        total_successful = len(successful_interactions)
        return {k: v / total_successful for k, v in patterns.items()}
    
    def identify_patterns_in_memories(self, memories: List[Dict]) -> Dict[str, int]:
        """Identify recurring patterns in episodic memories"""
        patterns = defaultdict(int)
        
        for memory in memories:
            # Create pattern signature from memory
            pattern = self.create_pattern_signature(memory)
            patterns[pattern] += 1
        
        return dict(patterns)
    
    def create_pattern_signature(self, memory: Dict) -> str:
        """Create a pattern signature from a memory for pattern matching"""
        # Extract key features that might form patterns
        features = []
        
        if "agent" in memory:
            features.append(f"agent_type:{memory['agent'][:4]}")  # Agent type prefix
        if "type" in memory:
            features.append(f"interaction:{memory['type']}")
        if "outcome" in memory:
            features.append(f"outcome:{memory['outcome']}")
        
        return "|".join(sorted(features))
    
    # --- Abstract methods to be implemented by subclasses ---
    
    def handle_resource_request(self, sender: str, content: Dict[str, Any]):
        """Handle incoming resource requests - implement in subclasses"""
        pass
    
    def handle_resource_offer(self, sender: str, content: Dict[str, Any]):
        """Handle incoming resource offers - implement in subclasses"""
        pass
    
    def handle_resource_response(self, sender: str, content: Dict[str, Any]):
        """Handle responses to resource requests - implement in subclasses"""
        pass
    
    def handle_status_update(self, sender: str, content: Dict[str, Any]):
        """Handle status updates from other agents - implement in subclasses"""
        pass
    
    def handle_collaboration_request(self, sender: str, content: Dict[str, Any]):
        """Handle collaboration requests - implement in subclasses"""
        pass
    
    def handle_unknown_message(self, sender: str, msg_type: str, content: Dict[str, Any]):
        """Handle unknown message types - implement in subclasses"""
        logger.warning(f"Unknown message type {msg_type} from {sender}")
    
    def generate_action_for_strategy(self, strategy: str) -> Optional[Dict[str, Any]]:
        """Generate an action for a given strategy - implement in subclasses"""
        return None
    
    def generate_exploratory_action(self) -> Dict[str, Any]:
        """Generate an exploratory action when no strategies are strong"""
        return {"type": "explore", "target": "random"}
    
    def increase_exploration(self):
        """Increase exploratory behavior when energy is low"""
        # Reduce weights of current strategies to encourage exploration
        for strategy in self.strategy_weights:
            self.strategy_weights[strategy] *= 0.9
    
    def check_preferred_partners(self) -> bool:
        """Check if any preferred partners are available"""
        # This would check with the model for partner availability
        return len(self.preferred_partners) > 0
    
    def send_resource_request(self, action: Dict[str, Any]):
        """Send a resource request - implement in subclasses"""
        pass
    
    def send_resource_offer(self, action: Dict[str, Any]):
        """Send a resource offer - implement in subclasses"""
        pass
    
    def seek_collaboration(self, action: Dict[str, Any]):
        """Seek collaboration with other agents - implement in subclasses"""
        pass
    
    def explore_environment(self, action: Dict[str, Any]):
        """Explore the environment for new opportunities"""
        # Basic exploration - move randomly or try new interactions
        pass
