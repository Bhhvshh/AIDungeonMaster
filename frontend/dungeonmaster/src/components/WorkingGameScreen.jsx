import React, { useState, useEffect } from "react";
import axios from "axios";
import "./GameScreen.css";

const API_BASE = "http://localhost:5000/api";

// Demo fallback data
const demoData = {
  story: "You stand at the entrance of a dark, ancient dungeon. The Dungeon Master awaits your decision.",
  choices: [
    "Enter the dungeon cautiously",
    "Examine the entrance for traps", 
    "Call out to announce your presence"
  ],
  stats: {
    name: "Adventurer",
    health: 100,
    gold: 50,
    level: 1
  }
};

export default function GameScreen({ onBack }) {
  const [gameState, setGameState] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [history, setHistory] = useState([]);
  const [sessionId, setSessionId] = useState(null);
  const [demoMode, setDemoMode] = useState(false);

  // Initialize game
  useEffect(() => {
    startNewGame();
  }, []);

  const startNewGame = async () => {
    try {
      setIsLoading(true);
      setError(null);
      setDemoMode(false);

      const response = await axios.post(`${API_BASE}/start-game`, {
        player_name: "Adventurer",
      });

      if (response.data && response.data.success) {
        setGameState({
          story: response.data.story,
          choices: response.data.choices,
          stats: response.data.player_stats,
        });
        setSessionId(response.data.session_id);
        setHistory([]);
      } else {
        throw new Error("Failed to start game");
      }
    } catch (err) {
      console.warn("Backend not available, using demo mode:", err.message);
      // Fallback to demo mode
      setDemoMode(true);
      setGameState(demoData);
      setHistory([]);
      setError(null);
    } finally {
      setIsLoading(false);
    }
  };

  const makeChoice = async (choiceIndex) => {
    if (demoMode) {
      // Demo mode logic
      setHistory(prev => [...prev, {
        story: gameState.story,
        choice: gameState.choices[choiceIndex],
        timestamp: new Date()
      }]);

      setGameState({
        story: `You chose: "${gameState.choices[choiceIndex]}"\n\nThe adventure continues in demo mode...`,
        choices: [
          "Continue exploring",
          "Check your surroundings",
          "Try something different"
        ],
        stats: gameState.stats
      });
      return;
    }

    if (!sessionId) {
      setError("No active game session");
      return;
    }

    try {
      setIsLoading(true);

      // Add current story to history
      if (gameState) {
        setHistory(prev => [...prev, {
          story: gameState.story,
          choice: gameState.choices[choiceIndex],
          timestamp: new Date()
        }]);
      }

      const response = await axios.post(`${API_BASE}/make-choice`, {
        session_id: sessionId,
        choice_index: choiceIndex,
      });

      if (response.data && response.data.success) {
        setGameState({
          story: response.data.story,
          choices: response.data.choices,
          stats: response.data.player_stats,
        });
        setError(null);
      } else {
        throw new Error("Failed to process choice");
      }
    } catch (err) {
      console.error("Failed to make choice:", err);
      setError("Failed to process your choice. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading && !gameState) {
    return (
      <div style={{ 
        padding: '4rem', 
        textAlign: 'center', 
        color: '#d4af37',
        minHeight: '60vh',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center'
      }}>
        <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🔮</div>
        <h2>Initializing your adventure...</h2>
      </div>
    );
  }

  return (
    <div style={{ 
      padding: '2rem', 
      color: '#f5deb3',
      minHeight: '80vh'
    }}>
      {/* Header */}
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center', 
        marginBottom: '2rem',
        padding: '1rem 2rem',
        background: 'rgba(40, 30, 10, 0.9)',
        borderRadius: '1rem',
        border: '2px solid #d4af37'
      }}>
        <h1 style={{ color: '#d4af37', margin: 0 }}>
          AI Dungeon Master {demoMode && "(Demo Mode)"}
        </h1>
        <div style={{ display: 'flex', gap: '1rem' }}>
          {onBack && (
            <button 
              onClick={onBack}
              style={{
                background: '#654321',
                color: 'white',
                padding: '0.5rem 1rem',
                border: 'none',
                borderRadius: '0.5rem',
                cursor: 'pointer'
              }}
            >
              ← Back to Menu
            </button>
          )}
          <button 
            onClick={startNewGame}
            style={{
              background: '#8b4513',
              color: 'white',
              padding: '0.5rem 1rem',
              border: 'none',
              borderRadius: '0.5rem',
              cursor: 'pointer'
            }}
          >
            New Adventure
          </button>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '2rem' }}>
        {/* Main Panel */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          {/* Story Panel */}
          <div style={{
            background: 'rgba(40, 30, 10, 0.95)',
            borderRadius: '1rem',
            border: '2px solid #d4af37',
            padding: '2rem'
          }}>
            <h2 style={{ color: '#d4af37', marginBottom: '1rem' }}>
              The Dungeon Master Speaks
            </h2>
            <div style={{
              color: '#f5f5dc',
              fontSize: '1.1rem',
              lineHeight: '1.7',
              minHeight: '100px'
            }}>
              {isLoading ? "The Dungeon Master is thinking..." : gameState?.story}
            </div>
          </div>

          {/* Choices Panel */}
          {gameState?.choices && (
            <div style={{
              background: 'rgba(30, 20, 10, 0.95)',
              borderRadius: '1rem',
              border: '2px solid #8b4513',
              padding: '1.5rem'
            }}>
              <h3 style={{ color: '#cd853f', marginBottom: '1rem' }}>
                Choose Your Path
              </h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                {gameState.choices.map((choice, index) => (
                  <button
                    key={index}
                    onClick={() => makeChoice(index)}
                    disabled={isLoading}
                    style={{
                      background: 'linear-gradient(135deg, #8b4513 0%, #cd853f 100%)',
                      color: 'white',
                      border: 'none',
                      borderRadius: '0.75rem',
                      padding: '1rem 1.5rem',
                      cursor: isLoading ? 'not-allowed' : 'pointer',
                      fontSize: '1rem',
                      textAlign: 'left',
                      opacity: isLoading ? 0.6 : 1
                    }}
                  >
                    {index + 1}. {choice}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Error Message */}
          {error && (
            <div style={{
              background: 'rgba(211, 47, 47, 0.1)',
              border: '1px solid #d32f2f',
              borderRadius: '0.5rem',
              padding: '1rem',
              color: '#ffcdd2',
              textAlign: 'center'
            }}>
              {error}
            </div>
          )}
        </div>

        {/* Sidebar */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          {/* Player Stats */}
          <div style={{
            background: 'rgba(25, 15, 5, 0.95)',
            borderRadius: '1rem',
            border: '2px solid #654321',
            padding: '1.5rem'
          }}>
            <h3 style={{ color: '#daa520', marginBottom: '1rem' }}>Player Stats</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {gameState?.stats && Object.entries(gameState.stats).map(([key, value]) => (
                <div key={key} style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  padding: '0.5rem',
                  background: 'rgba(101, 67, 33, 0.2)',
                  borderRadius: '0.5rem'
                }}>
                  <span style={{ color: '#cd853f', textTransform: 'capitalize' }}>
                    {key}:
                  </span>
                  <span style={{ color: '#e0c080', fontWeight: 'bold' }}>
                    {value}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* History Panel */}
          <div style={{
            background: 'rgba(20, 10, 5, 0.95)',
            borderRadius: '1rem',
            border: '2px solid #5d4e37',
            padding: '1.5rem',
            maxHeight: '300px',
            overflow: 'hidden'
          }}>
            <h3 style={{ color: '#deb887', marginBottom: '1rem' }}>Adventure Log</h3>
            <div style={{ overflowY: 'auto', maxHeight: '200px' }}>
              {history.length === 0 ? (
                <p style={{ color: '#8b7355', fontStyle: 'italic' }}>
                  Your journey begins now...
                </p>
              ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                  {history.slice(-5).reverse().map((entry, index) => (
                    <div key={index} style={{
                      padding: '0.5rem',
                      background: 'rgba(93, 78, 55, 0.2)',
                      borderRadius: '0.5rem',
                      fontSize: '0.9rem'
                    }}>
                      <strong style={{ color: '#deb887' }}>Choice:</strong>{' '}
                      <span style={{ color: '#f5f5dc' }}>"{entry.choice}"</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
