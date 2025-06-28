#!/usr/bin/env python3
"""Simple FEP test to verify basic functionality"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

import numpy as np
from agents.fep_cognitive_system import FEPCognitiveSystem

def main():
    print("Testing FEP Cognitive System...")
    
    # Create FEP system
    fep = FEPCognitiveSystem(state_size=3, action_size=2)
    print("✓ FEP system created")
    
    # Test observation
    obs = np.array([0.5, 0.3, 0.8])
    surprise = fep.observe(obs)
    print(f"✓ Observation processed, surprise: {surprise:.3f}")
    
    # Test action selection
    state = np.array([0.4, 0.6, 0.2])
    action, confidence = fep.select_action(state)
    print(f"✓ Action selected: {action}, confidence: {confidence:.3f}")
    
    # Test cognitive state
    cognitive_state = fep.get_cognitive_state()
    print(f"✓ Cognitive state retrieved, accuracy: {cognitive_state['prediction_accuracy']:.3f}")
    
    print("\n🎉 All basic tests passed!")

if __name__ == "__main__":
    main()
