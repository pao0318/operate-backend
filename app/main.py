from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.exceptions import APIException
from app.api.router import api_router

app = FastAPI(
    title="Operate Backend API",
    description="FastAPI backend service with SSE support and Case Management APIs",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"message": exc.detail}},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    if settings.APP_DEBUG:
        return JSONResponse(
            status_code=500,
            content={"error": {"message": str(exc), "type": type(exc).__name__}},
        )
    return JSONResponse(
        status_code=500,
        content={"error": {"message": "Internal Server Error"}},
    )


app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    return {
        "message": "Operate Backend API",
        "docs": "/docs",
        "health": "/api/health"
    }
