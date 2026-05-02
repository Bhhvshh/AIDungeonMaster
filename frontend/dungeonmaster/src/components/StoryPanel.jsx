import React from "react";
import { motion } from "framer-motion";
import { Book } from "lucide-react";
import "./StoryPanel.css";

export default function StoryPanel({ story, isLoading }) {
  return (
    <motion.div
      className="story-panel"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <div className="story-header">
        <Book className="story-icon" size={24} />
        <h2>The Dungeon Master Speaks</h2>
      </div>

      <div className="story-content">
        {isLoading ? (
          <div className="story-loading">
            <div className="loading-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
            <p>The Dungeon Master is weaving your tale...</p>
          </div>
        ) : (
          <motion.div
            className="story-text"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            {story}
          </motion.div>
        )}
      </div>
    </motion.div>
  );
}
