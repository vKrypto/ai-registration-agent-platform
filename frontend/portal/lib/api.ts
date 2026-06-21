const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export async function createApplication(payload: {
  registration_type: string;
  full_name: string;
  email: string;
  phone: string;
}) {
  const response = await fetch(`${API_BASE_URL}/api/v1/applications`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error("Failed to create application");
  }

  return response.json();
}

export async function getApplicationStatus(applicationId: string) {
  const response = await fetch(`${API_BASE_URL}/api/v1/applications/${applicationId}/status`);

  if (!response.ok) {
    throw new Error("Failed to fetch application status");
  }

  return response.json();
}

export async function getReviewQueue() {
  const response = await fetch(`${API_BASE_URL}/api/v1/reviewer/queue`);

  if (!response.ok) {
    throw new Error("Failed to fetch review queue");
  }

  return response.json();
}
