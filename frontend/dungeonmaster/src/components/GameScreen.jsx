import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import axios from "axios";
import StoryPanel from "./StoryPanel";
import ChoicesPanel from "./ChoicesPanel";
import PlayerStats from "./PlayerStats";
import HistoryPanel from "./HistoryPanel";
import LoadingScreen from "./LoadingScreen";
import "./GameScreen.css";

const API_BASE = "http://localhost:5000/api";

export default function GameScreen({ onBack }) {
  const [gameState, setGameState] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [history, setHistory] = useState([]);
  const [sessionId, setSessionId] = useState(null);

  // Initialize game
  useEffect(() => {
    startNewGame();
  }, []);

  const startNewGame = async () => {
    try {
      setIsLoading(true);
      setError(null);

      const response = await axios.post(`${API_BASE}/start-game`, {
        player_name: "Adventurer",
      });

      if (response.data.success) {
        setGameState({
          story: response.data.story,
          choices: response.data.choices,
          stats: response.data.player_stats,
        });
        setSessionId(response.data.session_id);
        setHistory([]);
      } else {
        throw new Error(response.data.message || "Failed to start game");
      }
    } catch (err) {
      console.error("Failed to start game:", err);
      setError(
        err.response?.data?.message ||
          "Failed to connect to game server. Please check if the backend is running on port 5000."
      );
    } finally {
      setIsLoading(false);
    }
  };

  const makeChoice = async (choiceIndex) => {
    if (!sessionId) {
      setError("No active game session");
      return;
    }

    try {
      setIsLoading(true);

      // Add current story to history
      if (gameState) {
        setHistory((prev) => [
          ...prev,
          {
            story: gameState.story,
            choice: gameState.choices[choiceIndex],
            timestamp: new Date(),
          },
        ]);
      }

      const response = await axios.post(`${API_BASE}/make-choice`, {
        session_id: sessionId,
        choice_index: choiceIndex,
      });

      if (response.data.success) {
        setGameState({
          story: response.data.story,
          choices: response.data.choices,
          stats: response.data.player_stats,
        });
        setError(null);
      } else {
        throw new Error(response.data.message || "Failed to process choice");
      }
    } catch (err) {
      console.error("Failed to make choice:", err);
      setError(
        err.response?.data?.message ||
          "Failed to process your choice. Please try again."
      );
    } finally {
      setIsLoading(false);
    }
  };

  // Save game function
  const saveGame = async () => {
    if (!sessionId) return;

    try {
      const response = await axios.post(`${API_BASE}/save-game`, {
        session_id: sessionId,
        save_name: "web_save",
      });

      if (response.data.success) {
        setError("Game saved successfully!");
        setTimeout(() => setError(null), 3000);
      }
    } catch (err) {
      console.error("Failed to save game:", err);
      setError("Failed to save game");
    }
  };

  if (isLoading && !gameState) {
    return <LoadingScreen message="Initializing your adventure..." />;
  }

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
          <button onClick={saveGame} className="save-btn">
            💾 Save Game
          </button>
          <button onClick={startNewGame} className="new-game-btn">
            New Adventure
          </button>
        </div>
      </div>

      <div className="game-layout">
        <div className="main-panel">
          <StoryPanel
            story={gameState?.story || "Your adventure awaits..."}
            isLoading={isLoading}
          />

          {gameState?.choices && (
            <ChoicesPanel
              choices={gameState.choices}
              onChoice={makeChoice}
              disabled={isLoading}
            />
          )}

          {error && <div className="error-message">{error}</div>}
        </div>

        <div className="sidebar">
          <PlayerStats stats={gameState?.stats || {}} />
          <HistoryPanel history={history} />
        </div>
      </div>
    </motion.div>
  );
}
