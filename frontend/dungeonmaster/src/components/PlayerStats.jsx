import React from "react";
import { motion } from "framer-motion";
import { User, Heart, Coins, Shield, Zap } from "lucide-react";
import "./PlayerStats.css";

export default function PlayerStats({ stats }) {
  const getStatIcon = (statKey) => {
    switch (statKey.toLowerCase()) {
      case "hp":
      case "health":
        return <Heart size={16} />;
      case "gold":
      case "coins":
        return <Coins size={16} />;
      case "defense":
      case "armor":
        return <Shield size={16} />;
      case "strength":
      case "attack":
        return <Zap size={16} />;
      default:
        return <User size={16} />;
    }
  };

  const formatStatKey = (key) => {
    return key.charAt(0).toUpperCase() + key.slice(1).replace(/_/g, " ");
  };

  const getStatColor = (key, value) => {
    switch (key.toLowerCase()) {
      case "hp":
      case "health":
        if (typeof value === "number") {
          if (value > 75) return "#4caf50";
          if (value > 25) return "#ff9800";
          return "#f44336";
        }
        return "#4caf50";
      case "gold":
      case "coins":
        return "#ffd700";
      default:
        return "#e0c080";
    }
  };

  return (
    <motion.div
      className="player-stats"
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.6 }}
    >
      <div className="stats-header">
        <User className="stats-icon" size={24} />
        <h3>Player Stats</h3>
      </div>

      <div className="stats-content">
        {Object.keys(stats).length === 0 ? (
          <div className="no-stats">
            <p>Stats will appear once your adventure begins...</p>
          </div>
        ) : (
          <div className="stats-grid">
            {Object.entries(stats).map(([key, value], index) => (
              <motion.div
                key={key}
                className="stat-item"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: index * 0.1 }}
              >
                <div className="stat-icon-wrapper">{getStatIcon(key)}</div>
                <div className="stat-info">
                  <span className="stat-label">{formatStatKey(key)}</span>
                  <span
                    className="stat-value"
                    style={{ color: getStatColor(key, value) }}
                  >
                    {Array.isArray(value) ? value.join(", ") : value}
                  </span>
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </motion.div>
  );
}
