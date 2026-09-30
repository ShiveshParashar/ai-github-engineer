from fastapi import FastAPI
from app.api.repositories import router as repository_router

app = FastAPI(
    title="AI GitHub Repository Engineer",
    description="AI-powered GitHub repository analysis platform",
    version="1.0.0"
)

app.include_router(repository_router)


@app.get("/")
def root():
    return {
        "message": "AI GitHub Repository Engineer is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }