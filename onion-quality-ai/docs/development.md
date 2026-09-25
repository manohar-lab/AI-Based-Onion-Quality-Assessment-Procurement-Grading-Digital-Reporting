# Development Guide

> **STATUS: PLACEHOLDER — to be expanded**

## Prerequisites

- Python 3.11+
- Flutter 3.x+
- Docker & Docker Compose
- PostgreSQL 16 (via Docker or native)

## Backend Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Frontend Setup

```bash
cd frontend
flutter pub get
flutter run
```

## Docker Setup

```bash
docker compose up --build
```

## Running Tests

```bash
cd backend
pytest -v
```

## Future Sections

- Environment variable reference
- IDE setup (VS Code / Android Studio)
- Code style and linting
- Git branching strategy
- CI/CD pipeline
