"""
Demonstration script for the AI Dungeon Master
Shows how the game components work together
"""

from config import Config
from memory import GameMemory
from dungeon_master import DungeonMaster

def demo_game():
    """Demonstrate the game functionality"""
    print("🎮 AI Dungeon Master - Demo Mode")
    print("=" * 50)
    
    # Initialize game components
    memory = GameMemory()
    dm = DungeonMaster(memory)
    
    # Set up a demo player
    memory.update_player_stats(name="Demo Hero", hp=80)
    memory.add_to_inventory("magic potion")
    
    print(f"✅ Initialized game with player: {memory.player_stats['name']}")
    print(f"📊 Player Stats: {memory.player_stats}")
    
    # Start adventure
    print("\n🏰 Starting Adventure...")
    story, choices = dm.start_new_adventure()
    print(f"\n📖 Initial Story:\n{story}")
    print(f"\n⚡ Choices:")
    for i, choice in enumerate(choices, 1):
        print(f"  {i}. {choice}")
    
    # Simulate player actions
    demo_actions = [
        "I choose to: Carefully push open the cell door and step into the corridor",
        "I choose to: Follow the cool breeze toward a possible exit",
        "I choose to: Open the mysterious chest"
    ]
    
    for action in demo_actions:
        print(f"\n🎮 Player Action: {action}")
        
        # Generate AI response
        response, new_choices = dm.generate_response(action)
        
        # Update memory
        memory.add_story_entry(action, response, new_choices)
        
        print(f"\n🤖 DM Response:\n{response}")
        print(f"\n⚡ New Choices:")
        for i, choice in enumerate(new_choices, 1):
            print(f"  {i}. {choice}")
    
    # Show final stats
    print(f"\n📊 Final Player Status:\n{memory.get_player_status()}")
    print(f"\n💾 Story History: {len(memory.story_history)} entries")
    
    # Demonstrate save/load
    print("\n💾 Saving game...")
    memory.save_game("demo_save.json")
    
    print("✅ Demo completed successfully!")

if __name__ == "__main__":
    demo_game()
