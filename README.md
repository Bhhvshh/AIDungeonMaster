# AI Dungeon Master

An interactive text-based RPG powered by AI, where GPT acts as your Dungeon Master!

## 🎮 Features

- **AI-Powered Storytelling**: Uses OpenAI GPT to create dynamic, engaging narratives
- **Choice-Based Gameplay**: Always presents 3 meaningful choices at every decision point
- **Memory System**: Remembers your actions, stats, and story progression
- **Character Stats**: Track HP, inventory, level, and experience
- **Save/Load System**: Continue your adventures across sessions
- **Rich Terminal UI**: Beautiful colored text and formatted displays
- **Demo Mode**: Works even without OpenAI API (with pre-scripted responses)

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key (optional, for full AI functionality)

### Installation

1. **Clone or download this project**
2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up OpenAI API (optional but recommended):**

   - Get an API key from [OpenAI](https://platform.openai.com/api-keys)
   - Copy `.env.example` to `.env`
   - Add your API key to the `.env` file:
     ```
     OPENAI_API_KEY=your_actual_api_key_here
     ```

4. **Run the game:**
   ```bash
   python main.py
   ```

## 🎯 How to Play

1. **Start the Game**: Run `python main.py`
2. **Enter Your Name**: Choose your adventurer's name
3. **Read the Story**: The AI will describe your situation
4. **Make Choices**: Type `1`, `2`, or `3` to select your action
5. **Continue the Adventure**: The AI responds and gives you new choices

### Game Commands

- `1`, `2`, `3` - Make story choices
- `stats` - View your character stats
- `save` - Save your current game
- `load` - Load a previously saved game
- `quit`/`exit` - End the game

## 📁 Project Structure

```
DungeonMaster/
├── main.py              # Game entry point and UI
├── dungeon_master.py    # AI interaction and response generation
├── memory.py            # Game state and history management
├── config.py            # Configuration and settings
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
└── README.md           # This file
```

## 🔧 Configuration

### Game Settings (config.py)

- `OPENAI_MODEL`: AI model to use (default: "gpt-3.5-turbo")
- `MAX_MEMORY_ENTRIES`: How many story entries to remember
- `STARTING_HP`: Player's starting health points
- `STARTING_INVENTORY`: Initial items in player's inventory

### Environment Variables (.env)

- `OPENAI_API_KEY`: Your OpenAI API key for full AI functionality

## 🎲 Game Features Explained

### AI Dungeon Master

- Creates immersive fantasy scenarios
- Responds intelligently to player actions
- Maintains story consistency
- Always provides exactly 3 meaningful choices

### Memory System

- Tracks complete story history
- Remembers player stats (HP, inventory, level, XP)
- Saves NPC interactions and completed quests
- Provides context to AI for consistent storytelling

### Player Progression

- **Health Points**: Combat and hazard management
- **Inventory**: Collect and use items throughout your journey
- **Experience**: Gain XP from successful actions
- **Location Tracking**: Remember where you've been

## 🌐 Extending to Web App

This project is designed to be easily extended to a web application:

### Recommended Approach:

1. **Backend**: Use Flask or FastAPI to expose the game logic as REST APIs
2. **Frontend**: Create a web interface with HTML/CSS/JavaScript
3. **Database**: Replace JSON save files with PostgreSQL/MongoDB
4. **Real-time**: Add WebSocket support for live updates
5. **Multi-player**: Extend memory system to support multiple users

### Key Extension Points:

- `GameInterface` class can be adapted for web responses
- `GameMemory` can be modified to use database storage
- `DungeonMaster` API calls can become web service endpoints

## 🛠️ Development

### Adding New Features

- **NPC System**: Extend `memory.py` to track NPC relationships
- **Combat System**: Add combat mechanics in `dungeon_master.py`
- **Magic System**: Implement spells and magical items
- **Multiplayer**: Modify memory system for shared adventures

### Dependencies

- `openai>=1.3.0`: AI response generation
- `rich>=13.0.0`: Beautiful terminal UI
- `python-dotenv>=1.0.0`: Environment variable management

## 🐛 Troubleshooting

### Common Issues

1. **"OpenAI API key not found"**: Create a `.env` file with your API key
2. **Import errors**: Make sure all dependencies are installed (`pip install -r requirements.txt`)
3. **Save/load issues**: Check file permissions in the project directory

### Demo Mode

If you don't have an OpenAI API key, the game runs in demo mode with pre-scripted responses. This still provides a fun experience to test the game mechanics!

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to contribute by:

- Adding new story scenarios
- Improving the AI prompts
- Adding new game mechanics
- Creating a web interface
- Fixing bugs or improving code

## 🎉 Have Fun!

Embark on epic adventures, make legendary choices, and let the AI guide you through unforgettable stories!

_Your adventure awaits, brave explorer!_ ⚔️🏰✨
