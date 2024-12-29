from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.resources import (
    auth_resource,
    user_resource,
    ship_resource
)

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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
