[README-2.md](https://github.com/user-attachments/files/32912867/README-2.md)
# AI GitHub Repository Engineer

A FastAPI service with a web dashboard that clones a public GitHub repository, analyzes it, and shows the results. Every analysis is saved to a database so you can look back at past runs.

## Features

- **Repository analysis**: current branch, commit count, project structure and language detection (by file extension)
- **Git history**: commits, branches, contributors and the latest commit
- **Testing**: detects test files and reports test status
- **CI/CD**: detects CI configuration and workflows
- **Dependencies**: dependency analysis through a dedicated agent
- **Health score**: a 0-100 score derived from tests, CI/CD and security findings
- **Persistence**: every report is stored in SQLite (or PostgreSQL) and can be listed, fetched or deleted through the API
- **Interactive dashboard**: dark/light theme, animated stats, language bar, commit timeline with filter, collapsible project tree, and recent-repo shortcuts

## Tech stack

- Python 3.10+
- FastAPI and Uvicorn
- GitPython (repository cloning)
- SQLAlchemy 2.x (SQLite by default, PostgreSQL optional)
- Jinja2 templates with plain HTML, CSS and JavaScript on the frontend

## Project structure

```
.
├── app/
│   ├── main.py                 # FastAPI app, static files, routers, table creation
│   ├── dashboard_route.py      # GET /dashboard
│   ├── database.py             # Engine, session, get_db dependency
│   ├── models.py               # Analysis table and save_analysis()
│   ├── api/
│   │   └── repositories.py     # /repositories endpoints
│   ├── agents/
│   │   ├── orchestrator.py     # Runs all agents and builds the report
│   │   ├── repository_agent.py
│   │   ├── dependency_agent.py
│   │   ├── test_agent.py
│   │   ├── ci_agent.py
│   │   └── git_history_agent.py
│   ├── services/
│   │   ├── git_service.py      # Clones repositories
│   │   ├── github_service.py   # Language detection
│   │   ├── report_service.py   # Builds the report and health score
│   │   └── report_storage.py   # Saves the report to disk
│   ├── tools/                  # Low-level analysis helpers (git, structure, tests, CI, dependencies)
│   ├── templates/
│   │   └── dashboard.html
│   └── static/
│       ├── css/dashboard.css
│       └── js/dashboard.js
├── repositories/               # Cloned repositories (created at runtime)
└── analyses.db                 # SQLite database (created at runtime)
```

## Getting started

### Prerequisites

- Python 3.10 or newer
- Git installed and available on your `PATH` (GitPython uses it to clone)

### Install

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install fastapi "uvicorn[standard]" gitpython sqlalchemy jinja2
```

### Run

```bash
uvicorn app.main:app --reload --reload-dir app
```

`--reload-dir app` stops the `repositories/` folder and the database file from triggering restarts in the middle of an analysis.

Then open:

| URL | What |
|---|---|
| http://127.0.0.1:8000/dashboard | Web dashboard |
| http://127.0.0.1:8000/docs | Interactive API docs (Swagger) |
| http://127.0.0.1:8000/health | Health check |

The first start creates `analyses.db` and the `analyses` table automatically.

## Using the dashboard

1. Open `/dashboard`.
2. Paste a public repository URL, for example `https://github.com/owner/repository`.
3. Click **Analyze repository**.

Cloning can take a while for large repositories. Recently analyzed repositories show up as chips under the search box for one-click re-runs.

## API reference

### `POST /repositories/analyze`

Clones the repository, runs all analysis agents, saves the result and returns it.

```bash
curl -X POST http://127.0.0.1:8000/repositories/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com/owner/repository"}'
```

Response shape:

```json
{
  "id": 1,
  "repository_url": "https://github.com/owner/repository",
  "analysis": {
    "report_metadata": {},
    "health_summary": {},
    "repository": {},
    "code_analysis": {},
    "dependencies": {},
    "tests": {},
    "ci_cd": {},
    "security": {},
    "git_history": {}
  }
}
```

### `GET /repositories/history`

Lists saved analyses, newest first.

| Query parameter | Description |
|---|---|
| `repository_url` | Only analyses for this repository |
| `limit` | Number of rows to return (default 20, maximum 100) |

### `GET /repositories/{id}`

Returns the full saved report without re-cloning the repository.

### `DELETE /repositories/{id}`

Deletes a saved analysis.

## Health score

The score starts at 100 and loses points for:

| Condition | Penalty |
|---|---|
| No tests detected | -15 |
| Tests present but failing | -20 |
| No CI/CD detected | -15 |
| Each critical security finding | -15 |
| Each high security finding | -8 |

The score never goes below 0.

> **Note:** the security step in the orchestrator is currently a placeholder that always reports zero findings. Plug in a real scanner there to make the security part of the score meaningful.

## Configuration

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./analyses.db` | SQLAlchemy database URL |

### Using PostgreSQL

```bash
pip install psycopg2-binary
export DATABASE_URL="postgresql+psycopg2://user:password@localhost:5432/github_engineer"
```

No code changes are needed.

## Development notes

- **Static files are not cached.** `main.py` serves `/static` with `Cache-Control: no-store`, so edits to the CSS and JS show up on a normal refresh. Remove `NoCacheStaticFiles` before deploying to production.
- **Schema changes.** `create_all` only creates missing tables. If you change the model, use Alembic migrations, or delete `analyses.db` while developing.
- **Each run adds a row**, even for the same repository. That gives you history over time.
- **Previous clones are replaced.** Cloning the same repository again removes the old copy in `repositories/` first.

## Limitations

- Public repositories only; private repositories need credentials, which aren't supported yet.
- Language detection counts files by extension, not lines of code.
- Cloned repositories are kept on disk and never cleaned up automatically.
- There is no authentication or rate limiting, so don't expose the service publicly as is. Anyone who can reach it can make the server clone arbitrary URLs.

## Roadmap ideas

- Past-analyses list and per-repository health trend in the dashboard
- Real security scanning (dependency vulnerabilities, secret detection)
- Line-of-code language statistics
- Background jobs so long analyses don't block the request
- Automatic cleanup of cloned repositories
