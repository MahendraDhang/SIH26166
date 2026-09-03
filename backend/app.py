from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from routes.analysis import router as analysis_router


# ============================================================
# BASE / RESULT DIRECTORY
# ============================================================

# Project root:
# D:\SIH26166
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

# Result directory:
# Local  -> D:\SIH26166\Result
# Render -> /app/Result
RESULT_DIR = os.path.join(
    BASE_DIR,
    "Result"
)


# ============================================================
# CREATE RESULT DIRECTORY
# ============================================================

os.makedirs(
    RESULT_DIR,
    exist_ok=True
)


# ============================================================
# APP
# ============================================================

app = FastAPI(
    title="SIH26166 Image Correspondence API",
    description="Chandrayaan-2 Multi-Modal Image Correspondence System",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# SERVE RESULT IMAGES
# ============================================================

app.mount(
    "/results",
    StaticFiles(
        directory=RESULT_DIR
    ),
    name="results"
)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "message": "SIH26166 Backend is running",
        "status": "success"
    }


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "service": "SIH26166 Backend"
    }


# ============================================================
# ANALYSIS ROUTES
# ============================================================

app.include_router(
    analysis_router
)