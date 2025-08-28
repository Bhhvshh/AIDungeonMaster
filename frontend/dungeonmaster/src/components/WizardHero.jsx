import React from "react";
import { motion } from "framer-motion";
import "./WizardHero.css";

export default function WizardHero() {
  return (
    <motion.div
      className="wizard-hero"
      initial={{ opacity: 0, y: -50 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 1, ease: "easeOut" }}
    >
      <div className="wizard-container">
        <motion.div
          className="wizard-orb"
          animate={{
            scale: [1, 1.1, 1],
            rotate: [0, 360],
          }}
          transition={{
            duration: 6,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        >
          <div className="orb-glow"></div>
          <div className="orb-inner">🧙‍♂️</div>
        </motion.div>

        <motion.div
          className="magical-particles"
          animate={{ rotate: 360 }}
          transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
        >
          <div className="particle particle-1">✨</div>
          <div className="particle particle-2">⭐</div>
          <div className="particle particle-3">✨</div>
          <div className="particle particle-4">⭐</div>
        </motion.div>
      </div>

      <motion.p
        className="wizard-quote"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.8, duration: 1 }}
      >
        "Welcome, brave adventurer. Your destiny awaits within these ancient
        halls..."
      </motion.p>
    </motion.div>
  );
}
