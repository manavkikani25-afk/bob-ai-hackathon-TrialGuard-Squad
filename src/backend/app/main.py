import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .database.session import Base, engine, SessionLocal, BASE_DIR
from .seed.seed_data import seed_database
from .services.risk_scoring import recalculate_site_risk_scores
from .api import dashboard, sites, deviations, capa, copilot

app = FastAPI(
    title="TrialGuard AI — Backend API",
    description="Clinical Trial Risk Monitor & Protocol Deviation Detector API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
        recalculate_site_risk_scores(db)
    finally:
        db.close()

app.include_router(dashboard.router)
app.include_router(sites.router)
app.include_router(deviations.router)
app.include_router(capa.router)
app.include_router(copilot.router)

@app.get("/api/health")
def health_check():
    return {
        "system": "TrialGuard AI",
        "status": "online",
        "documentation": "/docs"
    }

# Locate static frontend directory for single unified serving
possible_dist_dirs = [
    os.path.join(BASE_DIR, "dist"),
    os.path.join(os.path.dirname(BASE_DIR), "dist"),
    os.path.join(os.path.dirname(BASE_DIR), "src", "frontend", "dist"),
]

dist_dir = None
for d in possible_dist_dirs:
    if os.path.exists(d) and os.path.exists(os.path.join(d, "index.html")):
        dist_dir = d
        break

if dist_dir:
    assets_dir = os.path.join(dist_dir, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="static")

    @app.get("/{full_path:path}")
    def serve_frontend(full_path: str):
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="API route not found")
        index_file = os.path.join(dist_dir, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        raise HTTPException(status_code=404, detail="Frontend index.html not found")
