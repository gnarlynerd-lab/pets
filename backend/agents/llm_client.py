"""
LLM Client for Semantic Consciousness System
Supports multiple LLM providers with fallback mechanisms for robust consciousness.
"""

import json
import logging
import asyncio
import os
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod
from dataclasses import dataclass

import httpx
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


@dataclass
class LLMResponse:
    """Structured response from LLM with confidence and reasoning"""
    content: Dict[str, Any]
    confidence: float
    reasoning: str
    provider: str
    tokens_used: int = 0
    response_time: float = 0.0


class BaseLLMProvider(ABC):
    """Base class for LLM providers"""
    
    @abstractmethod
    async def generate_response(self, prompt: str, max_tokens: int = 500) -> LLMResponse:
        """Generate structured response from LLM"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if provider is configured and available"""
        pass


class OpenAIProvider(BaseLLMProvider):
    """OpenAI GPT provider for semantic analysis"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.client = AsyncOpenAI(api_key=self.api_key) if self.api_key else None
        
    def is_available(self) -> bool:
        return self.api_key is not None and self.client is not None
    
    async def generate_response(self, prompt: str, max_tokens: int = 500) -> LLMResponse:
        """Generate response using OpenAI API"""
        if not self.is_available():
            raise ValueError("OpenAI provider not configured - missing API key")
        
        import time
        start_time = time.time()
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are the consciousness module of a digital companion. Analyze user interactions and respond with structured JSON containing emotional analysis, intent recognition, and relationship insights. Be precise and insightful."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            response_time = time.time() - start_time
            content_text = response.choices[0].message.content
            
            try:
                content_dict = json.loads(content_text)
            except json.JSONDecodeError:
                # Fallback parsing if JSON is malformed
                content_dict = self._parse_fallback_response(content_text)
            
            return LLMResponse(
                content=content_dict,
                confidence=min(1.0, content_dict.get("confidence", 0.8)),
                reasoning=content_dict.get("reasoning", "AI analysis of user interaction"),
                provider="openai",
                tokens_used=response.usage.total_tokens if response.usage else 0,
                response_time=response_time
            )
            
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            raise
    
    def _parse_fallback_response(self, content: str) -> Dict[str, Any]:
        """Fallback parsing for non-JSON responses"""
        return {
            "user_emotional_state": "uncertain",
            "user_intent": "interaction", 
            "relationship_context": "ongoing",
            "predicted_needs": ["engagement"],
            "optimal_response_style": "adaptive",
            "confidence": 0.5,
            "reasoning": f"Fallback parsing applied: {content[:100]}..."
        }


class LocalLLMProvider(BaseLLMProvider):
    """Local LLM provider using HTTP endpoints (Ollama, etc.)"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama2"):
        self.base_url = base_url
        self.model = model
        self.client = httpx.AsyncClient(timeout=30.0)
        
    def is_available(self) -> bool:
        """Check if local LLM server is running"""
        try:
            # This would need to be tested with actual local setup
            return True  # Optimistic availability
        except:
            return False
    
    async def generate_response(self, prompt: str, max_tokens: int = 500) -> LLMResponse:
        """Generate response using local LLM API"""
        import time
        start_time = time.time()
        
        try:
            # Ollama API format
            payload = {
                "model": self.model,
                "prompt": f"""You are the consciousness of a digital companion analyzing user interactions.
                
{prompt}

Respond with JSON containing: user_emotional_state, user_intent, relationship_context, predicted_needs (array), optimal_response_style, confidence (0-1), reasoning.

Response:""",
                "stream": False,
                "options": {
                    "num_predict": max_tokens,
                    "temperature": 0.7
                }
            }
            
            response = await self.client.post(
                f"{self.base_url}/api/generate",
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                response_time = time.time() - start_time
                content_text = result.get("response", "")
                
                # Try to extract JSON from response
                content_dict = self._extract_json_from_text(content_text)
                
                return LLMResponse(
                    content=content_dict,
                    confidence=content_dict.get("confidence", 0.7),
                    reasoning=content_dict.get("reasoning", "Local LLM analysis"),
                    provider="local",
                    tokens_used=0,  # Local models don't report token usage
                    response_time=response_time
                )
            else:
                raise Exception(f"Local LLM returned status {response.status_code}")
                
        except Exception as e:
            logger.error(f"Local LLM call failed: {e}")
            raise
    
    def _extract_json_from_text(self, text: str) -> Dict[str, Any]:
        """Extract JSON from potentially noisy LLM output"""
        try:
            # Find JSON object in text
            start = text.find('{')
            end = text.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = text[start:end]
                return json.loads(json_str)
        except:
            pass
        
        # Fallback structured response
        return {
            "user_emotional_state": "neutral",
            "user_intent": "communication",
            "relationship_context": "developing",
            "predicted_needs": ["understanding", "response"],
            "optimal_response_style": "supportive",
            "confidence": 0.6,
            "reasoning": "Local LLM provided unstructured response"
        }


class FallbackProvider(BaseLLMProvider):
    """Fallback provider with intelligent heuristics when no LLM is available"""
    
    def is_available(self) -> bool:
        return True  # Always available as fallback
    
    async def generate_response(self, prompt: str, max_tokens: int = 500) -> LLMResponse:
        """Generate heuristic response based on prompt analysis"""
        # Analyze the prompt for key indicators
        emotional_indicators = {
            "positive": ["happy", "joy", "smile", "😊", "😄", "🥰", "❤️", "🎉"],
            "negative": ["sad", "angry", "frustrated", "😢", "😠", "💔"],
            "curious": ["question", "wonder", "explore", "🤔", "👋", "new"],
            "playful": ["fun", "play", "game", "😄", "🎯", "🎮"]
        }
        
        intent_indicators = {
            "social_connection": ["hello", "hi", "friend", "together", "👋", "🤝"],
            "emotional_support": ["help", "comfort", "support", "care", "❤️", "🤗"],
            "playful_interaction": ["play", "fun", "game", "😄", "🎯", "🎊"],
            "exploration": ["new", "explore", "discover", "try", "🔍", "👀"]
        }
        
        # Simple heuristic analysis
        prompt_lower = prompt.lower()
        
        # Determine emotional state
        emotional_state = "neutral"
        for emotion, indicators in emotional_indicators.items():
            if any(indicator in prompt_lower for indicator in indicators):
                emotional_state = emotion
                break
        
        # Determine intent
        user_intent = "social_connection"
        for intent, indicators in intent_indicators.items():
            if any(indicator in prompt_lower for indicator in indicators):
                user_intent = intent
                break
        
        # Generate contextual response
        relationship_contexts = {
            "social_connection": "building_connection",
            "emotional_support": "providing_comfort", 
            "playful_interaction": "engaging_playfully",
            "exploration": "encouraging_discovery"
        }
        
        predicted_needs = {
            "positive": ["positive_feedback", "shared_joy"],
            "negative": ["emotional_support", "understanding"],
            "curious": ["information", "exploration"],
            "playful": ["engagement", "fun_interaction"],
            "neutral": ["acknowledgment", "gentle_interaction"]
        }
        
        response_styles = {
            "positive": "enthusiastic_and_warm",
            "negative": "gentle_and_supportive", 
            "curious": "informative_and_encouraging",
            "playful": "fun_and_energetic",
            "neutral": "warm_and_responsive"
        }
        
        return LLMResponse(
            content={
                "user_emotional_state": emotional_state,
                "user_intent": user_intent,
                "relationship_context": relationship_contexts.get(user_intent, "ongoing_interaction"),
                "predicted_needs": predicted_needs.get(emotional_state, ["basic_interaction"]),
                "optimal_response_style": response_styles.get(emotional_state, "adaptive"),
                "confidence": 0.6,
                "reasoning": f"Heuristic analysis detected {emotional_state} emotion and {user_intent} intent based on prompt patterns"
            },
            confidence=0.6,
            reasoning="Intelligent heuristic analysis (no LLM available)",
            provider="fallback",
            tokens_used=0,
            response_time=0.01
        )


class LLMClient:
    """Main LLM client with provider fallback chain"""
    
    def __init__(self):
        self.providers: List[BaseLLMProvider] = []
        self._setup_providers()
        
    def _setup_providers(self):
        """Initialize providers in order of preference"""
        # 1. Try OpenAI first (most reliable)
        openai_provider = OpenAIProvider()
        if openai_provider.is_available():
            self.providers.append(openai_provider)
            logger.info("OpenAI provider configured successfully")
        else:
            logger.warning("OpenAI provider not available - missing API key")
        
        # 2. Try local LLM second
        local_provider = LocalLLMProvider()
        if local_provider.is_available():
            self.providers.append(local_provider)
            logger.info("Local LLM provider configured")
        
        # 3. Always have fallback
        self.providers.append(FallbackProvider())
        logger.info(f"LLM client initialized with {len(self.providers)} providers")
    
    async def generate_semantic_analysis(
        self, 
        prompt: str, 
        max_retries: int = 2,
        max_tokens: int = 500
    ) -> LLMResponse:
        """Generate semantic analysis with provider fallback"""
        
        last_exception = None
        
        for provider in self.providers:
            for attempt in range(max_retries + 1):
                try:
                    logger.debug(f"Attempting semantic analysis with {provider.__class__.__name__} (attempt {attempt + 1})")
                    response = await provider.generate_response(prompt, max_tokens)
                    
                    logger.info(f"Successful semantic analysis via {response.provider} (confidence: {response.confidence:.2f})")
                    return response
                    
                except Exception as e:
                    last_exception = e
                    logger.warning(f"{provider.__class__.__name__} attempt {attempt + 1} failed: {e}")
                    
                    if attempt < max_retries:
                        await asyncio.sleep(0.5 * (attempt + 1))  # Exponential backoff
                    continue
            
            # If all retries failed for this provider, try next one
            logger.warning(f"All attempts failed for {provider.__class__.__name__}, trying next provider")
        
        # If we get here, all providers failed
        logger.error(f"All LLM providers failed. Last error: {last_exception}")
        raise Exception(f"All LLM providers exhausted. Final error: {last_exception}")
    
    def get_provider_status(self) -> Dict[str, bool]:
        """Get status of all configured providers"""
        return {
            provider.__class__.__name__: provider.is_available()
            for provider in self.providers
        }


# Global LLM client instance
llm_client = LLMClient()