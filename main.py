"""
Main entry point for the AI Dungeon Master game
Handles the game loop, user interface, and coordinates all game components
"""

import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, IntPrompt
from rich.markdown import Markdown
from typing import List, Optional

from config import Config
from memory import GameMemory
from dungeon_master import DungeonMaster

class GameInterface:
    """Main game interface and controller"""
    
    def __init__(self):
        """Initialize the game interface"""
        self.console = Console()
        self.memory = GameMemory()
        self.dm = DungeonMaster(self.memory)
        self.current_choices: List[str] = []
        
    def display_welcome(self):
        """Display the welcome screen and game introduction"""
        welcome_text = """
# 🏰 Welcome to AI Dungeon Master! 🎲

An interactive text-based RPG where an AI acts as your Dungeon Master, 
guiding you through epic adventures with intelligent storytelling.

## How to Play:
- Read the story scenarios carefully
- Choose from 3 options presented to you (1, 2, or 3)
- The AI will remember your actions and adapt the story accordingly
- Your stats and inventory will be tracked throughout your journey

## Commands:
- Type `1`, `2`, or `3` to make choices
- Type `stats` to view your character status
- Type `save` to save your game
- Type `load` to load a saved game
- Type `quit` or `exit` to end the game

*May your adventure be legendary!* ⚔️
        """
        
        self.console.print(Panel(Markdown(welcome_text), title="🎮 AI Dungeon Master", border_style="bright_blue"))
        
        # Ask for player name
        player_name = Prompt.ask("\n🧙‍♂️ What is your adventurer's name?", default="Adventurer")
        self.memory.update_player_stats(name=player_name)
        
        self.console.print(f"\n✨ Welcome, {player_name}! Your adventure begins...\n")
    
    def display_story(self, story_text: str, choices: List[str]):
        """
        Display story text and available choices
        
        Args:
            story_text (str): The narrative text to display
            choices (List[str]): List of 3 choices for the player
        """
        # Display the story in a panel
        story_panel = Panel(
            Text(story_text, justify="left"),
            title="📖 Story",
            border_style="green"
        )
        self.console.print(story_panel)
        
        # Display choices
        choices_text = "\n🎯 **What do you choose?**\n"
        for i, choice in enumerate(choices, 1):
            choices_text += f"{i}. {choice}\n"
        
        choices_panel = Panel(
            Markdown(choices_text),
            title="⚡ Your Options",
            border_style="yellow"
        )
        self.console.print(choices_panel)
        
        self.current_choices = choices
    
    def get_player_input(self) -> str:
        """
        Get and validate player input
        
        Returns:
            str: The validated player input
        """
        while True:
            try:
                user_input = Prompt.ask("\n🎮 Your choice", default="").strip().lower()
                
                # Handle special commands
                if user_input in ['quit', 'exit']:
                    return 'quit'
                elif user_input == 'stats':
                    self.display_stats()
                    continue
                elif user_input == 'save':
                    self.save_game()
                    continue
                elif user_input == 'load':
                    self.load_game()
                    continue
                elif user_input in ['1', '2', '3']:
                    choice_num = int(user_input)
                    if 1 <= choice_num <= len(self.current_choices):
                        return self.dm.process_player_choice(choice_num, self.current_choices)
                    else:
                        self.console.print("❌ Invalid choice. Please select 1, 2, or 3.", style="red")
                        continue
                elif user_input == '':
                    self.console.print("❌ Please make a choice (1, 2, or 3) or use a command.", style="red")
                    continue
                else:
                    self.console.print("❌ Invalid input. Use 1, 2, or 3 to make choices.", style="red")
                    self.console.print("   Or use: 'stats', 'save', 'load', 'quit'", style="dim")
                    continue
                    
            except KeyboardInterrupt:
                self.console.print("\n\n👋 Thanks for playing! Your adventure ends here.")
                return 'quit'
    
    def display_stats(self):
        """Display player statistics"""
        stats_text = self.memory.get_player_status()
        stats_panel = Panel(
            Text(stats_text, justify="left"),
            title="📊 Character Status",
            border_style="blue"
        )
        self.console.print(stats_panel)
    
    def save_game(self):
        """Handle game saving"""
        try:
            filename = Prompt.ask("💾 Save filename", default=Config.SAVE_FILE)
            self.memory.save_game(filename)
        except Exception as e:
            self.console.print(f"❌ Error saving game: {e}", style="red")
    
    def load_game(self) -> bool:
        """
        Handle game loading
        
        Returns:
            bool: True if game was loaded successfully
        """
        try:
            filename = Prompt.ask("📂 Load filename", default=Config.SAVE_FILE)
            if self.memory.load_game(filename):
                self.console.print("✅ Game loaded successfully!", style="green")
                return True
            return False
        except Exception as e:
            self.console.print(f"❌ Error loading game: {e}", style="red")
            return False
    
    def run_game_loop(self):
        """Main game loop"""
        try:
            # Check if user wants to load a saved game
            if Prompt.ask("\n🎮 Do you want to load a saved game?", choices=["yes", "no"], default="no") == "yes":
                if self.load_game():
                    # Display current status after loading
                    self.display_stats()
                    
                    # Continue from where they left off
                    last_story = "You continue your adventure from where you left off..."
                    if self.memory.story_history:
                        last_entry = self.memory.story_history[-1]
                        self.current_choices = last_entry.get('choices', [
                            "Look around for new opportunities",
                            "Check your equipment and supplies", 
                            "Consider your next move carefully"
                        ])
                    else:
                        story_text, self.current_choices = self.dm.start_new_adventure()
                        last_story = story_text
                    
                    self.display_story(last_story, self.current_choices)
                else:
                    # If load failed, start new game
                    story_text, self.current_choices = self.dm.start_new_adventure()
                    self.display_story(story_text, self.current_choices)
            else:
                # Start new adventure
                story_text, self.current_choices = self.dm.start_new_adventure()
                self.display_story(story_text, self.current_choices)
            
            # Main game loop
            while True:
                player_action = self.get_player_input()
                
                if player_action == 'quit':
                    break
                
                # Show thinking indicator
                with self.console.status("🤔 The Dungeon Master ponders your action...", spinner="dots"):
                    dm_response, new_choices = self.dm.generate_response(player_action)
                
                # Update memory
                self.memory.add_story_entry(player_action, dm_response, new_choices)
                
                # Display the new story development
                self.console.print()  # Add spacing
                self.display_story(dm_response, new_choices)
                
                # Auto-save progress periodically
                if len(self.memory.story_history) % 5 == 0:
                    self.memory.save_game("autosave.json")
        
        except KeyboardInterrupt:
            self.console.print("\n\n👋 Game interrupted. Thanks for playing!")
        except Exception as e:
            self.console.print(f"\n❌ Unexpected error: {e}", style="red")
            self.console.print("The game will attempt to save your progress...", style="yellow")
            self.memory.save_game("emergency_save.json")

def main():
    """Main entry point for the game"""
    game = GameInterface()
    
    # Display welcome screen
    game.display_welcome()
    
    # Check if Gemini API is configured
    if not Config.GEMINI_API_KEY:
        demo_warning = """
⚠️  **Demo Mode Active** ⚠️

Gemini API key not found. The game will run with pre-scripted responses.

To enable full AI functionality:
1. Get an API key from Google AI Studio (https://aistudio.google.com/app/apikey)
2. Create a `.env` file in the project directory
3. Add: `GEMINI_API_KEY=your_key_here`

The demo version still provides a fun experience with basic story progression!
        """
        game.console.print(Panel(Markdown(demo_warning), border_style="yellow"))
    
    # Start the game
    game.run_game_loop()
    
    # Farewell message
    farewell_text = """
# 🏰 Thanks for Playing AI Dungeon Master! 🎲

Your adventure may have ended, but the memories will last forever.
Feel free to return anytime to continue your journey or start a new one!

*May your next adventure be even more epic!* ⚔️✨
    """
    
    game.console.print(Panel(Markdown(farewell_text), title="👋 Farewell, Adventurer!", border_style="bright_magenta"))

if __name__ == "__main__":
    main()
