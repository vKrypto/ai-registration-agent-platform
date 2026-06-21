from fastapi import FastAPI

from app.routes import agent, applications, health, reviewer

app = FastAPI(
    title="AI Registration Agent Platform API",
    description="Backend API for AI-powered registration, document processing, and approval workflows.",
    version="0.1.0",
)

app.include_router(health.router, tags=["health"])
app.include_router(applications.router, prefix="/api/v1/applications", tags=["applications"])
app.include_router(agent.router, prefix="/api/v1/agent", tags=["agent"])
app.include_router(reviewer.router, prefix="/api/v1/reviewer", tags=["reviewer"])


@app.get("/")
def root() -> dict[str, str]:
    return {
        "service": "ai-registration-agent-platform",
        "status": "running",
    }
