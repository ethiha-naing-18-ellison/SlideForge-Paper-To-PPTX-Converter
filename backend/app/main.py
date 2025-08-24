"""Main FastAPI application for SlideForge backend."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1 import router as v1_router
from .core.config import get_settings
from .core.logging import configure_logging, get_logger


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    # Configure logging
    configure_logging()
    
    # Get settings
    settings = get_settings()
    
    # Create FastAPI app
    app = FastAPI(
        title="SlideForge API",
        description="Paper-to-PPTX Converter API",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(v1_router)
    
    # Startup event
    @app.on_event("startup")
    async def startup_event():
        logger = get_logger(__name__)
        logger.info("SlideForge backend starting up")
    
    # Shutdown event
    @app.on_event("shutdown")
    async def shutdown_event():
        logger = get_logger(__name__)
        logger.info("SlideForge backend shutting down")
    
    return app


# Create app instance
app = create_app()


def main():
    """Main entry point for running the application."""
    import uvicorn
    from .core.config import get_settings
    
    settings = get_settings()
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )


if __name__ == "__main__":
    main()
