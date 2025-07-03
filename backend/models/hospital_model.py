"""
Hospital Model - Main simulation environment for DKS agent system
"""
import mesa
import numpy as np
import random
import uuid
import time
import logging
from typing import Dict, List, Any, Optional
from collections import defaultdict

from backend.agents.base_agent import DKSAgent

logger = logging.getLogger(__name__)


class HospitalModel(mesa.Model):
    """
    Hospital model implementing DKS principles:
    - No centralized optimization
    - Agents self-organize through local interactions
    - Emergent behaviors develop from simple rules
    - System maintains dynamic stability through continuous activity
    """
    
    def __init__(self, num_wards: int, num_staff: int, num_equipment: int, 
                 num_patients: int, redis_manager=None, data_collector=None):
        super().__init__()
        
        # Initialize random number generator for Mesa framework
        self.random = random.Random()
        
        # Model parameters
        self.num_wards = num_wards
        self.num_staff = num_staff
        self.num_equipment = num_equipment
        self.num_patients = num_patients
        
        # External managers
        self.redis_manager = redis_manager
        self.data_collector = data_collector
        
        # Model state
        self.running = False
        self.message_queue = []  # For inter-agent communication
        self.current_run_id = str(uuid.uuid4())
        
        # Environment state
        self.environment_state = {
            "time_of_day": 8.0,  # 8 AM start
            "day_of_week": 1,    # Monday
            "emergency_level": 0.0,
            "resource_scarcity": 0.0
        }
        
        # Set up Mesa components
        self.grid = mesa.space.MultiGrid(50, 50, True)
        self.schedule = mesa.time.RandomActivation(self)
        
        # Create agents
        self.create_agents()
        
        # Set up data collection
        self.setup_data_collection()
        
        logger.info(f"Hospital model initialized with {len(self.schedule.agents)} agents")
    
    def create_agents(self):
        """Create all agent types"""
        # For now, create simple test agents
        # In Stage 2, we'll implement the specific agent types
        
        agent_id = 0
        
        # Create ward agents
        for i in range(self.num_wards):
            agent = TestAgent(
                unique_id=f"ward_{agent_id}",
                model=self,
                agent_type="ward",
                initial_state={"capacity": 10, "specialty": f"ward_{i}"}
            )
            self.schedule.add(agent)
            
            # Place on grid
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))
            agent_id += 1
        
        # Create staff agents
        for i in range(self.num_staff):
            agent = TestAgent(
                unique_id=f"staff_{agent_id}",
                model=self,
                agent_type="staff",
                initial_state={"skill_level": self.random.random(), "specialty": "general"}
            )
            self.schedule.add(agent)
            
            # Place on grid
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))
            agent_id += 1
        
        # Create equipment agents
        for i in range(self.num_equipment):
            agent = TestAgent(
                unique_id=f"equipment_{agent_id}",
                model=self,
                agent_type="equipment",
                initial_state={"type": "general", "in_use": False}
            )
            self.schedule.add(agent)
            
            # Place on grid
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))
            agent_id += 1
        
        # Create patient agents
        for i in range(self.num_patients):
            agent = TestAgent(
                unique_id=f"patient_{agent_id}",
                model=self,
                agent_type="patient",
                initial_state={"condition": "stable", "wait_time": 0}
            )
            self.schedule.add(agent)
            
            # Place on grid
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))
            agent_id += 1
    
    def setup_data_collection(self):
        """Set up data collection for metrics and analysis"""
        if not self.data_collector:
            return
        
        # Model-level reporters
        model_reporters = {
            "Average_Wait_Time": self.calculate_avg_wait_time,
            "Resource_Utilization": self.calculate_resource_utilization,
            "Patient_Satisfaction": self.calculate_patient_satisfaction,
            "Network_Density": self.calculate_network_density,
            "Adaptation_Score": self.calculate_avg_adaptation_score
        }
        
        # Agent-level reporters
        agent_reporters = {
            "Agent_Type": "agent_type",
            "Resources": "resources",
            "Energy": "energy",
            "Adaptation_Score": "adaptation_score",
            "Success_Rate": "success_rate",
            "X": lambda agent: agent.pos[0] if agent.pos else 0,
            "Y": lambda agent: agent.pos[1] if agent.pos else 0
        }
        
        # Initialize Mesa's data collector
        self.datacollector = mesa.DataCollector(
            model_reporters=model_reporters,
            agent_reporters=agent_reporters
        )
    
    def step(self):
        """Advance the model by one step"""
        try:
            # Update environment state
            self.update_environment()
            
            # Process inter-agent messages
            self.process_messages()
            
            # Step all agents (this is where the DKS magic happens)
            self.schedule.step()
            
            # Collect data
            if hasattr(self, 'datacollector'):
                self.datacollector.collect(self)
            
            # Send data to data collector if available
            if self.data_collector:
                self.data_collector.collect_step_data(self)
            
        except Exception as e:
            logger.error(f"Error in model step: {e}")
    
    def update_environment(self):
        """Update environment state to simulate daily hospital patterns"""
        # Simulate time progression
        self.environment_state["time_of_day"] += 0.1  # 6 minutes per step
        if self.environment_state["time_of_day"] >= 24:
            self.environment_state["time_of_day"] = 0
            self.environment_state["day_of_week"] = (self.environment_state["day_of_week"] % 7) + 1
        
        # Simulate varying conditions
        time_of_day = self.environment_state["time_of_day"]
        
        # Morning rush (8-10 AM)
        if 8 <= time_of_day <= 10:
            self.environment_state["emergency_level"] = min(1.0, 
                self.environment_state["emergency_level"] + 0.1)
        else:
            self.environment_state["emergency_level"] = max(0.0,
                self.environment_state["emergency_level"] - 0.05)
        
        # Random events
        if self.random.random() < 0.01:  # 1% chance per step
            self.environment_state["resource_scarcity"] = min(1.0,
                self.environment_state["resource_scarcity"] + 0.2)
        else:
            self.environment_state["resource_scarcity"] = max(0.0,
                self.environment_state["resource_scarcity"] - 0.02)
    
    def process_messages(self):
        """Process queued messages between agents"""
        for message in self.message_queue:
            try:
                recipient_id = message.get("recipient")
                recipient_agent = self.get_agent_by_id(recipient_id)
                
                if recipient_agent:
                    recipient_agent.message_queue.append(message)
                else:
                    logger.warning(f"Message recipient {recipient_id} not found")
                    
            except Exception as e:
                logger.error(f"Error processing message: {e}")
        
        # Clear processed messages
        self.message_queue.clear()
    
    def get_agent_by_id(self, agent_id: str) -> Optional[DKSAgent]:
        """Get an agent by ID"""
        for agent in self.schedule.agents:
            if agent.unique_id == agent_id:
                return agent
        return None
    
    def get_agent_counts(self) -> Dict[str, int]:
        """Get count of each agent type"""
        counts = defaultdict(int)
        for agent in self.schedule.agents:
            counts[agent.agent_type] += 1
        return dict(counts)
    
    def get_agents_by_type(self, agent_type: str) -> List[DKSAgent]:
        """Get all agents of a specific type"""
        return [agent for agent in self.schedule.agents if agent.agent_type == agent_type]
    
    def get_network_data(self) -> Dict[str, Any]:
        """Get network data for visualization"""
        nodes = []
        links = []
        
        # Create nodes
        for agent in self.schedule.agents:
            nodes.append({
                "id": agent.unique_id,
                "type": agent.agent_type,
                "x": agent.pos[0] if agent.pos else 0,
                "y": agent.pos[1] if agent.pos else 0,
                "resources": agent.resources,
                "energy": agent.energy,
                "adaptation_score": agent.adaptation_score
            })
        
        # Create links based on connection strengths
        for agent in self.schedule.agents:
            for other_id, strength in agent.connection_strengths.items():
                if strength > 0.1:  # Only show significant connections
                    links.append({
                        "source": agent.unique_id,
                        "target": other_id,
                        "strength": strength,
                        "type": "interaction"
                    })
        
        return {"nodes": nodes, "links": links}
    
    # --- Metric calculation methods ---
    
    def calculate_avg_wait_time(self) -> float:
        """Calculate average patient wait time"""
        patients = self.get_agents_by_type("patient")
        if not patients:
            return 0.0
        
        total_wait = sum(agent.state.get("wait_time", 0) for agent in patients)
        return total_wait / len(patients)
    
    def calculate_resource_utilization(self) -> float:
        """Calculate overall resource utilization"""
        equipment = self.get_agents_by_type("equipment")
        if not equipment:
            return 0.0
        
        in_use = sum(1 for agent in equipment if agent.state.get("in_use", False))
        return in_use / len(equipment)
    
    def calculate_patient_satisfaction(self) -> float:
        """Calculate average patient satisfaction"""
        patients = self.get_agents_by_type("patient")
        if not patients:
            return 0.0
        
        # Satisfaction based on wait time and service quality
        satisfactions = []
        for patient in patients:
            wait_time = patient.state.get("wait_time", 0)
            base_satisfaction = 100
            satisfaction = max(0, base_satisfaction - wait_time * 2)
            satisfactions.append(satisfaction)
        
        return sum(satisfactions) / len(satisfactions)
    
    def calculate_network_density(self) -> float:
        """Calculate network connection density"""
        total_agents = len(self.schedule.agents)
        if total_agents < 2:
            return 0.0
        
        total_connections = 0
        for agent in self.schedule.agents:
            total_connections += len([s for s in agent.connection_strengths.values() if s > 0.1])
        
        max_connections = total_agents * (total_agents - 1)
        return total_connections / max_connections if max_connections > 0 else 0.0
    
    def calculate_avg_adaptation_score(self) -> float:
        """Calculate average adaptation score across all agents"""
        if not self.schedule.agents:
            return 0.0
        
        total_score = sum(agent.adaptation_score for agent in self.schedule.agents)
        return total_score / len(self.schedule.agents)


class TestAgent(DKSAgent):
    """
    Simple test agent for Stage 1 - just implements basic DKS behavior
    In Stage 2, we'll replace this with specialized agent types
    """
    
    def __init__(self, unique_id: str, model, agent_type: str, initial_state: Dict = None):
        super().__init__(unique_id, model, agent_type, initial_state)
        
        # Initialize some basic strategies
        self.strategy_weights = {
            "seek_resources": 0.5,
            "offer_help": 0.3,
            "explore": 0.2
        }
    
    def handle_resource_request(self, sender: str, content: Dict[str, Any]):
        """Handle resource requests"""
        # Simple response: agree if we have resources
        if self.resources > 0:
            self.send_message(sender, "resource_response", {
                "response": "accept",
                "amount": min(1, self.resources)
            })
            self.resources -= 1
        else:
            self.send_message(sender, "resource_response", {
                "response": "decline",
                "reason": "insufficient_resources"
            })
    
    def handle_resource_offer(self, sender: str, content: Dict[str, Any]):
        """Handle resource offers"""
        if self.resources < 5:  # Accept if we need resources
            self.send_message(sender, "resource_response", {
                "response": "accept"
            })
            self.resources += content.get("amount", 1)
    
    def handle_resource_response(self, sender: str, content: Dict[str, Any]):
        """Handle responses to our requests"""
        response = content.get("response", "decline")
        if response == "accept":
            self.record_successful_interaction(sender)
            self.resources += content.get("amount", 1)
        else:
            self.record_failed_interaction(sender)
    
    def generate_action_for_strategy(self, strategy: str) -> Optional[Dict[str, Any]]:
        """Generate actions based on strategy"""
        if strategy == "seek_resources" and self.resources < 3:
            # Find another agent to request resources from
            other_agents = [a for a in self.model.schedule.agents if a != self]
            if other_agents:
                target = self.model.random.choice(other_agents)
                return {
                    "type": "send_request",
                    "target": target.unique_id,
                    "resource_type": "general",
                    "amount": 1
                }
        
        elif strategy == "offer_help" and self.resources > 5:
            # Offer resources to another agent
            other_agents = [a for a in self.model.schedule.agents if a != self]
            if other_agents:
                target = self.model.random.choice(other_agents)
                return {
                    "type": "send_offer",
                    "target": target.unique_id,
                    "resource_type": "general",
                    "amount": 1
                }
        
        elif strategy == "explore":
            return {"type": "explore", "direction": "random"}
        
        return None
    
    def send_resource_request(self, action: Dict[str, Any]):
        """Send a resource request"""
        self.send_message(action["target"], "resource_request", {
            "resource_type": action.get("resource_type", "general"),
            "amount": action.get("amount", 1),
            "urgency": "normal"
        })
    
    def send_resource_offer(self, action: Dict[str, Any]):
        """Send a resource offer"""
        self.send_message(action["target"], "resource_offer", {
            "resource_type": action.get("resource_type", "general"),
            "amount": action.get("amount", 1)
        })
    
    def explore_environment(self, action: Dict[str, Any]):
        """Explore the environment"""
        # Move randomly on the grid
        if self.pos:
            x, y = self.pos
            dx = self.model.random.randint(-1, 1)
            dy = self.model.random.randint(-1, 1)
            new_x = max(0, min(self.model.grid.width - 1, x + dx))
            new_y = max(0, min(self.model.grid.height - 1, y + dy))
            self.model.grid.move_agent(self, (new_x, new_y))
        
        # Potentially find resources
        if self.model.random.random() < 0.1:  # 10% chance
            self.resources += 1
    
    def record_successful_interaction(self, other_agent: str):
        """Record a successful interaction"""
        self.connection_strengths[other_agent] = min(1.0, 
            self.connection_strengths[other_agent] + 0.1)
        
        # Update interaction history
        if self.interaction_history:
            self.interaction_history[-1]["outcome"] = "success"
    
    def record_failed_interaction(self, other_agent: str):
        """Record a failed interaction"""
        self.connection_strengths[other_agent] = max(0.0,
            self.connection_strengths[other_agent] - 0.05)
        
        # Update interaction history
        if self.interaction_history:
            self.interaction_history[-1]["outcome"] = "failure"
