# 🧅 AI-Based Onion Quality Assessment, Procurement Grading & Digital Reporting

> **Research-grade and production-oriented** system for Indian onion quality assessment using computer vision, government-specification-aware grading, and automated digital reporting.

---

## Problem Statement

Indian onion procurement and grading is currently manual, subjective, and prone to inconsistency. Quality assessments at mandis (agricultural markets) depend on individual inspectors, lack standardized measurement tools, and produce no auditable digital trail. This leads to:

- Inconsistent grading across procurement centres
- Disputes between farmers and procurement agencies
- Lack of traceability from assessment to final grade
- No scalable mechanism for applying updated government specifications

## Project Goal

Build an AI-powered system that:

1. **Detects** individual onions in images using object detection.
2. **Segments** each onion for precise measurement.
3. **Measures** diameter and computes shape metrics.
4. **Classifies** surface defects (rot, sprouting, cuts, etc.).
5. **Applies** versioned Government grading rules (AGMARK, NAFED, APMC) to AI-derived measurements.
6. **Gates** results through a confidence/evidence system (Jev) to decide accept / recapture / human review.
7. **Generates** auditable digital reports for every inspection.

---

## Architecture Overview

```
┌─────────────┐     ┌─────────────┐     ┌────────────┐
│   Flutter    │────▶│   FastAPI    │────▶│ PostgreSQL │
│   Frontend   │◀────│   Backend   │◀────│  Database   │
└─────────────┘     └──────┬──────┘     └────────────┘
                           │
                     ┌─────▼──────┐
                     │  ML Engine  │
                     │  (Python)   │
                     └──────┬─────┘
                            │
                  ┌─────────▼─────────┐
                  │  Government Rules  │
                  │     + Jev Gate     │
                  └───────────────────┘
```

---

## Repository Structure

```
onion-quality-ai/
├── backend/                 # FastAPI backend (Python)
│   ├── app/
│   │   ├── api/             # API routes (versioned under /api/v1)
│   │   ├── core/            # Config, database, logging
│   │   ├── models/          # SQLAlchemy ORM models
│   │   ├── schemas/         # Pydantic request/response schemas
│   │   ├── services/        # Business logic layer
│   │   ├── rules/           # Government grading rule engine
│   │   ├── workflows/       # LangGraph + Jev orchestration
│   │   └── utils/           # Shared utilities
│   ├── tests/               # Backend tests (pytest)
│   ├── alembic/             # Database migrations
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                # Flutter/Dart frontend
│   ├── lib/
│   │   ├── core/            # Config, theme, networking, utils
│   │   ├── features/        # Feature modules (home, inspection, etc.)
│   │   ├── models/          # Data models
│   │   ├── services/        # API services
│   │   └── widgets/         # Shared widgets
│   ├── test/                # Widget tests
│   ├── assets/              # Images, icons
│   └── pubspec.yaml
│
├── ml/                      # Machine learning modules
│   ├── detection/           # Object detection
│   ├── segmentation/        # Instance segmentation
│   ├── defects/             # Defect classification
│   ├── diameter/            # Diameter estimation
│   ├── preprocessing/       # Image preprocessing
│   ├── training/            # Training scripts
│   ├── evaluation/          # Evaluation metrics
│   └── common/              # Shared ML utilities
│
├── data/                    # Data assets (git-ignored)
│   ├── raw/                 # Original images
│   ├── processed/           # Preprocessed images
│   ├── annotations/         # Labels and masks
│   └── samples/             # Small test samples
│
├── models/                  # Trained model weights (git-ignored)
├── reports/                 # Generated reports (git-ignored)
├── docs/                    # Project documentation
├── tests/                   # Integration / E2E tests
│
├── .env.example             # Environment variable template
├── .gitignore
├── docker-compose.yml       # Docker development setup
└── README.md                # This file
```

---

## Technology Stack

| Layer           | Technology                                    |
| --------------- | --------------------------------------------- |
| Frontend        | Flutter / Dart                                |
| Backend API     | FastAPI (Python 3.11+)                        |
| Database        | PostgreSQL 16                                 |
| ORM             | SQLAlchemy 2 (async)                          |
| Migrations      | Alembic                                       |
| Validation      | Pydantic v2                                   |
| ML Framework    | PyTorch / Ultralytics *(NOT IMPLEMENTED YET)* |
| Workflow Engine | LangGraph *(NOT IMPLEMENTED YET)*             |
| Confidence Gate | Jev *(NOT IMPLEMENTED YET)*                   |
| Containerization| Docker / Docker Compose                       |
| Testing         | pytest, Flutter test                          |

---

## Development Roadmap

| Phase | Milestone                              | Status              |
| ----- | -------------------------------------- | ------------------- |
| 1     | Project foundation & skeleton          | ✅ Done             |
| 2     | Database models & CRUD API             | ✅ Done             |
| 3     | Image upload & storage                 | ❌ Not yet          |
| 4     | ML pipeline — detection & segmentation | ❌ Not yet          |
| 5     | ML pipeline — defects & diameter       | ❌ Not yet          |
| 6     | Government grading rule engine         | ❌ Not yet          |
| 7     | Jev confidence gate                    | ❌ Not yet          |
| 8     | LangGraph workflow orchestration       | ❌ Not yet          |
| 9     | Report generation                      | ❌ Not yet          |
| 10    | Flutter feature screens                | ❌ Not yet          |
| 11    | Integration testing                    | ❌ Not yet          |
| 12    | Deployment & documentation             | ❌ Not yet          |

---

## Getting Started

### 1. Start PostgreSQL & Backend (Docker)

```bash
cd onion-quality-ai

# Copy environment template
cp .env.example .env

# Start services
docker compose up --build
```

The backend will be available at **http://localhost:8000**.

- Health check: http://localhost:8000/api/v1/health
- Swagger docs: http://localhost:8000/docs

### 2. Start Backend (without Docker)

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux/macOS
pip install -r requirements.txt

# Make sure PostgreSQL is running and DATABASE_URL is set
uvicorn app.main:app --reload --port 8000
```

### 3. Run Backend Tests

```bash
cd backend
pytest -v
```

### 4. Start Flutter Frontend

```bash
cd frontend
flutter pub get
flutter run
```

### 5. Run Flutter Tests

```bash
cd frontend
flutter test
```

---

## License

*(To be determined)*
