#!/usr/bin/env python3

import sys
import os
sys.path.append('/Users/gerardlynn/agents/dks')

from backend.models.pet_model import PetModel
from backend.agents.digital_pet import DigitalPet

def test_emoji_system():
    print("Testing Enhanced Emoji Communication System...")
    
    # Create pet model and add a pet
    model = PetModel()
    pet = DigitalPet("test_pet", model)
    
    print(f"Created pet: {pet.unique_id}")
    print(f"Initial state: {pet.get_state()}")
    
    # Test emoji interaction
    print("\n=== Testing Emoji Interactions ===")
    
    # Test 1: Happy and hungry
    print("\nTest 1: User sends '😊🍎' (happy + hungry)")
    response1 = pet.interact_with_emoji('😊🍎')
    print(f"Pet responds: {response1['pet_response']}")
    print(f"Surprise level: {response1['surprise_level']:.3f}")
    print(f"Confidence: {response1['response_confidence']:.3f}")
    
    # Test 2: Love and play
    print("\nTest 2: User sends '❤️🎮' (love + play)")
    response2 = pet.interact_with_emoji('❤️🎮')
    print(f"Pet responds: {response2['pet_response']}")
    print(f"Surprise level: {response2['surprise_level']:.3f}")
    print(f"Confidence: {response2['response_confidence']:.3f}")
    
    # Test 3: Generate pet's own message
    print("\nTest 3: Pet generates its own emoji message")
    pet_message = pet.generate_emoji_message()
    print(f"Pet says: {pet_message}")
    
    # Test 4: Complex emoji sequence
    print("\nTest 4: User sends complex sequence '😊❤️🎉✨' (happy + love + celebration + sparkle)")
    response3 = pet.interact_with_emoji('😊❤️🎉✨')
    print(f"Pet responds: {response3['pet_response']}")
    print(f"Surprise level: {response3['surprise_level']:.3f}")
    print(f"Confidence: {response3['response_confidence']:.3f}")
    
    # Check trait evolution
    print(f"\nPet traits after interactions:")
    print(f"- Playfulness: {pet.traits.get('playfulness', 0.5):.3f}")
    print(f"- Affection: {pet.traits.get('affection', 0.5):.3f}")
    print(f"- Curiosity: {pet.traits.get('curiosity', 0.5):.3f}")
    
    print("\n✅ Emoji communication system test completed successfully!")
    return True

if __name__ == "__main__":
    test_emoji_system()
