# 🌐 Web App Extension Guide

This guide shows how to extend the AI Dungeon Master from a CLI game to a web application.

## Architecture Overview

```
Frontend (React/Vue/Vanilla JS)
    ↓ HTTP/WebSocket
Backend API (Flask/FastAPI)
    ↓
Game Logic (existing Python modules)
    ↓
Database (PostgreSQL/MongoDB)
```

## Step 1: Create Flask API Backend

```python
# web_api.py
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import uuid
from memory import GameMemory
from dungeon_master import DungeonMaster

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Store active game sessions
game_sessions = {}

@app.route('/api/start-game', methods=['POST'])
def start_game():
    """Start a new game session"""
    session_id = str(uuid.uuid4())
    data = request.json
    player_name = data.get('player_name', 'Adventurer')

    # Create new game instance
    memory = GameMemory()
    memory.update_player_stats(name=player_name)
    dm = DungeonMaster(memory)

    game_sessions[session_id] = {
        'memory': memory,
        'dm': dm
    }

    # Get initial scenario
    story, choices = dm.start_new_adventure()

    return jsonify({
        'session_id': session_id,
        'story': story,
        'choices': choices,
        'player_stats': memory.player_stats
    })

@app.route('/api/make-choice', methods=['POST'])
def make_choice():
    """Process player choice"""
    data = request.json
    session_id = data.get('session_id')
    choice_index = data.get('choice_index')

    if session_id not in game_sessions:
        return jsonify({'error': 'Invalid session'}), 400

    session_data = game_sessions[session_id]
    memory = session_data['memory']
    dm = session_data['dm']

    # Get the current choices (stored in memory)
    if not memory.story_history:
        return jsonify({'error': 'No game in progress'}), 400

    last_entry = memory.story_history[-1]
    current_choices = last_entry['choices']

    if choice_index < 0 or choice_index >= len(current_choices):
        return jsonify({'error': 'Invalid choice'}), 400

    # Process the choice
    player_action = dm.process_player_choice(choice_index + 1, current_choices)
    story, new_choices = dm.generate_response(player_action)

    # Update memory
    memory.add_story_entry(player_action, story, new_choices)

    return jsonify({
        'story': story,
        'choices': new_choices,
        'player_stats': memory.player_stats
    })

@app.route('/api/save-game', methods=['POST'])
def save_game():
    """Save game state"""
    data = request.json
    session_id = data.get('session_id')
    save_name = data.get('save_name', 'web_save')

    if session_id not in game_sessions:
        return jsonify({'error': 'Invalid session'}), 400

    memory = game_sessions[session_id]['memory']
    memory.save_game(f"{save_name}.json")

    return jsonify({'message': 'Game saved successfully'})

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
```

## Step 2: Frontend HTML/JavaScript

```html
<!-- index.html -->
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>AI Dungeon Master</title>
    <style>
      body {
        font-family: "Segoe UI", sans-serif;
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
      }
      .story-panel {
        background: #f0f8ff;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
      }
      .choices {
        display: flex;
        flex-direction: column;
        gap: 10px;
        margin: 20px 0;
      }
      .choice-btn {
        padding: 15px;
        background: #4caf50;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
      }
      .choice-btn:hover {
        background: #45a049;
      }
      .stats-panel {
        background: #e8f5e8;
        padding: 15px;
        border-radius: 8px;
      }
      .loading {
        color: #666;
        font-style: italic;
      }
    </style>
  </head>
  <body>
    <h1>🏰 AI Dungeon Master 🎲</h1>

    <div id="game-setup" class="story-panel">
      <h3>Welcome, Adventurer!</h3>
      <input
        type="text"
        id="player-name"
        placeholder="Enter your name"
        value="Adventurer"
      />
      <button onclick="startGame()">Start Adventure</button>
    </div>

    <div id="game-area" style="display: none;">
      <div id="story" class="story-panel"></div>
      <div id="choices" class="choices"></div>
      <div id="stats" class="stats-panel"></div>
      <button onclick="saveGame()">Save Game</button>
    </div>

    <script>
      let currentSession = null;

      async function startGame() {
        const playerName = document.getElementById("player-name").value;

        const response = await fetch("/api/start-game", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ player_name: playerName }),
        });

        const data = await response.json();
        currentSession = data.session_id;

        document.getElementById("game-setup").style.display = "none";
        document.getElementById("game-area").style.display = "block";

        displayStory(data.story, data.choices);
        displayStats(data.player_stats);
      }

      async function makeChoice(choiceIndex) {
        document.getElementById("choices").innerHTML =
          '<div class="loading">The Dungeon Master considers your choice...</div>';

        const response = await fetch("/api/make-choice", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            session_id: currentSession,
            choice_index: choiceIndex,
          }),
        });

        const data = await response.json();
        displayStory(data.story, data.choices);
        displayStats(data.player_stats);
      }

      function displayStory(story, choices) {
        document.getElementById("story").innerHTML = `<p>${story}</p>`;

        const choicesHtml = choices
          .map(
            (choice, index) =>
              `<button class="choice-btn" onclick="makeChoice(${index})">${
                index + 1
              }. ${choice}</button>`
          )
          .join("");

        document.getElementById("choices").innerHTML = choicesHtml;
      }

      function displayStats(stats) {
        document.getElementById("stats").innerHTML = `
                <h4>📊 ${stats.name}</h4>
                <p>HP: ${stats.hp}/${stats.max_hp} | Level: ${
          stats.level
        } | XP: ${stats.experience}</p>
                <p>Location: ${stats.location}</p>
                <p>Inventory: ${stats.inventory.join(", ")}</p>
            `;
      }

      async function saveGame() {
        await fetch("/api/save-game", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            session_id: currentSession,
            save_name: "web_game",
          }),
        });
        alert("Game saved successfully!");
      }
    </script>
  </body>
</html>
```

## Step 3: Database Integration

```python
# database.py
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class GameSession(Base):
    __tablename__ = 'game_sessions'

    id = Column(String, primary_key=True)
    player_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow)
    player_stats = Column(JSON)
    story_history = Column(JSON)

class SavedGame(Base):
    __tablename__ = 'saved_games'

    id = Column(Integer, primary_key=True)
    session_id = Column(String, nullable=False)
    save_name = Column(String, nullable=False)
    save_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

# Database setup
engine = create_engine('sqlite:///dungeon_master.db')  # Use PostgreSQL in production
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)
```

## Step 4: Enhanced Features

### Real-time Updates with WebSockets

```python
@socketio.on('join_game')
def handle_join_game(data):
    session_id = data['session_id']
    join_room(session_id)
    emit('joined_game', {'message': 'Connected to game session'})

@socketio.on('make_choice')
def handle_choice(data):
    # Process choice and emit to all players in room
    # (useful for multiplayer extensions)
    emit('story_update', response_data, room=data['session_id'])
```

### User Authentication

```python
from flask_login import LoginManager, UserMixin, login_required

class User(UserMixin):
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username

@app.route('/api/login', methods=['POST'])
def login():
    # Implement user authentication
    pass
```

### Advanced AI Features

```python
# Enhanced prompts for web version
WEB_SYSTEM_PROMPT = """
You are a web-based AI Dungeon Master. Consider:
1. Shorter, more engaging responses (1-2 paragraphs max)
2. Rich descriptions suitable for web display
3. Choices that create meaningful decision points
4. Maintain consistency across sessions
"""
```

## Step 5: Deployment

### Using Docker

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "web_api.py"]
```

### Docker Compose

```yaml
# docker-compose.yml
version: "3.8"
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/dungeon_master
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: dungeon_master
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## Benefits of Web Version

1. **Accessibility**: Play from any device with a browser
2. **Multiplayer**: Multiple players can join the same adventure
3. **Rich UI**: Images, animations, and better formatting
4. **Cloud Saves**: Games saved to database, accessible anywhere
5. **Analytics**: Track player choices and improve AI responses
6. **Monetization**: Premium features, custom scenarios

## Next Steps

1. Implement the Flask API
2. Create the HTML frontend
3. Add database persistence
4. Deploy to cloud platform (Heroku, AWS, etc.)
5. Add user accounts and authentication
6. Implement real-time multiplayer features

The modular design of the CLI version makes this transition straightforward!
