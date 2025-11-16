import React, { useRef, useEffect } from 'react';
import type { Point, Shape } from '../types';

interface CanvasProps {
  redPoints: Point[];
  bluePoints: Point[];
  shapes: Shape[];
  onCanvasClick: (x: number, y: number, isShiftPressed: boolean) => void;
  width?: number;
  height?: number;
}

const Canvas: React.FC<CanvasProps> = ({
  redPoints,
  bluePoints,
  shapes,
  onCanvasClick,
  width = 800,
  height = 600,
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    drawCanvas();
  }, [redPoints, bluePoints, shapes]);

  const drawCanvas = (): void => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    ctx.clearRect(0, 0, width, height);

    // Draw grid
    ctx.strokeStyle = '#e0e0e0';
    ctx.lineWidth = 0.5;
    for (let i = 0; i <= width; i += 50) {
      ctx.beginPath();
      ctx.moveTo(i, 0);
      ctx.lineTo(i, height);
      ctx.stroke();
    }
    for (let i = 0; i <= height; i += 50) {
      ctx.beginPath();
      ctx.moveTo(0, i);
      ctx.lineTo(width, i);
      ctx.stroke();
    }

    // Draw shapes (rectangles/squares)
    if (shapes && shapes.length > 0) {
      ctx.fillStyle = 'rgba(139, 92, 246, 0.15)';
      ctx.strokeStyle = '#8b5cf6';
      ctx.lineWidth = 2;

      shapes.forEach((shape) => {
        ctx.fillRect(shape.x, shape.y, shape.width, shape.height);
        ctx.strokeRect(shape.x, shape.y, shape.width, shape.height);
      });
    }

    // Draw blue points
    bluePoints.forEach((point) => {
      ctx.fillStyle = '#3b82f6';
      ctx.beginPath();
      ctx.arc(point.x, point.y, 6, 0, 2 * Math.PI);
      ctx.fill();

      // Add white border
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 2;
      ctx.stroke();
    });

    // Draw red points
    redPoints.forEach((point) => {
      ctx.fillStyle = '#ef4444';
      ctx.beginPath();
      ctx.arc(point.x, point.y, 6, 0, 2 * Math.PI);
      ctx.fill();

      // Add white border
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 2;
      ctx.stroke();
    });
  };

  const handleClick = (e: React.MouseEvent<HTMLCanvasElement>): void => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    onCanvasClick(x, y, e.shiftKey);
  };

  return (
    <canvas
      ref={canvasRef}
      width={width}
      height={height}
      onClick={handleClick}
      style={{
        border: '2px solid #ccc',
        borderRadius: '8px',
        cursor: 'crosshair',
        backgroundColor: '#ffffff',
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
      }}
    />
  );
};

export default Canvas;