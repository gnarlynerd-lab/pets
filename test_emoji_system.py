#!/usr/bin/env python3
"""
Test script for the complete Digital Pet emoji communication system
"""
from backend.agents.digital_pet import DigitalPet
from backend.models.pet_model import PetModel
import time

def test_emoji_system():
    print('=== Testing Digital Pet with Emoji Communication ===')
    
    # Create a simple model for the pet
    model = PetModel(num_pets=1)
    
    # Create a digital pet
    pet = DigitalPet('emoji_pet_001', model)
    print(f'✓ Created pet: {pet.unique_id}')
    print(f'✓ Pet traits: {list(pet.traits.keys())}')
    
    # Test emoji interaction
    print('\n--- Testing Pet Emoji Interaction ---')
    response = pet.interact_with_emoji('😊🍎')
    print(f'User: 😊🍎 (happy + hungry)')
    print(f'Pet: {response["emoji_response"]}')
    print(f'Surprise: {response["surprise_level"]:.3f}')
    
    # Test learning over multiple interactions
    print('\n--- Testing Pet Learning ---')
    emoji_inputs = ['😊🍕', '😍✨', '🤗❤️', '🎮🎉']
    
    for emoji_input in emoji_inputs:
        response = pet.interact_with_emoji(emoji_input)
        print(f'User: {emoji_input} → Pet: {response["emoji_response"]}')
    
    # Check pet's current emotional state
    print('\n--- Pet Emotional State ---')
    cognitive_state = pet.get_cognitive_state()
    beliefs_str = ', '.join([f'{x:.2f}' for x in cognitive_state['beliefs'][:5]])
    print(f'Current beliefs: [{beliefs_str}]')
    print(f'Prediction accuracy: {cognitive_state["prediction_accuracy"]:.3f}')
    
    # Test generate current communication
    print('\n--- Testing Pet Communication Generation ---')
    current_comm = pet.generate_current_communication()
    print(f'Pet says: {current_comm["emoji_message"]}')
    print(f'Context: {current_comm["context"]}')
    
    print('\n✅ Digital Pet emoji communication test completed successfully!')
    return True

if __name__ == "__main__":
    test_emoji_system()
