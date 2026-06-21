"use client";

import { useEffect, useState } from "react";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";
const DOCUMENT_TYPES = ["PAN", "AADHAAR", "BANK_LETTER"];

export default function UploadPage() {
  const [applicationId, setApplicationId] = useState("");
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    setApplicationId(params.get("applicationId") ?? "");
  }, []);

  async function handleUpload(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setMessage(null);

    const form = new FormData(event.currentTarget);
    const documentType = String(form.get("document_type"));
    const file = form.get("file");

    const uploadPayload = new FormData();
    uploadPayload.append("document_type", documentType);
    if (file instanceof File) {
      uploadPayload.append("file", file);
    }

    const response = await fetch(`${API_BASE_URL}/api/v1/applications/${applicationId}/documents`, {
      method: "POST",
      body: uploadPayload,
    });

    setMessage(response.ok ? `${documentType} uploaded successfully.` : "Upload failed.");
  }

  async function processApplication() {
    const response = await fetch(`${API_BASE_URL}/api/v1/applications/${applicationId}/process`, {
      method: "POST",
    });
    const result = await response.json();
    setMessage(`Processing completed. Status: ${result.status}`);
  }

  return (
    <section className="card">
      <h1>Upload Documents</h1>
      <p className="muted">Upload the required documents for the application.</p>

      <div className="form">
        <input
          value={applicationId}
          onChange={(event) => setApplicationId(event.target.value)}
          placeholder="Application ID"
        />
      </div>

      <div className="grid">
        {DOCUMENT_TYPES.map((documentType) => (
          <form className="card" onSubmit={handleUpload} key={documentType}>
            <h2>{documentType}</h2>
            <input type="hidden" name="document_type" value={documentType} />
            <input name="file" type="file" accept=".pdf,.jpg,.jpeg,.png" required />
            <button type="submit">Upload {documentType}</button>
          </form>
        ))}
      </div>

      <button type="button" onClick={processApplication}>Process Application</button>
      {message && <p>{message}</p>}
    </section>
  );
}
