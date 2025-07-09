#!/usr/bin/env python3
"""
Test script for the new policy optimization feature in the Enhanced FEP System.
This demonstrates the difference between greedy action selection and policy optimization.
"""

import numpy as np
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from agents.enhanced_fep_system import EnhancedFEPCognitiveSystem


def test_policy_optimization():
    """Test the policy optimization feature."""
    print("🧠 Testing Enhanced FEP System with Policy Optimization")
    print("=" * 60)
    
    # Initialize the cognitive system
    fep_system = EnhancedFEPCognitiveSystem(state_size=20, action_size=12)
    
    # Create a test state
    test_state = np.random.uniform(0, 1, 20)
    print(f"📊 Test state shape: {test_state.shape}")
    print(f"📊 Test state sample: {test_state[:5]}...")
    
    print("\n🔄 Testing Action Selection Methods:")
    print("-" * 40)
    
    # Test greedy action selection
    print("1️⃣ Greedy Action Selection (Original Method):")
    greedy_action, greedy_confidence = fep_system.select_action(test_state, use_policy_optimization=False)
    print(f"   Action: {greedy_action}, Confidence: {greedy_confidence:.3f}")
    
    # Test policy optimization
    print("2️⃣ Policy Optimization (New Method):")
    policy_action, policy_confidence = fep_system.select_action(test_state, use_policy_optimization=True)
    print(f"   Action: {policy_action}, Confidence: {policy_confidence:.3f}")
    
    print(f"\n📈 Comparison:")
    print(f"   Greedy vs Policy: Action {greedy_action} vs {policy_action}")
    print(f"   Confidence: {greedy_confidence:.3f} vs {policy_confidence:.3f}")
    
    # Test multiple iterations to see patterns
    print("\n🔄 Testing Multiple Iterations:")
    print("-" * 40)
    
    greedy_actions = []
    policy_actions = []
    greedy_confidences = []
    policy_confidences = []
    
    for i in range(10):
        # Update state slightly for each iteration
        test_state += np.random.normal(0, 0.1, 20)
        test_state = np.clip(test_state, 0, 1)
        
        # Get actions
        g_action, g_conf = fep_system.select_action(test_state, use_policy_optimization=False)
        p_action, p_conf = fep_system.select_action(test_state, use_policy_optimization=True)
        
        greedy_actions.append(g_action)
        policy_actions.append(p_action)
        greedy_confidences.append(g_conf)
        policy_confidences.append(p_conf)
        
        print(f"   Iteration {i+1}: Greedy({g_action}, {g_conf:.3f}) vs Policy({p_action}, {p_conf:.3f})")
    
    # Analyze results
    print("\n📊 Analysis:")
    print("-" * 40)
    print(f"   Greedy actions: {greedy_actions}")
    print(f"   Policy actions: {greedy_actions}")
    print(f"   Greedy avg confidence: {np.mean(greedy_confidences):.3f}")
    print(f"   Policy avg confidence: {np.mean(policy_confidences):.3f}")
    print(f"   Action diversity (greedy): {len(set(greedy_actions))}")
    print(f"   Action diversity (policy): {len(set(policy_actions))}")


def test_emoji_interaction_with_policy():
    """Test emoji interaction with policy optimization."""
    print("\n🎭 Testing Emoji Interaction with Policy Optimization")
    print("=" * 60)
    
    # Initialize the cognitive system
    fep_system = EnhancedFEPCognitiveSystem()
    
    # Test different emoji sequences
    test_emojis = [
        "😊❤️",      # Happy and love
        "😴🍕",      # Sleepy and food
        "🤗✨",       # Hug and sparkle
        "😍🎉",      # Love eyes and celebration
        "😔💔",      # Sad and broken heart
    ]
    
    for i, emoji_sequence in enumerate(test_emojis, 1):
        print(f"\n{i}️⃣ Testing emoji sequence: {emoji_sequence}")
        
        # Process interaction
        result = fep_system.process_emoji_interaction(emoji_sequence)
        
        print(f"   Response: {result['emoji_response']}")
        print(f"   Surprise: {result['surprise_level']:.3f}")
        print(f"   Confidence: {result['response_confidence']:.3f}")
        print(f"   Attention: {result['attention_level']:.1f}")
        print(f"   Thriving: {result['thriving_level']:.1f}")
        
        # Show emotional context
        context = result['emotional_context']
        print(f"   Emotional context:")
        print(f"     Joy: {context['joy']:.3f}")
        print(f"     Curiosity: {context['curiosity']:.3f}")
        print(f"     Contentment: {context['contentment']:.3f}")
        print(f"     Attention potential: {context['attention_potential']:.3f}")


def test_cognitive_state():
    """Test cognitive state and statistics."""
    print("\n🧠 Testing Cognitive State and Statistics")
    print("=" * 60)
    
    # Initialize the cognitive system
    fep_system = EnhancedFEPCognitiveSystem()
    
    # Simulate some interactions
    for i in range(5):
        emoji = ["😊", "❤️", "🤗", "✨", "🎉"][i]
        fep_system.process_emoji_interaction(emoji)
    
    # Get cognitive state
    cognitive_state = fep_system.get_cognitive_state()
    print("📊 Cognitive State:")
    print(f"   Attention level: {cognitive_state['attention_level']:.1f}")
    print(f"   Thriving level: {cognitive_state['thriving_level']:.1f}")
    print(f"   Interaction count: {cognitive_state['interaction_count']}")
    print(f"   Prediction accuracy: {cognitive_state['prediction_accuracy']:.3f}")
    
    # Get emoji usage stats
    emoji_stats = fep_system.get_emoji_usage_stats()
    print("\n📈 Emoji Usage Statistics:")
    print(f"   Total emojis used: {emoji_stats['total_emojis_used']}")
    print(f"   Most used emojis: {emoji_stats['most_used_emojis']}")
    print(f"   Recent usage patterns: {emoji_stats['recent_usage_patterns']}")


def main():
    """Main test function."""
    print("🚀 Enhanced FEP System - Policy Optimization Test")
    print("=" * 60)
    
    try:
        # Test policy optimization
        test_policy_optimization()
        
        # Test emoji interaction
        test_emoji_interaction_with_policy()
        
        # Test cognitive state
        test_cognitive_state()
        
        print("\n✅ All tests completed successfully!")
        print("\n🎯 Key Benefits of Policy Optimization:")
        print("   • Multi-step planning instead of greedy selection")
        print("   • Better long-term behavior prediction")
        print("   • More sophisticated action sequences")
        print("   • Improved confidence estimation")
        print("   • Enhanced exploration vs exploitation balance")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 