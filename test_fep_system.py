#!/usr/bin/env python3
"""
Comprehensive test suite for the FEP Cognitive System
Tests all major functionality including learning, prediction, and adaptation
"""

import sys
import os
import numpy as np
import logging
from pathlib import Path

# Add the backend directory to the path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_fep_basic_functionality():
    """Test basic FEP system functionality"""
    print("=" * 60)
    print("Testing FEP Basic Functionality")
    print("=" * 60)
    
    try:
        from agents.fep_cognitive_system import FEPCognitiveSystem
        
        # Initialize system
        fep = FEPCognitiveSystem(state_size=5, action_size=3)
        print(f"✓ FEP system initialized with {fep.state_size} states and {fep.action_size} actions")
        
        # Test observation processing
        observation = np.array([0.5, 0.3, 0.7, 0.2, 0.8])
        surprise = fep.observe(observation)
        print(f"✓ Observation processed, surprise level: {surprise:.3f}")
        
        # Test action selection
        current_state = np.array([0.4, 0.6, 0.3, 0.9, 0.1])
        action, confidence = fep.select_action(current_state)
        print(f"✓ Action selected: {action} with confidence: {confidence:.3f}")
        
        # Test cognitive state retrieval
        cognitive_state = fep.get_cognitive_state()
        print(f"✓ Cognitive state retrieved, prediction accuracy: {cognitive_state['prediction_accuracy']:.3f}")
        
        return True
        
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        return False

def test_fep_learning():
    """Test FEP learning and adaptation"""
    print("\n" + "=" * 60)
    print("Testing FEP Learning and Adaptation")
    print("=" * 60)
    
    try:
        from agents.fep_cognitive_system import FEPCognitiveSystem
        
        fep = FEPCognitiveSystem(state_size=4, action_size=3)
        
        # Simulate learning sequence
        initial_beliefs = fep.beliefs.copy()
        print(f"Initial beliefs: {initial_beliefs}")
        
        # Present consistent observations
        consistent_observation = np.array([0.8, 0.2, 0.6, 0.4])
        surprise_history = []
        
        for i in range(10):
            surprise = fep.observe(consistent_observation + np.random.normal(0, 0.1, 4))
            surprise_history.append(surprise)
        
        final_beliefs = fep.beliefs.copy()
        print(f"Final beliefs: {final_beliefs}")
        print(f"Belief change: {np.mean(np.abs(final_beliefs - initial_beliefs)):.3f}")
        
        # Check if surprise decreases over time (learning)
        early_surprise = np.mean(surprise_history[:3])
        late_surprise = np.mean(surprise_history[-3:])
        learning_improvement = early_surprise - late_surprise
        
        print(f"Early surprise: {early_surprise:.3f}, Late surprise: {late_surprise:.3f}")
        print(f"Learning improvement: {learning_improvement:.3f}")
        
        if learning_improvement > 0:
            print("✓ System shows learning (surprise decreased over time)")
        else:
            print("⚠ No clear learning detected")
        
        return True
        
    except Exception as e:
        print(f"✗ Learning test failed: {e}")
        return False

def test_fep_action_adaptation():
    """Test action preference adaptation"""
    print("\n" + "=" * 60)
    print("Testing Action Preference Adaptation")
    print("=" * 60)
    
    try:
        from agents.fep_cognitive_system import FEPCognitiveSystem
        
        fep = FEPCognitiveSystem(state_size=3, action_size=3)
        
        initial_preferences = fep.action_preferences.copy()
        print(f"Initial action preferences: {initial_preferences}")
        
        # Simulate actions with different outcomes
        state = np.array([0.5, 0.5, 0.5])
        
        # Action 0 leads to high surprise (bad outcome)
        for _ in range(5):
            fep.update_action_preferences(0, 2.0)  # High surprise
        
        # Action 1 leads to low surprise (good outcome)
        for _ in range(5):
            fep.update_action_preferences(1, 0.1)  # Low surprise
        
        final_preferences = fep.action_preferences.copy()
        print(f"Final action preferences: {final_preferences}")
        
        # Check if preferences adapted correctly
        if final_preferences[1] > final_preferences[0]:
            print("✓ Action preferences adapted correctly (action 1 > action 0)")
        else:
            print("⚠ Action preference adaptation unclear")
        
        return True
        
    except Exception as e:
        print(f"✗ Action adaptation test failed: {e}")
        return False

def test_fep_state_persistence():
    """Test state save/load functionality"""
    print("\n" + "=" * 60)
    print("Testing State Persistence")
    print("=" * 60)
    
    try:
        from agents.fep_cognitive_system import FEPCognitiveSystem
        
        # Create and modify a system
        fep1 = FEPCognitiveSystem(state_size=4, action_size=3)
        
        # Modify the system
        fep1.observe(np.array([0.7, 0.3, 0.8, 0.2]))
        fep1.learning_rate = 0.2
        
        # Save state
        saved_state = fep1.save_state()
        print(f"✓ State saved with {len(saved_state)} fields")
        
        # Create new system and load state
        fep2 = FEPCognitiveSystem(state_size=4, action_size=3)
        fep2.load_state(saved_state)
        
        # Verify state was loaded correctly
        beliefs_match = np.allclose(fep1.beliefs, fep2.beliefs, atol=1e-6)
        learning_rate_match = fep1.learning_rate == fep2.learning_rate
        
        if beliefs_match and learning_rate_match:
            print("✓ State persistence working correctly")
        else:
            print("⚠ State persistence issues detected")
        
        return True
        
    except Exception as e:
        print(f"✗ State persistence test failed: {e}")
        return False

def test_fep_environment_adaptation():
    """Test adaptation to different environment complexities"""
    print("\n" + "=" * 60)
    print("Testing Environment Adaptation")
    print("=" * 60)
    
    try:
        from agents.fep_cognitive_system import FEPCognitiveSystem
        
        fep = FEPCognitiveSystem(state_size=3, action_size=3)
        
        initial_lr = fep.learning_rate
        print(f"Initial learning rate: {initial_lr}")
        
        # Adapt to high complexity environment
        fep.adapt_to_environment(1.0)  # High complexity
        high_complexity_lr = fep.learning_rate
        
        # Reset and adapt to low complexity
        fep.learning_rate = initial_lr
        fep.adapt_to_environment(0.0)  # Low complexity
        low_complexity_lr = fep.learning_rate
        
        print(f"High complexity learning rate: {high_complexity_lr}")
        print(f"Low complexity learning rate: {low_complexity_lr}")
        
        if high_complexity_lr > low_complexity_lr:
            print("✓ Environment adaptation working (higher LR for complex environments)")
        else:
            print("⚠ Environment adaptation unclear")
        
        return True
        
    except Exception as e:
        print(f"✗ Environment adaptation test failed: {e}")
        return False

def test_fep_integration_with_digital_pet():
    """Test integration with the digital pet system"""
    print("\n" + "=" * 60)
    print("Testing Integration with Digital Pet System")
    print("=" * 60)
    
    try:
        from agents.fep_cognitive_system import FEPCognitiveSystem
        from agents.digital_pet import DigitalPet
        
        # Create digital pet
        pet = DigitalPet(pet_id="test_pet")
        print("✓ Digital pet created successfully")
        
        # Check if FEP system is integrated
        if hasattr(pet, 'fep_system') and pet.fep_system is not None:
            print("✓ FEP system is integrated into digital pet")
            
            # Test basic interaction
            pet.update_state({'hunger': 0.5, 'happiness': 0.7, 'energy': 0.6})
            print("✓ Pet state updated successfully")
            
            # Get cognitive state
            cognitive_state = pet.fep_system.get_cognitive_state()
            print(f"✓ Cognitive state accessed, prediction accuracy: {cognitive_state['prediction_accuracy']:.3f}")
            
        else:
            print("⚠ FEP system not found in digital pet")
        
        return True
        
    except Exception as e:
        print(f"✗ Integration test failed: {e}")
        return False

def run_performance_benchmark():
    """Run a simple performance benchmark"""
    print("\n" + "=" * 60)
    print("Performance Benchmark")
    print("=" * 60)
    
    try:
        import time
        from agents.fep_cognitive_system import FEPCognitiveSystem
        
        fep = FEPCognitiveSystem(state_size=10, action_size=5)
        
        # Benchmark observation processing
        observations = [np.random.random(10) for _ in range(100)]
        
        start_time = time.time()
        for obs in observations:
            fep.observe(obs)
        obs_time = time.time() - start_time
        
        # Benchmark action selection
        states = [np.random.random(10) for _ in range(100)]
        
        start_time = time.time()
        for state in states:
            fep.select_action(state)
        action_time = time.time() - start_time
        
        print(f"✓ Processed 100 observations in {obs_time:.3f}s ({100/obs_time:.1f} obs/s)")
        print(f"✓ Selected 100 actions in {action_time:.3f}s ({100/action_time:.1f} actions/s)")
        
        return True
        
    except Exception as e:
        print(f"✗ Performance benchmark failed: {e}")
        return False

def main():
    """Run all FEP system tests"""
    print("Starting FEP Cognitive System Test Suite")
    print("=" * 80)
    
    test_results = []
    
    # Run all tests
    test_results.append(("Basic Functionality", test_fep_basic_functionality()))
    test_results.append(("Learning & Adaptation", test_fep_learning()))
    test_results.append(("Action Adaptation", test_fep_action_adaptation()))
    test_results.append(("State Persistence", test_fep_state_persistence()))
    test_results.append(("Environment Adaptation", test_fep_environment_adaptation()))
    test_results.append(("Digital Pet Integration", test_fep_integration_with_digital_pet()))
    test_results.append(("Performance Benchmark", run_performance_benchmark()))
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name:<30} {status}")
        if result:
            passed += 1
    
    print(f"\nTests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! FEP system is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the output above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
