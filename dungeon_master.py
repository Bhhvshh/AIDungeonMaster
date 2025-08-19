"""
AI Dungeon Master - Handles all AI interactions and storytelling
Uses Google Gemini to generate responses and manage the game narrative
"""

import re
from typing import List, Tuple, Optional
import google.generativeai as genai
from config import Config
from memory import GameMemory

class DungeonMaster:
    """AI-powered Dungeon Master for text-based RPG"""
    
    def __init__(self, memory: GameMemory):
        """
        Initialize the Dungeon Master with game memory
        
        Args:
            memory (GameMemory): Game memory instance to track game state
        """
        self.memory = memory
        self.model = None
        self._initialize_gemini()
    
    def _initialize_gemini(self):
        """Initialize Gemini client with API key"""
        if not Config.GEMINI_API_KEY:
            print("⚠️  Warning: Gemini API key not found. Please set GEMINI_API_KEY in your .env file")
            print("   The game will run in demo mode with pre-scripted responses.")
            return
        
        try:
            genai.configure(api_key=Config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
            print("✅ Gemini API connected successfully")
        except Exception as e:
            print(f"❌ Error connecting to Gemini API: {e}")
            print("   The game will run in demo mode with pre-scripted responses.")
            self.model = None
    
    def generate_response(self, player_action: str) -> Tuple[str, List[str]]:
        """
        Generate AI response to player action
        
        Args:
            player_action (str): The action the player wants to take
            
        Returns:
            Tuple[str, List[str]]: DM response and list of 3 choices for the player
        """
        if self.model is None:
            return self._demo_response(player_action)
        
        try:
            # Prepare the context for the AI
            context = self.memory.get_context_for_ai()
            
            prompt = f"""{Config.SYSTEM_PROMPT}

Context:
{context}

Player Action: {player_action}

Please respond as the Dungeon Master and provide exactly 3 choices at the end."""
            
            response = self.model.generate_content(prompt)
            full_response = response.text.strip()
            
            # Parse the response to extract choices
            dm_response, choices = self._parse_ai_response(full_response)
            
            return dm_response, choices
            
        except Exception as e:
            print(f"❌ Error generating AI response: {e}")
            return self._demo_response(player_action)
    
    def _parse_ai_response(self, response: str) -> Tuple[str, List[str]]:
        """
        Parse AI response to separate narrative from choices
        
        Args:
            response (str): Full AI response text
            
        Returns:
            Tuple[str, List[str]]: Separated narrative and choices
        """
        # Look for the choices section
        choice_pattern = r"What do you choose\?\s*\n1\.\s*(.+)\n2\.\s*(.+)\n3\.\s*(.+)"
        match = re.search(choice_pattern, response, re.IGNORECASE)
        
        if match:
            # Split response at the choices
            narrative_end = response.find("What do you choose?")
            narrative = response[:narrative_end].strip()
            choices = [match.group(1).strip(), match.group(2).strip(), match.group(3).strip()]
        else:
            # Fallback: try to find numbered choices anywhere in the text
            lines = response.split('\n')
            choices = []
            narrative_lines = []
            
            for line in lines:
                line = line.strip()
                if re.match(r'^[123]\.\s*', line):
                    choice_text = re.sub(r'^[123]\.\s*', '', line).strip()
                    choices.append(choice_text)
                elif not line.startswith(('1.', '2.', '3.')) and line:
                    narrative_lines.append(line)
            
            narrative = '\n'.join(narrative_lines).strip()
            
            # Ensure we have exactly 3 choices
            if len(choices) < 3:
                choices.extend([
                    "Examine your surroundings more carefully",
                    "Check your inventory and equipment", 
                    "Wait and listen for any sounds"
                ][len(choices):])
        
        return narrative, choices[:3]  # Ensure exactly 3 choices
    
    def _demo_response(self, player_action: str) -> Tuple[str, List[str]]:
        """
        Generate demo responses when Gemini API is not available
        
        Args:
            player_action (str): Player's action
            
        Returns:
            Tuple[str, List[str]]: Demo response and choices
        """
        demo_responses = {
            "start": (
                "You find yourself in a mysterious dungeon. The stone walls are damp with moisture, "
                "and strange symbols glow faintly on the walls. A cool breeze suggests there might be "
                "an exit nearby, but you can also hear the sound of dripping water echoing from deeper within.",
                [
                    "Follow the cool breeze toward a possible exit",
                    "Investigate the glowing symbols on the wall",
                    "Head deeper into the dungeon toward the sound of water"
                ]
            ),
            "north": (
                "You walk north and discover a grand chamber with three passageways. Ancient torches "
                "flicker along the walls, casting dancing shadows. In the center of the room, you notice "
                "a dusty old chest that might contain treasure.",
                [
                    "Open the mysterious chest",
                    "Take the left passageway",
                    "Examine the torch flames more closely"
                ]
            ),
            "attack": (
                "Your attack connects! The creature staggers back, wounded but still dangerous. "
                "Your sword gleams with an unexpected magical light after striking the beast. "
                "The creature's eyes glow red with fury as it prepares its counterattack.",
                [
                    "Press the attack while the creature is wounded",
                    "Try to negotiate with the intelligent creature",
                    "Retreat to a defensive position"
                ]
            )
        }
        
        # Simple keyword matching for demo responses
        action_lower = player_action.lower()
        if any(word in action_lower for word in ["north", "forward", "ahead"]):
            return demo_responses["north"]
        elif any(word in action_lower for word in ["attack", "fight", "hit", "strike"]):
            return demo_responses["attack"]
        else:
            return demo_responses["start"]
    
    def start_new_adventure(self) -> Tuple[str, List[str]]:
        """
        Start a new adventure with the initial scenario
        
        Returns:
            Tuple[str, List[str]]: Initial scenario and starting choices
        """
        initial_choices = [
            "Carefully push open the cell door and step into the corridor",
            "Search the cell thoroughly for any useful items or clues",
            "Call out to see if anyone responds to your voice"
        ]
        
        return Config.INITIAL_SCENARIO, initial_choices
    
    def process_player_choice(self, choice_number: int, choices: List[str]) -> str:
        """
        Convert player's choice number to action text
        
        Args:
            choice_number (int): The number (1-3) the player selected
            choices (List[str]): List of available choices
            
        Returns:
            str: The action text corresponding to the choice
        """
        if 1 <= choice_number <= len(choices):
            return f"I choose to: {choices[choice_number - 1]}"
        else:
            return "I look around uncertainly, unsure what to do next."
