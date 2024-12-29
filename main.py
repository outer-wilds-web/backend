from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio

from api.resources import (
    auth_resource,
    user_resource,
    ship_resource
)

from kafka.consumer import start_consumer

tags_metadata = [
    {
        "name": "Auth"
    },
    {
        "name": "User"
    },
    {
        "name": "Ship"
    }
]

app = FastAPI(
    title="Outer Wilds API",
    openapi_tags=tags_metadata
)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
)

app.include_router(auth_resource.router)
app.include_router(user_resource.router)
app.include_router(ship_resource.router)


# Global task variable to manage the Kafka consumer task
consumer_task = None


@app.on_event("startup")
async def startup_event():
    """
    Event triggered when the application starts.
    Initializes the Kafka consumer as a background task.
    """
    global consumer_task
    consumer_task = asyncio.create_task(start_consumer())
    print("Kafka consumer task created during startup.")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Event triggered when the application shuts down.
    Cancels the Kafka consumer background task.
    """
    global consumer_task
    if consumer_task:
        consumer_task.cancel()
        try:
            await consumer_task
        except asyncio.CancelledError:
            print("Kafka consumer task was cancelled.")
        print("Kafka consumer task stopped during shutdown.")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
