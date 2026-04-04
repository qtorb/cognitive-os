# Cognitive OS - Personal Cognitive Infrastructure

A system to transform decisions into structured memory, traceable analysis, and accumulated learning over time.

## Features

- 🔐 **Google OAuth 2.0 Authentication** - Secure login for multiple users
- 🧠 **Decision Framework** - Structured decision tracking with context and signals
- 🤖 **AI Analysis** - Claude-powered analysis, counterarguments, and synthesis
- 📊 **Pattern Detection** - Identify recurring biases and decision patterns
- ⏱️ **Decision Review** - Compare expected vs. real outcomes

## Project Structure

```
Cognitive OS/
├── backend/          # FastAPI backend
│   ├── main.py       # API endpoints
│   ├── models.py     # SQLAlchemy models
│   ├── auth.py       # OAuth + JWT authentication
│   ├── ai_service.py # Claude AI integration
│   ├── requirements.txt
│   ├── .env.example
│   └── cognitive_os.db
└── README.md
```

## Quick Start

### Prerequisites

- Python 3.9+
- Google OAuth credentials (from Google Cloud Console)

### Backend Setup

1. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Create `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

3. Add your credentials to `.env`:
   - `GOOGLE_CLIENT_ID` - from Google Cloud Console
   - `GOOGLE_CLIENT_SECRET` - from Google Cloud Console
   - `GOOGLE_REDIRECT_URI` - e.g., `http://localhost:3000/auth/callback`
   - `JWT_SECRET` - any random string (for dev)
   - `ANTHROPIC_API_KEY` - your Claude API key

4. Run the backend:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Documentation

### Authentication

#### 1. Get Login URL
```
GET /auth/login-url
```
Returns the Google OAuth login URL.

#### 2. Process OAuth Callback
```
POST /auth/callback
Content-Type: application/json

{
  "code": "authorization_code_from_google"
}
```
Returns JWT token to use for authenticated requests.

#### 3. Get Current User
```
GET /auth/me
Authorization: Bearer {token}
```

### Onboarding

```
POST /onboarding
Authorization: Bearer {token}
Content-Type: application/json

{
  "role": "Product Manager",
  "decision_areas": ["Product Strategy", "Team Management"],
  "decision_types": ["operational", "strategic"],
  "horizon": "quarterly",
  "known_bias": "Tend to overestimate team capacity"
}
```

### Decisions

#### Create Decision
```
POST /decisions
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Expand to new market",
  "context": "We have 3 months runway...",
  "area": "Product Strategy",
  "decision_type": "strategic",
  "options": ["Option A", "Option B"],
  "hypotheses": ["Users will adopt quickly"],
  "signals": ["User feedback from surveys"],
  "conviction": 7
}
```

#### List Decisions
```
GET /decisions
Authorization: Bearer {token}
```

#### Get Decision
```
GET /decisions/{decision_id}
Authorization: Bearer {token}
```

#### Update Decision
```
PATCH /decisions/{decision_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "status": "decided",
  "decision_taken": "Chose Option A",
  "expected_outcome": "30% growth"
}
```

### AI Analysis

#### Analyze Decision
```
POST /decisions/{decision_id}/analyze
Authorization: Bearer {token}
```
Returns AI analysis identifying gaps, biases, and risks.

#### Counterargument
```
POST /decisions/{decision_id}/counterargument
Authorization: Bearer {token}
```
Returns opposing viewpoints to challenge your thinking.

#### Pre-mortem
```
POST /decisions/{decision_id}/premortem
Authorization: Bearer {token}
```
Imagines the decision fails and identifies risks.

#### Analyze Patterns
```
GET /patterns
Authorization: Bearer {token}
```
Detects recurring biases and strengths across your decisions.

## Architecture

- **FastAPI** - Modern async web framework
- **SQLAlchemy** - ORM for database operations
- **SQLite** - Data persistence
- **Claude API** - AI-powered analysis
- **Google OAuth 2.0** - Secure authentication
- **JWT** - Stateless authentication tokens

## Development

### Database

The system uses SQLite with two main tables:
- `users` - User profiles and OAuth data
- `decisions` - Decision records with analysis

### AI Service

Claude provides:
- Decision analysis (identify gaps, biases, risks)
- Counterarguments (opposing viewpoints)
- Synthesis (integrate multiple analyses)
- Pattern detection (recurring biases)
- Decision review (compare expected vs. real outcomes)

## Deployment

### Using Cloudflare Tunnel (Recommended)

```bash
# Install cloudflare CLI
npm install -g wrangler

# Expose local backend
cloudflare tunnel run --url http://localhost:8000
```

This gives you a public HTTPS URL without opening ports.

## Contributing

This is a personal MVP. Feedback from alpha testers is valuable for understanding how users think about decision-making.

## License

MIT
