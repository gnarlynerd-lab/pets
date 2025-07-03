#!/usr/bin/env python3
"""
Test the backend API to verify emoji communication is working
"""
import requests
import json

def test_backend_api():
    print("🔧 Testing Backend API...")
    
    # Test 1: Get available pets
    print("\n1. Getting available pets...")
    try:
        response = requests.get("http://localhost:8000/api/pets")
        if response.status_code == 200:
            pets_data = response.json()
            pets = pets_data.get('pets', [])
            print(f"✅ Found {len(pets)} pets")
            if pets:
                pet_id = pets[0]['id']
                print(f"   Using pet: {pet_id}")
                return pet_id
        else:
            print(f"❌ Failed to get pets: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting pets: {e}")
    
    return None

def test_emoji_interaction(pet_id):
    print(f"\n2. Testing emoji interaction with pet {pet_id}...")
    
    emoji_data = {
        "pet_id": pet_id,
        "emojis": "😊❤️",
        "user_id": "test_user"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/pets/emoji",
            headers={"Content-Type": "application/json"},
            data=json.dumps(emoji_data)
        )
        
        print(f"Status: {response.status_code}")
        response_data = response.json()
        print(f"Response: {json.dumps(response_data, indent=2)}")
        
        if response.status_code == 200:
            print("✅ Emoji interaction successful!")
            return True
        else:
            print("❌ Emoji interaction failed")
            return False
            
    except Exception as e:
        print(f"❌ Error in emoji interaction: {e}")
        return False

def main():
    print("🎉 DKS Backend API Test")
    print("=" * 30)
    
    # Test backend connection
    pet_id = test_backend_api()
    if not pet_id:
        print("\n❌ Cannot proceed without a valid pet ID")
        return
    
    # Test emoji interaction
    success = test_emoji_interaction(pet_id)
    
    if success:
        print("\n✅ Backend is working correctly!")
        print("🚀 Ready to start frontend!")
    else:
        print("\n❌ Backend has issues that need to be resolved")

if __name__ == "__main__":
    main()
