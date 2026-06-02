# online-courses

A personal monorepo of small, **independent** projects — each one a self-contained
course follow-along or prototype. There is no shared build or dependency between
folders; open and run each project on its own.

## Projects

| Project | Stack | What it is |
| --- | --- | --- |
| [`antigravity-nicegui`](antigravity-nicegui) | Python · NiceGUI | Portfolio / demo app built with NiceGUI |
| [`udemy-deploy-ml-models-with-streamlit`](udemy-deploy-ml-models-with-streamlit) | Python · Streamlit | Udemy course: deploying ML models with Streamlit |
| [`udemy-fastapi`](udemy-fastapi) | Python · FastAPI · Alembic | Udemy course: the complete FastAPI course |
| [`youtube-ai-agents`](youtube-ai-agents) | Python | YouTube course: building AI agents (LangGraph, RAG, HITL, …) |
| [`youtube-ai-news`](youtube-ai-news) | Python | YouTube project: AI-generated news app |
| [`youtube-ai-voice-agent`](youtube-ai-voice-agent) | Python | YouTube project: AI voice agent |
| [`youtube-docker-kubernetes-basics`](youtube-docker-kubernetes-basics) | Docker · Kubernetes | YouTube course: Docker & Kubernetes fundamentals (notes + manifests) |
| [`youtube-frontend-course`](youtube-frontend-course) | HTML · CSS · JS | YouTube course: frontend fundamentals |

## Conventions

- **Each folder is independent.** `cd` into a project before running anything.
- **Python projects use [uv](https://docs.astral.sh/uv/):** `uv sync` to install
  dependencies, then `uv run <entry>` (the entry point varies per project — see
  its own README).
- **Editor config is per-project.** Open an individual project folder (or its
  `.code-workspace`) so its `.vscode/` settings and recommended extensions apply
  only there, not across the whole repo.
- Shared hygiene (OS cruft, secrets, virtualenvs, databases, `node_modules`) is
  ignored repo-wide via the root [`.gitignore`](.gitignore), and
  [`.editorconfig`](.editorconfig) keeps formatting consistent across languages.
