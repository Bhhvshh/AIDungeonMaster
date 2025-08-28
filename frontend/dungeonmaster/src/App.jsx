import { useState } from "react";
import DungeonBackground from "./components/DungeonBackground";
import WizardHero from "./components/WizardHero";
import WorkingGameScreen from "./components/WorkingGameScreen";
import "./App.css";

function App() {
  const [started, setStarted] = useState(false);

  return (
    <DungeonBackground>
      <div className="overlay">
        {!started ? (
          <div className="landing">
            <WizardHero />
            <h1 className="title medieval">AI Dungeon Master</h1>
            <p className="subtitle">
              Embark on a legendary adventure guided by a mystical wizard!
            </p>
            <button
              className="start-btn medieval"
              onClick={() => setStarted(true)}
            >
              Start Adventure
            </button>
          </div>
        ) : (
          <WorkingGameScreen onBack={() => setStarted(false)} />
        )}
      </div>
    </DungeonBackground>
  );
}

export default App;
