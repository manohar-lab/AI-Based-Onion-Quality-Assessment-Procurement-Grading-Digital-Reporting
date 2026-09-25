# Architecture

> **STATUS: PLACEHOLDER — to be expanded**

## High-Level Overview

```
┌─────────────┐     ┌────────────┐     ┌────────────┐
│   Flutter    │────▶│  FastAPI    │────▶│ PostgreSQL │
│   Frontend   │◀────│  Backend   │◀────│  Database   │
└─────────────┘     └─────┬──────┘     └────────────┘
                          │
                    ┌─────▼──────┐
                    │  ML Engine  │
                    │ (Python)    │
                    └─────┬──────┘
                          │
                ┌─────────▼─────────┐
                │ Government Rules  │
                │    + Jev Gate     │
                └───────────────────┘
```

## Key Decisions

- **Flutter** for cross-platform mobile + web frontend.
- **FastAPI** (async Python) for backend API and ML orchestration.
- **PostgreSQL** for persistent storage of inspections, grades, and audit logs.
- **LangGraph** for workflow orchestration (pipeline graph).
- **Government rules** are decoupled from ML models and versioned independently.
- **Jev** acts as a confidence gate, not a rule engine.

## Future Sections

- Component interaction diagrams
- Data flow diagrams
- Deployment architecture (cloud / on-premise)
- Security model
