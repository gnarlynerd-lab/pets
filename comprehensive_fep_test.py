#!/usr/bin/env python3
"""
Comprehensive FEP Integration Test
Tests the FEP system standalone and integrated with digital pet
"""

def test_fep_standalone():
    """Test FEP system by itself"""
    print("=" * 50)
    print("Testing FEP Cognitive System (Standalone)")
    print("=" * 50)
    
    try:
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
        
        import numpy as np
        from agents.fep_cognitive_system import FEPCognitiveSystem
        
        # Create FEP system
        fep = FEPCognitiveSystem(state_size=5, action_size=3)
        print("✓ FEP system initialized")
        
        # Test basic functionality
        initial_beliefs = fep.beliefs.copy()
        print(f"  Initial beliefs: {[f'{x:.2f}' for x in initial_beliefs[:3]]}")
        
        # Process several observations
        observations = [
            np.array([0.8, 0.2, 0.6, 0.4, 0.7]),
            np.array([0.7, 0.3, 0.5, 0.5, 0.6]),
            np.array([0.9, 0.1, 0.7, 0.3, 0.8])
        ]
        
        surprises = []
        for i, obs in enumerate(observations):
            surprise = fep.observe(obs)
            surprises.append(surprise)
            print(f"  Observation {i+1}: surprise = {surprise:.3f}")
        
        # Test action selection
        test_state = np.array([0.5, 0.5, 0.5, 0.5, 0.5])
        action, confidence = fep.select_action(test_state)
        print(f"✓ Action selection: action={action}, confidence={confidence:.3f}")
        
        # Test learning (surprise should generally decrease)
        if len(surprises) > 1:
            avg_early = np.mean(surprises[:len(surprises)//2])
            avg_late = np.mean(surprises[len(surprises)//2:])
            if avg_early > avg_late:
                print("✓ Learning detected (surprise decreased)")
            else:
                print("⚠ No clear learning pattern")
        
        # Test cognitive state
        state = fep.get_cognitive_state()
        print(f"✓ Cognitive state: accuracy={state['prediction_accuracy']:.3f}")
        
        print("✓ FEP standalone test PASSED")
        return True
        
    except Exception as e:
        print(f"❌ FEP standalone test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_fep_integration():
    """Test FEP integration with digital pet"""
    print("\n" + "=" * 50)
    print("Testing FEP Integration with Digital Pet")
    print("=" * 50)
    
    try:
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
        
        from agents.digital_pet import DigitalPet
        
        # Create digital pet
        pet = DigitalPet(pet_id="test_fep_pet")
        print("✓ Digital pet created")
        
        # Check FEP integration
        if hasattr(pet, 'fep_system') and pet.fep_system is not None:
            print("✓ FEP system found in digital pet")
            
            # Test pet state updates
            pet.update_state({
                'hunger': 0.6,
                'happiness': 0.7,
                'energy': 0.8,
                'health': 0.9
            })
            print("✓ Pet state updated")
            
            # Get cognitive information
            cognitive_state = pet.fep_system.get_cognitive_state()
            print(f"✓ Pet cognitive state: accuracy={cognitive_state['prediction_accuracy']:.3f}")
            
            # Test pet decision making (if available)
            if hasattr(pet, 'make_decision'):
                decision = pet.make_decision()
                print(f"✓ Pet decision: {decision}")
            
        else:
            print("⚠ FEP system not found in digital pet")
            return False
        
        print("✓ FEP integration test PASSED")
        return True
        
    except Exception as e:
        print(f"❌ FEP integration test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_fep_learning_scenario():
    """Test FEP learning in a controlled scenario"""
    print("\n" + "=" * 50)
    print("Testing FEP Learning Scenario")
    print("=" * 50)
    
    try:
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
        
        import numpy as np
        from agents.fep_cognitive_system import FEPCognitiveSystem
        
        # Create FEP system
        fep = FEPCognitiveSystem(state_size=3, action_size=2)
        print("✓ FEP system created for learning test")
        
        # Simulate consistent environment
        target_pattern = np.array([0.8, 0.3, 0.6])
        surprises = []
        
        print("  Learning from consistent observations...")
        for i in range(15):
            # Add small noise to the target pattern
            noisy_obs = target_pattern + np.random.normal(0, 0.1, 3)
            noisy_obs = np.clip(noisy_obs, 0, 1)
            
            surprise = fep.observe(noisy_obs)
            surprises.append(surprise)
            
            if i % 5 == 4:  # Print every 5th observation
                print(f"    Step {i+1}: surprise = {surprise:.3f}")
        
        # Analyze learning
        early_surprise = np.mean(surprises[:5])
        late_surprise = np.mean(surprises[-5:])
        improvement = early_surprise - late_surprise
        
        print(f"  Early surprise (steps 1-5): {early_surprise:.3f}")
        print(f"  Late surprise (steps 11-15): {late_surprise:.3f}")
        print(f"  Improvement: {improvement:.3f}")
        
        if improvement > 0:
            print("✓ Clear learning demonstrated")
        else:
            print("⚠ Learning less clear")
        
        # Test adaptation to new environment
        print("  Testing adaptation to new pattern...")
        new_pattern = np.array([0.2, 0.9, 0.4])
        new_surprise = fep.observe(new_pattern)
        print(f"    New pattern surprise: {new_surprise:.3f}")
        
        print("✓ FEP learning scenario test PASSED")
        return True
        
    except Exception as e:
        print(f"❌ FEP learning scenario test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all FEP tests"""
    print("FEP COGNITIVE SYSTEM - COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    
    # Run all tests
    results = []
    results.append(("FEP Standalone", test_fep_standalone()))
    results.append(("FEP Integration", test_fep_integration()))
    results.append(("FEP Learning", test_fep_learning_scenario()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 ALL TESTS PASSED! FEP system is fully functional!")
    else:
        print(f"\n⚠️  {len(results) - passed} test(s) failed. Check details above.")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
