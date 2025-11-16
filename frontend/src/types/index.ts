// Point types
export interface Point {
  x: number;
  y: number;
}

// Shape types
export interface Shape {
  x: number;
  y: number;
  width: number;
  height: number;
}

// Algorithm types
export type AlgorithmType = 'rectangles' | 'squares';

// API Request types
export interface ComputeRequest {
  red_points: Point[];
  blue_points: Point[];
  algorithm: AlgorithmType;
  save_to_db: boolean;
}

// API Response types
export interface ComputeResponse {
  computation_id: number | null;
  shapes: Shape[];
  blue_covered: number;
  red_covered: number;
  total_red: number;
  total_blue: number;
  execution_time_ms: number;
  algorithm: string;
  created_at: string | null;
}

export interface HealthResponse {
  status: string;
  message: string;
  version: string;
  database_connected: boolean;
  timestamp?: string;
}

export interface AlgorithmInfo {
  name: string;
  time_complexity: string;
  space_complexity: string;
  description: string;
  use_case?: string;
}

export interface AlgorithmsResponse {
  [key: string]: AlgorithmInfo;
}

export interface VersionResponse {
  name: string;
  version: string;
  mode: string;
  api_prefix: string;
}

// Error types
export interface APIError {
  detail: string;
  error_code?: string;
  timestamp?: string;
}