# Dependencies & Environment

This project uses Python data science and Bayesian modeling libraries. The exact versions are managed via `requirements.txt` and `pyproject.toml`.

## Installation (High Level)

1. Set up a Python virtual environment (venv or conda).
2. Install dependencies: `pip install -r requirements.txt`.

## Key Libraries

### Data Processing
- pandas: Data manipulation and analysis.
- numpy: Numerical computations.

### Bayesian Change Point Modeling
- pymc: Bayesian modeling and MCMC sampling.
- arviz: Diagnostics, posterior summaries, and plots.

### Statistical Utilities
- statsmodels: Stationarity tests and time series utilities.

### Visualization
- matplotlib: Core plotting.
- seaborn/plotly: Optional, for richer visuals.

### API and Dashboard (Optional)
- FastAPI or Flask: API layer for dashboard data.
- Streamlit or React frontend (if implemented).

### Testing and Development
- pytest: Unit testing.
- jupyter: Interactive notebooks.

## System/Service Dependencies
- Python 3.11+ recommended.
- Docker & Docker Compose (for containerized setup).
- Git for version control.
- DVC (if you plan to version data artifacts).

## Other Tools
- Makefile: Automation of build and run tasks.
- VS Code or Jupyter Lab: For development and notebook execution.

See `requirements.txt` for the full list of Python dependencies.
- Prefer pinned versions for reproducibility.
- Use CI to validate installation and tests on push.
