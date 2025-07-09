#!/usr/bin/env python3
"""
Test script for the Enhanced User Modeling System

This script demonstrates how digital pets develop rich, personalized relationships
with users through personality recognition, preference learning, and adaptive behavior.
"""

import sys
import os
import time
import random
from typing import Dict, List, Any

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.agents.user_modeling import EnhancedUserModelingSystem
from backend.agents.digital_pet import DigitalPet
from backend.models.pet_model import PetModel

def create_test_users() -> List[Dict[str, Any]]:
    """Create test users with different personalities and interaction styles"""
    return [
        {
            "user_id": "playful_alice",
            "name": "Alice",
            "style": "playful",
            "interactions": [
                {"type": "play", "intensity": 0.8, "emoji_sequence": "🎮⚽🎯"},
                {"type": "play", "intensity": 0.9, "emoji_sequence": "🎪🎨🎭"},
                {"type": "feed", "intensity": 0.6, "emoji_sequence": "🍕🍪"},
                {"type": "play", "intensity": 0.7, "emoji_sequence": "🎯🎮"},
                {"type": "pet", "intensity": 0.5, "emoji_sequence": "🤗"},
            ]
        },
        {
            "user_id": "nurturing_bob",
            "name": "Bob",
            "style": "nurturing",
            "interactions": [
                {"type": "feed", "intensity": 0.9, "emoji_sequence": "🍕🍎🥛"},
                {"type": "pet", "intensity": 0.8, "emoji_sequence": "🤗💕"},
                {"type": "feed", "intensity": 0.7, "emoji_sequence": "🍪🍕"},
                {"type": "pet", "intensity": 0.9, "emoji_sequence": "❤️🥰"},
                {"type": "check", "intensity": 0.6, "emoji_sequence": "👋"},
            ]
        },
        {
            "user_id": "serious_carol",
            "name": "Carol",
            "style": "serious",
            "interactions": [
                {"type": "train", "intensity": 0.8, "emoji_sequence": "🎓"},
                {"type": "check", "intensity": 0.5, "emoji_sequence": "👋"},
                {"type": "train", "intensity": 0.9, "emoji_sequence": "🏆"},
                {"type": "check", "intensity": 0.4, "emoji_sequence": "👋"},
                {"type": "train", "intensity": 0.7, "emoji_sequence": "⭐"},
            ]
        },
        {
            "user_id": "inconsistent_dave",
            "name": "Dave",
            "style": "inconsistent",
            "interactions": [
                {"type": "play", "intensity": 0.8, "emoji_sequence": "🎮"},
                {"type": "ignore", "intensity": 0.3, "emoji_sequence": ""},
                {"type": "feed", "intensity": 0.6, "emoji_sequence": "🍕"},
                {"type": "ignore", "intensity": 0.5, "emoji_sequence": ""},
                {"type": "play", "intensity": 0.7, "emoji_sequence": "⚽"},
            ]
        }
    ]

def simulate_user_interactions(pet: DigitalPet, users: List[Dict[str, Any]]):
    """Simulate interactions between the pet and different users"""
    print("\n" + "="*60)
    print("SIMULATING USER INTERACTIONS")
    print("="*60)
    
    for user in users:
        print(f"\n--- Interacting with {user['name']} ({user['style']} style) ---")
        
        for i, interaction in enumerate(user['interactions'], 1):
            print(f"\nInteraction {i}: {interaction['type']} (intensity: {interaction['intensity']})")
            print(f"User emojis: {interaction['emoji_sequence']}")
            
            # Create user context
            user_context = {
                "user_id": user["user_id"],
                "intensity": interaction["intensity"],
                "user_emotional_state": "happy" if interaction["type"] != "ignore" else "neutral"
            }
            
            # Process interaction through pet's user modeling system
            if hasattr(pet, 'user_modeling'):
                interaction_data = {
                    "type": interaction["type"],
                    "intensity": interaction["intensity"],
                    "content": {"emoji_sequence": interaction["emoji_sequence"]},
                    "user_emotional_state": user_context["user_emotional_state"],
                    "relationship_impact": 0.1 if interaction["type"] != "ignore" else -0.1
                }
                
                # Update user modeling
                modeling_result = pet.user_modeling.process_interaction(user["user_id"], interaction_data)
                
                # Show insights
                insights = modeling_result.get("insights", {})
                print(f"  User style detected: {insights.get('user_style', 'unknown')}")
                print(f"  Relationship phase: {insights.get('relationship_phase', 'unknown')}")
                print(f"  Trust level: {insights.get('trust_level', 0):.2f}")
                print(f"  Familiarity level: {insights.get('familiarity_level', 0):.2f}")
            
            # Simulate emoji interaction
            if interaction["emoji_sequence"]:
                result = pet.interact_with_emoji(interaction["emoji_sequence"], user_context)
                print(f"  Pet response: {result['pet_response']}")
                print(f"  Original response: {result.get('original_response', result['pet_response'])}")
                
                # Show personalization differences
                if result.get('original_response') != result['pet_response']:
                    print(f"  → Personalized for {user['style']} style!")
            
            time.sleep(0.5)  # Brief pause for readability

def demonstrate_user_profiles(pet: DigitalPet, users: List[Dict[str, Any]]):
    """Demonstrate the rich user profiles that pets develop"""
    print("\n" + "="*60)
    print("USER PROFILES DEVELOPED BY PET")
    print("="*60)
    
    for user in users:
        print(f"\n--- {user['name']}'s Profile ---")
        
        try:
            profile = pet.get_user_profile(user["user_id"])
            
            if "error" in profile:
                print(f"  Error: {profile['error']}")
                continue
            
            # Display personality insights
            personality = profile.get("personality", {})
            print(f"  Dominant Style: {personality.get('dominant_style', 'unknown')}")
            print(f"  Confidence Level: {personality.get('confidence_level', 0):.2f}")
            
            # Display relationship insights
            relationship = profile.get("relationship", {})
            print(f"  Relationship Phase: {relationship.get('phase', 'unknown')}")
            print(f"  Trust: {relationship.get('trust', 0):.2f}")
            print(f"  Familiarity: {relationship.get('familiarity', 0):.2f}")
            print(f"  Affection: {relationship.get('affection', 0):.2f}")
            
            # Display memory insights
            memory = profile.get("memory", {})
            print(f"  Recent Interactions: {memory.get('recent_interactions', 0)}")
            favorite_activities = memory.get("favorite_activities", [])
            if favorite_activities:
                print(f"  Favorite Activity: {favorite_activities[0][0]} ({favorite_activities[0][1]} times)")
            
            # Display adaptation recommendations
            recommendations = pet.get_adaptation_recommendations(user["user_id"])
            print(f"  Adaptation Suggestions: {', '.join(recommendations)}")
            
        except Exception as e:
            print(f"  Error getting profile: {e}")

def demonstrate_predictive_behavior(pet: DigitalPet, users: List[Dict[str, Any]]):
    """Demonstrate how pets can predict user behavior"""
    print("\n" + "="*60)
    print("PREDICTIVE USER BEHAVIOR")
    print("="*60)
    
    for user in users:
        print(f"\n--- Predicting {user['name']}'s Behavior ---")
        
        try:
            # Predict user needs in different contexts
            contexts = [
                {"time_of_day": "morning", "user_mood": "tired"},
                {"time_of_day": "afternoon", "user_mood": "energetic"},
                {"time_of_day": "evening", "user_mood": "relaxed"}
            ]
            
            for context in contexts:
                prediction = pet.predict_user_behavior(user["user_id"], context)
                
                if "error" not in prediction:
                    print(f"  Context: {context}")
                    print(f"    Likely Need: {prediction.get('likely_need', 'unknown')}")
                    print(f"    Confidence: {prediction.get('confidence', 0):.2f}")
                    print(f"    Suggested Response: {prediction.get('suggested_response', 'unknown')}")
                else:
                    print(f"  Context: {context} - {prediction['error']}")
                    
        except Exception as e:
            print(f"  Error making predictions: {e}")

def demonstrate_relationship_evolution(pet: DigitalPet, users: List[Dict[str, Any]]):
    """Demonstrate how relationships evolve over time"""
    print("\n" + "="*60)
    print("RELATIONSHIP EVOLUTION")
    print("="*60)
    
    # Simulate extended interactions with one user
    test_user = users[0]  # Use Alice (playful user)
    print(f"\n--- Extended Interaction with {test_user['name']} ---")
    
    # Create extended interaction sequence
    extended_interactions = [
        {"type": "play", "intensity": 0.8, "emoji_sequence": "🎮"},
        {"type": "play", "intensity": 0.9, "emoji_sequence": "⚽"},
        {"type": "feed", "intensity": 0.7, "emoji_sequence": "🍕"},
        {"type": "play", "intensity": 0.8, "emoji_sequence": "🎯"},
        {"type": "pet", "intensity": 0.6, "emoji_sequence": "🤗"},
        {"type": "play", "intensity": 0.9, "emoji_sequence": "🎪"},
        {"type": "feed", "intensity": 0.8, "emoji_sequence": "🍪"},
        {"type": "play", "intensity": 0.7, "emoji_sequence": "🎨"},
    ]
    
    for i, interaction in enumerate(extended_interactions, 1):
        print(f"\nExtended Interaction {i}: {interaction['type']}")
        
        # Process interaction
        user_context = {"user_id": test_user["user_id"], "intensity": interaction["intensity"]}
        
        if hasattr(pet, 'user_modeling'):
            interaction_data = {
                "type": interaction["type"],
                "intensity": interaction["intensity"],
                "content": {"emoji_sequence": interaction["emoji_sequence"]},
                "relationship_impact": 0.1
            }
            
            modeling_result = pet.user_modeling.process_interaction(test_user["user_id"], interaction_data)
            insights = modeling_result.get("insights", {})
            
            print(f"  Relationship Phase: {insights.get('relationship_phase', 'unknown')}")
            print(f"  Trust Level: {insights.get('trust_level', 0):.2f}")
            print(f"  Familiarity Level: {insights.get('familiarity_level', 0):.2f}")
        
        # Simulate emoji interaction
        if interaction["emoji_sequence"]:
            result = pet.interact_with_emoji(interaction["emoji_sequence"], user_context)
            print(f"  Pet Response: {result['pet_response']}")
        
        time.sleep(0.3)

def main():
    """Main test function"""
    print("Enhanced User Modeling System Test")
    print("="*60)
    
    # Create test users
    users = create_test_users()
    print(f"Created {len(users)} test users with different personalities")
    
    # Create a pet model and digital pet
    print("\nInitializing pet with enhanced user modeling...")
    model = PetModel()
    pet = DigitalPet("test_pet_001", model)
    
    # Simulate interactions
    simulate_user_interactions(pet, users)
    
    # Demonstrate user profiles
    demonstrate_user_profiles(pet, users)
    
    # Demonstrate predictive behavior
    demonstrate_predictive_behavior(pet, users)
    
    # Demonstrate relationship evolution
    demonstrate_relationship_evolution(pet, users)
    
    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("="*60)
    print("\nKey Features Demonstrated:")
    print("✓ Personality recognition based on interaction patterns")
    print("✓ Rich user memory with episodic and semantic components")
    print("✓ Relationship evolution through different phases")
    print("✓ Predictive behavior based on learned patterns")
    print("✓ Personalized emoji responses adapted to user style")
    print("✓ Adaptation recommendations for optimal interaction")

if __name__ == "__main__":
    main() 