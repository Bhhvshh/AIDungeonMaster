"""
Configuration settings for the AI Dungeon Master backend
"""

from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List
import json


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # API Configuration
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 5000
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ]
    
    @field_validator('CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS_ORIGINS from string or JSON"""
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            # Try JSON first
            if v.startswith('['):
                try:
                    return json.loads(v)
                except json.JSONDecodeError:
                    pass
            # Fall back to comma-separated
            return [url.strip() for url in v.split(',') if url.strip()]
        return v
    
    # Gemini API Configuration
    GEMINI_API_KEY: str = ""
    # Primary model to use (recommended: gemini-2.0-flash for latest features)
    # Available: gemini-2.0-flash, gemini-1.5-pro, gemini-1.5-flash, gemini-pro
    GEMINI_MODEL: str = "gemini-2.0-flash"
    
    # Fallback models if primary is unavailable
    GEMINI_FALLBACK_MODELS: List[str] = [
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-pro",
    ]
    
    # Game Configuration
    MAX_MEMORY_ENTRIES: int = 50
    SESSION_TIMEOUT_MINUTES: int = 60
    
    # Player Starting Stats
    STARTING_HP: int = 100
    STARTING_GOLD: int = 50
    STARTING_LEVEL: int = 1
    STARTING_INVENTORY: List[str] = [
        "rusty sword",
        "leather armor",
        "5 gold coins"
    ]
    
    # Game Prompts
    SYSTEM_PROMPT: str = """You are an expert Dungeon Master for a fantasy RPG. Your role is to:
1. Create immersive, engaging storytelling
2. Respond to player actions with vivid descriptions
3. Present exactly 3 meaningful choices after each scenario
4. Keep track of the story context and player progress
5. Be creative but maintain story consistency
6. Make choices that feel consequential and affect the story

Always end your response with exactly 3 numbered choices.
Format: "What do you choose?\\n1. [Choice 1]\\n2. [Choice 2]\\n3. [Choice 3]"

Current Player Context:
- Name: {player_name}
- Health: {health}/100
- Level: {level}
- Gold: {gold}
- Inventory: {inventory}
"""
    
    INITIAL_STORY: str = """You awaken in a dimly lit dungeon cell. The musty air fills your lungs as consciousness slowly returns to you. 

Ancient stone walls surround you, weathered and cold to the touch. A single iron torch flickers in a rusted sconce outside your cell, casting dancing shadows across the damp floor. You can make out the faint outlines of the corridor beyond the iron bars of your prison.

As your eyes adjust to the darkness, you notice your equipment is still with you—a well-worn leather armor, a trusty sword hanging at your side, and a small pouch of coins at your belt. Fortune smiles upon you: the cell door stands slightly ajar, creaking softly with each draft that whistles through the dungeon.

In the distance, you hear the echo of footsteps and the faint sound of water dripping from the cavern ceiling. Your adventure begins now. What will you do?"""
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Load settings
settings = Settings()
