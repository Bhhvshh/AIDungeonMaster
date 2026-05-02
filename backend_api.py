"""
Flask Backend API for AI Dungeon Master
Converts the game logic into RESTful API endpoints
"""

from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_session import Session
import uuid
import os
from datetime import datetime
import json

from memory import GameMemory
from dungeon_master import DungeonMaster
from config import Config

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'ai-dungeon-master-secret-key')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True

CORS(app, supports_credentials=True)
Session(app)

# Store active game sessions
game_sessions = {}

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'AI Dungeon Master API is running',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/start-game', methods=['POST'])
def start_game():
    """Start a new game session"""
    try:
        data = request.get_json()
        player_name = data.get('player_name', 'Adventurer')
        
        # Generate unique session ID
        session_id = str(uuid.uuid4())
        
        # Create new game instance
        memory = GameMemory()
        memory.update_player_stats(name=player_name)
        dm = DungeonMaster(memory)
        
        # Store session
        game_sessions[session_id] = {
            'memory': memory,
            'dm': dm,
            'created_at': datetime.now().isoformat(),
            'last_activity': datetime.now().isoformat()
        }
        
        # Get initial scenario
        story, choices = dm.start_new_adventure()

        # Add initial story entry to memory so choices can be made
        memory.add_story_entry(
            player_action="Game started",
            dm_response=story,
            choices=choices
        )

        # Store initial story in session for Flask session management
        session['session_id'] = session_id

        return jsonify({
            'success': True,
            'session_id': session_id,
            'story': story,
            'choices': choices,
            'player_stats': memory.player_stats,
            'message': 'Game started successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to start game'
        }), 500

@app.route('/api/make-choice', methods=['POST'])
def make_choice():
    """Process player choice and get AI response"""
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        choice_index = data.get('choice_index')
        
        if not session_id or session_id not in game_sessions:
            return jsonify({
                'success': False,
                'error': 'Invalid or expired session',
                'message': 'Please start a new game'
            }), 400
        
        session_data = game_sessions[session_id]
        memory = session_data['memory']
        dm = session_data['dm']
        
        # Update last activity
        session_data['last_activity'] = datetime.now().isoformat()
        
        # Get current choices from the last story entry
        if not memory.story_history:
            return jsonify({
                'success': False,
                'error': 'No game in progress',
                'message': 'Please start a new game'
            }), 400
        
        last_entry = memory.story_history[-1]
        current_choices = last_entry.get('choices', [])
        
        # Validate choice
        if not isinstance(choice_index, int) or choice_index < 0 or choice_index >= len(current_choices):
            return jsonify({
                'success': False,
                'error': 'Invalid choice index',
                'message': 'Please select a valid choice'
            }), 400
        
        # Process the choice
        player_action = dm.process_player_choice(choice_index + 1, current_choices)
        story, new_choices = dm.generate_response(player_action)
        
        # Update memory
        memory.add_story_entry(player_action, story, new_choices)
        
        return jsonify({
            'success': True,
            'story': story,
            'choices': new_choices,
            'player_stats': memory.player_stats,
            'player_action': player_action,
            'message': 'Choice processed successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to process choice'
        }), 500

@app.route('/api/get-stats', methods=['POST'])
def get_stats():
    """Get current player statistics"""
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        
        if not session_id or session_id not in game_sessions:
            return jsonify({
                'success': False,
                'error': 'Invalid session',
                'message': 'Session not found'
            }), 400
        
        memory = game_sessions[session_id]['memory']
        
        return jsonify({
            'success': True,
            'player_stats': memory.player_stats,
            'story_count': len(memory.story_history),
            'message': 'Stats retrieved successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to get stats'
        }), 500

@app.route('/api/save-game', methods=['POST'])
def save_game():
    """Save current game state"""
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        save_name = data.get('save_name', 'web_save')
        
        if not session_id or session_id not in game_sessions:
            return jsonify({
                'success': False,
                'error': 'Invalid session',
                'message': 'Session not found'
            }), 400
        
        memory = game_sessions[session_id]['memory']
        filename = f"saves/{save_name}_{session_id[:8]}.json"
        
        # Ensure saves directory exists
        os.makedirs('saves', exist_ok=True)
        
        memory.save_game(filename)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'message': 'Game saved successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to save game'
        }), 500

@app.route('/api/get-history', methods=['POST'])
def get_history():
    """Get story history for the session"""
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        limit = data.get('limit', 10)  # Default to last 10 entries
        
        if not session_id or session_id not in game_sessions:
            return jsonify({
                'success': False,
                'error': 'Invalid session',
                'message': 'Session not found'
            }), 400
        
        memory = game_sessions[session_id]['memory']
        history = memory.story_history[-limit:] if memory.story_history else []
        
        return jsonify({
            'success': True,
            'history': history,
            'total_entries': len(memory.story_history),
            'message': 'History retrieved successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to get history'
        }), 500

@app.route('/api/end-session', methods=['POST'])
def end_session():
    """End and cleanup a game session"""
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        
        if session_id and session_id in game_sessions:
            # Optional: Save game before ending
            memory = game_sessions[session_id]['memory']
            memory.save_game(f"saves/auto_save_{session_id[:8]}.json")
            
            # Remove from active sessions
            del game_sessions[session_id]
        
        return jsonify({
            'success': True,
            'message': 'Session ended successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to end session'
        }), 500

@app.route('/api/sessions', methods=['GET'])
def get_active_sessions():
    """Get count of active sessions (for monitoring)"""
    return jsonify({
        'success': True,
        'active_sessions': len(game_sessions),
        'session_ids': list(game_sessions.keys())
    })

# Cleanup old sessions (run periodically)
def cleanup_old_sessions():
    """Remove sessions inactive for more than 1 hour"""
    current_time = datetime.now()
    sessions_to_remove = []
    
    for session_id, session_data in game_sessions.items():
        last_activity = datetime.fromisoformat(session_data['last_activity'])
        if (current_time - last_activity).total_seconds() > 3600:  # 1 hour
            sessions_to_remove.append(session_id)
    
    for session_id in sessions_to_remove:
        del game_sessions[session_id]
    
    return len(sessions_to_remove)

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'message': 'The requested API endpoint does not exist'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500

if __name__ == '__main__':
    print("🚀 Starting AI Dungeon Master API Server...")
    print(f"🔗 API will be available at: http://localhost:5000")
    print(f"📚 API Documentation:")
    print(f"   POST /api/start-game - Start a new game")
    print(f"   POST /api/make-choice - Make a choice in the game")
    print(f"   POST /api/get-stats - Get player statistics")
    print(f"   POST /api/save-game - Save current game")
    print(f"   GET  /api/health - Health check")
    
    # Create saves directory if it doesn't exist
    os.makedirs('saves', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
