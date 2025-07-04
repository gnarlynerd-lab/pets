#!/usr/bin/env python3
"""
Test script to verify the emoji API is working correctly
"""

import requests
import json

API_BASE_URL = "http://localhost:8000"

def test_emoji_interaction():
    """Test emoji interactions to verify the API is working"""
    
    # Get available pets
    print("🔍 Getting available pets...")
    response = requests.get(f"{API_BASE_URL}/api/pets")
    if response.status_code != 200:
        print(f"❌ Failed to get pets: {response.status_code}")
        return
    
    pets = response.json()["pets"]
    if not pets:
        print("❌ No pets available")
        return
    
    pet_id = pets[0]["id"]
    print(f"✅ Using pet: {pet_id}")
    
    # Test different emoji interactions
    test_emojis = ["❤️", "😊", "👋", "🎉", "🍎"]
    
    for emoji in test_emojis:
        print(f"\n🧪 Testing emoji: {emoji}")
        
        # This is exactly what the frontend sends
        payload = {
            "pet_id": pet_id,
            "emojis": emoji,
            "user_id": "frontend_user",
            "context": {"source": "frontend"}
        }
        
        print(f"📤 Sending: {json.dumps(payload, indent=2)}")
        
        response = requests.post(
            f"{API_BASE_URL}/api/pets/emoji",
            headers={"Content-Type": "application/json"},
            json=payload
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Response: {result['emoji_response']}")
            print(f"   Behavioral: {result['behavioral_response']}")
            print(f"   Surprise: {result['surprise_level']:.3f}")
            print(f"   Confidence: {result['response_confidence']:.3f}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   Response: {response.text}")

if __name__ == "__main__":
    test_emoji_interaction() 