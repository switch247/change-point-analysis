"""Central configuration for the financial portfolio forecasting project."""
from __future__ import annotations

from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_name: str = "Financial Portfolio Forecasting"

    # Base paths
    root_dir: Path = Path(__file__).resolve().parents[2]
    data_dir: Path = root_dir / "data"
    raw_data_dir: Path = data_dir / "raw"
    processed_data_dir: Path = data_dir / "processed"
    vector_store_dir: Path = root_dir / "vector_store"
    outputs_dir: Path = root_dir / "outputs"
    figures_dir: Path = outputs_dir / "figures"
    reports_dir: Path = outputs_dir / "reports"
    models_dir: Path = outputs_dir / "models"

    # File names for financial data
    tsla_raw_file: str = "tsla_raw.csv"
    bnd_raw_file: str = "bnd_raw.csv"
    spy_raw_file: str = "spy_raw.csv"
    combined_raw_file: str = "financial_data_raw.csv"

    # Asset tickers
    tickers: list[str] = ["TSLA", "BND", "SPY"]

    # Date range
    start_date: str = "2015-01-01"
    end_date: str = "2026-01-15"

    @property
    def tsla_raw_path(self) -> Path:
        return self.raw_data_dir / self.tsla_raw_file

    @property
    def bnd_raw_path(self) -> Path:
        return self.raw_data_dir / self.bnd_raw_file

    @property
    def spy_raw_path(self) -> Path:
        return self.raw_data_dir / self.spy_raw_file

    @property
    def combined_raw_path(self) -> Path:
        return self.raw_data_dir / self.combined_raw_file


settings = Settings()

# Backward-compatible mapping used by legacy modules
DATA_PATHS = {
    "raw": str(settings.raw_data_dir),
    "processed": str(settings.processed_data_dir),
    "figures": str(settings.figures_dir),
    "reports": str(settings.reports_dir),
}
