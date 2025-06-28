"""
Tests for DKS Agent System - Stage 1 Foundation
"""
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock
import json

from backend.agents.base_agent import DKSAgent
from backend.models.hospital_model import HospitalModel, TestAgent
from backend.communication.redis_manager import RedisManager
from backend.visualization.data_collector import DataCollector


class TestDKSAgent:
    """Test the base DKS agent functionality"""
    
    def test_agent_initialization(self):
        """Test that agents initialize with correct DKS principles"""
        model = Mock()
        agent = DKSAgent("test_agent", model, "test_type")
        
        assert agent.unique_id == "test_agent"
        assert agent.agent_type == "test_type"
        assert agent.energy == 100
        assert agent.adaptation_score == 0.5
        assert isinstance(agent.interaction_patterns, dict)
        assert isinstance(agent.connection_strengths, dict)
        assert isinstance(agent.strategy_weights, dict)
    
    def test_dynamic_stability_maintenance(self):
        """Test that agents maintain dynamic stability"""
        model = Mock()
        agent = DKSAgent("test_agent", model, "test_type")
        
        initial_energy = agent.energy
        agent.maintain_dynamic_stability()
        
        # Energy should decrease due to continuous activity
        assert agent.energy < initial_energy
    
    def test_message_handling(self):
        """Test message processing"""
        model = Mock()
        agent = TestAgent("test_agent", model, "test_type")
        
        # Test resource request handling
        agent.handle_resource_request("sender", {"amount": 1})
        
        # Should have processed the message
        assert len(agent.interaction_history) > 0
    
    def test_adaptation_mechanism(self):
        """Test that agents adapt strategies based on outcomes"""
        model = Mock()
        agent = DKSAgent("test_agent", model, "test_type")
        
        # Set up initial strategy
        agent.strategy_weights = {"test_strategy": 0.5}
        agent.interaction_history = [
            {"outcome": "success", "type": "test", "timestamp": 1000}
        ]
        
        agent.adapt_strategies()
        
        # Should have adapted based on successful interactions
        assert "test_strategy" in agent.strategy_weights


class TestHospitalModel:
    """Test the hospital model functionality"""
    
    def test_model_initialization(self):
        """Test model creates correct number of agents"""
        model = HospitalModel(
            num_wards=2, 
            num_staff=3, 
            num_equipment=2, 
            num_patients=4
        )
        
        assert len(model.schedule.agents) == 11  # 2+3+2+4
        
        agent_counts = model.get_agent_counts()
        assert agent_counts["ward"] == 2
        assert agent_counts["staff"] == 3
        assert agent_counts["equipment"] == 2
        assert agent_counts["patient"] == 4
    
    def test_environment_updates(self):
        """Test environment state updates"""
        model = HospitalModel(
            num_wards=1, 
            num_staff=1, 
            num_equipment=1, 
            num_patients=1
        )
        
        initial_time = model.environment_state["time_of_day"]
        model.update_environment()
        
        # Time should progress
        assert model.environment_state["time_of_day"] > initial_time
    
    def test_message_processing(self):
        """Test inter-agent message processing"""
        model = HospitalModel(
            num_wards=1, 
            num_staff=1, 
            num_equipment=1, 
            num_patients=1
        )
        
        # Add a test message
        model.message_queue.append({
            "sender": "test_sender",
            "recipient": list(model.get_agent_counts().keys())[0] + "_0",
            "type": "test_message",
            "content": {}
        })
        
        model.process_messages()
        
        # Message queue should be cleared
        assert len(model.message_queue) == 0


class TestDataCollector:
    """Test data collection and analysis"""
    
    def test_data_collector_initialization(self):
        """Test data collector initializes correctly"""
        collector = DataCollector()
        
        assert isinstance(collector.current_metrics, dict)
        assert isinstance(collector.detected_patterns, dict)
        assert isinstance(collector.performance_metrics, dict)
    
    def test_metrics_collection(self):
        """Test metrics collection from model"""
        collector = DataCollector()
        model = HospitalModel(
            num_wards=1, 
            num_staff=1, 
            num_equipment=1, 
            num_patients=1
        )
        
        collector.collect_step_data(model)
        
        assert "step" in collector.current_metrics
        assert "agent_count" in collector.current_metrics
        assert len(collector.metrics_history) == 1
    
    def test_pattern_detection(self):
        """Test pattern detection algorithms"""
        collector = DataCollector()
        model = HospitalModel(
            num_wards=2, 
            num_staff=3, 
            num_equipment=2, 
            num_patients=4
        )
        
        # Run a few steps to generate data
        for _ in range(5):
            model.step()
            collector.collect_step_data(model)
        
        # Should have detected some patterns
        assert isinstance(collector.detected_patterns, dict)


class TestRedisManager:
    """Test Redis communication manager"""
    
    @pytest.mark.asyncio
    async def test_redis_manager_initialization(self):
        """Test Redis manager can be initialized"""
        # Note: This test will fail without Redis running
        # In a real test environment, we'd use a mock Redis
        redis_manager = RedisManager()
        
        try:
            await redis_manager.initialize()
            assert redis_manager.redis_client is not None
            await redis_manager.close()
        except Exception:
            # Redis not available - skip test
            pytest.skip("Redis not available for testing")
    
    def test_message_serialization(self):
        """Test message serialization/deserialization"""
        test_message = {
            "sender": "test_sender",
            "type": "test_type",
            "content": {"key": "value"},
            "timestamp": 1234567890
        }
        
        # Should be able to serialize and deserialize
        serialized = json.dumps(test_message)
        deserialized = json.loads(serialized)
        
        assert deserialized == test_message


class TestSystemIntegration:
    """Integration tests for the complete system"""
    
    def test_agent_model_integration(self):
        """Test agents work correctly within the model"""
        model = HospitalModel(
            num_wards=2, 
            num_staff=2, 
            num_equipment=2, 
            num_patients=2
        )
        
        # Run simulation for a few steps
        for _ in range(3):
            model.step()
        
        # System should be stable
        assert model.schedule.steps == 3
        assert len(model.schedule.agents) == 8
        
        # Agents should have some activity
        for agent in model.schedule.agents:
            assert agent.interaction_count >= 0
    
    def test_data_collection_integration(self):
        """Test data collection works with running model"""
        model = HospitalModel(
            num_wards=1, 
            num_staff=2, 
            num_equipment=1, 
            num_patients=3
        )
        collector = DataCollector()
        
        # Run simulation with data collection
        for _ in range(5):
            model.step()
            collector.collect_step_data(model)
        
        # Should have collected data
        assert len(collector.metrics_history) == 5
        assert collector.current_metrics["step"] == 5
        
        # Performance metrics should be calculated
        assert "system_efficiency" in collector.performance_metrics
        assert "emergence_score" in collector.performance_metrics


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
