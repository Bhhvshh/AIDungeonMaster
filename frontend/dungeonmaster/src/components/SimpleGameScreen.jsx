import React, { useState } from "react";
import { motion } from "framer-motion";
import "./GameScreen.css";

// Demo data for testing UI without backend
const demoData = {
  story:
    "You stand at the entrance of a dark, ancient dungeon. Shadows dance on the weathered stone walls, and a mystical energy fills the air. The Dungeon Master's eyes gleam with ancient wisdom as he presents your options.",
  choices: [
    "Step forward into the mysterious corridor",
    "Examine the ancient runes carved into the wall",
    "Call out to see if anyone else is nearby",
  ],
  stats: {
    name: "Brave Adventurer",
    health: 100,
    gold: 25,
    level: 1,
    experience: 0,
  },
};

export default function GameScreen({ onBack }) {
  const [gameState, setGameState] = useState(demoData);
  const [history, setHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const makeChoice = (choiceIndex) => {
    // Add to history
    setHistory((prev) => [
      ...prev,
      {
        story: gameState.story,
        choice: gameState.choices[choiceIndex],
        timestamp: new Date(),
      },
    ]);

    // Update with new demo content
    setGameState({
      story: `You chose: "${gameState.choices[choiceIndex]}"\n\nThe dungeon seems to respond to your decision. New paths appear before you, each more mysterious than the last.`,
      choices: [
        "Venture deeper into the shadows",
        "Search for hidden treasures",
        "Try to find a way back",
      ],
      stats: {
        ...gameState.stats,
        experience: gameState.stats.experience + 10,
      },
    });
  };

  const startNewGame = () => {
    setGameState(demoData);
    setHistory([]);
  };

  return (
    <motion.div
      className="game-screen"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.8 }}
    >
      <div className="game-header">
        <h1 className="game-title">AI Dungeon Master</h1>
        <div className="header-buttons">
          {onBack && (
            <button onClick={onBack} className="back-btn">
              ← Back to Menu
            </button>
          )}
          <button onClick={startNewGame} className="new-game-btn">
            New Adventure
          </button>
        </div>
      </div>

      <div className="game-layout">
        <div className="main-panel">
          {/* Story Panel */}
          <div className="story-panel">
            <div className="story-header">
              <h2>The Dungeon Master Speaks</h2>
            </div>
            <div className="story-content">
              <div className="story-text">{gameState.story}</div>
            </div>
          </div>

          {/* Choices Panel */}
          <div className="choices-panel">
            <div className="choices-header">
              <h3>Choose Your Path</h3>
            </div>
            <div className="choices-grid">
              {gameState.choices.map((choice, index) => (
                <button
                  key={index}
                  className="choice-btn"
                  onClick={() => makeChoice(index)}
                  disabled={isLoading}
                >
                  <span className="choice-number">{index + 1}</span>
                  <span className="choice-text">{choice}</span>
                  <span className="choice-arrow">→</span>
                </button>
              ))}
            </div>
          </div>
        </div>

        <div className="sidebar">
          {/* Player Stats */}
          <div className="player-stats">
            <div className="stats-header">
              <h3>Player Stats</h3>
            </div>
            <div className="stats-content">
              <div className="stats-grid">
                {Object.entries(gameState.stats).map(([key, value]) => (
                  <div key={key} className="stat-item">
                    <div className="stat-info">
                      <span className="stat-label">
                        {key.charAt(0).toUpperCase() + key.slice(1)}
                      </span>
                      <span className="stat-value">{value}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* History Panel */}
          <div className="history-panel">
            <div className="history-header">
              <h3>Adventure Log</h3>
            </div>
            <div className="history-content">
              {history.length === 0 ? (
                <div className="no-history">
                  <p>Your journey begins now...</p>
                </div>
              ) : (
                <div className="history-list">
                  {history
                    .slice(-5)
                    .reverse()
                    .map((entry, index) => (
                      <div key={index} className="history-entry">
                        <div className="entry-choice">
                          <span className="choice-label">You chose:</span>
                          <span className="choice-text">"{entry.choice}"</span>
                        </div>
                      </div>
                    ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
