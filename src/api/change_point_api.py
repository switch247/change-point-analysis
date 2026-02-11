from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

import pandas as pd
import numpy as np
from flask import Flask, jsonify, request
from flask_cors import CORS

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "BrentOilPrices.csv"
EVENTS_PATH = PROJECT_ROOT / "data" / "processed" / "events.csv"

app = Flask(__name__)
CORS(app)


def _load_prices() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["Date"] = pd.to_datetime(df["Date"], format="mixed", dayfirst=True, errors="coerce")
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    df = df.dropna(subset=["Date", "Price"]).sort_values("Date").reset_index(drop=True)
    return df


def _load_events() -> pd.DataFrame:
    df = pd.read_csv(EVENTS_PATH)
    df["event_date"] = pd.to_datetime(df["event_date"], errors="coerce")
    return df


def _filter_date_range(
    df: pd.DataFrame,
    date_col: str,
    start: Optional[str],
    end: Optional[str],
) -> pd.DataFrame:
    if start:
        start_dt = pd.to_datetime(start, errors="coerce")
        if pd.notna(start_dt):
            df = df[df[date_col] >= start_dt]
    if end:
        end_dt = pd.to_datetime(end, errors="coerce")
        if pd.notna(end_dt):
            df = df[df[date_col] <= end_dt]
    return df


def _estimate_change_point(df: pd.DataFrame, window: int = 30) -> Dict[str, Any]:
    df = df.copy()
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    df = df.dropna(subset=["Price"]).reset_index(drop=True)
    df["log_price"] = np.log(df["Price"].where(df["Price"] > 0))
    df["log_return"] = df["log_price"].diff()
    df_lr = df.dropna(subset=["log_return"]).reset_index(drop=True)

    if len(df_lr) < window * 2:
        return {
            "status": "insufficient_data",
            "window": window,
        }

    diffs = []
    for idx in range(window, len(df_lr) - window):
        before = df_lr["log_return"].iloc[idx - window : idx].mean()
        after = df_lr["log_return"].iloc[idx : idx + window].mean()
        diffs.append((idx, abs(after - before), before, after))

    best_idx, best_diff, mu_before, mu_after = max(diffs, key=lambda x: x[1])
    cp_date = df_lr.loc[best_idx, "Date"]
    return {
        "status": "ok",
        "change_point_date": cp_date.strftime("%Y-%m-%d"),
        "window": window,
        "mean_before": float(mu_before),
        "mean_after": float(mu_after),
        "mean_shift": float(mu_after - mu_before),
    }


@app.get("/api/health")
def health() -> Dict[str, str]:
    return {"status": "ok", "service": "change-point-api"}


@app.get("/api/prices")
def prices() -> Any:
    df = _load_prices()
    start = request.args.get("start")
    end = request.args.get("end")
    df = _filter_date_range(df, "Date", start, end)
    payload = df.rename(columns={"Date": "date", "Price": "price"})
    return jsonify(payload.to_dict(orient="records"))


@app.get("/api/log-returns")
def log_returns() -> Any:
    df = _load_prices()
    df["log_price"] = np.log(df["Price"].where(df["Price"] > 0))
    df["log_return"] = df["log_price"].diff()
    df = df.dropna(subset=["log_return"]).reset_index(drop=True)
    start = request.args.get("start")
    end = request.args.get("end")
    df = _filter_date_range(df, "Date", start, end)
    payload = df[["Date", "log_return"]].rename(columns={"Date": "date"})
    return jsonify(payload.to_dict(orient="records"))


@app.get("/api/events")
def events() -> Any:
    df = _load_events()
    start = request.args.get("start")
    end = request.args.get("end")
    df = _filter_date_range(df, "event_date", start, end)
    payload = df.rename(columns={"event_date": "date"})
    payload["date"] = payload["date"].dt.strftime("%Y-%m-%d")
    return jsonify(payload.to_dict(orient="records"))


@app.get("/api/change-point")
def change_point() -> Any:
    df = _load_prices()
    window = request.args.get("window", default=30, type=int)
    result = _estimate_change_point(df, window=window)
    return jsonify(result)


@app.get("/api/summary")
def summary() -> Any:
    df = _load_prices()
    events_df = _load_events()
    result = {
        "start_date": df["Date"].min().strftime("%Y-%m-%d"),
        "end_date": df["Date"].max().strftime("%Y-%m-%d"),
        "total_records": int(len(df)),
        "event_count": int(len(events_df)),
    }
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
