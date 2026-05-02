"""
Pydantic models for request/response validation
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# ============================================================================
# Player & Game State Models
# ============================================================================

class PlayerStats(BaseModel):
    """Player statistics"""
    name: str = Field(..., min_length=1, max_length=50)
    health: int = Field(default=100, ge=0, le=200)
    max_health: int = Field(default=100, ge=1, le=200)
    level: int = Field(default=1, ge=1, le=100)
    gold: int = Field(default=0, ge=0)
    experience: int = Field(default=0, ge=0)
    inventory: List[str] = Field(default_factory=list)


class GameState(BaseModel):
    """Current game state"""
    story: str = Field(..., min_length=10)
    choices: List[str] = Field(..., min_items=3, max_items=3)
    player_stats: PlayerStats
    turn_number: int = Field(default=0, ge=0)
    timestamp: datetime = Field(default_factory=datetime.now)


class GameSession(BaseModel):
    """Game session metadata"""
    session_id: str
    player_name: str
    created_at: datetime
    last_activity: datetime
    turn_count: int = 0
    history: List[dict] = Field(default_factory=list)


# ============================================================================
# Request Models
# ============================================================================

class StartGameRequest(BaseModel):
    """Request to start a new game"""
    player_name: str = Field(default="Adventurer", min_length=1, max_length=50)


class MakeChoiceRequest(BaseModel):
    """Request to make a choice in the game"""
    session_id: str = Field(..., min_length=1)
    choice_index: int = Field(..., ge=0, le=2)


class SaveGameRequest(BaseModel):
    """Request to save the current game"""
    session_id: str = Field(..., min_length=1)
    save_name: str = Field(default="autosave", min_length=1, max_length=100)


# ============================================================================
# Response Models
# ============================================================================

class SuccessResponse(BaseModel):
    """Generic success response"""
    success: bool = True
    message: str = ""
    data: Optional[dict] = None


class StartGameResponse(BaseModel):
    """Response when game is started"""
    success: bool = True
    session_id: str
    story: str
    choices: List[str]
    player_stats: PlayerStats
    message: str = "Game started successfully"


class MakeChoiceResponse(BaseModel):
    """Response after making a choice"""
    success: bool = True
    story: str
    choices: List[str]
    player_stats: PlayerStats
    turn_number: int
    message: str = "Choice processed successfully"


class SaveGameResponse(BaseModel):
    """Response after saving game"""
    success: bool = True
    save_name: str
    timestamp: datetime
    message: str = "Game saved successfully"


class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str = "healthy"
    message: str = "AI Dungeon Master API is running"
    timestamp: datetime = Field(default_factory=datetime.now)


class ErrorResponse(BaseModel):
    """Error response"""
    success: bool = False
    error: str
    message: str = "An error occurred"
    details: Optional[str] = None
