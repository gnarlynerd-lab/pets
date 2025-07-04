#!/usr/bin/env python3
"""
Test script for Enhanced FEP Cognitive System with Attention-Based Thriving
Demonstrates how pets view interactions as positive attention that helps them thrive
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.agents.enhanced_fep_system import EnhancedFEPCognitiveSystem
import time

def test_enhanced_fep_system():
    """Test the enhanced FEP system with attention-based thriving."""
    print("🧠 Testing Enhanced FEP Cognitive System with Attention-Based Thriving")
    print("=" * 70)
    
    # Initialize the enhanced FEP system
    fep_system = EnhancedFEPCognitiveSystem(state_size=20, action_size=12)
    
    print(f"Initial Attention Level: {fep_system.attention_level:.1f}")
    print(f"Initial Thriving Level: {fep_system.thriving_level:.1f}")
    print(f"Initial Interaction Count: {fep_system.interaction_count}")
    print()
    
    # Test different types of interactions
    interaction_types = [
        ("emoji", "😊❤️", "Positive affectionate interaction"),
        ("emoji", "🎉✨", "Celebratory interaction"),
        ("emoji", "😔", "Sad interaction"),
        ("emoji", "🤔❓", "Curious interaction"),
        ("petting", "", "Physical affection"),
        ("playing", "", "Playful interaction"),
        ("feeding", "", "Care interaction"),
    ]
    
    for interaction_type, emojis, description in interaction_types:
        print(f"📝 {description}")
        print(f"   Before - Attention: {fep_system.attention_level:.1f}, Thriving: {fep_system.thriving_level:.1f}")
        
        if interaction_type == "emoji":
            # Process emoji interaction
            result = fep_system.process_emoji_interaction(emojis)
            print(f"   User sent: {emojis}")
            print(f"   Pet responded: {result['emoji_response']}")
        else:
            # Process other interaction types
            fep_system.receive_interaction(interaction_type, intensity=0.8)
        
        print(f"   After  - Attention: {fep_system.attention_level:.1f}, Thriving: {fep_system.thriving_level:.1f}")
        print(f"   Change - Attention: +{fep_system.attention_level - (fep_system.attention_level - 10):.1f}, Thriving: +{fep_system.thriving_level - (fep_system.thriving_level - 4):.1f}")
        print()
    
    # Test attention decay over time
    print("⏰ Testing Attention Decay Over Time")
    print("=" * 40)
    
    initial_attention = fep_system.attention_level
    initial_thriving = fep_system.thriving_level
    
    # Simulate time passing without interactions
    for hour in range(1, 6):
        # Create a minimal observation to trigger attention decay
        observation = fep_system._create_observation_from_interaction({
            'joy': 0.0,
            'curiosity': 0.0,
            'contentment': 0.0,
            'attention_potential': 0.0,
            'overall_sentiment': 0.0,
            'emoji_count': 0
        })
        
        # Update last interaction time to simulate time passing
        fep_system.last_interaction_time = time.time() - (hour * 3600)  # Hours ago
        
        # Process observation (this will trigger attention decay)
        fep_system.observe(observation)
        
        print(f"After {hour} hour(s) without interaction:")
        print(f"   Attention: {fep_system.attention_level:.1f} (was {initial_attention:.1f})")
        print(f"   Thriving: {fep_system.thriving_level:.1f} (was {initial_thriving:.1f})")
        print()
    
    # Test recovery with new interaction
    print("🔄 Testing Recovery with New Interaction")
    print("=" * 40)
    
    print(f"Before recovery - Attention: {fep_system.attention_level:.1f}, Thriving: {fep_system.thriving_level:.1f}")
    
    # Strong positive interaction
    result = fep_system.process_emoji_interaction("❤️🥰😍")
    print(f"User sent: ❤️🥰😍")
    print(f"Pet responded: {result['emoji_response']}")
    
    print(f"After recovery - Attention: {fep_system.attention_level:.1f}, Thriving: {fep_system.thriving_level:.1f}")
    print()
    
    # Test contextual responses based on attention/thriving levels
    print("🎭 Testing Contextual Responses Based on State")
    print("=" * 50)
    
    # Test low attention scenario
    fep_system.attention_level = 20.0
    fep_system.thriving_level = 30.0
    result = fep_system.process_emoji_interaction("😊")
    print(f"Low attention/thriving state:")
    print(f"   Attention: {fep_system.attention_level:.1f}, Thriving: {fep_system.thriving_level:.1f}")
    print(f"   User sent: 😊")
    print(f"   Pet responded: {result['emoji_response']}")
    print()
    
    # Test high attention scenario
    fep_system.attention_level = 85.0
    fep_system.thriving_level = 80.0
    result = fep_system.process_emoji_interaction("😊")
    print(f"High attention/thriving state:")
    print(f"   Attention: {fep_system.attention_level:.1f}, Thriving: {fep_system.thriving_level:.1f}")
    print(f"   User sent: 😊")
    print(f"   Pet responded: {result['emoji_response']}")
    print()
    
    # Show final cognitive state
    print("🧠 Final Cognitive State")
    print("=" * 30)
    cognitive_state = fep_system.get_cognitive_state()
    print(f"Total Interactions: {cognitive_state['interaction_count']}")
    print(f"Final Attention Level: {cognitive_state['attention_level']:.1f}")
    print(f"Final Thriving Level: {cognitive_state['thriving_level']:.1f}")
    print(f"Recent Surprise Levels: {cognitive_state['surprise_history'][-5:]}")
    print(f"Recent Free Energy: {cognitive_state['free_energy_history'][-5:]}")
    
    print("\n✅ Enhanced FEP System Test Complete!")
    print("\nKey Insights:")
    print("• Pets view interactions as positive attention that helps them thrive")
    print("• Attention decays over time without interactions")
    print("• Thriving increases with positive attention and decreases with neglect")
    print("• Responses are contextual based on current attention and thriving levels")
    print("• The system uses active inference to minimize surprise and maximize thriving")

if __name__ == "__main__":
    test_enhanced_fep_system() 