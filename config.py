"""
Configuration file for AI Dungeon Master
Contains API keys, settings, and game constants
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the AI Dungeon Master game"""
    
    # Google Gemini API Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = "gemini-1.5-flash"
    
    # Game Settings
    MAX_MEMORY_ENTRIES = 50  # Maximum number of story entries to keep in memory
    SAVE_FILE = "game_save.json"
    
    # Player Starting Stats
    STARTING_HP = 100
    STARTING_INVENTORY = ["rusty sword", "leather armor", "5 gold coins"]
    
    # Game Prompts
    SYSTEM_PROMPT = """
    You are an expert Dungeon Master for a fantasy RPG. Your role is to:
    1. Create immersive, engaging storytelling
    2. Respond to player actions with vivid descriptions
    3. Present exactly 3 meaningful choices after each scenario
    4. Keep track of the story context and player progress
    5. Be creative but maintain story consistency
    
    Always end your response with exactly 3 numbered choices for the player.
    Format: "What do you choose?\n1. [Choice 1]\n2. [Choice 2]\n3. [Choice 3]"
    
    Consider the player's current stats and inventory when crafting scenarios.
    """
    
    INITIAL_SCENARIO = """
    You awaken in a dimly lit dungeon cell. The musty air fills your lungs as you slowly regain consciousness. 
    Ancient stone walls surround you, and a faint light flickers from a torch in the corridor beyond the iron bars. 
    You notice your basic equipment is still with you - your trusty sword, leather armor, and a small pouch of coins.
    
    As your eyes adjust to the darkness, you hear distant footsteps echoing through the dungeon halls. 
    The cell door appears to be unlocked, swinging slightly ajar. Your adventure begins now...
    """
