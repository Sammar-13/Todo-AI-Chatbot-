# Hackathon Todo Frontend

This is the Next.js frontend for the Todo AI Chatbot application.

## Vercel Deployment Note

**Important:** When deploying this repository to Vercel, you **MUST** set the **Root Directory** to `frontend` in your Vercel Project Settings -> General. 

Otherwise, the build will fail because it cannot find the `app` or `pages` directory (since they are inside `frontend/src/app`).

## Setup

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Run locally:
   ```bash
   npm run dev
   ```

3. Environment Variables (Vercel):
   - No sensitive vars needed for frontend (API calls are proxied or use public endpoints).
   - Ensure `next.config.js` points to the correct backend URL.