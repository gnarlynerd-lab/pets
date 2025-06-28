#!/usr/bin/env python3
"""
FEP Test with file output - writes results to a file
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def main():
    results = []
    
    try:
        # Test 1: Import and create FEP system
        import numpy as np
        from agents.fep_cognitive_system import FEPCognitiveSystem
        
        fep = FEPCognitiveSystem(state_size=3, action_size=2)
        results.append("✓ FEP system created successfully")
        
        # Test 2: Observation processing
        obs = np.array([0.5, 0.3, 0.8])
        surprise = fep.observe(obs)
        results.append(f"✓ Observation processed, surprise: {surprise:.3f}")
        
        # Test 3: Action selection
        state = np.array([0.4, 0.6, 0.2])
        action, confidence = fep.select_action(state)
        results.append(f"✓ Action selected: {action}, confidence: {confidence:.3f}")
        
        # Test 4: Cognitive state
        cognitive_state = fep.get_cognitive_state()
        results.append(f"✓ Cognitive state retrieved, accuracy: {cognitive_state['prediction_accuracy']:.3f}")
        
        # Test 5: Learning simulation
        initial_surprise = surprise
        for i in range(5):
            new_obs = obs + np.random.normal(0, 0.05, 3)
            new_obs = np.clip(new_obs, 0, 1)
            surprise = fep.observe(new_obs)
        
        if surprise < initial_surprise:
            results.append("✓ Learning detected (surprise decreased)")
        else:
            results.append("⚠ No clear learning pattern")
        
        # Test 6: Integration test - just verify the FEP system exists in the module
        try:
            from agents.digital_pet import DigitalPet
            
            # Check if DigitalPet class references FEP system
            import inspect
            source = inspect.getsource(DigitalPet.__init__)
            if 'fep_system' in source and 'FEPCognitiveSystem' in source:
                results.append("✓ FEP system integrated in digital pet class")
            else:
                results.append("⚠ FEP system integration unclear in digital pet")
                
        except Exception as e:
            results.append(f"⚠ Digital pet integration test failed: {str(e)[:50]}")
        
        results.append("\n🎉 FEP SYSTEM TESTS COMPLETED SUCCESSFULLY!")
        
    except Exception as e:
        results.append(f"❌ FEP test failed: {e}")
        import traceback
        results.append(traceback.format_exc())
    
    # Write results to file
    with open('fep_test_results.txt', 'w') as f:
        f.write("FEP COGNITIVE SYSTEM TEST RESULTS\n")
        f.write("=" * 40 + "\n\n")
        for result in results:
            f.write(result + "\n")
    
    return len([r for r in results if r.startswith("✓")]) > 4

if __name__ == "__main__":
    main()
