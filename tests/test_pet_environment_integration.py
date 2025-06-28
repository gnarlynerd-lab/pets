"""
Integration tests for pet, environment and fluid boundary interaction
"""
import unittest
import time
from unittest.mock import MagicMock, patch
import pytest
from backend.agents.fluid_boundary import FluidBoundarySystem, EnvironmentalExchangeSystem, PetEnergySystem
from backend.agents.pet_environment import PetEnvironment, ObservableCognitiveDevelopment
from backend.agents.digital_pet import DigitalPet
from backend.models.pet_model import PetModel


class TestPetEnvironmentAPI(unittest.TestCase):
    """Test suite for pet-environment API integration."""
    
    def setUp(self):
        """Set up test environment"""
        self.pet_model = PetModel(pet_id="test_pet_1", name="TestPet", species="Testimal")
        self.pet = DigitalPet(name=self.pet_model.name, species=self.pet_model.species, pet_id=self.pet_model.pet_id)
        self.boundary_system = FluidBoundarySystem(self.pet.id)
        self.exchange_system = EnvironmentalExchangeSystem(self.pet.id, self.boundary_system)
        self.energy_system = PetEnergySystem(self.pet.id)
        self.environment = PetEnvironment()
        self.cognitive_system = ObservableCognitiveDevelopment(self.pet.id)
    
    def test_pet_environment_data_collection(self):
        """Test that pet model correctly collects environment interaction data."""
        # Set up mock for model's data collection
        data_collected = []
        
        def mock_add_environment_data(env_data):
            data_collected.append(env_data)
            
        self.pet_model.add_environment_interaction_data = mock_add_environment_data
        
        # Create an environment interaction
        env_state = self.environment.get_state()
        interaction = {
            "action": "explore", 
            "time": env_state["time_of_day"],
            "weather": env_state["weather"],
            "result": "found_resource",
            "resource_type": "food",
            "boundary_state": self.boundary_system.boundary_permeability
        }
        
        # Record the interaction
        self.pet_model.add_environment_interaction_data(interaction)
        
        # Verify data was collected
        self.assertEqual(len(data_collected), 1)
        self.assertEqual(data_collected[0]["action"], "explore")
        self.assertEqual(data_collected[0]["result"], "found_resource")
    
    def test_boundary_metrics_recording(self):
        """Test that boundary metrics are recorded correctly."""
        # Set up mock for model's metric recording
        recorded_metrics = {}
        
        def mock_record_metric(name, value):
            recorded_metrics[name] = value
            
        self.pet_model.record_metric = mock_record_metric
        
        # Generate some boundary metrics
        boundary_metrics = {
            "permeability": self.boundary_system.boundary_permeability,
            "stability": 0.75,
            "energy_cost": 2.5,
            "element_transfers": 3
        }
        
        # Record metrics
        for name, value in boundary_metrics.items():
            self.pet_model.record_metric(f"boundary_{name}", value)
        
        # Verify metrics were recorded
        for name, value in boundary_metrics.items():
            metric_name = f"boundary_{name}"
            self.assertIn(metric_name, recorded_metrics)
            self.assertEqual(recorded_metrics[metric_name], value)
    
    def test_cognitive_development_tracking(self):
        """Test that cognitive development is tracked in pet model."""
        # Set up mock for cognitive data tracking
        cognitive_data = []
        
        def mock_add_cognitive_data(data):
            cognitive_data.append(data)
            
        self.pet_model.add_cognitive_development_data = mock_add_cognitive_data
        
        # Generate cognitive development event
        cognitive_event = {
            "timestamp": time.time(),
            "event_type": "learning",
            "cognitive_areas": self.cognitive_system.cognitive_areas.copy(),
            "growth_rate": 0.05
        }
        
        # Record the event
        self.pet_model.add_cognitive_development_data(cognitive_event)
        
        # Verify data was collected
        self.assertEqual(len(cognitive_data), 1)
        self.assertEqual(cognitive_data[0]["event_type"], "learning")
        self.assertIn("cognitive_areas", cognitive_data[0])


class TestPetBehaviorEnvironmentResponse(unittest.TestCase):
    """Test suite for pet behavior responding to environment."""
    
    def setUp(self):
        """Set up test environment"""
        self.pet = DigitalPet(name="TestPet", species="Test")
        self.boundary_system = FluidBoundarySystem(self.pet.id)
        self.environment = PetEnvironment()
    
    def test_weather_affects_behavior_options(self):
        """Test that weather affects available behavior options."""
        # Set different weather conditions and check behaviors
        self.environment.set_weather("sunny")
        sunny_env = self.environment.get_state()
        
        self.environment.set_weather("rainy")
        rainy_env = self.environment.get_state()
        
        self.environment.set_weather("stormy")
        stormy_env = self.environment.get_state()
        
        # Get behavior options for each environment
        sunny_behaviors = self.pet.get_behavior_options(sunny_env)
        rainy_behaviors = self.pet.get_behavior_options(rainy_env)
        stormy_behaviors = self.pet.get_behavior_options(stormy_env)
        
        # Verify differences in available behaviors
        self.assertIn("sunbathe", sunny_behaviors)
        self.assertNotIn("sunbathe", rainy_behaviors)
        self.assertNotIn("sunbathe", stormy_behaviors)
        
        self.assertIn("seek_shelter", stormy_behaviors)
        self.assertIn("play_in_puddles", rainy_behaviors)
    
    def test_resource_availability_affects_behavior(self):
        """Test that resource availability affects behavior choices."""
        # Create environments with different resources
        food_env = self.environment.copy()
        food_env.add_element("food", 100)
        
        no_food_env = self.environment.copy()
        if "food" in no_food_env.elements:
            no_food_env.remove_element("food")
        
        # Get behavior options
        with_food_behaviors = self.pet.get_behavior_options(food_env.get_state())
        without_food_behaviors = self.pet.get_behavior_options(no_food_env.get_state())
        
        # Verify differences
        self.assertIn("eat", with_food_behaviors)
        self.assertNotIn("eat", without_food_behaviors)
        self.assertIn("search_for_food", without_food_behaviors)
    
    def test_pet_adapts_behavior_to_environment(self):
        """Test that pet adapts behavior to environment over time."""
        # Set up a specific environment
        self.environment.set_weather("hot")
        self.environment.add_element("water", 20)
        hot_env = self.environment.get_state()
        
        # Track behavior selections
        behavior_counts = {}
        
        # Simulate multiple behavior selections
        for _ in range(20):
            # Select behavior
            behavior = self.pet.select_behavior(hot_env)
            
            # Count occurrences
            if behavior not in behavior_counts:
                behavior_counts[behavior] = 0
            behavior_counts[behavior] += 1
            
            # Simulate performing the behavior
            self.pet.perform_behavior(behavior, hot_env)
        
        # Verify adaptation - should prefer cooling behaviors in hot weather
        cooling_behaviors = ["find_shade", "drink", "rest", "swim"]
        heating_behaviors = ["sunbathe", "run", "exercise"]
        
        cooling_count = sum(behavior_counts.get(b, 0) for b in cooling_behaviors)
        heating_count = sum(behavior_counts.get(b, 0) for b in heating_behaviors)
        
        self.assertGreater(cooling_count, heating_count)
    
    def test_boundary_state_affects_behavior(self):
        """Test that boundary state affects behavior selection."""
        # Set up environment
        env_state = self.environment.get_state()
        
        # Test with different boundary states
        self.boundary_system.boundary_permeability = 0.2  # Very closed
        self.pet.boundary_system = self.boundary_system
        closed_behaviors = self.pet.get_behavior_options(env_state)
        closed_behavior = self.pet.select_behavior(env_state)
        
        self.boundary_system.boundary_permeability = 0.8  # Very open
        open_behaviors = self.pet.get_behavior_options(env_state)
        open_behavior = self.pet.select_behavior(env_state)
        
        # Verify differences
        self.assertGreaterEqual(len(open_behaviors), len(closed_behaviors))
        
        # With closed boundary, should prefer protective behaviors
        self.assertIn("rest", closed_behaviors)
        
        # With open boundary, should be more explorative
        self.assertIn("explore", open_behaviors)


class TestFullIntegrationSimulation(unittest.TestCase):
    """Test full integration of all systems in a long-term simulation."""
    
    def setUp(self):
        """Set up test environment"""
        self.pet = DigitalPet(name="TestPet", species="Test")
        self.boundary_system = FluidBoundarySystem(self.pet.id)
        self.exchange_system = EnvironmentalExchangeSystem(self.pet.id, self.boundary_system)
        self.energy_system = PetEnergySystem(self.pet.id)
        self.environment = PetEnvironment()
        self.cognitive_system = ObservableCognitiveDevelopment(self.pet.id)
        
        # Connect systems
        self.pet.boundary_system = self.boundary_system
        self.pet.energy_system = self.energy_system
        self.pet.cognitive_system = self.cognitive_system
        
        self.exchange_system.energy_system = self.energy_system
        self.exchange_system.cognitive_system = self.cognitive_system
    
    @unittest.skip("Long-running test, enable manually")
    def test_day_night_cycle_adaptation(self):
        """Test that pet adapts to day/night cycle appropriately."""
        # Set up tracking for behaviors and states
        day_behaviors = []
        night_behaviors = []
        boundary_states = []
        energy_levels = []
        
        # Run a simulation for multiple day/night cycles
        for hour in range(72):  # 3 days
            # Update environment time
            self.environment.set_time(hour % 24)
            env_state = self.environment.get_state()
            
            # Record if it's day or night
            is_day = 6 <= (hour % 24) < 18
            
            # Select and perform behavior
            behavior = self.pet.select_behavior(env_state)
            self.pet.perform_behavior(behavior, env_state)
            
            # Process energy allocation
            energy_result = self.energy_system.step(env_state)
            boundary_energy = energy_result["allocations"].get("boundary_maintenance", 0)
            
            # Update boundary
            boundary_result = self.boundary_system.update(env_state, boundary_energy)
            
            # Process exchanges
            self.exchange_system.process_exchange(env_state)
            
            # Record data
            if is_day:
                day_behaviors.append(behavior)
            else:
                night_behaviors.append(behavior)
                
            boundary_states.append(self.boundary_system.boundary_permeability)
            energy_levels.append(self.energy_system.energy)
            
            # Short rest between steps
            time.sleep(0.01)
        
        # Verify day/night behavior differences
        day_active_behaviors = ["play", "explore", "run", "sunbathe"]
        night_active_behaviors = ["sleep", "rest", "groom"]
        
        day_active_count = sum(1 for b in day_behaviors if b in day_active_behaviors)
        night_active_count = sum(1 for b in night_behaviors if b in day_active_behaviors)
        
        day_rest_count = sum(1 for b in day_behaviors if b in night_active_behaviors)
        night_rest_count = sum(1 for b in night_behaviors if b in night_active_behaviors)
        
        # Day should have more active behaviors
        self.assertGreater(day_active_count / len(day_behaviors), 
                          night_active_count / len(night_behaviors))
        
        # Night should have more resting behaviors
        self.assertGreater(night_rest_count / len(night_behaviors),
                          day_rest_count / len(day_behaviors))
        
        # Verify boundary permeability cycle
        day_permeability = []
        night_permeability = []
        
        for i, hour in enumerate(range(72)):
            if 6 <= (hour % 24) < 18:
                day_permeability.append(boundary_states[i])
            else:
                night_permeability.append(boundary_states[i])
        
        # Daytime should have higher average permeability
        avg_day = sum(day_permeability) / len(day_permeability)
        avg_night = sum(night_permeability) / len(night_permeability)
        self.assertGreater(avg_day, avg_night)
    
    @unittest.skip("Long-running test, enable manually")
    def test_resilience_to_environmental_changes(self):
        """Test pet resilience to environmental changes."""
        # Initial stable phase
        self.environment.set_weather("sunny")
        self.environment.add_element("food", 100)
        self.environment.add_element("water", 100)
        
        # Track metrics
        stability_metrics = []
        
        # Run stable period
        for _ in range(20):
            env_state = self.environment.get_state()
            self.run_simulation_step(env_state)
            stability_metrics.append(self.get_stability_metric())
        
        avg_stable = sum(stability_metrics) / len(stability_metrics)
        
        # Introduce environmental challenge
        self.environment.set_weather("storm")
        self.environment.add_element("toxin", 30)
        self.environment.remove_element("food")
        
        # Track metrics during challenge
        challenge_metrics = []
        
        # Run challenge period
        for _ in range(20):
            env_state = self.environment.get_state()
            self.run_simulation_step(env_state)
            challenge_metrics.append(self.get_stability_metric())
        
        avg_challenge = sum(challenge_metrics) / len(challenge_metrics)
        
        # Challenge should decrease stability
        self.assertLess(avg_challenge, avg_stable)
        
        # Recovery period
        self.environment.set_weather("sunny")
        self.environment.remove_element("toxin")
        self.environment.add_element("food", 100)
        
        # Track metrics during recovery
        recovery_metrics = []
        
        # Run recovery period
        for _ in range(30):
            env_state = self.environment.get_state()
            self.run_simulation_step(env_state)
            recovery_metrics.append(self.get_stability_metric())
        
        # Check recovery pattern - should improve over time
        avg_early_recovery = sum(recovery_metrics[:10]) / 10
        avg_late_recovery = sum(recovery_metrics[-10:]) / 10
        
        # Later recovery should be better than early recovery
        self.assertGreater(avg_late_recovery, avg_early_recovery)
        
        # Should approach original stability
        self.assertGreater(avg_late_recovery, 0.7 * avg_stable)
    
    def run_simulation_step(self, env_state):
        """Helper method to run one simulation step."""
        # Select and perform behavior
        behavior = self.pet.select_behavior(env_state)
        self.pet.perform_behavior(behavior, env_state)
        
        # Process energy allocation
        energy_result = self.energy_system.step(env_state)
        boundary_energy = energy_result["allocations"].get("boundary_maintenance", 0)
        
        # Update boundary
        boundary_result = self.boundary_system.update(env_state, boundary_energy)
        
        # Process exchanges
        self.exchange_system.process_exchange(env_state)
    
    def get_stability_metric(self):
        """Calculate a stability metric for the pet."""
        energy_factor = min(1.0, self.energy_system.energy / 100)
        boundary_factor = 1.0 - abs(0.5 - self.boundary_system.boundary_permeability)
        
        return (energy_factor + boundary_factor) / 2


if __name__ == '__main__':
    unittest.main()
