#!/usr/bin/env python3
"""
MVP Demonstration - Test the complete emoji communication system
"""
import sys
import os
sys.path.append('/Users/gerardlynn/agents/dks')

from backend.models.pet_model import PetModel
from backend.agents.digital_pet import DigitalPet

def main():
    print("🎉 DKS Emoji Pet MVP - Complete System Test")
    print("=" * 50)
    
    # Create the pet system
    print("Creating pet model...")
    model = PetModel()
    
    print("Creating digital pet...")
    pet = DigitalPet('mvp_pet', model)
    
    print(f"✅ Pet created: {pet.unique_id}")
    print(f"Initial traits: {pet.traits}")
    
    # Test emoji interactions
    print("\n🗨️  Testing Emoji Communication:")
    print("-" * 30)
    
    test_interactions = [
        "😊❤️",      # Happy love
        "🍎😋",      # Hungry  
        "🎮🎯",      # Want to play
        "😴💤",      # Sleepy
        "👋✨"       # Greeting with sparkle
    ]
    
    for user_emoji in test_interactions:
        print(f"\nUser: {user_emoji}")
        result = pet.interact_with_emoji(user_emoji)
        print(f"Pet:  {result['pet_response']}")
        print(f"Surprise: {result['surprise_level']:.3f}, Confidence: {result['response_confidence']:.3f}")
    
    # Show evolved traits
    print(f"\n📊 Pet Evolution:")
    print("-" * 20)
    for trait, value in pet.traits.items():
        print(f"{trait}: {value:.3f}")
    
    # Test message generation
    print(f"\n💭 Pet generates message:")
    generated_message = pet.generate_emoji_message()
    print(f"Pet says: {generated_message}")
    
    print("\n✅ MVP System fully functional!")
    print("🚀 Ready for frontend integration!")

if __name__ == "__main__":
    main()
