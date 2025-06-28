"""
Data Collector for DKS Agent System Visualization and Analysis
"""
import time
import json
import logging
from typing import Dict, List, Any, Optional
from collections import defaultdict, deque

logger = logging.getLogger(__name__)


class DataCollector:
    """
    Collects and processes data from the DKS agent system for:
    - Real-time visualization
    - Pattern analysis
    - Performance metrics
    - Emergent behavior detection
    """
    
    def __init__(self):
        # Current state data
        self.current_metrics = {}
        self.current_network_data = {"nodes": [], "links": []}
        
        # Historical data (keeping recent history for analysis)
        self.metrics_history = deque(maxlen=1000)
        self.network_history = deque(maxlen=100)
        self.interaction_history = deque(maxlen=500)
        
        # Pattern detection
        self.detected_patterns = {}
        self.pattern_history = deque(maxlen=50)
        
        # Performance tracking
        self.performance_metrics = {
            "system_efficiency": 0.0,
            "adaptation_rate": 0.0,
            "emergence_score": 0.0,
            "stability_score": 0.0
        }
        
        # Aggregated statistics
        self.agent_statistics = defaultdict(dict)
        self.interaction_statistics = defaultdict(int)
        
        self.last_update = time.time()
    
    def collect_step_data(self, model):
        """Collect data from a model step"""
        try:
            # Collect basic metrics
            self.current_metrics = {
                "step": model.schedule.steps,
                "timestamp": time.time(),
                "agent_count": len(model.schedule.agents),
                "environment_state": model.environment_state.copy(),
                
                # Performance metrics
                "avg_wait_time": model.calculate_avg_wait_time(),
                "resource_utilization": model.calculate_resource_utilization(),
                "patient_satisfaction": model.calculate_patient_satisfaction(),
                "network_density": model.calculate_network_density(),
                "avg_adaptation_score": model.calculate_avg_adaptation_score()
            }
            
            # Collect network data
            self.current_network_data = model.get_network_data()
            
            # Store in history
            self.metrics_history.append(self.current_metrics.copy())
            self.network_history.append(self.current_network_data.copy())
            
            # Update agent statistics
            self.update_agent_statistics(model)
            
            # Detect patterns
            self.detect_patterns(model)
            
            # Calculate performance metrics
            self.calculate_performance_metrics()
            
            self.last_update = time.time()
            
        except Exception as e:
            logger.error(f"Error collecting step data: {e}")
    
    def update_agent_statistics(self, model):
        """Update statistics for each agent"""
        for agent in model.schedule.agents:
            agent_id = agent.unique_id
            agent_type = agent.agent_type
            
            # Update agent-specific statistics
            self.agent_statistics[agent_id] = {
                "type": agent_type,
                "resources": agent.resources,
                "energy": agent.energy,
                "adaptation_score": agent.adaptation_score,
                "success_rate": agent.success_rate,
                "interaction_count": agent.interaction_count,
                "connection_count": len([s for s in agent.connection_strengths.values() if s > 0.1]),
                "position": agent.pos if hasattr(agent, 'pos') and agent.pos else (0, 0)
            }
            
            # Count interactions by type
            for interaction in agent.interaction_history[-10:]:  # Recent interactions
                interaction_key = f"{agent_type}_{interaction.get('type', 'unknown')}"
                self.interaction_statistics[interaction_key] += 1
    
    def detect_patterns(self, model):
        """Detect emerging patterns in agent behavior"""
        try:
            current_patterns = {}
            
            # Pattern 1: Agent specialization
            specialization_patterns = self.detect_specialization_patterns(model)
            current_patterns.update(specialization_patterns)
            
            # Pattern 2: Resource flow patterns
            resource_flow_patterns = self.detect_resource_flow_patterns(model)
            current_patterns.update(resource_flow_patterns)
            
            # Pattern 3: Network clustering
            clustering_patterns = self.detect_clustering_patterns(model)
            current_patterns.update(clustering_patterns)
            
            # Pattern 4: Temporal patterns
            temporal_patterns = self.detect_temporal_patterns()
            current_patterns.update(temporal_patterns)
            
            # Store detected patterns
            self.detected_patterns = current_patterns
            self.pattern_history.append({
                "timestamp": time.time(),
                "step": model.schedule.steps,
                "patterns": current_patterns.copy()
            })
            
        except Exception as e:
            logger.error(f"Error detecting patterns: {e}")
    
    def detect_specialization_patterns(self, model) -> Dict[str, Any]:
        """Detect if agents are developing specialized roles"""
        patterns = {}
        
        # Group agents by type and analyze their behavior
        agent_types = defaultdict(list)
        for agent in model.schedule.agents:
            agent_types[agent.agent_type].append(agent)
        
        for agent_type, agents in agent_types.items():
            if len(agents) < 2:
                continue
            
            # Check for specialization within agent type
            specialization_scores = []
            for agent in agents:
                # Calculate specialization based on strategy weights
                max_strategy_weight = max(agent.strategy_weights.values()) if agent.strategy_weights else 0
                specialization_scores.append(max_strategy_weight)
            
            avg_specialization = sum(specialization_scores) / len(specialization_scores)
            
            if avg_specialization > 0.6:  # High specialization threshold
                patterns[f"{agent_type}_specialization"] = {
                    "type": "specialization",
                    "agent_type": agent_type,
                    "score": avg_specialization,
                    "description": f"{agent_type} agents showing specialized behavior patterns"
                }
        
        return patterns
    
    def detect_resource_flow_patterns(self, model) -> Dict[str, Any]:
        """Detect patterns in resource distribution and flow"""
        patterns = {}
        
        # Analyze resource distribution
        resource_by_type = defaultdict(int)
        for agent in model.schedule.agents:
            resource_by_type[agent.agent_type] += agent.resources
        
        # Check for resource imbalances
        if len(resource_by_type) > 1:
            resource_values = list(resource_by_type.values())
            max_resources = max(resource_values)
            min_resources = min(resource_values)
            
            if max_resources > 0 and min_resources / max_resources < 0.3:  # Significant imbalance
                patterns["resource_imbalance"] = {
                    "type": "resource_flow",
                    "imbalance_ratio": min_resources / max_resources,
                    "description": "Resource imbalance detected between agent types",
                    "distribution": dict(resource_by_type)
                }
        
        return patterns
    
    def detect_clustering_patterns(self, model) -> Dict[str, Any]:
        """Detect clustering patterns in agent networks"""
        patterns = {}
        
        # Analyze connection patterns
        strong_connections = defaultdict(int)
        total_connections = 0
        
        for agent in model.schedule.agents:
            strong_connections_for_agent = len([
                s for s in agent.connection_strengths.values() if s > 0.5
            ])
            strong_connections[agent.agent_type] += strong_connections_for_agent
            total_connections += len(agent.connection_strengths)
        
        if total_connections > 0:
            # Check for clustering by agent type
            for agent_type, connections in strong_connections.items():
                if connections > 3:  # Threshold for clustering
                    patterns[f"{agent_type}_clustering"] = {
                        "type": "clustering",
                        "agent_type": agent_type,
                        "strong_connections": connections,
                        "description": f"{agent_type} agents forming strong connection clusters"
                    }
        
        return patterns
    
    def detect_temporal_patterns(self) -> Dict[str, Any]:
        """Detect temporal patterns in system behavior"""
        patterns = {}
        
        if len(self.metrics_history) < 10:
            return patterns
        
        # Analyze trends in key metrics
        recent_metrics = list(self.metrics_history)[-10:]
        
        # Check for improving performance trends
        wait_times = [m.get("avg_wait_time", 0) for m in recent_metrics]
        if len(wait_times) >= 5:
            early_avg = sum(wait_times[:3]) / 3
            recent_avg = sum(wait_times[-3:]) / 3
            
            if early_avg > 0 and recent_avg / early_avg < 0.8:  # 20% improvement
                patterns["performance_improvement"] = {
                    "type": "temporal",
                    "metric": "wait_time",
                    "improvement": (early_avg - recent_avg) / early_avg,
                    "description": "System showing sustained performance improvement"
                }
        
        # Check for adaptation patterns
        adaptation_scores = [m.get("avg_adaptation_score", 0.5) for m in recent_metrics]
        if len(adaptation_scores) >= 5:
            trend = sum(adaptation_scores[-3:]) / 3 - sum(adaptation_scores[:3]) / 3
            if trend > 0.1:  # Significant improvement
                patterns["adaptation_trend"] = {
                    "type": "temporal",
                    "metric": "adaptation",
                    "trend": trend,
                    "description": "Agents showing increasing adaptation to environment"
                }
        
        return patterns
    
    def calculate_performance_metrics(self):
        """Calculate overall system performance metrics"""
        if not self.metrics_history:
            return
        
        recent_metrics = list(self.metrics_history)[-20:]  # Last 20 steps
        
        # System efficiency (inverse of wait time, normalized)
        avg_wait_times = [m.get("avg_wait_time", 0) for m in recent_metrics]
        if avg_wait_times:
            avg_wait = sum(avg_wait_times) / len(avg_wait_times)
            self.performance_metrics["system_efficiency"] = max(0, 1 - (avg_wait / 100))
        
        # Adaptation rate (rate of change in adaptation scores)
        adaptation_scores = [m.get("avg_adaptation_score", 0.5) for m in recent_metrics]
        if len(adaptation_scores) >= 2:
            adaptation_change = adaptation_scores[-1] - adaptation_scores[0]
            self.performance_metrics["adaptation_rate"] = adaptation_change
        
        # Emergence score (based on detected patterns)
        emergence_indicators = len(self.detected_patterns)
        self.performance_metrics["emergence_score"] = min(1.0, emergence_indicators / 5)
        
        # Stability score (low variance in key metrics)
        resource_utilizations = [m.get("resource_utilization", 0) for m in recent_metrics]
        if len(resource_utilizations) > 1:
            variance = sum((x - sum(resource_utilizations) / len(resource_utilizations)) ** 2 
                          for x in resource_utilizations) / len(resource_utilizations)
            self.performance_metrics["stability_score"] = max(0, 1 - variance)
    
    def get_current_metrics(self) -> Dict[str, Any]:
        """Get current system metrics"""
        return {
            **self.current_metrics,
            "performance_metrics": self.performance_metrics,
            "detected_patterns": self.detected_patterns,
            "agent_statistics": dict(self.agent_statistics),
            "interaction_statistics": dict(self.interaction_statistics)
        }
    
    def get_network_data(self) -> Dict[str, Any]:
        """Get current network data for visualization"""
        return self.current_network_data
    
    def get_historical_data(self, metric: str, steps: int = 50) -> List[float]:
        """Get historical data for a specific metric"""
        if not self.metrics_history:
            return []
        
        recent_history = list(self.metrics_history)[-steps:]
        return [m.get(metric, 0) for m in recent_history]
    
    def get_pattern_analysis(self) -> Dict[str, Any]:
        """Get analysis of detected patterns"""
        if not self.pattern_history:
            return {"patterns": [], "trends": {}}
        
        # Analyze pattern trends
        pattern_trends = defaultdict(list)
        for pattern_data in self.pattern_history:
            for pattern_name, pattern_info in pattern_data["patterns"].items():
                pattern_trends[pattern_name].append({
                    "timestamp": pattern_data["timestamp"],
                    "step": pattern_data["step"],
                    "data": pattern_info
                })
        
        # Calculate pattern stability
        stable_patterns = {}
        for pattern_name, occurrences in pattern_trends.items():
            if len(occurrences) >= 3:  # Pattern appeared multiple times
                stable_patterns[pattern_name] = {
                    "frequency": len(occurrences),
                    "first_seen": occurrences[0]["step"],
                    "last_seen": occurrences[-1]["step"],
                    "stability": len(occurrences) / len(self.pattern_history)
                }
        
        return {
            "current_patterns": self.detected_patterns,
            "stable_patterns": stable_patterns,
            "pattern_trends": dict(pattern_trends)
        }
    
    def export_data(self, format: str = "json") -> str:
        """Export collected data in specified format"""
        export_data = {
            "metadata": {
                "export_time": time.time(),
                "total_steps": len(self.metrics_history),
                "collection_period": self.metrics_history[-1]["timestamp"] - self.metrics_history[0]["timestamp"] if len(self.metrics_history) > 1 else 0
            },
            "metrics_history": list(self.metrics_history),
            "network_history": list(self.network_history),
            "pattern_analysis": self.get_pattern_analysis(),
            "performance_summary": self.performance_metrics
        }
        
        if format.lower() == "json":
            return json.dumps(export_data, indent=2)
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def reset(self):
        """Reset all collected data"""
        self.current_metrics = {}
        self.current_network_data = {"nodes": [], "links": []}
        self.metrics_history.clear()
        self.network_history.clear()
        self.interaction_history.clear()
        self.detected_patterns = {}
        self.pattern_history.clear()
        self.agent_statistics.clear()
        self.interaction_statistics.clear()
        
        # Reset performance metrics
        self.performance_metrics = {
            "system_efficiency": 0.0,
            "adaptation_rate": 0.0,
            "emergence_score": 0.0,
            "stability_score": 0.0
        }
        
        logger.info("Data collector reset")
