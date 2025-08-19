"""
Example extension: NPC System
Shows how to add NPCs (Non-Player Characters) to the AI Dungeon Master
"""

from typing import Dict, List
import json

class NPC:
    """Represents a Non-Player Character in the game"""
    
    def __init__(self, name: str, description: str, personality: str, location: str = ""):
        self.name = name
        self.description = description
        self.personality = personality
        self.location = location
        self.relationship_level = 0  # -100 (hostile) to 100 (friendly)
        self.dialogue_history: List[str] = []
        self.items: List[str] = []
        self.quests: List[str] = []
        self.alive = True
    
    def add_dialogue(self, dialogue: str):
        """Add dialogue to NPC's history"""
        self.dialogue_history.append(dialogue)
        if len(self.dialogue_history) > 10:  # Keep only recent dialogues
            self.dialogue_history = self.dialogue_history[-10:]
    
    def adjust_relationship(self, change: int):
        """Adjust relationship level with bounds"""
        self.relationship_level = max(-100, min(100, self.relationship_level + change))
    
    def to_dict(self) -> Dict:
        """Convert NPC to dictionary for saving"""
        return {
            "name": self.name,
            "description": self.description,
            "personality": self.personality,
            "location": self.location,
            "relationship_level": self.relationship_level,
            "dialogue_history": self.dialogue_history,
            "items": self.items,
            "quests": self.quests,
            "alive": self.alive
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'NPC':
        """Create NPC from dictionary"""
        npc = cls(data["name"], data["description"], data["personality"], data["location"])
        npc.relationship_level = data.get("relationship_level", 0)
        npc.dialogue_history = data.get("dialogue_history", [])
        npc.items = data.get("items", [])
        npc.quests = data.get("quests", [])
        npc.alive = data.get("alive", True)
        return npc

class NPCManager:
    """Manages all NPCs in the game"""
    
    def __init__(self):
        self.npcs: Dict[str, NPC] = {}
        self._create_default_npcs()
    
    def _create_default_npcs(self):
        """Create some default NPCs for the game"""
        self.add_npc(NPC(
            name="Eldara the Wise",
            description="An ancient elf mage with silver hair and knowing eyes",
            personality="Wise, cryptic, helpful to those who prove themselves worthy",
            location="Ancient Library"
        ))
        
        self.add_npc(NPC(
            name="Grunk the Guard",
            description="A burly orc guard with battle scars and a stern expression", 
            personality="Suspicious of strangers, but respects strength and honor",
            location="Castle Gates"
        ))
        
        self.add_npc(NPC(
            name="Pip the Merchant",
            description="A cheerful halfling trader with a cart full of mysterious goods",
            personality="Friendly, greedy, always looking for a good deal",
            location="Market Square"
        ))
    
    def add_npc(self, npc: NPC):
        """Add an NPC to the game"""
        self.npcs[npc.name.lower()] = npc
    
    def get_npc(self, name: str) -> NPC:
        """Get an NPC by name"""
        return self.npcs.get(name.lower())
    
    def get_npcs_in_location(self, location: str) -> List[NPC]:
        """Get all NPCs in a specific location"""
        return [npc for npc in self.npcs.values() if npc.location.lower() == location.lower()]
    
    def get_npc_context_for_ai(self, player_location: str) -> str:
        """Get NPC context for AI based on player location"""
        local_npcs = self.get_npcs_in_location(player_location)
        if not local_npcs:
            return ""
        
        context = f"NPCs in {player_location}:\n"
        for npc in local_npcs:
            relationship = "friendly" if npc.relationship_level > 20 else "neutral" if npc.relationship_level > -20 else "hostile"
            context += f"- {npc.name}: {npc.description} (Relationship: {relationship})\n"
            if npc.dialogue_history:
                context += f"  Recent interaction: {npc.dialogue_history[-1]}\n"
        
        return context
    
    def save_npcs(self, filename: str = "npcs_save.json"):
        """Save all NPCs to file"""
        npc_data = {name: npc.to_dict() for name, npc in self.npcs.items()}
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(npc_data, f, indent=2, ensure_ascii=False)
            print(f"✅ NPCs saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving NPCs: {e}")
    
    def load_npcs(self, filename: str = "npcs_save.json") -> bool:
        """Load NPCs from file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                npc_data = json.load(f)
            
            self.npcs = {name: NPC.from_dict(data) for name, data in npc_data.items()}
            print(f"✅ NPCs loaded from {filename}")
            return True
        except FileNotFoundError:
            print(f"❌ NPC save file {filename} not found")
            return False
        except Exception as e:
            print(f"❌ Error loading NPCs: {e}")
            return False

# Example of how to integrate NPCs with the existing game system
class ExtendedGameMemory:
    """Extended version of GameMemory that includes NPC management"""
    
    def __init__(self):
        # Include all original GameMemory functionality
        from memory import GameMemory
        self.base_memory = GameMemory()
        
        # Add NPC management
        self.npc_manager = NPCManager()
    
    def get_context_for_ai(self) -> str:
        """Enhanced context that includes NPC information"""
        base_context = self.base_memory.get_context_for_ai()
        npc_context = self.npc_manager.get_npc_context_for_ai(self.base_memory.player_stats["location"])
        
        if npc_context:
            return f"{base_context}\n\n{npc_context}"
        return base_context
    
    def interact_with_npc(self, npc_name: str, interaction_type: str, dialogue: str = ""):
        """Record an interaction with an NPC"""
        npc = self.npc_manager.get_npc(npc_name)
        if npc:
            npc.add_dialogue(dialogue)
            
            # Adjust relationship based on interaction type
            relationship_changes = {
                "friendly": 5,
                "helpful": 10,
                "aggressive": -15,
                "trade": 3,
                "quest_complete": 20
            }
            
            if interaction_type in relationship_changes:
                npc.adjust_relationship(relationship_changes[interaction_type])
    
    def save_extended_game(self, filename: str = "extended_save.json"):
        """Save game with NPC data"""
        self.base_memory.save_game(filename)
        npc_filename = filename.replace(".json", "_npcs.json")
        self.npc_manager.save_npcs(npc_filename)

def demo_npc_system():
    """Demonstrate the NPC system"""
    print("🧙‍♂️ AI Dungeon Master - NPC System Demo")
    print("=" * 45)
    
    # Create extended memory with NPCs
    extended_memory = ExtendedGameMemory()
    
    # Simulate player entering different locations
    locations = ["Ancient Library", "Castle Gates", "Market Square"]
    
    for location in locations:
        print(f"\n📍 Player enters: {location}")
        extended_memory.base_memory.update_player_stats(location=location)
        
        # Get NPCs in this location
        npcs = extended_memory.npc_manager.get_npcs_in_location(location)
        for npc in npcs:
            print(f"  👤 {npc.name}: {npc.description}")
            print(f"     Personality: {npc.personality}")
            print(f"     Relationship: {npc.relationship_level}")
        
        # Simulate interaction
        if npcs:
            npc = npcs[0]
            print(f"\n  🗣️  Interacting with {npc.name}...")
            extended_memory.interact_with_npc(npc.name, "friendly", "The player greets the NPC politely")
            print(f"     Relationship changed to: {npc.relationship_level}")
    
    # Show enhanced context
    print(f"\n🎯 Enhanced AI Context:\n{extended_memory.get_context_for_ai()}")
    
    # Save the extended game
    print("\n💾 Saving extended game...")
    extended_memory.save_extended_game("demo_extended.json")
    
    print("\n✅ NPC system demo completed!")

if __name__ == "__main__":
    demo_npc_system()
