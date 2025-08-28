import React from "react";
import "./DungeonBackground.css";

export default function DungeonBackground({ children }) {
  return (
    <div className="dungeon-background">
      <div className="stone-texture"></div>
      <div className="torch-glow torch-1"></div>
      <div className="torch-glow torch-2"></div>
      <div className="torch-glow torch-3"></div>
      <div className="torch-glow torch-4"></div>
      <div className="background-overlay">{children}</div>
    </div>
  );
}
