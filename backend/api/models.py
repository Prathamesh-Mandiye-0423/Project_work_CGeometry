from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional, List
from datetime import datetime, timezone
from enum import Enum

class PointSchema(BaseModel):
    x: float =Field(..., description="X coordinate of the point")
    y: float = Field(..., description="Y coord of the point")

    @field_validator('x','y')
    @classmethod
    def validate_coordinates(cls, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Coordinates must be numeric values.")
        if not (-1e10<=value<=1e10):
            raise ValueError("Coords out of range")
        return float(value)
    
    class Config:
        json_schema_extra = {
            "example":{
                "x":100.0,
                "y":150.0
            }
        }
class AlgoType(str, Enum):
    rectangles="rectangles"
    squares="squares"
        
class SeperatorRequest(BaseModel):
    red_points: List[PointSchema] = Field(
        ..., description="List of red points",
        min_length=1
        )
    blue_points: List[PointSchema]= Field(
        default=[], 
        description="List of blue points to minm coverage",

        )

    algorithm: AlgoType = Field(
        default=AlgoType.rectangles,
        description="Algorithm to use"
        )

    save_to_db: bool= Field(
        default= False,
        description="Whether to save the request and result to the database"
        )

    @field_validator('red_points')
    @classmethod
    def validate_red_points(cls,value):
        if len(value)<1:
            raise ValueError("At least one red point should be there")
        if len(value)>10000:
            raise ValueError("Too many red pts max(10000)")
        return value
    @field_validator('blue_points')
    @classmethod
    def validate_blue_points(cls,value):
        if len(value)>1000:
            raise ValueError("Too many blue pts max(1000)")
        return value
            
    class Config:
        json_schema_extra={
            "example": {
                "red_points":[
                        {"x": 100.0, "y": 100.0},
                        {"x": 200.0, "y": 150.0},
                        {"x": 150.0, "y": 200.0}
                    ],
                    "blue_points":[
                        {"x": 120.0, "y": 120.0},
                        {"x": 180.0, "y": 160.0}
                    ],
                    "algorithm":"rectangles",
                    "save_to_db":False
                }
            }
class ShapeSchema(BaseModel):
    """Shape (rectangle/square) schema"""
    x: float = Field(..., description="X coordinate of top-left corner")
    y: float = Field(..., description="Y coordinate of top-left corner")
    width: float = Field(..., description="Width of the shape", gt=0)
    height: float = Field(..., description="Height of the shape", gt=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "x": 95.0,
                "y": 95.0,
                "width": 110.0,
                "height": 110.0
            }
        }
class SeperatorResponse(BaseModel):
    computation_id: Optional[int]=Field(
        None,
        description="Unique ID for the computation request"
    )
    shapes: List[ShapeSchema]=Field(
        ...,
        description="List of shapes (rectangles/squares) that separate the red points"

    )
    blue_covered: int= Field(
        ...,
        description="Number of blue points covered by the shapes",
        ge=0
    )
    red_covered: int= Field(
        ...,
        description="Number of red points covered by the shapes",
        ge=0
    )
    total_red: int= Field(
        ...,
        description="Total red points",
        ge=0
    )
    total_blue: int= Field(
        ...,
        description="Total blue points",
        ge=0
    )
    execution_time_ms: float= Field(
        ...,
        description="Time taken to compute the separation in seconds",
        ge=0
    )

    algorithm: str= Field(
        ...,
        description="Algorithm used for separation"
    )
    created_at: Optional[datetime]= Field(
        None,
        description="Timestamp when the computation was created"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "computation_id": None,
                "shapes": [
                    {"x": 95.0, "y": 95.0, "width": 110.0, "height": 110.0},
                    {"x": 145.0, "y": 145.0, "width": 65.0, "height": 65.0}
                ],
                "blue_covered": 2,
                "red_covered": 3,
                "total_red": 3,
                "total_blue": 2,
                "execution_time_ms": 1.23,
                "algorithm": "rectangles",
                "created_at": None
            }
        }
class HealthResponse(BaseModel):
    status: str = Field(..., description="Service status")
    message: str = Field(..., description="Status message")
    version: str = Field(..., description= "API Version")
    database_connected: bool =Field(..., description="DB connection status")
    timestamp: Optional[datetime]= Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="HEalth check timestamp"
    )
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "message": "Separator API is running",
                "version": "1.0.0",
                "database_connected": False,
                "timestamp": "2024-01-15T10:30:00"
            }
        }

class ErrorResponse(BaseModel):
    detail: str= Field(..., description="Error detail message")
    error_code: str= Field(
        default="INTERNAL_ERROR",
        description="Error Code"
    )
    timestamp: Optional[datetime]= Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Error timestamp"
    )
    class Config:
        json_schema_extra = {
            "example": {
                "detail": "An error occurred",
                "error_code": "VALIDATION_ERROR",
                "timestamp": "2024-01-15T10:30:00"
            }
        }

class AlgoInfo(BaseModel):
    name: str =Field(..., description="Algo Name")
    time_complexity: str = Field(..., description="Tiem Complexity")
    space_complexity: str= Field(..., description= "Space Complexity")
    description: str= Field(..., description="Algo Description")
    use_case: Optional[str]= Field(None, description="Recommended use case")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Two Disjoint Axis-Parallel Rectangles",
                "time_complexity": "O(m + n) with O(m log m + n log n) preprocessing",
                "space_complexity": "O(m + n)",
                "description": "Computes two disjoint rectangles",
                "use_case": "Best for most scenarios"
            }
        }

###NOTE: Implement database models sepearatlt