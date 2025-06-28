"""
Tests for cognitive development through boundary interactions
"""
import unittest
import time
from unittest.mock import MagicMock, patch
from backend.agents.fluid_boundary import FluidBoundarySystem, EnvironmentalExchangeSystem
from backend.agents.pet_environment import PetEnvironment, ObservableCognitiveDevelopment
from backend.agents.digital_pet import DigitalPet


class TestCognitiveDevelopment(unittest.TestCase):
    """Tests for cognitive development system."""
    
    def setUp(self):
        """Set up test environment"""
        self.pet = DigitalPet(name="TestPet", species="Test")
        self.cognitive_system = ObservableCognitiveDevelopment(self.pet.id)
        self.boundary_system = FluidBoundarySystem(self.pet.id)
        self.environment = PetEnvironment()
    
    def test_basic_development(self):
        """Test basic cognitive development from experiences."""
        # Get initial cognitive levels
        initial_cognition = self.cognitive_system.cognitive_areas.copy()
        
        # Process an experience
        result = self.cognitive_system.process_experience(
            "exploration",  # Type of experience
            0.7,            # Intensity
            {"curiosity": 0.8, "openness": 0.7}  # Relevant traits
        )
        
        # Verify cognitive growth
        self.assertTrue(result["success"])
        self.assertGreater(
            self.cognitive_system.cognitive_areas["pattern_recognition"],
            initial_cognition["pattern_recognition"]
        )
    
    def test_boundary_interaction_contributes_to_cognition(self):
        """Test that boundary interactions directly contribute to cognitive development."""
        # Set up exchange system
        exchange_system = EnvironmentalExchangeSystem(self.pet.id, self.boundary_system)
        
        # Create an environmental element that promotes learning
        element = {
            "type": "resource",
            "id": "information",
            "properties": {"name": "information", "amount": 10, "quality": 0.8},
            "difficulty": 0.5
        }
        
        # Mock cognitive system to track development
        original_process = self.cognitive_system.process_experience
        process_calls = []
        
        def mock_process_experience(experience_type, intensity, traits):
            process_calls.append((experience_type, intensity, traits))
            return original_process(experience_type, intensity, traits)
        
        self.cognitive_system.process_experience = mock_process_experience
        
        # Set up exchange system to use our cognitive system
        exchange_system.cognitive_system = self.cognitive_system
        
        # Process the information element
        exchange_system.process_element_impact(element)
        
        # Verify cognitive development was triggered
        self.assertGreaterEqual(len(process_calls), 1)
        self.assertEqual(process_calls[0][0], "information_processing")  # Experience type
    
    def test_cognitive_areas_develop_independently(self):
        """Test that different cognitive areas develop independently."""
        # Record initial cognitive values
        initial_pattern = self.cognitive_system.cognitive_areas["pattern_recognition"]
        initial_awareness = self.cognitive_system.cognitive_areas["environmental_awareness"]
        initial_boundary = self.cognitive_system.cognitive_areas["boundary_control"]
        
        # Process experiences targeting different areas
        self.cognitive_system.process_experience(
            "pattern_analysis",  # Focus on pattern recognition
            0.8,
            {"intelligence": 0.8}
        )
        
        self.cognitive_system.process_experience(
            "environment_mapping",  # Focus on environmental awareness
            0.7,
            {"perception": 0.8}
        )
        
        # Verify differential development
        pattern_increase = self.cognitive_system.cognitive_areas["pattern_recognition"] - initial_pattern
        awareness_increase = self.cognitive_system.cognitive_areas["environmental_awareness"] - initial_awareness
        boundary_increase = self.cognitive_system.cognitive_areas["boundary_control"] - initial_boundary
        
        # Pattern and environmental awareness should increase more than boundary control
        self.assertGreater(pattern_increase, 0)
        self.assertGreater(awareness_increase, 0)
        self.assertLess(boundary_increase, pattern_increase)
    
    def test_learning_from_beneficial_vs_harmful(self):
        """Test that learning occurs from both beneficial and harmful experiences."""
        # Record initial cognitive values
        initial_cognition = sum(self.cognitive_system.cognitive_areas.values())
        
        # Process a beneficial experience
        self.cognitive_system.process_experience(
            "positive_interaction",
            0.6,  # Moderate intensity
            {"resilience": 0.5}
        )
        
        beneficial_cognition = sum(self.cognitive_system.cognitive_areas.values())
        
        # Process a harmful experience
        self.cognitive_system.process_experience(
            "negative_interaction",
            0.8,  # High intensity (harmful experiences often teach more)
            {"resilience": 0.7}
        )
        
        harmful_cognition = sum(self.cognitive_system.cognitive_areas.values())
        
        # Verify both experiences contributed to learning
        self.assertGreater(beneficial_cognition, initial_cognition)
        self.assertGreater(harmful_cognition, beneficial_cognition)
    
    def test_development_plateaus(self):
        """Test that cognitive development shows diminishing returns."""
        # Set all cognitive areas near their maximum
        for area in self.cognitive_system.cognitive_areas:
            self.cognitive_system.cognitive_areas[area] = 0.9
        
        # Process several high-quality experiences
        gains = []
        
        for i in range(5):
            initial_sum = sum(self.cognitive_system.cognitive_areas.values())
            
            self.cognitive_system.process_experience(
                "advanced_learning",
                0.9,  # Very high intensity
                {"intelligence": 0.9, "openness": 0.9}  # Ideal traits
            )
            
            new_sum = sum(self.cognitive_system.cognitive_areas.values())
            gain = new_sum - initial_sum
            gains.append(gain)
        
        # Verify diminishing returns
        for i in range(len(gains) - 1):
            self.assertGreaterEqual(gains[i], gains[i+1])


class TestCognitiveEnvironmentInteraction(unittest.TestCase):
    """Tests for how cognition affects environment interaction."""
    
    def setUp(self):
        """Set up test environment"""
        self.pet = DigitalPet(name="TestPet", species="Test")
        self.cognitive_system = ObservableCognitiveDevelopment(self.pet.id)
        self.boundary_system = FluidBoundarySystem(self.pet.id)
        self.exchange_system = EnvironmentalExchangeSystem(self.pet.id, self.boundary_system)
        self.exchange_system.cognitive_system = self.cognitive_system
        self.environment = PetEnvironment()
    
    def test_pattern_recognition_improves_resource_finding(self):
        """Test that better pattern recognition improves resource finding."""
        # Create a randomized environment
        environment = PetEnvironment(seed=42)  # Fixed seed for reproducibility
        environment.add_element("hidden_food", 50, pattern=True)  # Add patterned resource
        
        # Set up two cognitive systems with different levels
        low_cognition = ObservableCognitiveDevelopment(self.pet.id + "_low")
        low_cognition.cognitive_areas["pattern_recognition"] = 0.2  # Low
        
        high_cognition = ObservableCognitiveDevelopment(self.pet.id + "_high")
        high_cognition.cognitive_areas["pattern_recognition"] = 0.9  # High
        
        # Mock exchange systems
        low_exchange = EnvironmentalExchangeSystem(self.pet.id + "_low", self.boundary_system)
        low_exchange.cognitive_system = low_cognition
        
        high_exchange = EnvironmentalExchangeSystem(self.pet.id + "_high", self.boundary_system)
        high_exchange.cognitive_system = high_cognition
        
        # Track discovered resources
        low_found = []
        high_found = []
        
        def mock_assimilate_low(element):
            low_found.append(element)
            return {"success": True, "element_id": element["id"]}
        
        def mock_assimilate_high(element):
            high_found.append(element)
            return {"success": True, "element_id": element["id"]}
        
        low_exchange.assimilate_element = mock_assimilate_low
        high_exchange.assimilate_element = mock_assimilate_high
        
        # Run several iterations of environment interaction
        env_state = environment.get_state()
        
        for _ in range(10):
            low_exchange.process_exchange(env_state)
            high_exchange.process_exchange(env_state)
        
        # Verify high cognition found more resources
        self.assertLess(len(low_found), len(high_found))
    
    def test_cognitive_memory_formation(self):
        """Test that memory traces form from significant experiences."""
        # Ensure memory system is empty at start
        self.cognitive_system.clear_memories()
        self.assertEqual(len(self.cognitive_system.get_memories()), 0)
        
        # Create a significant experience
        self.cognitive_system.process_experience(
            "significant_event",
            0.9,  # Very significant
            {"emotional_sensitivity": 0.8}
        )
        
        # Verify memory was created
        memories = self.cognitive_system.get_memories()
        self.assertGreaterEqual(len(memories), 1)
        self.assertEqual(memories[0]["type"], "significant_event")
    
    def test_memory_affects_future_behavior(self):
        """Test that memories affect future behavior choices."""
        # Create a memory of a negative experience with a specific element
        self.cognitive_system.clear_memories()
        self.cognitive_system.store_memory({
            "type": "negative_interaction",
            "subject": "toxic_element",
            "emotional_impact": -0.8,
            "time": time.time() - 100  # Recently
        })
        
        # Create elements for testing
        toxic_element = {
            "type": "resource",
            "id": "toxic_element",
            "properties": {"name": "toxin", "amount": 10},
            "difficulty": 0.5
        }
        
        neutral_element = {
            "type": "resource",
            "id": "neutral_element",
            "properties": {"name": "neutral", "amount": 10},
            "difficulty": 0.5
        }
        
        # Mock pet memory retrieval function
        def mock_retrieve_memory(subject):
            if subject == "toxic_element":
                return {
                    "type": "negative_interaction",
                    "subject": "toxic_element",
                    "emotional_impact": -0.8
                }
            return None
        
        self.pet.retrieve_memory = mock_retrieve_memory
        
        # Set exchange system to use pet for memory
        self.exchange_system.pet = self.pet
        
        # Check element desirability
        toxic_desire = self.exchange_system.calculate_element_desirability(toxic_element)
        neutral_desire = self.exchange_system.calculate_element_desirability(neutral_element)
        
        # Verify memory reduces desirability
        self.assertLess(toxic_desire, neutral_desire)


class TestLongTermDevelopment(unittest.TestCase):
    """Test long-term cognitive development patterns."""
    
    def setUp(self):
        """Set up test environment"""
        self.pet = DigitalPet(name="TestPet", species="Test")
        self.cognitive_system = ObservableCognitiveDevelopment(self.pet.id)
        self.boundary_system = FluidBoundarySystem(self.pet.id)
        self.exchange_system = EnvironmentalExchangeSystem(self.pet.id, self.boundary_system)
        self.environment = PetEnvironment()
    
    @unittest.skip("Long-running test, enable manually")
    def test_developmental_phases(self):
        """Test that pet development passes through expected phases."""
        # Reset cognitive areas
        for area in self.cognitive_system.cognitive_areas:
            self.cognitive_system.cognitive_areas[area] = 0.1
        
        # Run a long-term development simulation
        phases = []
        cognition_history = []
        
        # Simulate for 100 "days"
        for day in range(100):
            daily_cog = {}
            
            # Multiple experiences per day
            for _ in range(5):
                # Different experience types at different stages
                experience_type = "basic_learning"
                intensity = 0.5
                traits = {"curiosity": 0.5, "openness": 0.5}
                
                # Change experience type based on current development
                avg_cognition = sum(self.cognitive_system.cognitive_areas.values()) / len(self.cognitive_system.cognitive_areas)
                
                if avg_cognition > 0.3:
                    experience_type = "structured_learning"
                    intensity = 0.6
                    traits["intelligence"] = 0.6
                
                if avg_cognition > 0.6:
                    experience_type = "advanced_synthesis"
                    intensity = 0.7
                    traits["creativity"] = 0.7
                    traits["intelligence"] = 0.8
                
                # Process the experience
                self.cognitive_system.process_experience(experience_type, intensity, traits)
            
            # Record the state after each day
            avg_cognition = sum(self.cognitive_system.cognitive_areas.values()) / len(self.cognitive_system.cognitive_areas)
            cognition_history.append(avg_cognition)
            
            # Identify phase transitions
            if len(phases) == 0 and avg_cognition > 0.3:
                phases.append(("basic_to_intermediate", day))
            elif len(phases) == 1 and avg_cognition > 0.6:
                phases.append(("intermediate_to_advanced", day))
        
        # Verify developmental phases
        self.assertEqual(len(phases), 2)
        self.assertLess(phases[0][1], phases[1][1])
        
        # Verify growth pattern (should follow S-curve - slow start, rapid middle, plateau)
        early_growth = cognition_history[10] - cognition_history[0]
        middle_growth = cognition_history[50] - cognition_history[40]
        late_growth = cognition_history[90] - cognition_history[80]
        
        self.assertLess(early_growth, middle_growth)
        self.assertLess(late_growth, middle_growth)


if __name__ == '__main__':
    unittest.main()
