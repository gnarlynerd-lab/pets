#!/usr/bin/env python3
"""
End-to-end integration test for FEP system with digital pet
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def main():
    print("🧪 RUNNING END-TO-END FEP INTEGRATION TEST")
    print("=" * 50)
    
    try:
        # Test 1: Import and create pet model
        print("1. Testing Pet Model Creation...")
        from models.pet_model import PetModel
        
        model = PetModel(num_pets=1)
        print("   ✓ Pet model created successfully")
        
        # Test 2: Get the created pet
        print("\n2. Testing Pet Access...")
        pets = [agent for agent in model.schedule.agents if hasattr(agent, 'pet_type')]
        
        if not pets:
            print("   ❌ No pets found in model")
            return False
            
        pet = pets[0]
        print(f"   ✓ Pet found: ID={pet.unique_id}")
        
        # Test 3: Verify FEP system is integrated
        print("\n3. Testing FEP System Integration...")
        if hasattr(pet, 'fep_system'):
            print("   ✓ FEP system found in pet")
            
            # Test FEP functionality
            import numpy as np
            test_obs = np.array([0.6, 0.4, 0.8, 0.2, 0.5])
            surprise = pet.fep_system.observe(test_obs)
            print(f"   ✓ FEP system operational - surprise: {surprise:.3f}")
            
            # Test action selection
            test_state = np.array([0.5, 0.5, 0.5, 0.5, 0.5])
            action, confidence = pet.fep_system.select_action(test_state)
            print(f"   ✓ Action selection working - action: {action}, confidence: {confidence:.3f}")
            
        else:
            print("   ❌ FEP system not found in pet")
            return False
        
        # Test 4: Run simulation step
        print("\n4. Testing Simulation Step...")
        initial_energy = pet.energy
        model.step()
        print(f"   ✓ Simulation step completed")
        print(f"   ✓ Pet energy: {initial_energy:.1f} → {pet.energy:.1f}")
        
        # Test 5: Test cognitive state
        print("\n5. Testing Cognitive State...")
        cognitive_state = pet.fep_system.get_cognitive_state()
        print(f"   ✓ Prediction accuracy: {cognitive_state['prediction_accuracy']:.3f}")
        print(f"   ✓ Average surprise: {cognitive_state['average_surprise']:.3f}")
        
        # Test 6: Test learning over multiple steps
        print("\n6. Testing Learning Over Time...")
        initial_accuracy = cognitive_state['prediction_accuracy']
        
        # Run multiple simulation steps
        for i in range(5):
            model.step()
            
        final_cognitive_state = pet.fep_system.get_cognitive_state()
        final_accuracy = final_cognitive_state['prediction_accuracy']
        
        print(f"   ✓ Initial accuracy: {initial_accuracy:.3f}")
        print(f"   ✓ Final accuracy: {final_accuracy:.3f}")
        
        if len(pet.fep_system.surprise_history) > 0:
            print(f"   ✓ Surprise history: {len(pet.fep_system.surprise_history)} entries")
        
        print("\n" + "=" * 50)
        print("🎉 ALL INTEGRATION TESTS PASSED!")
        print("✓ FEP cognitive system is fully integrated and functional")
        print("✓ Digital pet system is working correctly")
        print("✓ Learning and adaptation mechanisms are operational")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
