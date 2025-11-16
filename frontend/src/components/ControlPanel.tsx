import React from 'react';
import type { AlgorithmType } from '../types';
import './ControlPanel.css';

interface ControlPanelProps {
  algorithm: AlgorithmType;
  setAlgorithm: (algorithm: AlgorithmType) => void;
  onCompute: () => void;
  onClear: () => void;
  onGenerateRandom: () => void;
  isComputing: boolean;
  redCount: number;
  blueCount: number;
}

const ControlPanel: React.FC<ControlPanelProps> = ({
  algorithm,
  setAlgorithm,
  onCompute,
  onClear,
  onGenerateRandom,
  isComputing,
  redCount,
  blueCount,
}) => {
  return (
    <div className="control-panel">
      <h2>Controls</h2>

      {/* Algorithm Selection */}
      <div className="control-group">
        <label htmlFor="algorithm">Algorithm</label>
        <select
          id="algorithm"
          value={algorithm}
          onChange={(e) => setAlgorithm(e.target.value as AlgorithmType)}
          disabled={isComputing}
        >
          <option value="rectangles">Two Rectangles</option>
          <option value="squares">Two Squares</option>
        </select>
      </div>

      {/* Action Buttons */}
      <div className="button-group">
        <button
          className="btn btn-primary"
          onClick={onCompute}
          disabled={isComputing || redCount === 0}
        >
          {isComputing ? '⏳ Computing...' : '▶️ Run Algorithm'}
        </button>

        <button
          className="btn btn-secondary"
          onClick={onGenerateRandom}
          disabled={isComputing}
        >
          🎲 Random Points
        </button>

        <button className="btn btn-danger" onClick={onClear} disabled={isComputing}>
          🗑️ Clear All
        </button>
      </div>

      {/* Instructions */}
      <div className="instructions">
        <h3>Instructions</h3>
        <ul>
          <li>
            <span className="red-dot"></span> Click to add red points
          </li>
          <li>
            <span className="blue-dot"></span> Shift + Click to add blue points
          </li>
          <li>Select algorithm and click "Run Algorithm"</li>
        </ul>
      </div>

      {/* Point Counter */}
      <div className="point-counter">
        <div className="counter-item">
          <span className="red-dot"></span>
          <span>Red Points: {redCount}</span>
        </div>
        <div className="counter-item">
          <span className="blue-dot"></span>
          <span>Blue Points: {blueCount}</span>
        </div>
      </div>
    </div>
  );
};

export default ControlPanel;