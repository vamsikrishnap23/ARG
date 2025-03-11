from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from app.auth.router import router as auth_router
from app.profile.router import router as profile_router
from app.config import settings

app = FastAPI(
    title="Cloud Mystery Game API",
    description="Backend API for Cloud-Based ARG Game",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(profile_router, prefix="/profile", tags=["Profile"])  # Fixed here

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to Cloud Mystery Game API"}
