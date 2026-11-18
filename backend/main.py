from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import pandas as pd

app = FastAPI(title="PathSnap Route Reconstruction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE = Path(__file__).resolve().parent.parent
RESULT_FILE = BASE / "results" / "reconstructed_route.csv"


@app.get("/")
def home():
    return {"message": "PathSnap API is running"}


@app.get("/route")
def get_route():
    if not RESULT_FILE.exists():
        return {"error": "Route file not found"}

    data = pd.read_csv(RESULT_FILE)

    return {
        "total_points": len(data),
        "route": data.to_dict(orient="records")
    }


@app.get("/health")
def health():
    return {"status": "healthy"}