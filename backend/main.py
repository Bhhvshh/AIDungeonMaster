"""
AI Dungeon Master - FastAPI Backend
Main application file with API endpoints
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import uvicorn

from config import settings
from models import (
    StartGameRequest, StartGameResponse,
    MakeChoiceRequest, MakeChoiceResponse,
    SaveGameRequest, SaveGameResponse,
    HealthCheckResponse, ErrorResponse,
    GameState
)
from ai_manager import AIManager
from game_engine import GameEngine

# ============================================================================
# Logging Configuration
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# Global State
# ============================================================================

ai_manager = None
game_engine = None


# ============================================================================
# Lifespan Events
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application startup and shutdown
    """
    # Startup
    global ai_manager, game_engine
    logger.info("Starting AI Dungeon Master Backend...")
    
    ai_manager = AIManager()
    game_engine = GameEngine(ai_manager)
    
    logger.info("Backend initialization complete")
    yield
    
    # Shutdown
    logger.info("Shutting down AI Dungeon Master Backend...")
    logger.info(f"Active sessions: {len(game_engine.sessions)}")


# ============================================================================
# FastAPI App Setup
# ============================================================================

app = FastAPI(
    title="AI Dungeon Master Backend",
    description="RESTful API for AI-powered text-based RPG",
    version="2.0.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Health & Status Endpoints
# ============================================================================

@app.get("/api/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint"""
    return HealthCheckResponse(
        status="healthy",
        message="AI Dungeon Master API is running"
    )


@app.get("/api/status")
async def status():
    """Get backend status"""
    return {
        "status": "online",
        "ai_available": ai_manager.available,
        "active_sessions": len(game_engine.sessions),
        "debug_mode": settings.DEBUG
    }


# ============================================================================
# Game Endpoints
# ============================================================================

@app.post("/api/start-game", response_model=StartGameResponse)
async def start_game(request: StartGameRequest):
    """
    Start a new game session
    
    Args:
        request: StartGameRequest with player name
    
    Returns:
        StartGameResponse with initial game state
    """
    try:
        logger.info(f"Starting new game for player: {request.player_name}")
        
        session_id, game_state = game_engine.create_new_game(request.player_name)
        
        return StartGameResponse(
            session_id=session_id,
            story=game_state.story,
            choices=game_state.choices,
            player_stats=game_state.player_stats,
            message="Game started successfully"
        )
    
    except Exception as e:
        logger.error(f"Error starting game: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.post("/api/make-choice", response_model=MakeChoiceResponse)
async def make_choice(request: MakeChoiceRequest):
    """
    Process player choice and return next game state
    
    Args:
        request: MakeChoiceRequest with session_id and choice_index
    
    Returns:
        MakeChoiceResponse with updated game state
    """
    try:
        logger.info(f"Processing choice for session: {request.session_id}, choice: {request.choice_index}")
        
        # Validate session exists
        if request.session_id not in game_engine.sessions:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        # Process the choice
        new_state = game_engine.process_choice(request.session_id, request.choice_index)
        
        return MakeChoiceResponse(
            story=new_state.story,
            choices=new_state.choices,
            player_stats=new_state.player_stats,
            turn_number=new_state.turn_number,
            message="Choice processed successfully"
        )
    
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    except Exception as e:
        logger.error(f"Error processing choice: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.post("/api/save-game", response_model=SaveGameResponse)
async def save_game(request: SaveGameRequest):
    """
    Save the current game state
    
    Args:
        request: SaveGameRequest with session_id and optional save_name
    
    Returns:
        SaveGameResponse with save information
    """
    try:
        logger.info(f"Saving game for session: {request.session_id}")
        
        if request.session_id not in game_engine.sessions:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        save_info = game_engine.save_game(request.session_id, request.save_name)
        
        return SaveGameResponse(
            save_name=save_info["save_name"],
            timestamp=save_info["saved_at"],
            message="Game saved successfully"
        )
    
    except Exception as e:
        logger.error(f"Error saving game: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.get("/api/game/{session_id}")
async def get_game_state(session_id: str):
    """
    Get current game state for a session
    
    Args:
        session_id: Game session ID
    
    Returns:
        Current game state
    """
    try:
        if session_id not in game_engine.sessions:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        state = game_engine.get_game_state(session_id)
        return state.model_dump()
    
    except Exception as e:
        logger.error(f"Error getting game state: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.get("/api/session/{session_id}")
async def get_session_info(session_id: str):
    """
    Get session information
    
    Args:
        session_id: Game session ID
    
    Returns:
        Session metadata
    """
    try:
        info = game_engine.get_session_info(session_id)
        return info
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error getting session info: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ============================================================================
# Error Handlers
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    return ErrorResponse(
        error=exc.detail,
        message="An error occurred"
    ).model_dump()


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {exc}")
    return ErrorResponse(
        error="Internal server error",
        message=str(exc) if settings.DEBUG else "An unexpected error occurred"
    ).model_dump()


# ============================================================================
# Root Endpoint
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "AI Dungeon Master Backend",
        "version": "2.0.0",
        "status": "running",
        "docs": "/docs"
    }


# ============================================================================
# Development Server
# ============================================================================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
