# AI Dungeon Master Backend

A clean, modern FastAPI backend for the AI Dungeon Master game. This backend replaces the old Flask implementation with a better architecture, proper error handling, and clear separation of concerns.

## Features

✅ **FastAPI Framework** - Modern, fast, and highly performant  
✅ **Pydantic Models** - Strong type validation for all requests/responses  
✅ **Clean Architecture** - Separated concerns: AI management, game logic, and API  
✅ **Google Gemini Integration** - AI-powered story generation  
✅ **Session Management** - Proper game session handling with automatic cleanup  
✅ **CORS Enabled** - Works seamlessly with your React frontend  
✅ **Comprehensive Logging** - Track all operations for debugging  
✅ **Interactive API Docs** - Auto-generated Swagger UI at `/docs`

## Project Structure

```
backend/
├── main.py                 # FastAPI application & endpoints
├── config.py              # Configuration settings
├── models.py              # Pydantic request/response models
├── ai_manager.py          # Google Gemini integration
├── game_engine.py         # Core game logic & session management
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── start.sh              # Startup script
└── README.md             # This file
```

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Copy the template and add your Gemini API key:

```bash
cp .env.example .env
```

Edit `.env` and add:
```
GEMINI_API_KEY=your_actual_api_key_here
```

### 3. Start the Server

**Option A - Using the startup script:**
```bash
chmod +x start.sh
./start.sh
```

**Option B - Direct Python:**
```bash
python main.py
```

**Option C - Using uvicorn:**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

The API will be available at: `http://localhost:5000`

## API Endpoints

### Health & Status

- `GET /api/health` - Health check
- `GET /api/status` - Backend status with session info
- `GET /` - Root endpoint with API info

### Game Management

- `POST /api/start-game` - Start a new game
  ```json
  {
    "player_name": "Adventurer"
  }
  ```

- `POST /api/make-choice` - Make a choice in the game
  ```json
  {
    "session_id": "uuid",
    "choice_index": 0
  }
  ```

- `POST /api/save-game` - Save game state
  ```json
  {
    "session_id": "uuid",
    "save_name": "autosave"
  }
  ```

- `GET /api/game/{session_id}` - Get current game state
- `GET /api/session/{session_id}` - Get session information

## Architecture Overview

### AI Manager (`ai_manager.py`)
- Handles all Gemini API interactions
- Parses AI responses to extract narrative and choices
- Provides fallback responses when AI is unavailable
- Comprehensive error handling and logging

### Game Engine (`game_engine.py`)
- Manages game sessions and state
- Processes player choices
- Updates player statistics
- Builds game context from history
- Handles session expiration

### Configuration (`config.py`)
- Settings loaded from environment variables
- Type-safe using Pydantic
- Easy to customize game mechanics

### Models (`models.py`)
- Request validation: `StartGameRequest`, `MakeChoiceRequest`, `SaveGameRequest`
- Response models: `StartGameResponse`, `MakeChoiceResponse`
- Data models: `PlayerStats`, `GameState`, `GameSession`

## Configuration Options

Edit `.env` to customize:

```bash
# API Settings
DEBUG=True
HOST=0.0.0.0
PORT=5000

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Gemini AI
GEMINI_API_KEY=your_api_key
GEMINI_MODEL=gemini-1.5-flash

# Game Settings
SESSION_TIMEOUT_MINUTES=60
MAX_MEMORY_ENTRIES=50

# Player Starting Stats
STARTING_HP=100
STARTING_GOLD=50
STARTING_LEVEL=1
```

## Interactive API Documentation

Once the server is running, visit:

- **Swagger UI**: `http://localhost:5000/docs`
- **ReDoc**: `http://localhost:5000/redoc`

These provide interactive documentation where you can test all endpoints directly.

## Development

### Running with Auto-Reload

```bash
uvicorn main:app --reload
```

### Viewing Logs

The backend logs all important events:

```
2024-04-23 10:30:45 - ai_manager - INFO - Gemini API initialized successfully
2024-04-23 10:30:46 - game_engine - INFO - Created new game session
2024-04-23 10:30:50 - game_engine - INFO - Processed choice for session
```

### Session Management

Sessions automatically expire after `SESSION_TIMEOUT_MINUTES` (default: 60 minutes) of inactivity. You can manually clean up expired sessions, or they're removed when the backend is restarted.

## Troubleshooting

### Gemini API Not Available

If you see: `"AI features will be unavailable"`, check:
- `.env` file has valid `GEMINI_API_KEY`
- API key has not expired
- Backend has been restarted after setting the key

### CORS Issues

Ensure your frontend URL is in the `CORS_ORIGINS` in `.env`:
```
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Port Already in Use

If port 5000 is already in use:
```bash
python main.py --port 8000
```

Or configure `PORT` in `.env`:
```
PORT=8000
```

## Future Enhancements

- [ ] Database persistence (MongoDB/PostgreSQL)
- [ ] User authentication and profiles
- [ ] Game saves to database
- [ ] Multiplayer support
- [ ] Advanced player statistics
- [ ] Game-specific NPC interactions
- [ ] Inventory management
- [ ] Combat system

## Notes

- All sessions are stored in memory. Restarting the backend will clear all active games.
- For production, implement database persistence and proper session storage.
- The AI responses depend on Gemini API availability; fallback responses are used when unavailable.

## License

Part of the AI Dungeon Master project.
