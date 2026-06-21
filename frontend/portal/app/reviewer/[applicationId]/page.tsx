"use client";

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export default function ReviewerDetailPage() {
  const params = useParams<{ applicationId: string }>();
  const applicationId = params.applicationId;
  const [application, setApplication] = useState<any>(null);
  const [message, setMessage] = useState<string | null>(null);

  async function loadDetails() {
    const response = await fetch(`${API_BASE_URL}/api/v1/reviewer/applications/${applicationId}`);
    const result = await response.json();
    setApplication(result);
  }

  async function sendDecision(action: "approve" | "reject" | "request-info") {
    const response = await fetch(`${API_BASE_URL}/api/v1/reviewer/applications/${applicationId}/${action}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        comment: "Reviewed from portal",
        reason: "Reviewer decision submitted",
      }),
    });
    const result = await response.json();
    setMessage(`Decision submitted. New status: ${result.status}`);
    await loadDetails();
  }

  useEffect(() => {
    loadDetails();
  }, []);

  if (!application) {
    return <p>Loading review details...</p>;
  }

  return (
    <section className="card">
      <h1>Review Application</h1>
      <h2>{application.application_id}</h2>
      <p className="status-pill">{application.status}</p>
      <p>Risk score: {application.risk_score ?? "Not calculated"}</p>
      <p>Decision: {application.decision ?? "Pending"}</p>

      <div className="card">
        <h2>Validation Results</h2>
        {(application.validation_results ?? []).map((result: any) => (
          <p key={result.rule}>{result.rule}: {result.result}</p>
        ))}
      </div>

      <div className="grid">
        <button type="button" onClick={() => sendDecision("approve")}>Approve</button>
        <button type="button" onClick={() => sendDecision("reject")}>Reject</button>
        <button type="button" onClick={() => sendDecision("request-info")}>Request Info</button>
      </div>

      {message && <p>{message}</p>}
    </section>
  );
}
