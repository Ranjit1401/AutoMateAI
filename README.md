# AutoMateAI

A multi-agent AI travel assistant: FastAPI + LangGraph backend, Next.js frontend, real Gmail/Calendar/Drive/Sheets, Twilio, and Vapi integrations.

This is a rebuild of the original prototype, addressing everything found in
the technical audit: authentication, persistence, duplicate/dead code,
broken frontend<->backend wiring, and five new specialized agents.
Deployment (Docker/CI) was explicitly out of scope for this pass —
everything else was.

## What changed from the audit

- **Auth**: JWT sessions in an httpOnly cookie. Signup/login/logout/me.
- **Database**: SQLite by default (zero setup), swappable to Postgres via
  `DATABASE_URL` — same SQLAlchemy models, no code changes. Alembic
  migrations included (`backend/alembic/`).
- **Persistence**: conversations, messages, long-term memory, tasks, and
  logs all live in the DB now — nothing is in-process RAM anymore.
- **Dead code removed**: the duplicate `agents/nodes.py` + `agents/workflow.py`
  (unreachable, superseded by `graph/*`), duplicate tool base classes and
  registries, duplicate config systems, the unused `master_agent.py` stub.
- **New agents**: Restaurant, Maps, Budget, Itinerary, Booking, Memory —
  each backed by a real tool (Google Places, Google Directions, live
  currency rates, PDF generation) rather than a placeholder.
- **Fixed bugs**: Research Agent no longer returns hardcoded Goa data for
  every destination; Twilio webhook signature validation is actually
  enabled (was commented out); Google OAuth tokens are now per-user in the
  DB instead of a process-RAM dict that leaked across users; CORS no longer
  combines `allow_origins=["*"]` with credentials; `GoogleConnect.tsx`'s
  broken `/google/login` path is fixed to the real `/google/auth` route.
- **Frontend**: all 7 pages (chat, tasks, apps, memory, logs, settings, plus
  new login/signup) are wired to real backend endpoints — no more empty
  static arrays. Chat streams live pipeline progress via SSE. Visual design
  (Aurora background, glass cards, Nav) is unchanged.
- **Tests**: the old 15 ad-hoc `test_*.py` scratch scripts are replaced with
  a real pytest suite (`backend/tests/`, 18 tests, all passing).

## Honest scope notes

- **Booking**: there's no universal public API to actually purchase a
  flight/hotel without a commercial partnership (Amadeus, Booking.com
  Partner Hub, a payment processor). The Booking agent creates a real,
  persisted *provisional reservation* record — it does not charge a card
  or issue a ticket. See `backend/app/tools/booking_tool.py`.
- **n8n**: there's no way to "integrate" with an automation tool without
  your instance URL. `webhook_trigger` is a generic, working POST-to-webhook
  tool that's n8n-compatible (also works with Zapier/Make) — set
  `N8N_WEBHOOK_URL` to use it.
- **Maps/Restaurant/PDF**: these use real APIs (Google Maps Platform,
  reportlab) — you need to supply your own `GOOGLE_MAPS_API_KEY` etc. See
  `backend/.env.example`.

## Setup

### Backend
```bash
cd backend
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # fill in GROQ_API_KEY at minimum
alembic upgrade head    # optional -- the app also auto-creates tables on startup
uvicorn app.main:app --reload
```
Runs at `http://localhost:8000`. Interactive API docs at `/docs`.

Run tests: `pytest` (from `backend/`, with the venv active).

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Runs at `http://localhost:3000`.

### Minimum to try it
Only `GROQ_API_KEY` (free tier at console.groq.com) is required to sign up,
log in, and chat. Weather/flights/hotels/maps/restaurants degrade
gracefully with a clear error message if their respective API keys aren't
set -- the rest of the app keeps working.
