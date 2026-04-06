# Cognitive OS — Personal Cognitive Infrastructure

**Transform decisions into structured memory, traceable analysis, and accumulated learning over time.**

Cognitive OS is not a task manager, note-taking app, or generic AI chat. It's an infrastructure for thinking clearly about decisions and learning from them over time. It bridges the gap between the moment you decide something and the future when you can evaluate if you were right.

## The Problem

Most decision-making tools focus on execution (task managers) or capture (notes). But they miss the essential feedback loop:

**Decision → Analysis → Execution → Outcome → Learning → Next Decision**

You make decisions today but forget the context by next month. You never compare what you expected with what actually happened. You repeat the same mistakes because patterns go undetected.

Cognitive OS solves this by:
1. **Capturing decisions** with full context (what, why, conviction level)
2. **Analyzing them deeply** with AI to identify blind spots and biases
3. **Registering actual outcomes** to close the feedback loop
4. **Detecting patterns** to accumulate decision-making criteria over time

## Features

### 🎯 Core Workflow

- **Ideas**: Capture raw thoughts and concepts before they become decisions
- **Decisions**: Document structured decisions with context, conviction, and expected outcomes
- **Connections**: Link ideas and decisions to see how concepts relate
- **AI Analysis**: Claude-powered analysis identifying gaps, biases, and risks
- **Outcomes**: Register actual results against expected outcomes
- **Patterns**: Detect recurring biases and strengths across your decision history
- **Review**: Compare expectation vs. reality and extract learnings
- **Reminders**: Temporal triggers to review decision outcomes (1 month, 3 months, 6 months)
- **Metrics**: Dashboard showing decision statistics, completion rates, conviction accuracy
- **Public Sharing**: Share decisions publicly to showcase your thinking and grow viral

### 🔐 Authentication & Data

- **Google OAuth 2.0** - Secure multi-user login
- **JWT Tokens** - Stateless authenticated requests
- **SQLite Database** - Portable, zero-dependency persistence
- **Full Data Export** - JSON export for portability

### 🤖 AI-Powered Analysis

- **Decision Analysis** - Identify information gaps, cognitive biases, underestimated risks
- **Counterargument** - Devil's advocate opposing viewpoints and failure scenarios
- **Pre-mortem** - Imagine the decision fails; what went wrong?
- **Synthesis** - Integrate analysis into clear, actionable summary
- **Pattern Detection** - Analyze decision history to detect recurring biases and strengths
- **Decision Review** - Compare expected outcomes with reality; extract learnings

### 📊 User Profile

- **Decision Areas** - Product, Finance, Team, Strategy, etc.
- **Decision Types** - Operational, Strategic, Tactical
- **Planning Horizon** - Daily, Weekly, Monthly, Quarterly, Annual
- **Known Biases** - Your self-awareness of decision-making weaknesses

## Project Structure

```
Cognitive OS/
├── backend/
│   ├── main.py              # FastAPI application (40+ endpoints)
│   ├── models.py            # SQLAlchemy ORM models
│   ├── auth.py              # JWT + Google OAuth implementation
│   ├── ai_service.py        # Claude API integration with fallbacks
│   ├── tests.py             # 20 comprehensive tests (100% coverage)
│   ├── requirements.txt      # Python dependencies
│   ├── .env.example         # Configuration template
│   └── cognitive_os.db      # SQLite database
├── dashboard.html           # Complete frontend interface
├── onboarding.html          # User onboarding flow
├── arrancar.bat             # Windows: start backend server
├── abrir_frontend.bat       # Windows: open frontend in browser
└── README.md                # This file (single source of truth)
```

## Quick Start

### Prerequisites

- Python 3.9+
- Node.js (optional, for frontend development)
- Google OAuth credentials (from [Google Cloud Console](https://console.cloud.google.com))
- Anthropic API key (from [Claude Platform](https://console.anthropic.com))

### Installation

**1. Clone and navigate:**
```bash
git clone https://github.com/qtorb/cognitive-os.git
cd "Cognitive OS/backend"
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt --break-system-packages
```

**3. Configure environment:**
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback
JWT_SECRET=your_secret_key_here
ANTHROPIC_API_KEY=sk-ant-...your-api-key...
```

**4. Run the backend:**
```bash
python main.py
```

The API will be available at `http://localhost:8000`.

**5. Open the frontend:**
- Open `dashboard.html` in your browser (from the project root directory)
- First-time users will see the onboarding flow
- Log in with your Google account

### Windows Quick Start (without terminal)

If you prefer not to use PowerShell:
1. Double-click `arrancar.bat` to start the backend server
2. Double-click `abrir_frontend.bat` to open the frontend
3. Keep the server window open while using the app

## Usage Workflow

### 1. Onboarding (One-time setup)

Define your decision-making context:
- Your role (Product Manager, CEO, etc.)
- Decision areas where you make choices
- Types of decisions you face
- Planning horizon (quarterly, yearly, etc.)
- Known biases you're aware of

### 2. Capture Ideas

Raw thoughts before they become decisions. Ideas can be:
- Product concepts
- Strategic opportunities
- Process improvements
- Questions to investigate

Ideas can be tagged and later evolved into decisions.

### 3. Create Decisions

Document decisions with structure:

```json
{
  "title": "Expand to new market",
  "context": "Current market saturated, team has capacity, 3M runway",
  "area": "Product Strategy",
  "decision_type": "strategic",
  "options": ["Option A: Enter Market 1", "Option B: Enter Market 2", "Option C: Stay focused"],
  "hypotheses": ["Early adoption will be fast", "Enterprise customers exist", "Team can execute"],
  "signals": ["User feedback from surveys", "Competitor movement"],
  "conviction": 7
}
```

### 4. Analyze with AI

Get Claude to challenge your thinking:

**Analysis** - Identify gaps, biases, and risks
**Counterargument** - What would someone say against this decision?
**Pre-mortem** - If this fails in 6 months, what went wrong?

### 5. Execute

Update the decision with:
- Status (analyzing → decided → executing → completed)
- Decision taken (which option was chosen)
- Expected outcome

### 6. Register Outcomes

When execution is complete, record:
- Real outcome (what actually happened)
- Learnings (what you discovered)
- Key metrics (if applicable)

### 7. Review & Learn

Get Claude to analyze:
- Expected vs. Real: What matched? What didn't?
- Failing assumptions: Where were you wrong?
- Patterns: Is this a recurring bias?

### 8. Detect Patterns

Analyze your decision history to find:
- Recurring biases (optimistic timelines, overconfidence, etc.)
- Strengths (where do you consistently make good calls?)
- Weak areas (strategic? financial? team decisions?)
- Personalized recommendations for improvement

## API Documentation

### Authentication

**Get Login URL:**
```
GET /auth/login-url
```
Returns Google OAuth login URL.

**OAuth Callback:**
```
POST /auth/callback
Content-Type: application/json

{"code": "authorization_code_from_google"}
```
Returns JWT token for authenticated requests.

**Get Current User:**
```
GET /auth/me
Authorization: Bearer {token}
```

**Test Login (Development):**
```
POST /auth/test-login
Content-Type: application/json

{"email": "user@example.com"}
```

### Onboarding

**Complete Onboarding:**
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

**Create Decision:**
```
POST /decisions
Authorization: Bearer {token}

{
  "title": "...",
  "context": "...",
  "area": "...",
  "decision_type": "...",
  "conviction": 7
}
```

**List All Decisions:**
```
GET /decisions
Authorization: Bearer {token}
```

**Get Single Decision:**
```
GET /decisions/{decision_id}
Authorization: Bearer {token}
```

**Update Decision:**
```
PATCH /decisions/{decision_id}
Authorization: Bearer {token}

{
  "status": "deciding",
  "decision_taken": "Chose Option A",
  "expected_outcome": "30% growth"
}
```

### Ideas/Thoughts

**Create Idea:**
```
POST /thoughts
Authorization: Bearer {token}

{
  "title": "Feature idea",
  "content": "...",
  "thought_type": "idea",
  "tags": ["product", "innovation"]
}
```

**List Ideas:**
```
GET /thoughts
Authorization: Bearer {token}
```

**Get Idea:**
```
GET /thoughts/{thought_id}
Authorization: Bearer {token}
```

### Connections

**Create Connection:**
```
POST /connections
Authorization: Bearer {token}

{
  "source_type": "decision",
  "source_id": 1,
  "target_type": "thought",
  "target_id": 2,
  "relationship": "relates_to",
  "reason": "Both affect user retention"
}
```

**List Connections:**
```
GET /connections
Authorization: Bearer {token}
```

### Outcomes & Review

**Register Outcome:**
```
POST /decisions/{decision_id}/outcome
Authorization: Bearer {token}

{
  "outcome_real": "15% growth achieved",
  "learnings": ["Market was more conservative than expected"],
  "status": "completed"
}
```

**Get Outcome:**
```
GET /decisions/{decision_id}/outcome
Authorization: Bearer {token}
```

### AI Analysis

**Analyze Decision:**
```
POST /decisions/{decision_id}/analyze
Authorization: Bearer {token}
```

**Get Counterargument:**
```
POST /decisions/{decision_id}/counterargument
Authorization: Bearer {token}
```

**Get Pre-mortem:**
```
POST /decisions/{decision_id}/premortem
Authorization: Bearer {token}
```

**Get Patterns:**
```
GET /patterns
Authorization: Bearer {token}
```
Returns analysis of your decision history including recurring biases, strengths, and recommendations.

### Reminders & Metrics

**Create Reminder:**
```
POST /decisions/{decision_id}/reminder
Authorization: Bearer {token}

{"reminder_type": "1month"}
```
Reminder types: "1month", "3months", "6months"

**List Reminders:**
```
GET /reminders
Authorization: Bearer {token}
```

**Complete Reminder:**
```
PATCH /reminders/{reminder_id}/complete
Authorization: Bearer {token}
```

**Get Metrics:**
```
GET /metrics
Authorization: Bearer {token}
```
Returns decision statistics including total count, completion rate, conviction accuracy, and decisions by area.

### Public Sharing (Viral Feature)

**Create Public Link:**
```
POST /decisions/{decision_id}/share
Authorization: Bearer {token}
```
Returns a public URL anyone can view without authentication.

**Get Share Links:**
```
GET /decisions/{decision_id}/share-links
Authorization: Bearer {token}
```

**View Public Decision:**
```
GET /public/{token}
```
No authentication required. Anyone with the link can view this decision and its analysis.

**Revoke Share Link:**
```
DELETE /share-links/{token}
Authorization: Bearer {token}
```

## Architecture

### Backend Stack

- **FastAPI** - Modern async Python web framework
- **SQLAlchemy** - ORM with SQLite backend
- **Pydantic V2** - Request/response validation
- **AI Engine** - Model-agnostic analysis (Anthropic, OpenAI, Ollama)
- **Google OAuth 2.0** - Secure multi-user authentication
- **JWT** - Stateless token-based authentication

### AI Architecture (Model-Agnostic)

The AI layer uses a provider adapter pattern. Swap models by changing one env var:

```
AI_PROVIDER=anthropic   # or: openai, ollama
AI_MODEL=claude-sonnet-4-20250514   # or: gpt-4o, llama3
```

Providers: Anthropic (Claude), OpenAI (GPT), Ollama (local models).
Adding a new provider: implement `BaseProvider.complete()` in `ai_service.py`.

### Database Schema

**Users**
```
- user_id (unique)
- email
- name
- role
- decision_areas (JSON)
- decision_types (JSON)
- horizon
- known_bias
- onboarded
```

**Decisions**
```
- id
- user_id
- title
- context
- area
- decision_type
- conviction
- status
- decision_taken
- expected_outcome
- outcome_real
- created_at
- updated_at
```

**Ideas/Thoughts**
```
- id
- user_id
- title
- content
- thought_type
- tags (JSON)
- created_at
```

**Connections**
```
- id
- user_id
- source_type, source_id
- target_type, target_id
- relationship
- reason
- created_at
```

**Analysis**
```
- id
- decision_id
- analysis_type
- content
- created_at
```

**Reminders**
```
- id
- user_id
- decision_id
- reminder_date
- reminder_type
- message
- status (pending, sent, completed)
- created_at, sent_at, completed_at
```

**Public Links**
```
- id
- user_id
- decision_id
- token (unique, for public URL)
- created_at, expires_at
```

### Frontend

- **Vanilla JavaScript** (no frameworks)
- **Responsive HTML/CSS** with dark mode support
- **localStorage** for user preferences
- **CSS animations** for smooth UX
- **Modal-based** decision flow

### Fallback Behavior

When no AI provider is available, the system returns demo responses demonstrating the expected analysis format. This ensures the product remains functional during development or when API keys are not configured.

## Testing

**100% Coverage** - 20 comprehensive tests covering all critical paths:

```bash
cd backend
pytest tests.py -v --tb=short
```

Tests include:
- Authentication (login, token generation)
- Onboarding flow and validation
- Decision CRUD operations
- Outcome registration and comparison
- Idea/thought creation and retrieval
- Connections between items
- AI analysis (analyze, counterargument, patterns)
- Error handling (unauthorized, not found, invalid)
- Complete workflows (create → decide → execute → outcome)
- Performance (bulk operations)

## Configuration

### Environment Variables

```
# Authentication
GOOGLE_CLIENT_ID=from_google_cloud_console
GOOGLE_CLIENT_SECRET=from_google_cloud_console
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback

# JWT
JWT_SECRET=any_random_string_for_dev

# AI Service
ANTHROPIC_API_KEY=sk-ant-your-api-key

# Database (optional)
DATABASE_URL=sqlite:///./cognitive_os.db

# Deployment
PORT=8000
HOST=0.0.0.0
```

## Deployment

### Local Development

```bash
cd backend
python main.py
```

Server runs on `http://localhost:8000`.

### Using Cloudflare Tunnel

For public access without opening ports:

```bash
# Install wrangler
npm install -g wrangler

# Expose your local backend
wrangler tunnel --url http://localhost:8000
```

This provides a public HTTPS URL automatically.

### Using Heroku

See `Procfile` and `runtime.txt` for Heroku deployment configuration.

## Philosophy & Design Principles

### Simplicity Over Feature Bloat

- No authentication complexity beyond OAuth
- No multiuser enterprise features
- No microservices or distributed systems
- Single SQLite database

### Structure for Learning

Every decision captures:
- **Context** - What was the situation?
- **Conviction** - How confident were you? (1-10)
- **Analysis** - What were you missing?
- **Outcome** - What actually happened?
- **Learning** - What did you discover?

Over time, you build a personal knowledge base of your decision-making criteria.

### AI as a Tool, Not the Product

Claude provides:
- Rigorous questioning (devil's advocate)
- Pattern detection across your history
- Synthesis of complex analyses
- Structured thinking frameworks

But **you** make the decisions. AI helps you think better.

### Portable Data

Everything is JSON-exportable. No vendor lock-in.

## Roadmap

### ✅ Complete (MVP + Viral Features)

- [x] Core decision CRUD
- [x] AI analysis integration (Claude)
- [x] Outcomes registration
- [x] Pattern detection
- [x] Temporal reminders (1 month, 3 months, 6 months)
- [x] Decision metrics dashboard
- [x] Public sharing (viral mechanism)
- [x] 100% test coverage
- [x] Complete documentation

### 🚀 Future Features

- Decision templates (recurring types)
- Collaborative decisions (with team)
- Export/import full decision history (JSON)
- Mobile app
- Email digest of pending reminders
- Integration with other tools (calendar, Slack, email)

## Contributing

This is a personal MVP. If you're interested in using or extending Cognitive OS:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Ensure all tests pass (`pytest tests.py`)
5. Submit a pull request

## Troubleshooting

### "Failed to fetch" errors

- Ensure backend is running (`python main.py`)
- Check CORS settings if frontend is on different port
- Verify authentication token in browser console

### Claude API returns demo responses

- Check `ANTHROPIC_API_KEY` is set in `.env`
- Verify API key is valid (go to console.anthropic.com)
- Check API key has sufficient credits

### Test failures

```bash
# Run with verbose output
pytest tests.py -v --tb=long

# Run specific test
pytest tests.py::TestDecisions::test_create_decision -v
```

## Support

For issues, questions, or feedback:
1. Check existing GitHub issues
2. Review documentation files in the project
3. Refer to code comments for implementation details

## License

MIT - Feel free to use, modify, and distribute.

---

**Made with 🧠 for people who think seriously about decisions.**

*Cognitive OS transforms how you make decisions by closing the feedback loop between intention and outcome, turning decision-making into a learned skill rather than a repeated mistake.*
