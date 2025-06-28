#!/usr/bin/env python3
"""
Test script to verify the DKS Digital Pet System is working correctly
"""

import sys
import os
sys.path.append('.')

def test_imports():
    """Test that all core components can be imported"""
    try:
        print("Testing imports...")
        
        # Test Mesa import
        import mesa
        print("✓ Mesa imported successfully")
        
        # Test core agents
        from backend.agents.digital_pet import DigitalPet
        print("✓ DigitalPet imported successfully")
        
        from backend.agents.fep_cognitive_system import FEPCognitiveSystem
        print("✓ FEPCognitiveSystem imported successfully")
        
        from backend.agents.fluid_boundary import FluidBoundarySystem, PetEnergySystem
        print("✓ Fluid boundary systems imported successfully")
        
        from backend.agents.pet_environment import PetEnvironment, ObservableCognitiveDevelopment
        print("✓ Pet environment systems imported successfully")
        
        from backend.models.pet_model import PetModel
        print("✓ PetModel imported successfully")
        
        print("\n✅ All imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_fep_system():
    """Test basic FEP system functionality"""
    try:
        print("\nTesting FEP System...")
        
        import numpy as np
        from backend.agents.fep_cognitive_system import FEPCognitiveSystem
        
        # Create FEP system
        fep = FEPCognitiveSystem(state_size=5, action_size=3)
        print(f"✓ FEP system created with {fep.state_size} states and {fep.action_size} actions")
        
        # Test observation processing
        observation = np.random.uniform(0, 1, 5)
        surprise = fep.observe(observation)
        print(f"✓ FEP observation processed: surprise={surprise:.3f}")
        
        # Test action selection
        current_state = np.random.uniform(0, 1, 5)
        action, confidence = fep.select_action(current_state)
        print(f"✓ FEP action selection: action={action}, confidence={confidence:.3f}")
        
        # Test prediction
        predicted_state = fep.predict_next_state(current_state, action)
        print(f"✓ FEP prediction: {len(predicted_state)} state values")
        
        # Test cognitive state
        cognitive_state = fep.get_cognitive_state()
        print(f"✓ FEP cognitive state retrieved: {len(cognitive_state)} fields")
        
        # Test adaptation
        fep.adapt_to_environment(0.5)
        print(f"✓ FEP environment adaptation: learning_rate={fep.learning_rate:.3f}")
        
        # Test state save/load
        saved_state = fep.save_state()
        fep.load_state(saved_state)
        print("✓ FEP state save/load successful")
        
        print("✅ FEP system tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ FEP test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_digital_pet_creation():
    """Test creating a digital pet"""
    try:
        print("\nTesting Digital Pet Creation...")
        
        import mesa
        from backend.models.pet_model import PetModel
        
        # Create a simple model
        model = PetModel(num_pets=1)
        
        # Get the first pet
        pets = [agent for agent in model.schedule.agents if hasattr(agent, 'pet_type')]
        
        if pets:
            pet = pets[0]
            print(f"✓ Pet created: ID={pet.unique_id}, type={pet.pet_type}")
            print(f"✓ Pet traits: {len(pet.traits)} traits")
            print(f"✓ Pet energy: {pet.energy}")
            print(f"✓ Pet mood: {pet.mood}")
            
            # Test FEP system integration
            if hasattr(pet, 'fep_system'):
                print(f"✓ FEP system integrated")
                
            print("✅ Digital Pet creation tests passed!")
            return True
        else:
            print("❌ No pets found in model")
            return False
            
    except Exception as e:
        print(f"❌ Digital Pet test error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 DKS Digital Pet System Test Suite")
    print("=" * 50)
    
    success = True
    
    # Run tests
    success &= test_imports()
    success &= test_fep_system()
    success &= test_digital_pet_creation()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! The DKS Digital Pet System is working correctly.")
    else:
        print("❌ Some tests failed. Check the errors above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
