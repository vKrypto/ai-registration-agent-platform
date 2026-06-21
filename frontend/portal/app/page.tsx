export default function HomePage() {
  return (
    <section>
      <div className="hero">
        <h1>AI Registration Portal</h1>
        <p className="muted">
          Create applications, upload documents, check status, and review submitted registrations.
        </p>
        <a className="button" href="/register">Start Registration</a>
      </div>

      <div className="grid">
        <div className="card">
          <h2>User Registration</h2>
          <p className="muted">Create a new application and follow the document checklist.</p>
        </div>
        <div className="card">
          <h2>Document Upload</h2>
          <p className="muted">Submit PAN, Aadhaar, and bank letter documents.</p>
        </div>
        <div className="card">
          <h2>Reviewer Dashboard</h2>
          <p className="muted">Review applications that need manual action.</p>
        </div>
      </div>
    </section>
  );
}
