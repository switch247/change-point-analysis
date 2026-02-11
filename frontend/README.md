# Brent Change Point Dashboard

## Local Setup

### Backend API

```bash
python -m src.api.change_point_api
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend calls the API at `http://localhost:8000` by default. To override:

```bash
VITE_API_BASE=http://localhost:8000 npm run dev
```

## Responsiveness

- Layout uses responsive grid and chart containers to adapt across desktop, tablet, and mobile widths.
- Charts and tables scale to the available width while maintaining readable labels.

## Filters and Interactions

- Date range filters for prices, log returns, and events.
- Change point window size control (days).
- Click an event in the timeline strip to highlight its date on the price chart.
