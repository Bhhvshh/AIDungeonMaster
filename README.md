# AI Dungeon Master

An interactive text-based RPG powered by Google Gemini AI, available as both a **CLI game** and a **full-stack web application**.

## 🎮 Features

- **AI-Powered Storytelling**: Uses Google Gemini to create dynamic, engaging narratives
- **Choice-Based Gameplay**: Always presents 3 meaningful choices at every decision point
- **Memory System**: Remembers your actions, stats, and story progression
- **Character Stats**: Track HP, gold, inventory, and level
- **Save/Load System**: Continue your adventures across sessions
- **Rich Terminal UI**: Beautiful colored text and formatted displays (CLI mode)
- **Web App**: Full-stack React frontend + FastAPI backend
- **Demo Mode**: Works even without a Gemini API key (with pre-scripted responses)

## 🏗️ Architecture

```
AIDungeonMaster/
├── main.py              # CLI game entry point
├── dungeon_master.py    # CLI AI interaction and response generation
├── memory.py            # CLI game state and history management
├── config.py            # CLI configuration and settings
├── requirements.txt     # CLI Python dependencies
├── .env.example         # Environment variables template
├── GEMINI_SETUP_GUIDE.md # Gemini API key setup guide
│
├── backend/             # FastAPI REST API backend
│   ├── main.py          # API entry point and route handlers
│   ├── ai_manager.py    # Gemini AI integration
│   ├── game_engine.py   # Core game logic and session management
│   ├── models.py        # Pydantic request/response models
│   ├── config.py        # Backend configuration (pydantic-settings)
│   ├── requirements.txt # Backend Python dependencies
│   ├── quickstart.py    # Helper script to start the backend
│   └── start.sh         # Shell script to start the backend
│
└── frontend/
    └── dungeonmaster/   # React + Vite frontend
        ├── src/         # React components and app logic
        ├── index.html   # HTML entry point
        └── vite.config.js
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Node.js 18+ (for the web frontend)
- Google Gemini API key (optional, for full AI functionality — see [GEMINI_SETUP_GUIDE.md](GEMINI_SETUP_GUIDE.md))

### Environment Setup

Copy `.env.example` to `.env` and add your Gemini API key:

```bash
cp .env.example .env
```

Then edit `.env`:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

---

### Option 1: CLI Game

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the game:**

   ```bash
   python main.py
   ```

---

### Option 2: Web App (Backend + Frontend)

#### Backend (FastAPI)

1. **Navigate to the backend directory:**

   ```bash
   cd backend
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Copy the environment file:**

   ```bash
   cp ../.env.example .env
   # Edit .env to add your GEMINI_API_KEY
   ```

4. **Start the server:**

   ```bash
   python main.py
   # or use the helper scripts:
   # python quickstart.py
   # bash start.sh
   ```

   The API will be available at `http://localhost:5000`.  
   Interactive API docs: `http://localhost:5000/docs`

#### Frontend (React + Vite)

1. **Navigate to the frontend directory:**

   ```bash
   cd frontend/dungeonmaster
   ```

2. **Install dependencies:**

   ```bash
   npm install
   ```

3. **Start the development server:**

   ```bash
   npm run dev
   ```

   The app will be available at `http://localhost:5173`.

---

## 🎯 How to Play (CLI)

1. **Start the Game**: Run `python main.py`
2. **Enter Your Name**: Choose your adventurer's name
3. **Read the Story**: Gemini AI will describe your situation
4. **Make Choices**: Type `1`, `2`, or `3` to select your action
5. **Continue the Adventure**: The AI responds and gives you new choices

### CLI Commands

| Command       | Action                        |
|---------------|-------------------------------|
| `1`, `2`, `3` | Make a story choice           |
| `stats`       | View your character stats     |
| `save`        | Save your current game        |
| `load`        | Load a previously saved game  |
| `quit`/`exit` | End the game                  |

---

## 🌐 API Endpoints

| Method | Endpoint                  | Description                      |
|--------|---------------------------|----------------------------------|
| GET    | `/api/health`             | Health check                     |
| GET    | `/api/status`             | Backend status and AI availability |
| POST   | `/api/start-game`         | Start a new game session         |
| POST   | `/api/make-choice`        | Process a player choice          |
| POST   | `/api/save-game`          | Save the current game state      |
| GET    | `/api/game/{session_id}`  | Get current game state           |
| GET    | `/api/session/{session_id}` | Get session metadata           |

---

## 🔧 Configuration

### Environment Variables (`.env`)

| Variable        | Default              | Description                                    |
|-----------------|----------------------|------------------------------------------------|
| `GEMINI_API_KEY` | *(empty)*           | Your Google Gemini API key                     |
| `GEMINI_MODEL`  | `gemini-2.0-flash`   | Gemini model to use                            |
| `DEBUG`         | `True`               | Enable debug mode (backend)                    |
| `HOST`          | `0.0.0.0`            | Backend server host                            |
| `PORT`          | `5000`               | Backend server port                            |
| `CORS_ORIGINS`  | `http://localhost:5173,...` | Allowed CORS origins (comma-separated) |

### CLI Game Settings (`config.py`)

- `GEMINI_MODEL`: AI model to use (default: `gemini-1.5-flash`)
- `MAX_MEMORY_ENTRIES`: How many story entries to keep in memory
- `STARTING_HP`: Player's starting health points
- `STARTING_INVENTORY`: Initial items in player's inventory

---

## 🎲 Game Features Explained

### AI Dungeon Master

- Creates immersive fantasy scenarios
- Responds intelligently to player actions
- Maintains story consistency across turns
- Always provides exactly 3 meaningful choices

### Memory System

- Tracks complete story history
- Remembers player stats (HP, gold, inventory, level)
- Provides rolling context window to AI for consistent storytelling

### Player Progression

- **Health Points**: Combat and hazard management
- **Gold**: Collect treasure throughout your journey
- **Inventory**: Collect and use items
- **Level**: Character power progression

---

## 🛠️ Development

### CLI Dependencies

- `google-generativeai>=0.3.0`: AI response generation
- `rich>=13.0.0`: Beautiful terminal UI
- `python-dotenv>=1.0.0`: Environment variable management

### Backend Dependencies

- `fastapi==0.104.1`: REST API framework
- `uvicorn==0.24.0`: ASGI server
- `pydantic==2.5.0` / `pydantic-settings==2.1.0`: Data validation and settings
- `google-genai`: Google Gemini SDK
- `python-dotenv==1.0.0`: Environment variable management

---

## 🐛 Troubleshooting

### Common Issues

1. **"Gemini API key not found"**: Create a `.env` file with your `GEMINI_API_KEY`. See [GEMINI_SETUP_GUIDE.md](GEMINI_SETUP_GUIDE.md) for instructions.
2. **Import errors**: Make sure all dependencies are installed (`pip install -r requirements.txt`)
3. **CORS errors in browser**: Ensure the frontend origin is listed in `CORS_ORIGINS` in your `.env`
4. **Save/load issues**: Check file permissions in the project directory

### Demo Mode

If no Gemini API key is configured, the game runs in demo mode with pre-scripted responses. This still provides a playable experience to test the game mechanics!

---

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to contribute by:

- Adding new story scenarios or AI prompts
- Improving game mechanics
- Enhancing the React frontend
- Adding multiplayer support
- Fixing bugs or improving performance

## 🎉 Have Fun!

Embark on epic adventures, make legendary choices, and let the AI guide you through unforgettable stories!

_Your adventure awaits, brave explorer!_ ⚔️🏰✨
