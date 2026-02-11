import React, { useEffect, useMemo, useState } from "react";
import {
  Area,
  AreaChart,
  CartesianGrid,
  Line,
  LineChart,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";
import { fetchJson } from "./api.js";

const formatNumber = (value) => new Intl.NumberFormat("en-US", {
  maximumFractionDigits: 2
}).format(value);

const formatDate = (value) => new Date(value).toLocaleDateString("en-US", {
  year: "numeric",
  month: "short",
  day: "numeric"
});

export default function App() {
  const [summary, setSummary] = useState(null);
  const [prices, setPrices] = useState([]);
  const [returns, setReturns] = useState([]);
  const [events, setEvents] = useState([]);
  const [changePoint, setChangePoint] = useState(null);
  const [dateRange, setDateRange] = useState({ start: "2013-01-01", end: "2022-12-31" });
  const [windowSize, setWindowSize] = useState(30);
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [error, setError] = useState(null);

  const loadData = async () => {
    try {
      const [summaryData, pricesData, returnsData, eventsData, changePointData] = await Promise.all([
        fetchJson("/api/summary"),
        fetchJson(`/api/prices?start=${dateRange.start}&end=${dateRange.end}`),
        fetchJson(`/api/log-returns?start=${dateRange.start}&end=${dateRange.end}`),
        fetchJson(`/api/events?start=${dateRange.start}&end=${dateRange.end}`),
        fetchJson(`/api/change-point?window=${windowSize}`)
      ]);

      setSummary(summaryData);
      setPrices(pricesData);
      setReturns(returnsData);
      setEvents(eventsData);
      setChangePoint(changePointData);
      setError(null);
    } catch (err) {
      setError(err.message || "Failed to load data");
    }
  };

  useEffect(() => {
    loadData();
  }, [dateRange, windowSize]);

  const eventDates = useMemo(() => new Set(events.map((event) => event.date)), [events]);

  const highlightedEvents = useMemo(() => {
    return events
      .slice()
      .sort((a, b) => new Date(a.date) - new Date(b.date));
  }, [events]);

  return (
    <div className="page">
      <header className="hero">
        <div>
          <p className="eyebrow">Brent Crude Market Signals</p>
          <h1>Change Point Intelligence Dashboard</h1>
          <p className="subtitle">
            Track structural shifts in Brent oil prices and connect them to geopolitical events.
          </p>
        </div>
        <div className="summary">
          <div>
            <span>Coverage</span>
            <strong>{summary ? `${summary.start_date} - ${summary.end_date}` : "Loading"}</strong>
          </div>
          <div>
            <span>Records</span>
            <strong>{summary ? formatNumber(summary.total_records) : "Loading"}</strong>
          </div>
          <div>
            <span>Events</span>
            <strong>{summary ? formatNumber(summary.event_count) : "Loading"}</strong>
          </div>
        </div>
      </header>

      <section className="controls">
        <div>
          <label htmlFor="start">Start date</label>
          <input
            id="start"
            type="date"
            value={dateRange.start}
            onChange={(event) => setDateRange((prev) => ({ ...prev, start: event.target.value }))}
          />
        </div>
        <div>
          <label htmlFor="end">End date</label>
          <input
            id="end"
            type="date"
            value={dateRange.end}
            onChange={(event) => setDateRange((prev) => ({ ...prev, end: event.target.value }))}
          />
        </div>
        <div>
          <label htmlFor="window">Change window (days)</label>
          <input
            id="window"
            type="number"
            min="14"
            max="90"
            value={windowSize}
            onChange={(event) => setWindowSize(Number(event.target.value))}
          />
        </div>
        {error && <div className="error">{error}</div>}
      </section>

      <section className="grid">
        <div className="card">
          <div className="card-header">
            <h2>Price Trajectory</h2>
            <p>Daily Brent prices with event markers.</p>
          </div>
          <div className="chart">
            <ResponsiveContainer width="100%" height={320}>
              <LineChart data={prices}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e1b3a" />
                <XAxis dataKey="date" tickFormatter={formatDate} minTickGap={35} />
                <YAxis tickFormatter={formatNumber} width={80} />
                <Tooltip labelFormatter={formatDate} formatter={(value) => formatNumber(value)} />
                <Line type="monotone" dataKey="price" stroke="#ff8a5b" strokeWidth={2} dot={false} />
                {selectedEvent && (
                  <ReferenceLine x={selectedEvent.date} stroke="#fbbf24" strokeDasharray="5 5" />
                )}
              </LineChart>
            </ResponsiveContainer>
          </div>
          <div className="events-strip">
            {highlightedEvents.map((event) => (
              <button
                key={`${event.date}-${event.event_name}`}
                type="button"
                className={selectedEvent?.event_name === event.event_name ? "active" : ""}
                onClick={() => setSelectedEvent(event)}
              >
                <span>{event.date}</span>
                <strong>{event.event_name}</strong>
              </button>
            ))}
          </div>
        </div>

        <div className="card">
          <div className="card-header">
            <h2>Volatility Pulse</h2>
            <p>Log returns highlight volatility clustering.</p>
          </div>
          <div className="chart">
            <ResponsiveContainer width="100%" height={320}>
              <AreaChart data={returns}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e1b3a" />
                <XAxis dataKey="date" tickFormatter={formatDate} minTickGap={35} />
                <YAxis tickFormatter={(value) => value.toFixed(3)} width={80} />
                <Tooltip labelFormatter={formatDate} formatter={(value) => value.toFixed(4)} />
                <Area type="monotone" dataKey="log_return" stroke="#6ed3cf" fill="#0ea5a8" fillOpacity={0.3} />
                {changePoint?.change_point_date && (
                  <ReferenceLine x={changePoint.change_point_date} stroke="#6d28d9" strokeDasharray="6 6" />
                )}
              </AreaChart>
            </ResponsiveContainer>
          </div>
          <div className="insight">
            <h3>Change Point Estimate</h3>
            {changePoint?.status === "ok" ? (
              <div className="insight-grid">
                <div>
                  <span>Date</span>
                  <strong>{changePoint.change_point_date}</strong>
                </div>
                <div>
                  <span>Mean shift</span>
                  <strong>{changePoint.mean_shift.toFixed(5)}</strong>
                </div>
                <div>
                  <span>Window</span>
                  <strong>{changePoint.window} days</strong>
                </div>
              </div>
            ) : (
              <p>Insufficient data for the selected window.</p>
            )}
          </div>
        </div>

        <div className="card events-table">
          <div className="card-header">
            <h2>Event Correlations</h2>
            <p>Filter and review the event list for the selected range.</p>
          </div>
          <div className="table">
            <table>
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Event</th>
                  <th>Category</th>
                  <th>Description</th>
                </tr>
              </thead>
              <tbody>
                {events.map((event) => (
                  <tr key={`${event.date}-${event.event_name}`}>
                    <td>{event.date}</td>
                    <td>{event.event_name}</td>
                    <td>{event.category}</td>
                    <td>{event.description}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <footer className="footer">
        <p>
          API status: {error ? "offline" : "connected"}. Built for Task 3 dashboard delivery.
        </p>
        <div className="legend">
          <span className="dot price" /> Price series
          <span className="dot return" /> Log returns
          <span className="dot change" /> Change point
        </div>
      </footer>
    </div>
  );
}
