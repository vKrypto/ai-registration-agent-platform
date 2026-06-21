"use client";

import { useEffect, useState } from "react";
import { getReviewQueue } from "../../lib/api";

export default function ReviewerPage() {
  const [items, setItems] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  async function loadQueue() {
    setError(null);
    try {
      const result = await getReviewQueue();
      setItems(result.items ?? []);
    } catch {
      setError("Could not load reviewer queue.");
    }
  }

  useEffect(() => {
    loadQueue();
  }, []);

  return (
    <section className="card">
      <h1>Reviewer Dashboard</h1>
      <p className="muted">Applications that need manual review are shown here.</p>
      <button type="button" onClick={loadQueue}>Refresh Queue</button>

      <div className="grid">
        {items.map((item) => (
          <div className="card" key={item.application_id}>
            <h2>{item.application_id}</h2>
            <p className="status-pill">{item.status}</p>
            <p>Risk score: {item.risk_score}</p>
            <p>Reason: {item.reason}</p>
            <a className="button" href={`/reviewer/${item.application_id}`}>Open Review</a>
          </div>
        ))}
      </div>

      {items.length === 0 && <p>No applications are waiting for review.</p>}
      {error && <p>{error}</p>}
    </section>
  );
}
