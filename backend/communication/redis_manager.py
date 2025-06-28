"""
Redis Manager for Inter-Agent Communication
"""
import redis.asyncio as redis
import json
import logging
from typing import Dict, List, Optional, Any
import os

logger = logging.getLogger(__name__)


class RedisManager:
    """Manages Redis connections and message passing for agents"""
    
    def __init__(self):
        self.redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
        self.redis_client: Optional[redis.Redis] = None
        self.pubsub: Optional[redis.client.PubSub] = None
        
    async def initialize(self):
        """Initialize Redis connection"""
        try:
            self.redis_client = redis.from_url(self.redis_url, decode_responses=True)
            
            # Test connection
            await self.redis_client.ping()
            logger.info(f"Connected to Redis at {self.redis_url}")
            
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise
    
    async def close(self):
        """Close Redis connections"""
        if self.pubsub:
            await self.pubsub.close()
        if self.redis_client:
            await self.redis_client.close()
    
    async def send_message(self, recipient_id: str, message: Dict[str, Any]):
        """Send a message to a specific agent"""
        if not self.redis_client:
            raise RuntimeError("Redis client not initialized")
        
        message_key = f"agent:{recipient_id}:messages"
        serialized_message = json.dumps(message)
        
        try:
            await self.redis_client.rpush(message_key, serialized_message)
            logger.debug(f"Message sent to {recipient_id}: {message.get('type', 'unknown')}")
        except Exception as e:
            logger.error(f"Failed to send message to {recipient_id}: {e}")
    
    async def get_messages(self, agent_id: str) -> List[Dict[str, Any]]:
        """Get all messages for a specific agent"""
        if not self.redis_client:
            raise RuntimeError("Redis client not initialized")
        
        message_key = f"agent:{agent_id}:messages"
        
        try:
            # Get all messages and clear the queue
            messages = await self.redis_client.lrange(message_key, 0, -1)
            if messages:
                await self.redis_client.delete(message_key)
            
            # Deserialize messages
            return [json.loads(msg) for msg in messages]
            
        except Exception as e:
            logger.error(f"Failed to get messages for {agent_id}: {e}")
            return []
    
    async def broadcast_message(self, channel: str, message: Dict[str, Any]):
        """Broadcast a message to a channel"""
        if not self.redis_client:
            raise RuntimeError("Redis client not initialized")
        
        try:
            serialized_message = json.dumps(message)
            await self.redis_client.publish(channel, serialized_message)
            logger.debug(f"Message broadcast to {channel}: {message.get('type', 'unknown')}")
        except Exception as e:
            logger.error(f"Failed to broadcast to {channel}: {e}")
    
    async def subscribe_to_channel(self, channel: str):
        """Subscribe to a broadcast channel"""
        if not self.redis_client:
            raise RuntimeError("Redis client not initialized")
        
        try:
            if not self.pubsub:
                self.pubsub = self.redis_client.pubsub()
            
            await self.pubsub.subscribe(channel)
            logger.info(f"Subscribed to channel: {channel}")
            
        except Exception as e:
            logger.error(f"Failed to subscribe to {channel}: {e}")
    
    async def get_channel_message(self) -> Optional[Dict[str, Any]]:
        """Get a message from subscribed channels"""
        if not self.pubsub:
            return None
        
        try:
            message = await self.pubsub.get_message(ignore_subscribe_messages=True)
            if message and message['type'] == 'message':
                return json.loads(message['data'])
        except Exception as e:
            logger.error(f"Failed to get channel message: {e}")
        
        return None
    
    async def store_interaction(self, sender_id: str, receiver_id: str, 
                              message_type: str, content: Dict[str, Any], 
                              outcome: Optional[str] = None):
        """Store interaction data for analysis"""
        if not self.redis_client:
            raise RuntimeError("Redis client not initialized")
        
        interaction_data = {
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "message_type": message_type,
            "content": content,
            "outcome": outcome,
            "timestamp": json.dumps({"$date": {"$numberLong": str(int(__import__('time').time() * 1000))}})
        }
        
        try:
            # Store in interactions list for analysis
            interactions_key = "system:interactions"
            serialized_data = json.dumps(interaction_data)
            await self.redis_client.rpush(interactions_key, serialized_data)
            
            # Keep only recent interactions (last 1000)
            await self.redis_client.ltrim(interactions_key, -1000, -1)
            
        except Exception as e:
            logger.error(f"Failed to store interaction: {e}")
    
    async def get_recent_interactions(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent interactions for analysis"""
        if not self.redis_client:
            return []
        
        try:
            interactions_key = "system:interactions"
            raw_interactions = await self.redis_client.lrange(interactions_key, -limit, -1)
            return [json.loads(interaction) for interaction in raw_interactions]
        except Exception as e:
            logger.error(f"Failed to get recent interactions: {e}")
            return []
    
    async def update_connection_strength(self, agent_a: str, agent_b: str, delta: float = 0.1):
        """Update connection strength between two agents"""
        if not self.redis_client:
            return
        
        try:
            # Create sorted key to ensure consistency
            key_pair = tuple(sorted([agent_a, agent_b]))
            connection_key = f"connection:{key_pair[0]}:{key_pair[1]}"
            
            # Get current strength
            current_strength = await self.redis_client.get(connection_key)
            if current_strength:
                new_strength = min(1.0, float(current_strength) + delta)
            else:
                new_strength = delta
            
            # Store updated strength
            await self.redis_client.set(connection_key, new_strength)
            
        except Exception as e:
            logger.error(f"Failed to update connection strength: {e}")
    
    async def get_all_connections(self) -> Dict[str, float]:
        """Get all connection strengths for network visualization"""
        if not self.redis_client:
            return {}
        
        try:
            connections = {}
            pattern = "connection:*"
            
            async for key in self.redis_client.scan_iter(match=pattern):
                strength = await self.redis_client.get(key)
                if strength:
                    # Extract agent IDs from key
                    key_parts = key.split(':')
                    if len(key_parts) >= 3:
                        agent_pair = f"{key_parts[1]}:{key_parts[2]}"
                        connections[agent_pair] = float(strength)
            
            return connections
            
        except Exception as e:
            logger.error(f"Failed to get connections: {e}")
            return {}
