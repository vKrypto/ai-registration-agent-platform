"use client";

import { useState } from "react";
import { getApplicationStatus } from "../../lib/api";

export default function StatusPage() {
  const [applicationId, setApplicationId] = useState("");
  const [status, setStatus] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  async function fetchStatus() {
    setError(null);
    setStatus(null);

    try {
      const result = await getApplicationStatus(applicationId);
      setStatus(result);
    } catch {
      setError("Could not fetch status.");
    }
  }

  return (
    <section className="card">
      <h1>Application Status</h1>
      <p className="muted">Enter an application ID to check the current state.</p>

      <div className="form">
        <input
          value={applicationId}
          onChange={(event) => setApplicationId(event.target.value)}
          placeholder="Application ID"
        />
        <button type="button" onClick={fetchStatus}>Check Status</button>
      </div>

      {status && (
        <div className="card">
          <h2>{status.application_id}</h2>
          <p className="status-pill">{status.status}</p>
          <p>{status.message}</p>
          <p>Next action required: {String(status.next_action_required)}</p>
        </div>
      )}

      {error && <p>{error}</p>}
    </section>
  );
}
