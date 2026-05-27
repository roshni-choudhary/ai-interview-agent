from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import settings
from app.database import init_db
from app.routes import auth, interview, progress
import uvicorn

app = FastAPI(
    title="AI Coding Interview Agent",
    description="Adaptive coding interview practice platform driven by agentic AI and sandboxed execution.",
    version="1.0.0"
)

# CORS headers setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(auth.router)
app.include_router(interview.router)
app.include_router(progress.router)

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/health")
async def health_check():
    return {"status": "healthy", "provider": settings.LLM_PROVIDER}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"An unexpected error occurred: {str(exc)}"}
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
