"""
AI Manager - Handles all interactions with Google Gemini API
"""

import google.genai as genai
import re
from typing import Tuple, List, Optional
from config import settings
import logging

logger = logging.getLogger(__name__)


class AIManager:
    """Manages AI interactions with Google Gemini"""
    
    def __init__(self):
        """Initialize the AI manager"""
        self.client = None
        self.model_name = None
        self.available = False
        self._initialize_gemini()
    
    def _initialize_gemini(self) -> None:
        """Initialize Gemini API connection with fallback model support"""
        if not settings.GEMINI_API_KEY:
            logger.warning("Gemini API key not configured. AI features will be unavailable.")
            self.available = False
            return
        
        try:
            # Initialize the Gemini client with API key
            self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
            self.model_name = settings.GEMINI_MODEL
            self.available = True
            logger.info(f"✅ Gemini API initialized successfully with model: {settings.GEMINI_MODEL}")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize Gemini API: {e}")
            self.available = False
    
    def generate_story_response(
        self,
        player_action: str,
        game_context: str,
        player_name: str,
        health: int,
        level: int,
        gold: int,
        inventory: List[str]
    ) -> Tuple[str, List[str]]:
        """
        Generate AI story response to player action
        
        Args:
            player_action: Player's chosen action
            game_context: Current game context/history
            player_name: Player's name
            health: Player's current health
            level: Player's level
            gold: Player's gold
            inventory: Player's inventory items
        
        Returns:
            Tuple of (story_text, choices_list)
        """
        if not self.available:
            return self._get_fallback_response(player_action)
        
        try:
            # Format the system prompt with player context
            system_prompt = settings.SYSTEM_PROMPT.format(
                player_name=player_name,
                health=health,
                level=level,
                gold=gold,
                inventory=", ".join(inventory) if inventory else "Nothing"
            )
            
            # Build the complete prompt
            prompt = f"""{system_prompt}

Game Context:
{game_context}

Player's Action: {player_action}

Please respond with an engaging story response and exactly 3 numbered choices."""
            
            # Call Gemini API
            try:
                response = self.client.models.generate_content(
                    model=f"models/{self.model_name}",
                    contents=prompt,
                    config={
                        'temperature': 0.8,
                        'top_p': 0.9,
                        'max_output_tokens': 500,
                    }
                )
                full_response = response.text.strip()
                
                # Parse response to extract narrative and choices
                story, choices = self._parse_ai_response(full_response)
                
                if not choices or len(choices) != 3:
                    # If parsing failed, try again with fallback
                    return self._get_fallback_response(player_action)
                
                logger.info(f"Successfully generated story response for action: {player_action[:50]}")
                return story, choices
            
            except Exception as api_error:
                logger.error(f"Gemini API error: {api_error}")
                return self._get_fallback_response(player_action)
            
        except Exception as e:
            logger.error(f"Error in generate_story_response: {e}")
            return self._get_fallback_response(player_action)
    
    def _parse_ai_response(self, response: str) -> Tuple[str, List[str]]:
        """
        Parse AI response to separate narrative from choices
        
        Args:
            response: Full AI response text
        
        Returns:
            Tuple of (narrative, choices)
        """
        try:
            # Look for "What do you choose?" section
            choice_pattern = r"What do you choose\?\s*\n1\.\s*([^\n]+)\n2\.\s*([^\n]+)\n3\.\s*([^\n]+)"
            match = re.search(choice_pattern, response, re.IGNORECASE | re.DOTALL)
            
            if match:
                # Extract narrative (everything before choices)
                narrative_end = response.find("What do you choose?")
                narrative = response[:narrative_end].strip()
                
                choices = [
                    match.group(1).strip(),
                    match.group(2).strip(),
                    match.group(3).strip()
                ]
                
                return narrative, choices
            
            # Fallback: try to find any numbered list
            lines = response.split('\n')
            choices = []
            narrative_lines = []
            parsing_choices = False
            
            for line in lines:
                if re.match(r'^\s*1\.\s*', line):
                    parsing_choices = True
                
                if parsing_choices:
                    # Extract choice text
                    match = re.match(r'^\s*\d+\.\s*(.+)', line)
                    if match:
                        choices.append(match.group(1).strip())
                else:
                    narrative_lines.append(line)
            
            if len(choices) >= 3:
                return '\n'.join(narrative_lines).strip(), choices[:3]
            
            # If still no choices found, return original response with default choices
            return response, ["Continue exploring", "Rest and recover", "Search for clues"]
            
        except Exception as e:
            logger.error(f"Error parsing AI response: {e}")
            return response, ["Continue exploring", "Rest and recover", "Search for clues"]
    
    def _get_fallback_response(self, player_action: str) -> Tuple[str, List[str]]:
        """
        Get fallback response when AI is unavailable
        
        Args:
            player_action: Player's action
        
        Returns:
            Tuple of (story, choices)
        """
        stories = {
            "explore": "You venture deeper into the darkness. Your sword gleams faintly in the torchlight as echoing sounds fill the corridor ahead.",
            "rest": "You find a relatively safe corner and take a moment to catch your breath. Your energy slowly returns.",
            "attack": "You draw your weapon, ready for combat. The air crackles with tension.",
            "escape": "You move cautiously toward what appears to be an exit, staying alert for any dangers.",
        }
        
        story = stories.get(player_action.lower()[:10], 
                           f"You decide to {player_action}. The adventure continues...")
        
        choices = [
            "Continue forward",
            "Examine surroundings",
            "Try something else"
        ]
        
        return story, choices
