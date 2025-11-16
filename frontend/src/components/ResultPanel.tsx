import React from 'react';
import type { ComputeResponse } from '../types';
import './ResultPanel.css';

interface ResultPanelProps {
  result: ComputeResponse | null;
  isVisible: boolean;
}

const ResultPanel: React.FC<ResultPanelProps> = ({ result, isVisible }) => {
  if (!isVisible || !result) return null;

  const efficiency =
    result.total_blue > 0
      ? ((1 - result.blue_covered / result.total_blue) * 100).toFixed(1)
      : '100.0';

  return (
    <div className="result-panel">
      <h2>Results</h2>

      <div className="result-grid">
        <div className="result-card primary">
          <div className="result-label">Red Points Covered</div>
          <div className="result-value">{result.red_covered}</div>
          <div className="result-subtitle">of {result.total_red} total</div>
        </div>

        <div className="result-card warning">
          <div className="result-label">Blue Points Covered</div>
          <div className="result-value">{result.blue_covered}</div>
          <div className="result-subtitle">of {result.total_blue} total</div>
        </div>

        <div className="result-card success">
          <div className="result-label">Efficiency</div>
          <div className="result-value">{efficiency}%</div>
          <div className="result-subtitle">Coverage optimization</div>
        </div>

        <div className="result-card info">
          <div className="result-label">Execution Time</div>
          <div className="result-value">{result.execution_time_ms.toFixed(2)}</div>
          <div className="result-subtitle">milliseconds</div>
        </div>
      </div>

      <div className="result-details">
        <div className="detail-row">
          <span className="detail-label">Algorithm:</span>
          <span className="detail-value">{result.algorithm}</span>
        </div>
        <div className="detail-row">
          <span className="detail-label">Shapes Found:</span>
          <span className="detail-value">{result.shapes.length}</span>
        </div>
      </div>

      {result.shapes.length > 0 && (
        <div className="shapes-info">
          <h3>Shape Details</h3>
          {result.shapes.map((shape, index) => (
            <div key={index} className="shape-item">
              <div className="shape-header">Shape {index + 1}</div>
              <div className="shape-details">
                <span>
                  Position: ({shape.x.toFixed(1)}, {shape.y.toFixed(1)})
                </span>
                <span>
                  Size: {shape.width.toFixed(1)} × {shape.height.toFixed(1)}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ResultPanel;