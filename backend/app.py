from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from backend.api.routes import router as api_router
from backend.config import get_settings
import logging as logger
import uvicorn
import time

settings=get_settings()

app=FastAPI(
    title=settings.PROJECT_NAME,
    description="API for geometric point seperation algo (Testing Mode)",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time=time.time()
    response=await call_next(request)
    process_time=time.time()-start_time
    response.headers["X-Process-Time"]= str(process_time)
    return response

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exec: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "detail":"Validation error",
            "errors": exec.errors(),
            "body": exec.body
        }
    )

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up the Separator API service...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down the Separator API service...")

app.include_router(api_router)
@app.get("/", tags=["Root"])
async def root():
    return{
        "message": f"{settings.PROJECT_NAME} - Testing Mode",
        "version": settings.VERSION,
        "mode": "No Database",
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        },
        "endpoints": {
            "compute_separators": f"{settings.API_V1_PREFIX}/compute-separators",
            "health": f"{settings.API_V1_PREFIX}/health",
            "algorithms": f"{settings.API_V1_PREFIX}/algorithms"
        }
    }

@app.get("/favicon.ico",include_in_schema=False)
async def favicon():
    return JSONResponse(status_code=204, content={})
# @app.get("/")
# def read_root():
#     return {"message": "Hello"}


if __name__=="__main__":
    print("Hello from backend/app.py")
    uvicorn.run(
        "backend.app:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        # debug=settings.DEBUG,
        log_level=settings.LOG_LEVEL
    )
