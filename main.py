# main.py
from fastapi import FastAPI

from routes.centralities import router as centralities_router
from routes.generate import router as generate_router
from routes.health import router as health_router
from routes.image import router as image_router
from routes.properties import router as properties_router

app = FastAPI(
    title="Graph API",
    version="0.2.0",
    description="Analyse undirected and directed graphs – "
                "centralities, properties, degree sequences, and visualisation.",
)

# ── Register routers ─────────────────────────────────────────────────
app.include_router(health_router)
app.include_router(generate_router)
app.include_router(centralities_router)
app.include_router(properties_router)
app.include_router(image_router)

# ── Entry point ──────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

