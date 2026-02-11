
# Change Point API (Task 3)

Run the Flask service from the repository root:

```bash
python -m src.api.change_point_api
```

The API serves:

- `GET /api/health`
- `GET /api/summary`
- `GET /api/prices?start=YYYY-MM-DD&end=YYYY-MM-DD`
- `GET /api/log-returns?start=YYYY-MM-DD&end=YYYY-MM-DD`
- `GET /api/events?start=YYYY-MM-DD&end=YYYY-MM-DD`
- `GET /api/change-point?window=30`
