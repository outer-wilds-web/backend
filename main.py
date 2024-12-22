from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import config.config as config
from database.script import feed_database

from api.resources import (
    auth_resource,
    user_resource,
    entreprise_resource,
    dossier_resource,
    echantillon_resource,
    analyse_resource
)

tags_metadata = [
    {
        "name": "Auth"
    },
    {
        "name": "User"
    },
    {
        "name": "Entreprise"
    },
    {
        "name": "Dossier"
    },
    {
        "name": "Echantillon"
    },
    {
        "name": "Analyse"
    }
]

app = FastAPI(
    title="Horus Manager",
    openapi_tags=tags_metadata
)

origins = [
    "http://localhost:27017",
    "http://localhost:8081",
    "https://gehorus-woupyltbaa-nn.a.run.app",
    "https://horus-334822343093.northamerica-northeast1.run.app",
    "https://horus-woupyltbaa-nn.a.run.app",
    "https://horus-visualizer-woupyltbaa-nn.a.run.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
)

if config.config["env"]["name"] == "dev":
    feed_database()

app.include_router(auth_resource.router)
app.include_router(user_resource.router)
app.include_router(entreprise_resource.router)
app.include_router(dossier_resource.router)
app.include_router(echantillon_resource.router)
app.include_router(analyse_resource.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
