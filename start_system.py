#!/usr/bin/env python3
"""
DKS Digital Pet System - Development Startup Script
"""

import sys
import os
import asyncio
import logging
sys.path.insert(0, '.')

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_system():
    """Test all system components before starting"""
    print("🔧 TESTING DKS DIGITAL PET SYSTEM")
    print("=" * 50)
    
    # Test 1: Core imports
    try:
        from backend.main import app
        print("✅ FastAPI app imported")
    except Exception as e:
        print(f"❌ FastAPI app import failed: {e}")
        return False
    
    # Test 2: Pet model creation
    try:
        from backend.models.pet_model import PetModel
        model = PetModel(num_pets=2)
        print("✅ Pet model created")
        
        pets = [agent for agent in model.schedule.agents if hasattr(agent, 'pet_type')]
        print(f"✅ Created {len(pets)} digital pets")
    except Exception as e:
        print(f"❌ Pet model creation failed: {e}")
        return False
    
    # Test 3: FEP system integration
    try:
        if pets and hasattr(pets[0], 'fep_system'):
            print("✅ FEP cognitive system integrated")
            
            # Test FEP functionality
            import numpy as np
            test_obs = np.array([0.5, 0.5, 0.5, 0.5, 0.5])
            surprise = pets[0].fep_system.observe(test_obs)
            print(f"✅ FEP system operational (surprise: {surprise:.3f})")
        else:
            print("⚠ FEP system not found in pets")
    except Exception as e:
        print(f"❌ FEP system test failed: {e}")
        return False
    
    # Test 4: Simulation step
    try:
        model.step()
        print("✅ Simulation step successful")
    except Exception as e:
        print(f"❌ Simulation step failed: {e}")
        return False
    
    print("\n🎉 ALL SYSTEM TESTS PASSED!")
    print("🚀 System is ready to run")
    return True

def start_development_server():
    """Start the development server"""
    print("\n🚀 STARTING DEVELOPMENT SERVER")
    print("=" * 50)
    
    try:
        import uvicorn
        from backend.main import app
        
        print("Starting FastAPI server on http://localhost:8000")
        print("API documentation available at http://localhost:8000/docs")
        print("Press Ctrl+C to stop the server")
        print("")
        
        # Start server
        uvicorn.run(
            "backend.main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="info"
        )
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Server startup failed: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main function"""
    print("DKS DIGITAL PET SYSTEM - DEVELOPMENT STARTUP")
    print("=" * 60)
    print("🐾 Free Energy Principle Enhanced Digital Pets")
    print("=" * 60)
    
    # Test system first
    if not test_system():
        print("\n❌ System tests failed. Please check the errors above.")
        return False
    
    # Ask user if they want to start the server
    print("\n" + "=" * 50)
    response = input("Start the development server? (y/n): ").strip().lower()
    
    if response in ['y', 'yes']:
        start_development_server()
    else:
        print("👋 System tested successfully. Run again with 'y' to start the server.")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
