import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Toaster, toast } from "react-hot-toast";
import GameInterface from "../dungeonmaster/src/components/GameInterface";
import WelcomeScreen from "../dungeonmaster/src/components/WelcomeScreen";
import LoadingSpinner from "../dungeonmaster/src/components/LoadingSpinner";
import { gameApi } from "./services/api";

function App() {
  const [gameState, setGameState] = useState("welcome"); // 'welcome', 'playing', 'loading'
  const [sessionId, setSessionId] = useState(null);
  const [currentStory, setCurrentStory] = useState("");
  const [currentChoices, setCurrentChoices] = useState([]);
  const [playerStats, setPlayerStats] = useState(null);
  const [storyHistory, setStoryHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const startNewGame = async (playerName) => {
    setIsLoading(true);
    setGameState("loading");

    try {
      const response = await gameApi.startGame(playerName);

      setSessionId(response.session_id);
      setCurrentStory(response.story);
      setCurrentChoices(response.choices);
      setPlayerStats(response.player_stats);
      setStoryHistory([]);
      setGameState("playing");

      toast.success(`Welcome, ${playerName}! Your adventure begins...`, {
        icon: "🎮",
        duration: 3000,
      });
    } catch (error) {
      console.error("Failed to start game:", error);
      toast.error("Failed to start game. Please try again.");
      setGameState("welcome");
    } finally {
      setIsLoading(false);
    }
  };

  const makeChoice = async (choiceIndex) => {
    if (!sessionId) return;

    setIsLoading(true);

    try {
      const response = await gameApi.makeChoice(sessionId, choiceIndex);

      // Add the player's action to history
      setStoryHistory((prev) => [
        ...prev,
        {
          type: "player",
          content: response.player_action,
          timestamp: new Date().toISOString(),
        },
      ]);

      // Update current story and choices
      setCurrentStory(response.story);
      setCurrentChoices(response.choices);
      setPlayerStats(response.player_stats);

      // Add the DM's response to history
      setStoryHistory((prev) => [
        ...prev,
        {
          type: "dm",
          content: response.story,
          choices: response.choices,
          timestamp: new Date().toISOString(),
        },
      ]);

      toast.success("The adventure continues...", {
        icon: "📖",
        duration: 2000,
      });
    } catch (error) {
      console.error("Failed to process choice:", error);
      toast.error("Failed to process your choice. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const saveGame = async () => {
    if (!sessionId) return;

    try {
      const saveName = `save_${
        new Date().toISOString().split("T")[0]
      }_${Date.now()}`;
      await gameApi.saveGame(sessionId, saveName);

      toast.success("Game saved successfully!", {
        icon: "💾",
        duration: 2000,
      });
    } catch (error) {
      console.error("Failed to save game:", error);
      toast.error("Failed to save game. Please try again.");
    }
  };

  const getPlayerStats = async () => {
    if (!sessionId) return;

    try {
      const response = await gameApi.getStats(sessionId);
      setPlayerStats(response.player_stats);
    } catch (error) {
      console.error("Failed to get stats:", error);
      toast.error("Failed to retrieve player stats.");
    }
  };

  const endGame = async () => {
    if (sessionId) {
      try {
        await gameApi.endSession(sessionId);
      } catch (error) {
        console.error("Failed to end session:", error);
      }
    }

    setSessionId(null);
    setCurrentStory("");
    setCurrentChoices([]);
    setPlayerStats(null);
    setStoryHistory([]);
    setGameState("welcome");

    toast.success("Adventure ended. Thanks for playing!", {
      icon: "👋",
      duration: 3000,
    });
  };

  // Cleanup session on page unload
  useEffect(() => {
    const handleBeforeUnload = () => {
      if (sessionId) {
        gameApi.endSession(sessionId).catch(console.error);
      }
    };

    window.addEventListener("beforeunload", handleBeforeUnload);
    return () => window.removeEventListener("beforeunload", handleBeforeUnload);
  }, [sessionId]);

  const pageVariants = {
    initial: { opacity: 0, y: 20 },
    in: { opacity: 1, y: 0 },
    out: { opacity: 0, y: -20 },
  };

  const pageTransition = {
    type: "tween",
    ease: "anticipate",
    duration: 0.5,
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-dark-900 via-dark-800 to-dark-900">
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 3000,
          style: {
            background: "#1e293b",
            color: "#ffffff",
            border: "1px solid #475569",
          },
        }}
      />

      <AnimatePresence mode="wait">
        {gameState === "welcome" && (
          <motion.div
            key="welcome"
            initial="initial"
            animate="in"
            exit="out"
            variants={pageVariants}
            transition={pageTransition}
          >
            <WelcomeScreen onStartGame={startNewGame} />
          </motion.div>
        )}

        {gameState === "loading" && (
          <motion.div
            key="loading"
            initial="initial"
            animate="in"
            exit="out"
            variants={pageVariants}
            transition={pageTransition}
            className="flex items-center justify-center min-h-screen"
          >
            <LoadingSpinner message="The Dungeon Master is preparing your adventure..." />
          </motion.div>
        )}

        {gameState === "playing" && (
          <motion.div
            key="playing"
            initial="initial"
            animate="in"
            exit="out"
            variants={pageVariants}
            transition={pageTransition}
          >
            <GameInterface
              currentStory={currentStory}
              currentChoices={currentChoices}
              playerStats={playerStats}
              storyHistory={storyHistory}
              isLoading={isLoading}
              onMakeChoice={makeChoice}
              onSaveGame={saveGame}
              onEndGame={endGame}
              onGetStats={getPlayerStats}
            />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export default App;
