import  { useState, useEffect } from 'react';
import Canvas from './components/Canvas';
import ControlPanel from './components/ControlPanel';
import ResultPanel from './components/ResultPanel';
import { separatorAPI } from './services/api';
import type {
  Point,
  AlgorithmType,
  ComputeResponse,
  HealthResponse,
} from './types';
import './App.css';

function App() {
  const [redPoints, setRedPoints] = useState<Point[]>([]);
  const [bluePoints, setBluePoints] = useState<Point[]>([]);
  const [algorithm, setAlgorithm] = useState<AlgorithmType>('rectangles');
  const [result, setResult] = useState<ComputeResponse | null>(null);
  const [isComputing, setIsComputing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [apiHealth, setApiHealth] = useState<HealthResponse | null>(null);

  // Check API health on mount
  useEffect(() => {
    checkAPIHealth();
  }, []);

  const checkAPIHealth = async (): Promise<void> => {
    try {
      const health = await separatorAPI.getHealth();
      setApiHealth(health);
      console.log('API Health:', health);
    } catch (err) {
      console.error('API Health Check Failed:', err);
      setApiHealth({
        status: 'unhealthy',
        message: (err as Error).message,
        version: 'unknown',
        database_connected: false,
      });
    }
  };

  const handleCanvasClick = (
    x: number,
    y: number,
    isShiftPressed: boolean
  ): void => {
    const newPoint: Point = { x, y };

    if (isShiftPressed) {
      setBluePoints([...bluePoints, newPoint]);
    } else {
      setRedPoints([...redPoints, newPoint]);
    }

    setResult(null);
  };

  const handleClear = (): void => {
    setRedPoints([]);
    setBluePoints([]);
    setResult(null);
    setError(null);
  };

  const handleGenerateRandom = (): void => {
    const CANVAS_WIDTH = 800;
    const CANVAS_HEIGHT = 600;
    const PADDING = 50;

    const newRedPoints: Point[] = [];
    const newBluePoints: Point[] = [];

    const redCount = Math.floor(Math.random() * 6) + 10;
    for (let i = 0; i < redCount; i++) {
      newRedPoints.push({
        x: PADDING + Math.random() * (CANVAS_WIDTH - 2 * PADDING),
        y: PADDING + Math.random() * (CANVAS_HEIGHT - 2 * PADDING),
      });
    }

    const blueCount = Math.floor(Math.random() * 11) + 15;
    for (let i = 0; i < blueCount; i++) {
      newBluePoints.push({
        x: PADDING + Math.random() * (CANVAS_WIDTH - 2 * PADDING),
        y: PADDING + Math.random() * (CANVAS_HEIGHT - 2 * PADDING),
      });
    }

    setRedPoints(newRedPoints);
    setBluePoints(newBluePoints);
    setResult(null);
    setError(null);
  };

  const handleCompute = async (): Promise<void> => {
    if (redPoints.length === 0) {
      setError('Please add at least one red point');
      return;
    }

    setIsComputing(true);
    setError(null);

    try {
      const response = await separatorAPI.computeSeparators({
        red_points: redPoints,
        blue_points: bluePoints,
        algorithm,
        save_to_db: false,
      });

      setResult(response);
      console.log('Computation Result:', response);
    } catch (err) {
      setError((err as Error).message);
      console.error('Computation Error:', err);
    } finally {
      setIsComputing(false);
    }
  };

  return (
    <div className="app">

      {/* Header */}
      <header className="app-header">
        <div className="header-content">
          <h1>🔷 Asymmetric Separator Visualizer</h1>
          <p>Compute optimal separators for bichromatic point sets</p>
        </div>
        {apiHealth && (
          <div className={`api-status ${apiHealth.status}`}>
            <span className="status-dot"></span>
            {apiHealth.status === 'healthy' ? 'API Connected' : 'API Disconnected'}
          </div>
        )}
      </header>

      {/* Main Content */}
      <div className="app-content">
        {/* Left Sidebar */}
        <aside className="sidebar-left">
          <ControlPanel
            algorithm={algorithm}
            setAlgorithm={setAlgorithm}
            onCompute={handleCompute}
            onClear={handleClear}
            onGenerateRandom={handleGenerateRandom}
            isComputing={isComputing}
            redCount={redPoints.length}
            blueCount={bluePoints.length}
          />
        </aside>

        {/* Center - Canvas */}
        <main className="main-content">
          {error && (
            <div className="error-banner">
              <span className="error-icon">⚠️</span>
              {error}
              <button className="error-close" onClick={() => setError(null)}>
                ×
              </button>
            </div>
          )}

          <div className="canvas-container">
            <Canvas
              redPoints={redPoints}
              bluePoints={bluePoints}
              shapes={result?.shapes || []}
              onCanvasClick={handleCanvasClick}
            />
          </div>
        </main>

        {/* Right Sidebar - Results */}
        {result && (
          <aside className="sidebar-right">
            <ResultPanel result={result} isVisible={!!result} />
          </aside>
        )}
      </div>

      {/* Footer */}
      <footer className="app-footer">
        <p>
          Made using FastAPI + React + TypeScript |{" "}
          <a
            href="http://localhost:8000/docs"
            target="_blank"
            rel="noopener noreferrer"
          >
            API Docs
          </a>
        </p>
      </footer>
    </div>
  );
}

export default App;
