# Task 1 - Analysis Foundation (Week 11)

This document outlines the Task 1 workflow for the Brent oil price change point analysis, including assumptions, limitations, and communication channels. Task tracking notes and early experiments should be captured in the `experiments/` folder.

## Analysis Workflow (End-to-End)

1. **Data loading and validation**
   - Load Brent daily prices from `data/processed/BrentOilPrices.csv`.
   - Parse dates and confirm coverage (1987-05-20 to 2022-09-30).
   - Check missing values and duplicates.

2. **Exploratory data analysis**
   - Plot price levels to identify major regimes and shocks.
   - Compute log prices and log returns to assess stationarity.
   - Inspect volatility clustering with rolling standard deviation.

3. **Event research and structuring**
   - Compile 10-15 key geopolitical, OPEC, and macro events (2013-2022).
   - Store events as a structured table in `data/processed/events.csv`.

4. **Model design (Bayesian change point)**
   - Define a discrete prior over the change point index ($\tau$).
   - Define pre/post parameters (e.g., $\mu_1$, $\mu_2$, $\sigma$).
   - Use a switch function to map the mean based on $t < \tau$.

5. **Model fitting and diagnostics**
   - Run MCMC sampling and check convergence (R-hat, ESS).
   - Inspect posterior traces and posterior predictive checks.

6. **Interpretation and event alignment**
   - Convert posterior $\tau$ to calendar dates.
   - Compare detected change points with the events table.
   - Quantify pre/post mean shifts and uncertainty bounds.

7. **Reporting and delivery**
   - Summarize findings in `reports/interim.md` and `reports/final.md`.
   - Provide event-aligned figures for the dashboard.

## Time Series Properties and Modeling Implications

- **Trend**: Long-run nonstationarity in prices motivates differencing or log returns.
- **Stationarity**: Log returns are expected to be closer to stationary than price levels.
- **Volatility patterns**: Clustering suggests heteroskedasticity; consider extensions if needed.
- **Structural breaks**: Change point models provide interpretable regime shifts.

## Assumptions and Limitations

- **Correlation vs causation**: A change point aligned to an event indicates temporal correlation, not causal proof.
- **Single-factor view**: Prices reflect many simultaneous factors (demand, supply, policy, geopolitics).
- **Event dating**: Event start dates are approximate and can be multi-day or multi-month.
- **Model simplicity**: A single-change-point model may not capture multiple regimes without extensions.

## Communication Channels

- **Technical report**: Methods, diagnostics, and quantified impacts.
- **Dashboard**: Interactive views of prices, change points, and events.
- **Briefing slides**: One-page executive summary for policymakers and investors.
- **Stakeholder Q&A**: Short session focused on assumptions and uncertainty.

## Expected Outputs (Change Point Analysis)

- Posterior distribution of $\tau$ (likely break date range).
- Posterior distributions of pre/post means and volatility.
- A quantified statement such as: "Post-event mean price shifted by $X$ with $Y$% credible interval."

