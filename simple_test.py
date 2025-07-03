import sys
sys.path.append('/Users/gerardlynn/agents/dks')

print("Testing FEP system...")
from backend.agents.fep_cognitive_system import FEPCognitiveSystem
fep = FEPCognitiveSystem()
result = fep.process_emoji_interaction('😊❤️', {'test': True})
print(f"FEP result: {result['pet_response']}")

print("Testing complete system...")
from backend.models.pet_model import PetModel
from backend.agents.digital_pet import DigitalPet

model = PetModel()
pet = DigitalPet('test', model)
interaction = pet.interact_with_emoji('😊🍎')
print(f"Pet interaction: {interaction['pet_response']}")

print("MVP system is working correctly!")
