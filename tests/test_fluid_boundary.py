"""
Test the fluid boundary system for digital pets
"""
import unittest
import time
from backend.agents.fluid_boundary import FluidBoundarySystem, EnvironmentalExchangeSystem, PetEnergySystem
from backend.agents.pet_environment import PetEnvironment, ObservableCognitiveDevelopment

class TestFluidBoundary(unittest.TestCase):
    """Test the fluid boundary system"""
    
    def setUp(self):
        """Set up test environment"""
        self.pet_id = "test_pet_1"
        self.boundary_system = FluidBoundarySystem(self.pet_id)
        self.exchange_system = EnvironmentalExchangeSystem(self.pet_id, self.boundary_system)
        self.energy_system = PetEnergySystem(self.pet_id)
        self.environment = PetEnvironment()
        self.cognitive_system = ObservableCognitiveDevelopment(self.pet_id)
    
    def test_boundary_maintenance(self):
        """Test that boundary requires energy for maintenance"""
        # Get environment state
        env_state = self.environment.get_state()
        
        # Initial boundary state
        initial_permeability = self.boundary_system.boundary_permeability
        
        # Update with sufficient energy
        result = self.boundary_system.update(env_state, 10.0)
        self.assertEqual(result["boundary_status"], "maintained")
        self.assertLess(result["permeability"], initial_permeability)
        
        # Update with insufficient energy
        result = self.boundary_system.update(env_state, 0.1)
        self.assertEqual(result["boundary_status"], "failing")
        self.assertGreater(result["permeability"], initial_permeability)
    
    def test_assimilation(self):
        """Test element assimilation through boundary"""
        # Create an environmental element
        element = {
            "type": "resource",
            "id": "test_resource",
            "properties": {"name": "food", "amount": 10},
            "difficulty": 0.3
        }
        
        # Make boundary highly permeable for testing
        self.boundary_system.boundary_permeability = 0.9
        
        # Try to assimilate
        result = self.exchange_system.assimilate_element(element)
        self.assertTrue(result["success"])
        self.assertIn("element_id", result)
        
        # Make boundary rigid
        self.boundary_system.boundary_permeability = 0.1
        
        # Try to assimilate again - should fail
        result = self.exchange_system.assimilate_element(element)
        self.assertFalse(result["success"])
    
    def test_energy_allocation(self):
        """Test energy allocation priorities"""
        env_state = self.environment.get_state()
        
        # Set initial energy
        self.energy_system.energy = 100.0
        
        # Step the energy system
        result = self.energy_system.step(env_state)
        
        # Verify allocations
        self.assertIn("boundary_maintenance", result["allocations"])
        self.assertGreater(result["allocations"]["boundary_maintenance"], 0)
        self.assertLess(result["energy_level"], 100.0)
    
    def test_cognitive_development(self):
        """Test cognitive development through experiences"""
        # Get initial cognitive levels
        initial_cognition = self.cognitive_system.cognitive_areas.copy()
        
        # Process an experience
        result = self.cognitive_system.process_experience(
            "exploration",
            0.8,  # High intensity
            {"curiosity": 0.8, "openness": 0.7}  # Good traits for learning
        )
        
        # Verify cognitive growth
        self.assertGreater(
            self.cognitive_system.cognitive_areas["environmental_awareness"],
            initial_cognition["environmental_awareness"]
        )
        self.assertGreater(
            self.cognitive_system.cognitive_areas["pattern_recognition"],
            initial_cognition["pattern_recognition"]
        )
    
    def test_environment_state(self):
        """Test environment state updates"""
        # Get initial state
        initial_state = self.environment.get_state()
        initial_time = initial_state["time_of_day"]
        
        # Step the environment
        updated_state = self.environment.step()
        
        # Verify changes
        self.assertNotEqual(updated_state["time_of_day"], initial_time)
        self.assertIn("weather", updated_state)
        self.assertIn("ambient_energy", updated_state)

if __name__ == '__main__':
    unittest.main()
