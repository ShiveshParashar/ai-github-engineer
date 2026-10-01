from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
 
from app.api.repositories import router as repository_router
from app.dashboard_route import router as dashboard_router
 
 
class NoCacheStaticFiles(StaticFiles):
    """Static files that the browser never caches (handy during development)."""
 
    async def get_response(self, path, scope):
        response = await super().get_response(path, scope)
        response.headers["Cache-Control"] = "no-store"
        return response
 
 
app = FastAPI(
    title="AI GitHub Repository Engineer",
    description="AI-powered GitHub repository analysis platform",
    version="1.0.0",
)
 
 
# -----------------------------------------
# API routes
# -----------------------------------------
 
app.include_router(repository_router)
 
 
# -----------------------------------------
# Static files
# -----------------------------------------
 
app.mount(
    "/static",
    NoCacheStaticFiles(directory="app/static"),
    name="static",
)
 
 
# -----------------------------------------
# Dashboard
# -----------------------------------------
 
app.include_router(dashboard_router)
 
 
# -----------------------------------------
# Root
# -----------------------------------------
 
@app.get("/")
def root():
    return {"message": "AI GitHub Repository Engineer is running"}
 
 
# -----------------------------------------
# Health
# -----------------------------------------
 
@app.get("/health")
def health():
    return {"status": "healthy"}
 