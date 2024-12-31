from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from kafka.consumer import kafka_lifespan
from config.config import get_logger
from api.resources import (
    auth_resource,
    user_resource,
    ship_resource,
    planet_resource
)


logger = get_logger()


# Metadata for API documentation
tags_metadata = [
    {"name": "Auth", "description": "Authentication related endpoints."},
    {"name": "User", "description": "User management endpoints."},
    {"name": "Ship", "description": "Ship management endpoints."},
    {"name": "Planet", "description": "Planet management endpoints."},
    {"name": "Health", "description": "Health check endpoint."}
]

# Create FastAPI application
app = FastAPI(
    title="Outer Wilds API",
    description="API for managing users, ships, and planets in the Outer Wilds universe.",
    version="1.0.0",
    openapi_tags=tags_metadata
)

# CORS configuration
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
)

# Health check route


@app.get("/ping", tags=["Health"], summary="Check API status")
async def ping():
    """Ping the API to check if it's running."""
    logger.info("Health check endpoint accessed.")
    return {"message": "API is running"}

# Include routers from resources
app.include_router(auth_resource.router)
app.include_router(user_resource.router)
app.include_router(ship_resource.router)
app.include_router(planet_resource.router)

# Integrate Kafka consumer into the application's lifecycle
app.router.lifespan_context = kafka_lifespan

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Outer Wilds API...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
