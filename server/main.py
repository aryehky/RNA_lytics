from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional
import numpy as np

app = FastAPI(title="RNAlytics API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routes
@app.get("/")
async def root():
    return {"message": "Welcome to RNAlytics API"}

@app.get("/api/deg/{treatment}")
async def get_differential_expression(treatment: str, p_value_threshold: float = 0.05):
    """Get differential expression results for a specific treatment."""
    valid_treatments = ["CsA", "VOC"]
    if treatment not in valid_treatments:
        raise HTTPException(status_code=400, detail=f"Treatment must be one of {valid_treatments}")
    
    # TODO: Implement actual data loading from processed files
    return {
        "treatment": treatment,
        "deg_count": 1492 if treatment == "CsA" else 489,
        "threshold": p_value_threshold
    }

@app.get("/api/pathways/{treatment}")
async def get_pathway_analysis(treatment: str):
    """Get pathway analysis results for a specific treatment."""
    valid_treatments = ["CsA", "VOC"]
    if treatment not in valid_treatments:
        raise HTTPException(status_code=400, detail=f"Treatment must be one of {valid_treatments}")
    
    # TODO: Implement actual pathway analysis data loading
    return {
        "treatment": treatment,
        "top_pathway": "Cell Cycle" if treatment == "CsA" else "Protein Processing in ER"
    }

@app.get("/api/go-terms/{treatment}")
async def get_go_terms(treatment: str):
    """Get GO term enrichment results for a specific treatment."""
    valid_treatments = ["CsA", "VOC"]
    if treatment not in valid_treatments:
        raise HTTPException(status_code=400, detail=f"Treatment must be one of {valid_treatments}")
    
    # TODO: Implement actual GO term data loading
    return {
        "treatment": treatment,
        "significant_terms": 1134 if treatment == "CsA" else 1024
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 