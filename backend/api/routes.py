from fastapi import APIRouter, HTTPException, status, Request
from typing import List, Dict
import time
from datetime import datetime, timezone
import logging as logger
#NOTE:API Routes without DB connection for now
from backend.api.models import (
    AlgoInfo,
    HealthResponse,
    SeperatorRequest,
    SeperatorResponse,
    ErrorResponse,
    AlgoType
)

from backend.algorithm.seperators import(
    Point as AlgoPoint,
    RectangleSeperator,
    SquareSeperator
)

from backend.config import get_settings
router=APIRouter(prefix="/api", tags=["Seperator ALgorithms"])
settings=get_settings()

@router.post(
    "/compute-separators",
    response_model=SeperatorResponse,
    status_code=status.HTTP_200_OK,
    summary="Compute Optimal Seperators",
    responses={
        200: {
            "description": "Successfully computed separators",
            "model": SeperatorResponse
        },
        400: {
            "description": "Invalid input data",
            "model": ErrorResponse
        },
        422: {
            "description": "Validation error",
            "model": ErrorResponse
        },
        500: {
            "description": "Internal server error",
            "model": ErrorResponse
        }
    }

)

async def compute_separators(
    request: SeperatorRequest,
    http_request: Request
)-> SeperatorResponse:
    client_ip= http_request.client.host
    logger.info(
        f"Compute Requuest from {client_ip}: "
        f"{len(request.red_points)} red, {len(request.blue_points)} blue points, "
        f"algforithm: {request.algorithm.value}"
    )
    try:
        if not request.red_points:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Red points list cannot be empty"
            )

        total_points= len(request.red_points)+ len(request.blue_points)
        if (total_points>settings.MAX_POINTS):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Total points exceed maximum limit of {settings.MAX_POINTS}"
            )
        red_points=[AlgoPoint(x=pt.x, y=pt.y) for pt in request.red_points]
        blue_points=[AlgoPoint(x=pt.x, y=pt.y) for pt in request.blue_points]
        start_time=time.perf_counter()
        if request.algorithm==AlgoType.rectangles:
            seperator= RectangleSeperator(red_points, blue_points)
            result=seperator.solve()
            shapes_key="rectangles"
        else:
            seperator= SquareSeperator(red_points, blue_points)
            result=seperator.solve()
            shapes_key="squares"
        execution_time=(time.perf_counter()-start_time)*1000
        logger.info(
            f"Computation time: {execution_time:.2f} ms, "
            f"blue covered: {result.get('blue_covered',0)}/{len(request.blue_points)}"

        )
        response= SeperatorResponse(
            computation_id=None,
            shapes=result.get(shapes_key, []),
            blue_covered=result.get("blue_covered",0),
            red_covered=result.get("red_covered",0),
            total_red=len(request.red_points),
            total_blue=len(request.blue_points),
            execution_time_ms=round(execution_time, 2),
            algorithm=request.algorithm.value,
            created_at=None
        )

        return response
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Validation error : {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Internal server error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred"
        )

@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK, 
    summary="Health Check Endpoint",
    description="Check the health status of the Seperator API service",
)

async def health_check()->HealthResponse:
    return HealthResponse(
        status="healthy",
        message="Seperator API is running (Testing Mode - No Database)",
        version=settings.VERSION,
        database_connected=False,
        timestamp=datetime.now(timezone.utc)
    )

@router.get(
    "/algorithms",
    response_model=Dict[str,AlgoInfo],
    summary="Get algo info",
    description="Retrieve information about available separator algorithms",
)

async def get_algorithms()->Dict[str,AlgoInfo]:
    return {
        "rectangles": AlgoInfo(
            name="Two Disjoint Axis-Parallel Rectangles",
            time_complexity="O(m + n) with O(m log m + n log n) preprocessing",
            space_complexity="O(m + n)",
            description="Computes two disjoint rectangles that cover all red points while minimizing blue point coverage. Uses sweep line technique for optimal splitting.",
            use_case="Best for most scenarios due to linear time complexity after preprocessing"
        ),
        "squares": AlgoInfo(
            name="Two Disjoint Axis-Parallel Squares",
            time_complexity="O(nm) with O(m log m + n log n) preprocessing",
            space_complexity="O(m + n)",
            description="Computes two disjoint squares (equal width and height) that cover all red points while minimizing blue point coverage.",
            use_case="Use when equal dimensions are required; may be slower for large datasets"
        )
    }

@router.get(
    "/algorithms/{algorithm_name}",
    response_model=AlgoInfo,
    summary="Get algorithm details",
    description="Retrieve detailed information about a specific separator algorithm",
)

async def get_algorithm_info(algorithm_name: str)-> AlgoInfo:
    algorithms=await get_algorithms()
    if algorithm_name not in algorithms:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            details=f"Algorithm '{algorithm_name}' not found"
        )

    return algorithms[algorithm_name]

@router.get(
    "/version",
    summary="Get API version",
    description="Retrieve the current version of the Seperator API service",
)

async def get_version()->Dict[str,str]:
    return {
        "name":settings.PROJECT_NAME,
        "version":settings.VERSION,
        "mode":"Testing",
        "api_prefix": settings.API_V1_PREFIX

    }

#NOTE: Include Stats Summary and DB parts



#For Testing purpose
if __name__ == "__main__":
    print("Testing routes from backend/api/routes.py")
