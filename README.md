# Change Point Analysis of Brent Oil Prices

Week 11 challenge repository for detecting structural breaks in Brent oil prices and linking shifts to major geopolitical and economic events.

## Business Objective
- Identify key events that significantly impact Brent oil prices.
- Quantify the magnitude of shifts using Bayesian change point modeling.
- Communicate insights for investors, policymakers, and energy companies.

## Scope and Deliverables
- **Task 1: Foundation** - Define analysis workflow, build a structured events table (10-15 key events), and document assumptions and limitations.
- **Task 2: Change Point Modeling** - EDA, stationarity checks, Bayesian change point model in PyMC, and quantified impact statements.
- **Task 3: Dashboard** - Interactive UI to explore prices, change points, and event correlations (backend API + frontend UI).

## Repository Layout
```
<project root>
├── data/
│   ├── raw/                  # Raw inputs (starter datasets, reference codes)
│   └── processed/            # Enriched and analysis-ready datasets
├── docs/                     # Documentation and guides
├── experiments/              # Challenge brief and local experiment notes
├── notebooks/                # EDA, impact-modeling, forecasting notebooks
├── outputs/                  # Generated figures, models, reports, CSVs
├── scripts/                  # Utilities and pipeline helpers
├── src/
│   ├── api/                  # Backend API (Flask/FastAPI scaffold)
│   ├── dashboard/            # Dashboard app (if implemented)
│   └── utils/                # Reusable modules
├── tests/                    # Unit tests
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Quick Start
1. **Setup Environment**:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. **Run Notebooks**:
   - Open and run analysis notebooks in `notebooks/` using Jupyter or VS Code
   - Start with `notebooks/01_eda.ipynb` for trend/volatility analysis

3. **Run API (optional)**:
   ```powershell
   uvicorn src.api.main:app --host 0.0.0.0 --port 8000
   ```
   Access at http://localhost:8000

## Task 3 Dashboard
- Backend API (Flask): `python -m src.api.change_point_api`
- Frontend: see [frontend/README.md](frontend/README.md)

## Workflow and Best Practices
- Capture task notes and event research logs in `experiments/`.
- Keep exploratory work in notebooks and move reusable logic into `src/`.
- Save figures and tables to `outputs/` for report-ready assets.

## Dependencies
- Python 3.11+
- Key libraries: pandas, numpy, pymc, arviz, statsmodels, matplotlib
- See `requirements.txt` for full list

## References
- Challenge brief and task details: `experiments/todo.md`
- Business understanding: `docs/business_understanding.md`
- Data dependencies: `docs/dependencies.md`

## Contact
- For questions about implementation or results, refer to notebook outputs and dashboard

