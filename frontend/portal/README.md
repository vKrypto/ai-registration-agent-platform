# Frontend Portal

Next.js portal for the AI Registration Agent Platform.

## Current Pages

- `/` landing page
- `/register` create application
- `/upload` upload required documents
- `/status` check application status
- `/reviewer` reviewer queue
- `/reviewer/[applicationId]` review details and decisions

## Local Setup

```bash
cd frontend/portal
npm install
cp .env.example .env.local
npm run dev
```

The backend should be running on `http://localhost:8000` unless `NEXT_PUBLIC_API_BASE_URL` is changed.
