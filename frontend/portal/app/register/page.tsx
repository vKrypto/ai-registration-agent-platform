"use client";

import { useState } from "react";
import { createApplication } from "../../lib/api";

export default function RegisterPage() {
  const [applicationId, setApplicationId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);

    const form = new FormData(event.currentTarget);

    try {
      const result = await createApplication({
        registration_type: "individual",
        full_name: String(form.get("full_name")),
        email: String(form.get("email")),
        phone: String(form.get("phone")),
      });
      setApplicationId(result.application_id);
    } catch {
      setError("Could not create application.");
    }
  }

  return (
    <section className="card">
      <h1>Create Registration Application</h1>
      <p className="muted">Enter basic details to start the registration flow.</p>

      <form className="form" onSubmit={handleSubmit}>
        <input name="full_name" placeholder="Full name" required />
        <input name="email" placeholder="Email" type="email" required />
        <input name="phone" placeholder="Phone" required />
        <button type="submit">Create Application</button>
      </form>

      {applicationId && (
        <div className="card">
          <h2>Application Created</h2>
          <p>Application ID: {applicationId}</p>
          <a className="button" href={`/upload?applicationId=${applicationId}`}>Upload Documents</a>
        </div>
      )}

      {error && <p>{error}</p>}
    </section>
  );
}
