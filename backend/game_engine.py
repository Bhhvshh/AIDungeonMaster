"""
Game Engine - Core game logic and state management
"""

import uuid
from typing import List, Tuple
from datetime import datetime, timedelta
from models import PlayerStats, GameState, GameSession
from config import settings
import logging

logger = logging.getLogger(__name__)


class GameEngine:
    """Manages game logic and state"""
    
    def __init__(self, ai_manager):
        """
        Initialize the game engine
        
        Args:
            ai_manager: AI manager instance for story generation
        """
        self.ai_manager = ai_manager
        self.sessions: dict = {}  # session_id -> GameSession
    
    def create_new_game(self, player_name: str) -> Tuple[str, GameState]:
        """
        Create a new game session
        
        Args:
            player_name: Name of the player
        
        Returns:
            Tuple of (session_id, initial_game_state)
        """
        try:
            session_id = str(uuid.uuid4())
            
            # Create player stats
            player_stats = PlayerStats(
                name=player_name,
                health=settings.STARTING_HP,
                max_health=settings.STARTING_HP,
                level=settings.STARTING_LEVEL,
                gold=settings.STARTING_GOLD,
                inventory=settings.STARTING_INVENTORY.copy()
            )
            
            # Create game state with initial story
            game_state = GameState(
                story=settings.INITIAL_STORY,
                choices=[
                    "Enter the dungeon cautiously",
                    "Examine the cell for hidden items",
                    "Listen carefully to the footsteps"
                ],
                player_stats=player_stats,
                turn_number=0
            )
            
            # Create session
            session = GameSession(
                session_id=session_id,
                player_name=player_name,
                created_at=datetime.now(),
                last_activity=datetime.now(),
                history=[]
            )
            
            # Store session
            self.sessions[session_id] = {
                "session": session,
                "state": game_state,
                "history": []
            }
            
            logger.info(f"Created new game session {session_id} for player {player_name}")
            return session_id, game_state
            
        except Exception as e:
            logger.error(f"Error creating new game: {e}")
            raise
    
    def process_choice(
        self,
        session_id: str,
        choice_index: int
    ) -> GameState:
        """
        Process a player's choice and generate next state
        
        Args:
            session_id: Game session ID
            choice_index: Index of chosen option (0-2)
        
        Returns:
            Updated GameState
        
        Raises:
            ValueError: If session not found or invalid choice
        """
        if session_id not in self.sessions:
            raise ValueError(f"Session not found: {session_id}")
        
        if not (0 <= choice_index <= 2):
            raise ValueError(f"Invalid choice index: {choice_index}")
        
        try:
            session_data = self.sessions[session_id]
            session = session_data["session"]
            current_state = session_data["state"]
            
            # Verify session hasn't timed out
            if not self._is_session_active(session):
                raise ValueError(f"Session expired: {session_id}")
            
            # Get the chosen action
            chosen_action = current_state.choices[choice_index]
            
            # Add to history
            session_data["history"].append({
                "turn": current_state.turn_number,
                "action": chosen_action,
                "story": current_state.story,
                "timestamp": datetime.now().isoformat()
            })
            
            # Build context from history
            context = self._build_context(session_data["history"], current_state.player_stats)
            
            # Generate AI response
            story, choices = self.ai_manager.generate_story_response(
                player_action=chosen_action,
                game_context=context,
                player_name=current_state.player_stats.name,
                health=current_state.player_stats.health,
                level=current_state.player_stats.level,
                gold=current_state.player_stats.gold,
                inventory=current_state.player_stats.inventory
            )
            
            # Update player stats (simple logic - can be expanded)
            updated_stats = self._update_stats(current_state.player_stats, chosen_action)
            
            # Create new game state
            new_state = GameState(
                story=story,
                choices=choices,
                player_stats=updated_stats,
                turn_number=current_state.turn_number + 1
            )
            
            # Store updated state
            session_data["state"] = new_state
            session.last_activity = datetime.now()
            session.turn_count += 1
            
            logger.info(f"Processed choice for session {session_id}, turn {new_state.turn_number}")
            return new_state
            
        except Exception as e:
            logger.error(f"Error processing choice: {e}")
            raise
    
    def get_game_state(self, session_id: str) -> GameState:
        """
        Get current game state for a session
        
        Args:
            session_id: Game session ID
        
        Returns:
            Current GameState
        
        Raises:
            ValueError: If session not found
        """
        if session_id not in self.sessions:
            raise ValueError(f"Session not found: {session_id}")
        
        return self.sessions[session_id]["state"]
    
    def get_session_info(self, session_id: str) -> dict:
        """
        Get session information
        
        Args:
            session_id: Game session ID
        
        Returns:
            Session information dictionary
        """
        if session_id not in self.sessions:
            raise ValueError(f"Session not found: {session_id}")
        
        session_data = self.sessions[session_id]
        session = session_data["session"]
        
        return {
            "session_id": session.session_id,
            "player_name": session.player_name,
            "created_at": session.created_at.isoformat(),
            "last_activity": session.last_activity.isoformat(),
            "turn_count": session.turn_count,
            "history_length": len(session_data["history"])
        }
    
    def save_game(self, session_id: str, save_name: str = "autosave") -> dict:
        """
        Save a game session
        
        Args:
            session_id: Game session ID
            save_name: Name for the save
        
        Returns:
            Save information
        """
        if session_id not in self.sessions:
            raise ValueError(f"Session not found: {session_id}")
        
        session_data = self.sessions[session_id]
        session = session_data["session"]
        state = session_data["state"]
        
        save_info = {
            "save_name": save_name,
            "session_id": session_id,
            "player_name": session.player_name,
            "turn_count": session.turn_count,
            "player_stats": state.player_stats.model_dump(),
            "saved_at": datetime.now().isoformat(),
            "history": session_data["history"]
        }
        
        logger.info(f"Game saved for session {session_id}: {save_name}")
        return save_info
    
    def cleanup_expired_sessions(self) -> int:
        """
        Remove expired sessions
        
        Returns:
            Number of sessions cleaned up
        """
        now = datetime.now()
        timeout = timedelta(minutes=settings.SESSION_TIMEOUT_MINUTES)
        expired_sessions = []
        
        for session_id, session_data in self.sessions.items():
            if now - session_data["session"].last_activity > timeout:
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            del self.sessions[session_id]
            logger.info(f"Cleaned up expired session: {session_id}")
        
        return len(expired_sessions)
    
    def _is_session_active(self, session: GameSession) -> bool:
        """Check if a session is still active (not expired)"""
        now = datetime.now()
        timeout = timedelta(minutes=settings.SESSION_TIMEOUT_MINUTES)
        return (now - session.last_activity) <= timeout
    
    def _build_context(self, history: List[dict], player_stats: PlayerStats) -> str:
        """
        Build context string from game history
        
        Args:
            history: List of historical game events
            player_stats: Current player stats
        
        Returns:
            Context string for AI prompt
        """
        context_lines = [
            f"Player: {player_stats.name}",
            f"Level: {player_stats.level}, Health: {player_stats.health}/{player_stats.max_health}",
            f"Gold: {player_stats.gold}",
            "Recent story: "
        ]
        
        # Include last few turns
        for event in history[-5:]:
            context_lines.append(f"- Turn {event['turn']}: {event['action']}")
        
        return "\n".join(context_lines)
    
    def _update_stats(self, stats: PlayerStats, action: str) -> PlayerStats:
        """
        Update player stats based on action
        
        Args:
            stats: Current player stats
            action: Player's action
        
        Returns:
            Updated player stats
        """
        # Simple stat updates - can be expanded with more complex logic
        updated_stats = stats.model_copy()
        
        # Add some variation based on action keywords
        if "rest" in action.lower():
            updated_stats.health = min(stats.max_health, stats.health + 10)
        elif "fight" in action.lower() or "attack" in action.lower():
            updated_stats.health = max(0, stats.health - 5)
        elif "treasure" in action.lower() or "gold" in action.lower():
            updated_stats.gold += 10
        
        return updated_stats
