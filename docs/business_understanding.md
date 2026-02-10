# Business Understanding: Change Point Analysis of Brent Oil Prices

## Business Objective
Birhan Energies is a consultancy firm providing data-driven insights to stakeholders in the energy sector. The goal is to analyze how major political and economic events influence Brent oil prices and provide actionable intelligence for investors, policymakers, and energy companies.

The analysis focuses on identifying structural breaks in the price series, estimating how much prices shift before and after key events, and explaining those shifts in a clear, defensible way.

## Situational Overview (Business Need)
The oil market is highly volatile, which makes decision-making difficult for:
- Investors who need to manage risk and maximize returns.
- Policymakers who must plan for economic stability and energy security.
- Energy companies that need reliable price signals to manage costs and supply chains.

You will:
- Detect major changes in Brent oil prices using Bayesian change point modeling.
- Quantify the magnitude of those changes and relate them to known events.
- Communicate findings through a report and an interactive dashboard.

## Data
Historical Brent oil prices with daily observations from May 20, 1987 to September 30, 2022.

### Data Fields
- Date: Daily timestamp (formatted as day-month-year in the source data).
- Price: Brent oil price in USD per barrel.

## Assumptions and Limitations
- Statistical change points indicate structural breaks but do not prove causality.
- Event alignment is hypothesis-driven and may require domain validation.
- Daily prices can reflect multiple overlapping factors (policy, conflict, supply, macro trends).

## Learning Outcomes
### Skills:
- Change point analysis and interpretation
- Bayesian inference using PyMC
- MCMC diagnostics and model comparison
- Analytical storytelling with uncertainty-aware statements

### Knowledge:
- Choosing probability distributions for time series modeling
- Interpreting posterior distributions and uncertainty
- Communicating differences between correlation and causal impact

### Communication:
- Reporting to government bodies and non-technical stakeholders
- Creating intuitive dashboards for exploring event impacts

## Key Dates
- Challenge Introduction: 10:30 AM UTC on Wednesday, 04 Feb 2026
- Interim Submission: 8:00 PM UTC on Sunday, 08 Feb 2026
- Final Submission: 8:00 PM UTC on Tuesday, 10 Feb 2026

For a detailed breakdown of tasks and deliverables, see `experiments/todo.md`.
