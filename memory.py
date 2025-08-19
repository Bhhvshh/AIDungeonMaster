"""
Memory management system for the AI Dungeon Master
Handles game history, player stats, and save/load functionality
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any
from config import Config

class GameMemory:
    """Manages game state, history, and player information"""
    
    def __init__(self):
        """Initialize game memory with default values"""
        self.story_history: List[Dict[str, Any]] = []
        self.player_stats = {
            "name": "Adventurer",
            "hp": Config.STARTING_HP,
            "max_hp": Config.STARTING_HP,
            "inventory": Config.STARTING_INVENTORY.copy(),
            "location": "Dungeon Cell",
            "level": 1,
            "experience": 0
        }
        self.game_start_time = datetime.now()
        self.npcs_met: List[str] = []
        self.completed_quests: List[str] = []
        
    def add_story_entry(self, player_action: str, dm_response: str, choices: List[str]):
        """
        Add a new story entry to the game history
        
        Args:
            player_action (str): The action the player took
            dm_response (str): The DM's response to the action
            choices (List[str]): The choices presented to the player
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "player_action": player_action,
            "dm_response": dm_response,
            "choices": choices,
            "player_stats": self.player_stats.copy()
        }
        
        self.story_history.append(entry)
        
        # Limit memory to prevent context overflow
        if len(self.story_history) > Config.MAX_MEMORY_ENTRIES:
            self.story_history = self.story_history[-Config.MAX_MEMORY_ENTRIES:]
    
    def update_player_stats(self, **kwargs):
        """
        Update player statistics
        
        Args:
            **kwargs: Key-value pairs of stats to update
        """
        for key, value in kwargs.items():
            if key in self.player_stats:
                self.player_stats[key] = value
    
    def add_to_inventory(self, item: str):
        """
        Add an item to player's inventory
        
        Args:
            item (str): Item to add to inventory
        """
        self.player_stats["inventory"].append(item)
    
    def remove_from_inventory(self, item: str) -> bool:
        """
        Remove an item from player's inventory
        
        Args:
            item (str): Item to remove from inventory
            
        Returns:
            bool: True if item was removed, False if item not found
        """
        if item in self.player_stats["inventory"]:
            self.player_stats["inventory"].remove(item)
            return True
        return False
    
    def get_context_for_ai(self) -> str:
        """
        Generate context string for AI based on recent history and current stats
        
        Returns:
            str: Formatted context string for the AI
        """
        context = f"Current Player Stats: {self.player_stats}\n\n"
        
        if self.story_history:
            context += "Recent Story History:\n"
            # Include last 5 entries for context
            recent_history = self.story_history[-5:]
            for i, entry in enumerate(recent_history, 1):
                context += f"{i}. Player: {entry['player_action']}\n"
                context += f"   DM: {entry['dm_response'][:200]}{'...' if len(entry['dm_response']) > 200 else ''}\n\n"
        
        if self.npcs_met:
            context += f"NPCs Met: {', '.join(self.npcs_met)}\n"
        
        if self.completed_quests:
            context += f"Completed Quests: {', '.join(self.completed_quests)}\n"
        
        return context
    
    def save_game(self, filename: str = None):
        """
        Save the current game state to a JSON file
        
        Args:
            filename (str, optional): Custom filename for save file
        """
        if filename is None:
            filename = Config.SAVE_FILE
        
        save_data = {
            "story_history": self.story_history,
            "player_stats": self.player_stats,
            "game_start_time": self.game_start_time.isoformat(),
            "npcs_met": self.npcs_met,
            "completed_quests": self.completed_quests
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            print(f"✅ Game saved successfully to {filename}")
        except Exception as e:
            print(f"❌ Error saving game: {e}")
    
    def load_game(self, filename: str = None) -> bool:
        """
        Load a previously saved game state
        
        Args:
            filename (str, optional): Custom filename to load from
            
        Returns:
            bool: True if load was successful, False otherwise
        """
        if filename is None:
            filename = Config.SAVE_FILE
        
        if not os.path.exists(filename):
            print(f"❌ Save file {filename} not found")
            return False
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            self.story_history = save_data.get("story_history", [])
            self.player_stats = save_data.get("player_stats", {})
            self.npcs_met = save_data.get("npcs_met", [])
            self.completed_quests = save_data.get("completed_quests", [])
            
            if "game_start_time" in save_data:
                self.game_start_time = datetime.fromisoformat(save_data["game_start_time"])
            
            print(f"✅ Game loaded successfully from {filename}")
            return True
        except Exception as e:
            print(f"❌ Error loading game: {e}")
            return False
    
    def get_player_status(self) -> str:
        """
        Get formatted player status string
        
        Returns:
            str: Formatted player status
        """
        status = f"""
📊 Player Status:
  Name: {self.player_stats['name']}
  HP: {self.player_stats['hp']}/{self.player_stats['max_hp']}
  Level: {self.player_stats['level']} (XP: {self.player_stats['experience']})
  Location: {self.player_stats['location']}
  
🎒 Inventory: {', '.join(self.player_stats['inventory'])}
        """.strip()
        return status
