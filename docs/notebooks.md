# Notebooks Guide

Use notebooks for exploration, modeling, and reporting. Keep reusable logic in `src/` and store intermediate assets in `outputs/`.

## Typical Flow

1. **Task 1: Data Exploration and Context**
   - Load Brent oil price data and parse dates.
   - Plot raw prices to identify large shocks or regime changes.
   - Compute log returns and test stationarity (ADF or KPSS).
   - Draft assumptions and limitations in notebook markdown.

2. **Task 2: Bayesian Change Point Modeling**
   - Define priors for change point index and before/after parameters.
   - Use `pm.math.switch` to build the likelihood.
   - Run MCMC, check convergence, and summarize posteriors.
   - Quantify impacts and align change points to event dates.

3. **Task 3: Results Packaging**
   - Export change point tables and event-aligned summaries for the API.
   - Produce figures for the report and dashboard.

## Practices

- Keep notebooks deterministic; set random seeds for reproducibility.
- Save generated figures and tables under `outputs/figures/`.
- Avoid side effects; move reusable code to `src/` and import.
- Document insights and justifications in markdown cells.

## Running

- Open notebooks in Jupyter Lab or VS Code.
- Ensure the virtual environment is active and dependencies installed.
- Execute cells top-to-bottom and commit meaningful results (e.g., plots, metrics).

Refer to the main README for project-specific commands.
