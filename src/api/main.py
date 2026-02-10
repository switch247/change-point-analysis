import pandas as pd
import mlflow.sklearn
import joblib
from fastapi import FastAPI, HTTPException, Query
from sqlalchemy import text
from .database import engine
from .schemas import TopProduct, ChannelActivity, MessageSearchResult, VisualContentStats
from typing import List
from src.api.pydantic_models import TransactionInput, PredictionOutput
import sys
from pathlib import Path

# Add project root to path to allow imports from src if needed
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

app = FastAPI(title="Test")

# Set tracking URI - assuming mlruns is in the root of the app
# In Docker, we'll set WORKDIR to /app and copy mlruns there
mlflow.set_tracking_uri("file:./mlruns")

model_name = "test"
model_version = "1"
model_uri = f"models:/{model_name}/{model_version}"

model = None


@app.on_event("startup")
def load_model():
    global model
    try:
        print(f"Attempting to load model from {model_uri}...")
        model = mlflow.sklearn.load_model(model_uri)
        print("Model loaded successfully from MLflow.")
    except Exception as e:
        print(f"Failed to load from MLflow: {e}")
        fallback_path = project_root / "outputs" / "models" / "model.pkl"
        print(f"Attempting fallback load from {fallback_path}...")
        try:
            model = joblib.load(fallback_path)
            print("Model loaded successfully from fallback path.")
        except Exception as e2:
            print(f"Error loading model from fallback: {e2}")
            # In production, we might want to fail startup, but for dev log it
            pass


@app.get("/")
def read_root():
    return {"message": "Credit Risk Fraud Detection API is running"}

