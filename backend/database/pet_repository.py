"""Repository for pet database operations."""

from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from backend.database.models import PetState, PetInteraction, PetMetric
from backend.database.db_connection import get_db

logger = logging.getLogger(__name__)


class PetRepository:
    """Repository for pet-related database operations."""
    
    @staticmethod
    def create_pet(pet_data: Dict[str, Any]) -> Optional[PetState]:
        """Create a new pet in the database."""
        try:
            with get_db() as db:
                pet = PetState(**pet_data)
                db.add(pet)
                db.commit()
                db.refresh(pet)
                return pet
        except SQLAlchemyError as e:
            logger.error(f"Error creating pet: {e}")
            return None
    
    @staticmethod
    def get_pet(pet_id: str) -> Optional[PetState]:
        """Get a pet by ID."""
        try:
            with get_db() as db:
                return db.query(PetState).filter(PetState.pet_id == pet_id).first()
        except SQLAlchemyError as e:
            logger.error(f"Error getting pet {pet_id}: {e}")
            return None
    
    @staticmethod
    def get_all_pets() -> List[PetState]:
        """Get all pets."""
        try:
            with get_db() as db:
                return db.query(PetState).all()
        except SQLAlchemyError as e:
            logger.error(f"Error getting all pets: {e}")
            return []
    
    @staticmethod
    def get_user_pets(user_id: str) -> List[PetState]:
        """Get all pets belonging to a user."""
        try:
            with get_db() as db:
                return db.query(PetState).filter(PetState.owner_id == user_id).all()
        except SQLAlchemyError as e:
            logger.error(f"Error getting pets for user {user_id}: {e}")
            return []
    
    @staticmethod
    def update_pet(pet_id: str, updates: Dict[str, Any]) -> Optional[PetState]:
        """Update a pet's state."""
        try:
            with get_db() as db:
                pet = db.query(PetState).filter(PetState.pet_id == pet_id).first()
                if not pet:
                    return None
                
                # Update fields
                for key, value in updates.items():
                    if hasattr(pet, key):
                        setattr(pet, key, value)
                
                pet.last_updated = datetime.utcnow()
                db.commit()
                db.refresh(pet)
                return pet
        except SQLAlchemyError as e:
            logger.error(f"Error updating pet {pet_id}: {e}")
            return None
    
    @staticmethod
    def save_pet_from_agent(agent) -> Optional[PetState]:
        """Save or update a pet from a DigitalPet agent."""
        try:
            with get_db() as db:
                # Check if pet exists
                existing = db.query(PetState).filter(PetState.pet_id == agent.unique_id).first()
                
                if existing:
                    # Update existing pet
                    existing.traits = {k: v for k, v in agent.traits.items()}
                    existing.trait_connections = {str(k): v for k, v in agent.trait_connections.items()}
                    existing.vital_stats = {
                        "health": agent.health,
                        "energy": agent.energy,
                        "mood": agent.mood
                    }
                    existing.needs = {k: v for k, v in agent.needs.items()}
                    existing.memory = agent.episodic_memory if hasattr(agent, 'episodic_memory') else []
                    existing.behavior_patterns = {k: v for k, v in agent.behavior_patterns.items()}
                    existing.attention_level = agent.attention_level
                    existing.development_stage = agent.development_stage
                    existing.age = agent.age
                    existing.position_x = agent.pos[0] if agent.pos else 0
                    existing.position_y = agent.pos[1] if agent.pos else 0
                    existing.last_updated = datetime.utcnow()
                    
                    db.commit()
                    db.refresh(existing)
                    return existing
                else:
                    # Create new pet
                    pet = PetState.from_agent(agent)
                    db.add(pet)
                    db.commit()
                    db.refresh(pet)
                    return pet
        except SQLAlchemyError as e:
            logger.error(f"Error saving pet from agent: {e}")
            return None
    
    @staticmethod
    def delete_pet(pet_id: str) -> bool:
        """Delete a pet."""
        try:
            with get_db() as db:
                pet = db.query(PetState).filter(PetState.pet_id == pet_id).first()
                if pet:
                    db.delete(pet)
                    db.commit()
                    return True
                return False
        except SQLAlchemyError as e:
            logger.error(f"Error deleting pet {pet_id}: {e}")
            return False
    
    @staticmethod
    def record_interaction(
        pet_id: str,
        interaction_type: str,
        content: Dict[str, Any],
        user_id: Optional[str] = None,
        mood_impact: float = 0,
        relationship_impact: float = 0,
        attention_impact: float = 0
    ) -> Optional[PetInteraction]:
        """Record a pet interaction."""
        try:
            with get_db() as db:
                interaction = PetInteraction(
                    pet_id=pet_id,
                    user_id=user_id,
                    interaction_type=interaction_type,
                    content=content,
                    mood_impact=mood_impact,
                    relationship_impact=relationship_impact,
                    attention_impact=attention_impact
                )
                db.add(interaction)
                db.commit()
                db.refresh(interaction)
                return interaction
        except SQLAlchemyError as e:
            logger.error(f"Error recording interaction: {e}")
            return None
    
    @staticmethod
    def get_pet_interactions(pet_id: str, limit: int = 100) -> List[PetInteraction]:
        """Get recent interactions for a pet."""
        try:
            with get_db() as db:
                return (db.query(PetInteraction)
                       .filter(PetInteraction.pet_id == pet_id)
                       .order_by(PetInteraction.timestamp.desc())
                       .limit(limit)
                       .all())
        except SQLAlchemyError as e:
            logger.error(f"Error getting interactions for pet {pet_id}: {e}")
            return []
    
    @staticmethod
    def record_metric(
        pet_id: str,
        environment_id: str,
        time_step: int,
        metric_type: str,
        metric_name: str,
        metric_value: float,
        additional_data: Optional[Dict[str, Any]] = None
    ) -> Optional[PetMetric]:
        """Record a pet metric."""
        try:
            with get_db() as db:
                metric = PetMetric(
                    pet_id=pet_id,
                    environment_id=environment_id,
                    time_step=time_step,
                    metric_type=metric_type,
                    metric_name=metric_name,
                    metric_value=metric_value,
                    additional_data=additional_data
                )
                db.add(metric)
                db.commit()
                db.refresh(metric)
                return metric
        except SQLAlchemyError as e:
            logger.error(f"Error recording metric: {e}")
            return None
    
    @staticmethod
    def get_pet_state_by_session_id(session_id: str) -> Optional[PetState]:
        """Get a pet state by session ID (for anonymous users)."""
        try:
            with get_db() as db:
                return db.query(PetState).filter(PetState.session_id == session_id).first()
        except SQLAlchemyError as e:
            logger.error(f"Error getting pet by session ID {session_id}: {e}")
            return None
    
    @staticmethod
    def get_pet_interactions_by_session(session_id: str, limit: int = 100) -> List[PetInteraction]:
        """Get pet interactions by session ID (for anonymous users)."""
        try:
            session_user_id = f"session_{session_id}"
            with get_db() as db:
                return (db.query(PetInteraction)
                       .filter(PetInteraction.user_id == session_user_id)
                       .order_by(PetInteraction.timestamp.desc())
                       .limit(limit)
                       .all())
        except SQLAlchemyError as e:
            logger.error(f"Error getting interactions for session {session_id}: {e}")
            return []