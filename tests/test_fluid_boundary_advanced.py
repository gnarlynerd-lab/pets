"""
Advanced tests for the fluid boundary system with environment integration
"""
import unittest
import time
import pytest
from unittest.mock import MagicMock, patch
from backend.agents.fluid_boundary import FluidBoundarySystem, EnvironmentalExchangeSystem, PetEnergySystem
from backend.agents.pet_environment import PetEnvironment, ObservableCognitiveDevelopment
from backend.agents.digital_pet import DigitalPet


class TestBoundaryPermeability(unittest.TestCase):
    """Advanced tests for boundary permeability calculations."""
    
    def setUp(self):
        """Set up test environment"""
        self.pet = DigitalPet(name="TestPet", species="Test")
        self.boundary_system = FluidBoundarySystem(self.pet.id)
        self.environment = PetEnvironment()
    
    def test_emotional_state_impact(self):
        """Test that emotional states correctly impact boundary permeability."""
        # Get baseline permeability
        baseline = self.boundary_system.boundary_permeability
        
        # Test with stressed state
        with patch.object(self.pet, 'get_emotional_state', return_value="stressed"):
            self.boundary_system.update(self.environment.get_state(), 10.0)
        
        stressed_permeability = self.boundary_system.boundary_permeability
        self.assertLess(stressed_permeability, baseline)
        
        # Reset
        self.boundary_system.boundary_permeability = baseline
        
        # Test with relaxed state
        with patch.object(self.pet, 'get_emotional_state', return_value="relaxed"):
            self.boundary_system.update(self.environment.get_state(), 10.0)
        
        relaxed_permeability = self.boundary_system.boundary_permeability
        self.assertGreater(relaxed_permeability, baseline)
    
    def test_environmental_pressure(self):
        """Test that environmental pressure affects boundary permeability."""
        # Get baseline with normal environment
        normal_env = self.environment.get_state()
        baseline = self.boundary_system.boundary_permeability
        
        # Create high-pressure environment
        self.environment.set_weather("storm")
        self.environment.add_element("stress", 50)
        high_pressure_env = self.environment.get_state()
        
        # Update boundary with high pressure environment
        self.boundary_system.update(high_pressure_env, 10.0)
        high_pressure_permeability = self.boundary_system.boundary_permeability
        
        # Verify boundary responds by becoming less permeable
        self.assertLess(high_pressure_permeability, baseline)
    
    def test_gradual_adaptation(self):
        """Test that boundaries gradually adapt to consistent environments."""
        # Set up challenging environment
        self.environment.set_weather("storm")
        self.environment.add_element("toxin", 20)
        challenging_env = self.environment.get_state()
        
        # Record permeability changes over time
        permeabilities = []
        
        # Make multiple updates
        for _ in range(10):
            result = self.boundary_system.update(challenging_env, 10.0)
            permeabilities.append(result["permeability"])
        
        # Verify gradual adaptation (permeability should decrease)
        self.assertGreater(permeabilities[0], permeabilities[-1])
        
        # Verify adaptation is gradual (not sudden jumps)
        diffs = [permeabilities[i] - permeabilities[i+1] for i in range(len(permeabilities)-1)]
        max_diff = max(diffs)
        self.assertLess(max_diff, 0.2)  # No sudden large jumps


class TestElementExchange(unittest.TestCase):
    """Advanced tests for element exchange across boundaries."""
    
    def setUp(self):
        """Set up test environment"""
        self.pet = DigitalPet(name="TestPet", species="Test")
        self.boundary_system = FluidBoundarySystem(self.pet.id)
        self.exchange_system = EnvironmentalExchangeSystem(self.pet.id, self.boundary_system)
        self.environment = PetEnvironment()
    
    def test_selective_permeability(self):
        """Test that boundaries can be selectively permeable to different elements."""
        # Add beneficial and harmful elements to environment
        self.environment.add_element("nutrient", 100)
        self.environment.add_element("toxin", 100)
        env_state = self.environment.get_state()
        
        # Set up pet's element preferences (mocked)
        with patch.object(self.pet, 'get_element_preference') as mock_pref:
            # Set preferences: high for nutrients, low for toxin
            def side_effect(element_type):
                if element_type == "nutrient": return 0.9
                if element_type == "toxin": return 0.1
                return 0.5
            
            mock_pref.side_effect = side_effect
            
            # Track absorbed elements
            absorbed_elements = {}
            
            # Mock the assimilate method to track what's absorbed
            def mock_assimilate(element):
                element_type = element["properties"]["name"]
                if element_type not in absorbed_elements:
                    absorbed_elements[element_type] = 0
                
                absorbed_elements[element_type] += element["properties"]["amount"]
                return {"success": True, "element_id": element["id"]}
                
            self.exchange_system.assimilate_element = mock_assimilate
            
            # Perform exchange
            self.exchange_system.process_exchange(env_state)
            
            # Verify more nutrients were absorbed than toxins
            self.assertIn("nutrient", absorbed_elements)
            self.assertIn("toxin", absorbed_elements)
            self.assertGreater(absorbed_elements["nutrient"], absorbed_elements["toxin"])
    
    def test_exchange_energy_economics(self):
        """Test energy costs of various exchange types."""
        # Create elements with different exchange costs
        easy_element = {
            "type": "resource",
            "id": "easy_resource",
            "properties": {"name": "water", "amount": 10},
            "difficulty": 0.1  # Easy to absorb
        }
        
        hard_element = {
            "type": "resource",
            "id": "hard_resource",
            "properties": {"name": "mineral", "amount": 10},
            "difficulty": 0.8  # Hard to absorb
        }
        
        # Mock energy system to track costs
        mock_energy_system = MagicMock()
        mock_energy_system.allocate_energy.return_value = True
        self.exchange_system.energy_system = mock_energy_system
        
        # Assimilate both elements
        self.exchange_system.assimilate_element(easy_element)
        self.exchange_system.assimilate_element(hard_element)
        
        # Verify different energy allocations
        calls = mock_energy_system.allocate_energy.call_args_list
        self.assertEqual(len(calls), 2)
        
        # First call is for easy_element, second for hard_element
        easy_cost = calls[0][0][0]  # First arg of first call
        hard_cost = calls[1][0][0]  # First arg of second call
        
        # Hard element should cost more energy
        self.assertLess(easy_cost, hard_cost)


class TestPetEnvironmentIntegration(unittest.TestCase):
    """Tests for complete integration of pet, boundary, and environment."""
    
    def setUp(self):
        """Set up test environment"""
        self.pet = DigitalPet(name="TestPet", species="Test")
        self.boundary_system = FluidBoundarySystem(self.pet.id)
        self.exchange_system = EnvironmentalExchangeSystem(self.pet.id, self.boundary_system)
        self.energy_system = PetEnergySystem(self.pet.id)
        self.environment = PetEnvironment()
        self.cognitive_system = ObservableCognitiveDevelopment(self.pet.id)
    
    def test_environment_adaptation_scenario(self):
        """Test full integration of systems in an adaptation scenario."""
        # Initialize systems
        self.energy_system.energy = 100.0
        
        # Set up initial environment
        self.environment.set_weather("sunny")
        self.environment.add_element("food", 50)
        self.environment.add_element("water", 50)
        
        # Store initial states
        initial_energy = self.energy_system.energy
        initial_permeability = self.boundary_system.boundary_permeability
        
        # Run normal simulation for a few steps
        for _ in range(5):
            # Get environment state
            env_state = self.environment.get_state()
            
            # Allocate energy
            energy_result = self.energy_system.step(env_state)
            boundary_energy = energy_result["allocations"]["boundary_maintenance"]
            
            # Update boundary
            boundary_result = self.boundary_system.update(env_state, boundary_energy)
            
            # Process exchanges
            self.exchange_system.process_exchange(env_state)
            
            # Process cognitive development
            self.cognitive_system.process_experience(
                "normal_day", 
                0.5,  # Moderate intensity
                {"curiosity": 0.5}
            )
        
        # Verify stable state after normal conditions
        self.assertGreater(self.energy_system.energy, 50)  # Still has plenty of energy
        self.assertLess(abs(self.boundary_system.boundary_permeability - initial_permeability), 0.3)
        
        # Now introduce a challenging environment
        self.environment.set_weather("storm")
        self.environment.add_element("toxin", 30)
        self.environment.set_temperature(5)  # Cold
        
        # Run simulation in challenging environment
        for _ in range(10):
            # Get environment state
            env_state = self.environment.get_state()
            
            # Allocate energy
            energy_result = self.energy_system.step(env_state)
            boundary_energy = energy_result["allocations"]["boundary_maintenance"]
            
            # Update boundary
            boundary_result = self.boundary_system.update(env_state, boundary_energy)
            
            # Process exchanges
            self.exchange_system.process_exchange(env_state)
            
            # Process cognitive development
            self.cognitive_system.process_experience(
                "storm_survival", 
                0.8,  # High intensity
                {"resilience": 0.7, "adaptability": 0.8}
            )
        
        # Verify adaptation to challenging conditions
        self.assertLess(self.boundary_system.boundary_permeability, initial_permeability)
        self.assertLess(self.energy_system.energy, initial_energy)
        
        # Verify cognitive development
        self.assertGreater(self.cognitive_system.cognitive_areas["environmental_awareness"], 0.5)
        self.assertGreater(self.cognitive_system.cognitive_areas["survival_instinct"], 0.5)
    
    def test_boundary_cognitive_feedback_loop(self):
        """Test that cognitive development improves boundary control."""
        # Set initial cognitive levels
        initial_cognition = 0.2
        self.cognitive_system.cognitive_areas["boundary_control"] = initial_cognition
        
        # First boundary adjustment with low cognition
        initial_permeability = self.boundary_system.boundary_permeability
        target_permeability = initial_permeability - 0.2
        
        # Track energy required for adjustment
        self.energy_system.energy = 100
        
        # Try to adjust boundary
        adjustment_cost_low_cognition = self.boundary_system.adjust_permeability(
            target_permeability,
            self.cognitive_system.cognitive_areas["boundary_control"]
        )
        
        # Now increase cognitive level
        self.cognitive_system.cognitive_areas["boundary_control"] = 0.8  # Much higher
        
        # Reset energy and boundary
        self.energy_system.energy = 100
        self.boundary_system.boundary_permeability = initial_permeability
        
        # Try to adjust boundary again
        adjustment_cost_high_cognition = self.boundary_system.adjust_permeability(
            target_permeability,
            self.cognitive_system.cognitive_areas["boundary_control"]
        )
        
        # Verify higher cognition reduces energy cost
        self.assertLess(adjustment_cost_high_cognition, adjustment_cost_low_cognition)


class TestPerformance(unittest.TestCase):
    """Performance tests for fluid boundary system."""
    
    def test_calculation_efficiency(self):
        """Test that boundary calculations are efficient."""
        pet_id = "test_pet"
        boundary = FluidBoundarySystem(pet_id)
        environment = PetEnvironment()
        env_state = environment.get_state()
        
        # Measure time to perform 1000 permeability calculations
        start_time = time.time()
        
        for _ in range(1000):
            boundary.calculate_permeability(env_state)
        
        duration = time.time() - start_time
        
        # Each calculation should take < 0.1ms on average (100ms for 1000 iterations)
        self.assertLess(duration, 0.1)
    
    @unittest.skip("Long-running performance test, enable manually")
    def test_system_scaling(self):
        """Test system performance with multiple pets."""
        num_pets = 50  # Test with 50 pets
        environment = PetEnvironment()
        
        # Create pets and systems
        boundaries = []
        exchange_systems = []
        energy_systems = []
        
        for i in range(num_pets):
            pet_id = f"test_pet_{i}"
            boundary = FluidBoundarySystem(pet_id)
            exchange = EnvironmentalExchangeSystem(pet_id, boundary)
            energy = PetEnergySystem(pet_id)
            energy.energy = 100
            
            boundaries.append(boundary)
            exchange_systems.append(exchange)
            energy_systems.append(energy)
        
        # Get environment state
        env_state = environment.get_state()
        
        # Measure performance for a full update cycle
        start_time = time.time()
        
        # Update all pets
        for i in range(num_pets):
            # Energy allocation
            energy_result = energy_systems[i].step(env_state)
            boundary_energy = energy_result["allocations"].get("boundary_maintenance", 0)
            
            # Boundary update
            boundary_result = boundaries[i].update(env_state, boundary_energy)
            
            # Exchange processing
            exchange_systems[i].process_exchange(env_state)
        
        duration = time.time() - start_time
        
        # Updates should complete in reasonable time (< 1s for 50 pets)
        self.assertLess(duration, 1.0)


if __name__ == '__main__':
    unittest.main()
