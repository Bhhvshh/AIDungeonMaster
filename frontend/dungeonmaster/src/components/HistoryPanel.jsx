import React from "react";
import { motion } from "framer-motion";
import { Scroll, Clock } from "lucide-react";
import "./HistoryPanel.css";

export default function HistoryPanel({ history }) {
  const formatTime = (timestamp) => {
    if (!timestamp) return "";
    return new Date(timestamp).toLocaleTimeString("en-US", {
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  return (
    <motion.div
      className="history-panel"
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.6, delay: 0.2 }}
    >
      <div className="history-header">
        <Scroll className="history-icon" size={24} />
        <h3>Adventure Log</h3>
      </div>

      <div className="history-content">
        {history.length === 0 ? (
          <div className="no-history">
            <p>Your journey begins now...</p>
            <small>Choices and events will be recorded here</small>
          </div>
        ) : (
          <div className="history-list">
            {history
              .slice(-10)
              .reverse()
              .map((entry, index) => (
                <motion.div
                  key={history.length - index}
                  className="history-entry"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3, delay: index * 0.05 }}
                >
                  <div className="entry-header">
                    <span className="entry-number">
                      #{history.length - index}
                    </span>
                    {entry.timestamp && (
                      <span className="entry-time">
                        <Clock size={12} />
                        {formatTime(entry.timestamp)}
                      </span>
                    )}
                  </div>

                  <div className="entry-content">
                    <div className="entry-story">{entry.story}</div>
                    {entry.choice && (
                      <div className="entry-choice">
                        <span className="choice-label">You chose:</span>
                        <span className="choice-text">"{entry.choice}"</span>
                      </div>
                    )}
                  </div>
                </motion.div>
              ))}

            {history.length > 10 && (
              <div className="history-overflow">
                <small>... and {history.length - 10} earlier entries</small>
              </div>
            )}
          </div>
        )}
      </div>
    </motion.div>
  );
}
