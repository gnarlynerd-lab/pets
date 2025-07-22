"""SQLAlchemy models for DKS database."""

from datetime import datetime
from typing import Optional, Dict, Any
import json
import uuid

from sqlalchemy import Column, String, Float, JSON, TIMESTAMP, ForeignKey, Integer, Enum, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from backend.database.db_connection import Base


class PetState(Base):
    """Pet state persistence model."""
    __tablename__ = "pet_states"
    
    pet_id = Column(String(100), primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_id = Column(String(100), nullable=True)
    session_id = Column(String(100), nullable=True)  # For anonymous users
    pet_name = Column(String(100), nullable=True)
    traits = Column(JSON, nullable=False)
    trait_connections = Column(JSON, nullable=False)
    vital_stats = Column(JSON, nullable=False)
    needs = Column(JSON, nullable=False)
    memory = Column(JSON, nullable=False)
    behavior_patterns = Column(JSON, nullable=False)
    attention_level = Column(Float, default=50.0)
    development_stage = Column(String(20), default='infant')
    age = Column(Float, default=0.0)
    position_x = Column(Float, default=0)
    position_y = Column(Float, default=0)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    last_updated = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    interactions = relationship("PetInteraction", back_populates="pet", cascade="all, delete-orphan")
    metrics = relationship("PetMetric", back_populates="pet", cascade="all, delete-orphan")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary."""
        return {
            "pet_id": self.pet_id,
            "owner_id": self.owner_id,
            "session_id": self.session_id,
            "pet_name": self.pet_name,
            "traits": self.traits,
            "trait_connections": self.trait_connections,
            "vital_stats": self.vital_stats,
            "needs": self.needs,
            "memory": self.memory,
            "behavior_patterns": self.behavior_patterns,
            "attention_level": self.attention_level,
            "development_stage": self.development_stage,
            "age": self.age,
            "position": {"x": self.position_x, "y": self.position_y},
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None
        }
    
    @classmethod
    def from_agent(cls, agent) -> "PetState":
        """Create PetState from DigitalPet agent."""
        return cls(
            pet_id=agent.unique_id,
            owner_id=getattr(agent, 'owner_id', None),
            session_id=getattr(agent, 'session_id', None),
            pet_name=getattr(agent, 'name', None),
            traits={k: v for k, v in agent.traits.items()},
            trait_connections={str(k): v for k, v in agent.trait_connections.items()},
            vital_stats={
                "health": agent.health,
                "energy": agent.energy,
                "mood": agent.mood
            },
            needs={k: v for k, v in agent.needs.items()},
            memory=agent.episodic_memory if hasattr(agent, 'episodic_memory') else [],
            behavior_patterns={k: v for k, v in agent.behavior_patterns.items()},
            attention_level=agent.attention_level,
            development_stage=agent.development_stage,
            age=agent.age,
            position_x=agent.pos[0] if agent.pos else 0,
            position_y=agent.pos[1] if agent.pos else 0
        )


class PetInteraction(Base):
    """Pet interaction history model."""
    __tablename__ = "pet_interactions"
    
    interaction_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), nullable=True)
    pet_id = Column(String(36), ForeignKey("pet_states.pet_id", ondelete="CASCADE"), nullable=False)
    interaction_type = Column(String(50), nullable=False)
    content = Column(JSON, nullable=False)
    mood_impact = Column(Float, default=0)
    relationship_impact = Column(Float, default=0)
    attention_impact = Column(Float, default=0)
    timestamp = Column(TIMESTAMP, server_default=func.current_timestamp())
    
    # Relationships
    pet = relationship("PetState", back_populates="interactions")


class PetEnvironment(Base):
    """Pet environment configuration model."""
    __tablename__ = "pet_environments"
    
    environment_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    environment_name = Column(String(100), nullable=False)
    environment_type = Column(String(50), nullable=False)
    parameters = Column(JSON, nullable=False)
    start_time = Column(TIMESTAMP, server_default=func.current_timestamp())
    end_time = Column(TIMESTAMP, nullable=True)
    status = Column(String(20), default='active')
    environment_metrics = Column(JSON, nullable=True)
    
    # Relationships
    metrics = relationship("PetMetric", back_populates="environment", cascade="all, delete-orphan")
    relationships = relationship("PetRelationship", back_populates="environment", cascade="all, delete-orphan")


class PetMetric(Base):
    """Pet performance metrics model."""
    __tablename__ = "pet_metrics"
    
    metric_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    pet_id = Column(String(36), ForeignKey("pet_states.pet_id", ondelete="CASCADE"), nullable=False)
    environment_id = Column(String(36), ForeignKey("pet_environments.environment_id", ondelete="CASCADE"), nullable=False)
    time_step = Column(Integer, nullable=False)
    metric_type = Column(String(50), nullable=False)
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(Float, nullable=False)
    additional_data = Column(JSON, nullable=True)
    timestamp = Column(TIMESTAMP, server_default=func.current_timestamp())
    
    # Relationships
    pet = relationship("PetState", back_populates="metrics")
    environment = relationship("PetEnvironment", back_populates="metrics")


class PetRelationship(Base):
    """Pet relationship network model."""
    __tablename__ = "pet_relationships"
    
    relationship_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    environment_id = Column(String(36), ForeignKey("pet_environments.environment_id", ondelete="CASCADE"), nullable=False)
    entity_a_id = Column(String(36), nullable=False)
    entity_a_type = Column(Enum('pet', 'user', name='entity_type'), nullable=False)
    entity_b_id = Column(String(36), nullable=False)
    entity_b_type = Column(Enum('pet', 'user', name='entity_type'), nullable=False)
    relationship_strength = Column(Float, default=0)
    relationship_quality = Column(String(50), nullable=True)
    interaction_count = Column(Integer, default=0)
    last_interaction = Column(TIMESTAMP, server_default=func.current_timestamp())
    
    # Relationships
    environment = relationship("PetEnvironment", back_populates="relationships")


class User(Base):
    """User account model."""
    __tablename__ = "users"
    
    user_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    user_preferences = Column(JSON, nullable=True)
    token_balance = Column(BigInteger, default=0)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    last_login = Column(TIMESTAMP, nullable=True)
    
    # Relationships
    tokens = relationship("Token", back_populates="user", cascade="all, delete-orphan")


class Token(Base):
    """Token transaction model."""
    __tablename__ = "tokens"
    
    transaction_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    transaction_type = Column(String(50), nullable=False)
    amount = Column(BigInteger, nullable=False)
    recipient_id = Column(String(36), nullable=True)
    related_pet_id = Column(String(36), nullable=True)
    transaction_data = Column(JSON, nullable=True)
    timestamp = Column(TIMESTAMP, server_default=func.current_timestamp())
    
    # Relationships
    user = relationship("User", back_populates="tokens")