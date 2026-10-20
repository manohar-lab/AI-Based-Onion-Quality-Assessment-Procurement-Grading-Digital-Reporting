# 🧅 AI-Based Onion Quality Assessment, Procurement Grading & Digital Reporting

> An automated, auditable system for Indian onion quality assessment, procurement grading against government specifications (AGMARK, NAFED, APMC), and digital inspection reporting.

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red.svg)](https://www.sqlalchemy.org/)
[![Alembic](https://img.shields.io/badge/Alembic-1.13-purple.svg)](https://alembic.sqlalchemy.org/)
[![Tests](https://img.shields.io/badge/Tests-24%20Passing-brightgreen.svg)](https://docs.pytest.org/)
[![Flutter](https://img.shields.io/badge/Flutter-3.x-02569B.svg)](https://flutter.dev/)

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Problem Statement](#2-problem-statement)
3. [Project Objectives](#3-project-objectives)
4. [Current Features and Implementation Status](#4-current-features-and-implementation-status)
5. [System Architecture](#5-system-architecture)
6. [Technology Stack](#6-technology-stack)
7. [Project Directory Structure](#7-project-directory-structure)
8. [Prerequisites](#8-prerequisites)
9. [Local Setup and Installation](#9-local-setup-and-installation)
10. [Environment Configuration](#10-environment-configuration)
11. [Database Setup and Migrations](#11-database-setup-and-migrations)
12. [Running the Backend](#12-running-the-backend)
13. [API Endpoints and Example Requests](#13-api-endpoints-and-example-requests)
14. [Running Backend Tests](#14-running-backend-tests)
15. [Flutter Frontend Setup and Execution](#15-flutter-frontend-setup-and-execution)
16. [Docker Setup](#16-docker-setup)
17. [Current Limitations and Unimplemented Features](#17-current-limitations-and-unimplemented-features)
18. [Development Roadmap](#18-development-roadmap)
19. [Troubleshooting](#19-troubleshooting)
20. [Contributing and License Information](#20-contributing-and-license-information)

---

## 1. Project Overview

The **AI-Based Onion Quality Assessment, Procurement Grading & Digital Reporting** project is designed to modernize and digitize the agricultural procurement and quality inspection process for onions across Indian mandis (agricultural produce markets) and procurement centres.

The platform provides:
- A **FastAPI** backend service handling procurement lot sessions, secure raw image ingestion, automated image-quality validation, and persistence with **PostgreSQL** and **SQLAlchemy**.
- A **Flutter** mobile client application providing an intuitive user interface for field inspectors.
- An extensible architecture planned to host machine learning inference pipelines (detection, segmentation, diameter estimation, and defect classification), government grading rules (AGMARK, NAFED, APMC), human-in-the-loop decision gating (Jev), and automated digital PDF quality certificates.

---

## 2. Problem Statement

Indian onion procurement and mandi grading currently rely almost exclusively on manual, visual inspections. This approach presents multiple critical challenges:

- **Subjectivity and Human Error**: Visual evaluations vary significantly between individual inspectors and procurement centres.
- **Farmer-Procurement Disputes**: Lack of standardized, objective measurement criteria leads to frequent grading disagreements and pricing disputes.
- **Absence of an Auditable Digital Trail**: Physical inspection slips and manual registries provide no verifiable photographic evidence or metric logs.
- **Rule Latency**: Static manual operations make it difficult to rapidly and consistently deploy revised government procurement guidelines (such as seasonal AGMARK, NAFED, or APMC quality specifications).

---

## 3. Project Objectives

The project aims to build an end-to-end, reproducible, and verifiable digital system with the following milestones:

1. **Session & Lot Management**: Track every procurement inspection by lot ID and assigned grading standard.
2. **Quality-Gated Image Ingestion**: Perform pre-inference image validation to reject blurry, underexposed, overexposed, or low-resolution images before they enter analysis.
3. **Computer Vision Inference** *(Planned)*:
   - Detect individual onions in produce trays or bulk view.
   - Segment boundaries for pixel-precise contour and shape analysis.
   - Calibrate and estimate physical diameter (in mm).
   - Classify surface defects (such as rot, sprouting, mechanical cuts, peeling, and mold).
4. **Government Rule-Based Grading** *(Planned)*: Apply deterministic, version-controlled rules matching official government grade specifications (AGMARK, NAFED, APMC) against AI measurements.
5. **Confidence & Evidence Gating (Jev)** *(Planned)*: Gate ambiguous or low-confidence assessments into an auditable human-in-the-loop review workflow.
6. **Digital Certification** *(Planned)*: Automatically generate tamper-evident PDF inspection certificates with embedded image evidence and detailed defect breakdowns.

---

## 4. Current Features and Implementation Status

The table below reflects the **verified state of the codebase**:

| Component / Feature | Module / Endpoint | Status | Description |
| :--- | :--- | :---: | :--- |
| **Health Check** | `GET /api/v1/health` | ✅ Implemented | Returns service status, name, and version. Operates independently of database availability. |
| **Inspection Session Creation** | `POST /api/v1/inspections` | ✅ Implemented | Initializes an inspection session for a lot ID with a specified grading profile (defaults to `AGMARK_2024_v1`). |
| **Inspection Pagination & Filter** | `GET /api/v1/inspections` | ✅ Implemented | Lists inspections ordered by `created_at` descending; supports `skip`, `limit` (1–100), and `lot_id` filtering. |
| **Inspection Detail Retrieval** | `GET /api/v1/inspections/{id}` | ✅ Implemented | Retrieves full inspection record, eagerly loading images, onion instances, grading results, and reports. |
| **Inspection Session Update** | `PATCH /api/v1/inspections/{id}` | ✅ Implemented | Updates `status` (e.g. `in_progress`, `completed`) and/or `grading_profile`. |
| **Image Upload & Storage** | `POST /api/v1/inspections/{id}/images` | ✅ Implemented | Accepts multipart JPEG/PNG uploads; enforces size limits; saves images with sanitized unique timestamps to disk. |
| **Image Quality Gates** | `app/services/image_quality_service.py` | ✅ Implemented | Evaluates image blur (Laplacian variance), underexposure, overexposure, and resolution; assigns `passed` or `recapture` with actionable feedback. |
| **Inspection Image Listing** | `GET /api/v1/inspections/{id}/images` | ✅ Implemented | Lists all images registered under an inspection with their quality evaluation metrics and reasons. |
| **Database Models & Migrations** | `app/models/` & `alembic/` | ✅ Implemented | 6 SQLAlchemy ORM models and 2 Alembic revisions (`20260925_0001`, `20260925_0002`). |
| **Test Suite & Isolation** | `backend/tests/` | ✅ Implemented | 24 passing unit/integration tests running on in-memory SQLite and isolated `tmp_path` image storage. |
| **Flutter Base Shell & Home** | `frontend/lib/` | ✅ Implemented | Dark theme application shell with Home screen; feature buttons contain informative "Not implemented yet" notifications. |
| **Onion Object Detection** | `ml/detection/` | ⏳ Planned | Placeholder directory; model inference not yet integrated. |
| **Instance Segmentation** | `ml/segmentation/` | ⏳ Planned | Placeholder directory; mask generation not yet integrated. |
| **Diameter Estimation** | `ml/diameter/` | ⏳ Planned | Placeholder directory; metric sizing not yet integrated. |
| **Defect Classification** | `ml/defects/` | ⏳ Planned | Placeholder directory; defect taxonomy classifier not yet integrated. |
| **Grading Rule Engine** | `backend/app/rules/` & `/grading` | ⏳ Planned | Grading route is a stub; rule execution logic not yet implemented. |
| **Jev Confidence Decision Gate** | `app/workflows/jev/` | ⏳ Planned | Placeholder directory; evidence gating not yet implemented. |
| **LangGraph Orchestration** | `app/workflows/langgraph/` | ⏳ Planned | Placeholder directory; workflow graphs not yet implemented. |
| **Digital PDF Reports** | `backend/app/reports/` & `/reports` | ⏳ Planned | Report generation service and route are stubs. |
| **Flutter Inspection / Camera** | `frontend/lib/features/` | ⏳ Planned | Feature directories exist with placeholder `.gitkeep.dart` files. |

---

## 5. System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       Flutter Client                        │
│             (Mobile / Field Inspector Interface)            │
└──────────────────────────────┬──────────────────────────────┘
                               │ HTTP / Multipart
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend Service                   │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐   │
│   │ /api/v1/health                                      │   │
│   │ /api/v1/inspections (CRUD, filtering, pagination)   │   │
│   │ /api/v1/inspections/{id}/images (Upload & Listing)  │   │
│   └──────────────────────────┬──────────────────────────┘   │
│                              │                              │
│     ┌────────────────────────┴────────────────────────┐     │
│     │ Image Quality Assessment Service                │     │
│     │  - Discrete Laplacian Variance (Blur Check)     │     │
│     │  - Grayscale Luminance (Under/Over-exposure)    │     │
│     │  - Resolution Boundaries (Min 480x480 px)       │     │
│     └────────────────────────┬────────────────────────┘     │
│                              │                              │
│     ┌────────────────────────┴────────────────────────┐     │
│     │ Planned Processing Pipeline                     │     │
│     │  [ML Detection] ──▶ [Segmentation & Sizing]     │     │
│     │        ──▶ [Defects] ──▶ [Grading Rules Engine]  │     │
│     │        ──▶ [Jev Gate] ──▶ [Report PDF Generator] │     │
│     └─────────────────────────────────────────────────┘     │
└───────────────────┬─────────────────────┬───────────────────┘
                    │                     │
                    ▼                     ▼
┌──────────────────────────────┐  ┌───────────────────────────┐
│     PostgreSQL Database      │  │    Local Image Storage    │
│  (Inspections, Images,       │  │ (data/raw/inspections/    │
│   Instances, Defects,        │  │  {inspection_id}/...)     │
│   Grading Results, Reports)  │  │                           │
└──────────────────────────────┘  └───────────────────────────┘
```

---

## 6. Technology Stack

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) `0.115.*`
- **ASGI Server**: [Uvicorn](https://www.uvicorn.org/) `0.30.*`
- **Validation & Settings**: [Pydantic v2](https://docs.pydantic.dev/) and `pydantic-settings` `2.*`
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/) `2.*` (asyncio mode)
- **Database Drivers**: `asyncpg` `>=0.30.0` (async PostgreSQL), `psycopg[binary]` `>=3.1.0` (Alembic sync operations), and `aiosqlite` `>=0.20.0` (in-memory test execution)
- **Database Migrations**: [Alembic](https://alembic.sqlalchemy.org/) `1.13.*`
- **Image Processing**: [Pillow](https://python-pillow.org/) `>=10.0.0` and [NumPy](https://numpy.org/) `>=1.26.0`
- **Testing**: [pytest](https://docs.pytest.org/) `8.*`, `pytest-asyncio` `0.23.*`, and [HTTPX](https://www.python-httpx.org/) `0.27.*`

### Frontend
- **Framework**: [Flutter](https://flutter.dev/) (SDK `>=3.0.0 <4.0.0`)
- **Networking**: `http` `^1.2.0`
- **State Management**: `provider` `^6.1.0`
- **Testing**: `flutter_test`

### Infrastructure
- **Containerization**: Docker & Docker Compose (configuration provided for PostgreSQL 16 Alpine and FastAPI backend)
- **Database Engine**: PostgreSQL 16

---

## 7. Project Directory Structure

```
onion-quality-ai/
├── .env.example                     # Sample configuration template
├── .gitignore                       # Git ignore rules
├── README.md                        # Root project documentation (this file)
├── docker-compose.yml               # Multi-container development environment
│
├── backend/                         # FastAPI application backend
│   ├── Dockerfile                   # Python 3.11-slim container image specification
│   ├── README.md                    # Quick-start backend guide
│   ├── requirements.txt             # Locked Python backend dependencies
│   ├── alembic.ini                  # Alembic migration configuration
│   ├── alembic/                     # Database migration scripts
│   │   ├── env.py                   # Async/sync Alembic migration runner
│   │   ├── script.py.mako           # Migration template
│   │   └── versions/                # Migration revisions
│   │       ├── 20260925_0001_initial_tables.py
│   │       └── 20260925_0002_add_quality_reasons.py
│   ├── app/                         # Application source code
│   │   ├── main.py                  # FastAPI application entry point & CORS
│   │   ├── api/
│   │   │   ├── router.py            # Aggregated /api/v1 API router
│   │   │   └── routes/              # Route controllers
│   │   │       ├── health.py        # GET /api/v1/health (Implemented)
│   │   │       ├── inspections.py   # Inspection & image ingestion routes (Implemented)
│   │   │       ├── images.py        # Direct image routes (Stub)
│   │   │       ├── grading.py       # Grading evaluation routes (Stub)
│   │   │       └── reports.py       # Report generation routes (Stub)
│   │   ├── core/                    # Core configuration and database
│   │   │   ├── config.py            # Pydantic Settings management
│   │   │   ├── database.py          # SQLAlchemy async sessionmaker & Base
│   │   │   └── logging.py           # Logging setup
│   │   ├── models/                  # SQLAlchemy ORM declarative models
│   │   │   ├── inspection.py        # Inspection entity
│   │   │   ├── image.py             # Image entity
│   │   │   ├── onion.py             # OnionInstance entity
│   │   │   ├── defect.py            # DefectObservation entity
│   │   │   ├── grading.py           # GradingResult entity
│   │   │   └── report.py            # QualityReport entity
│   │   ├── schemas/                 # Pydantic request/response schemas
│   │   │   ├── inspection.py
│   │   │   ├── image.py
│   │   │   ├── onion.py
│   │   │   ├── defect.py
│   │   │   ├── grading.py
│   │   │   └── report.py
│   │   ├── services/                # Business logic services
│   │   │   ├── inspection_service.py # Inspection queries and persistence
│   │   │   ├── image_service.py     # Safe file storage and image registration
│   │   │   ├── image_quality_service.py # Pre-inference optical & quality evaluation
│   │   │   ├── grading_service.py   # (Stub)
│   │   │   └── report_service.py    # (Stub)
│   │   ├── rules/                   # Government grading specifications (Planned)
│   │   ├── workflows/               # LangGraph and Jev confidence workflows (Planned)
│   │   └── utils/                   # General helper functions
│   └── tests/                       # Pytest test suite
│       ├── conftest.py              # In-memory SQLite fixture & storage monkeypatch
│       ├── test_health.py           # Health endpoint tests
│       ├── test_image_quality.py    # Image quality service unit tests
│       └── test_inspections.py      # Inspection CRUD & image upload tests
│
├── frontend/                        # Flutter mobile application
│   ├── pubspec.yaml                 # Flutter project dependencies
│   ├── lib/
│   │   ├── main.dart                # Flutter application entry point
│   │   ├── core/                    # Config, theme, and networking
│   │   │   ├── config/app_config.dart
│   │   │   ├── networking/api_client.dart
│   │   │   └── theme/app_theme.dart
│   │   ├── features/                # App screens and UI features
│   │   │   ├── home/home_screen.dart # Dashboard screen
│   │   │   ├── camera/              # Camera screen (Planned)
│   │   │   ├── inspection/          # Inspection wizard (Planned)
│   │   │   ├── results/             # Results display (Planned)
│   │   │   └── reports/             # Report viewer (Planned)
│   │   ├── models/                  # Frontend data models (Planned)
│   │   ├── services/                # Frontend API services (Planned)
│   │   └── widgets/                 # Reusable UI widgets (Planned)
│   └── test/
│       └── home_screen_test.dart    # Flutter widget tests for HomeScreen
│
├── ml/                              # Machine Learning modules (Planned)
│   ├── detection/                   # Object detection
│   ├── segmentation/                # Instance segmentation
│   ├── defects/                     # Defect classification
│   ├── diameter/                    # Physical sizing estimation
│   ├── preprocessing/               # Image normalization
│   ├── training/                    # Model training pipelines
│   └── evaluation/                  # Evaluation benchmarks
│
├── data/                            # Dataset storage (git-ignored)
│   ├── raw/                         # Raw uploaded produce images
│   ├── processed/                   # Preprocessed / masked images
│   ├── annotations/                 # Training annotations
│   └── samples/                     # Test datasets
│
├── models/                          # Trained model weights (.pt, .onnx) (git-ignored)
├── reports/                         # Generated inspection PDFs (git-ignored)
└── docs/                            # Architecture and design documentation
```

---

## 8. Prerequisites

Ensure your host development environment has the following installed:

- **Operating System**: Windows 10/11, Linux, or macOS.
- **Python**: Version `3.11` or higher (verified with Python 3.14).
- **PostgreSQL**: Version `16` (required for running the application outside of automated in-memory tests).
- **Flutter SDK**: Version `3.0.0` or higher (only required for running the frontend application).
- **Docker & Docker Compose**: *(Optional)* Required if running the multi-container development environment.

---

## 9. Local Setup and Installation

Follow these steps in PowerShell or Command Prompt on Windows.

### 1. Clone or Open the Repository

```powershell
# Navigate into the project folder
cd c:\Users\Mahendra\OneDrive\Desktop\AI-Based-Onion-Quality-Assessment-Procurement-Grading-Digital-Reporting\onion-quality-ai
```

### 2. Create and Activate a Python Virtual Environment

```powershell
cd backend
python -m venv .venv

# Activate on Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# Or activate on Windows (cmd.exe)
.\.venv\Scripts\activate.bat
```

> **Note for PowerShell execution policy**: If script execution is restricted, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` before activating.

### 3. Install Backend Dependencies

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 10. Environment Configuration

The backend reads configuration through Pydantic Settings from system environment variables or a local `.env` file.

Copy the provided template to initialize your configuration:

```powershell
# From the onion-quality-ai root directory:
Copy-Item .env.example .env
```

### Configuration Variables Reference

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `APP_NAME` | `onion-quality-backend` | Service name returned in health check. |
| `APP_VERSION` | `0.1.0` | Application version string. |
| `ENVIRONMENT` | `development` | Deployment environment (`development`, `production`). |
| `DEBUG` | `true` | Boolean flag enabling debug logs and OpenAPI docs. |
| `DATABASE_URL` | `postgresql+asyncpg://postgres:changeme@localhost:5432/onion_quality` | Async PostgreSQL database connection URL. |
| `MODEL_DIRECTORY` | `./models` | Directory path containing trained ML model weights. |
| `IMAGE_DIRECTORY` | `./data/raw` | Filesystem base path where uploaded produce images are saved. |
| `REPORT_DIRECTORY` | `./reports` | Filesystem path where generated PDF certificates are stored. |
| `MAX_IMAGE_SIZE_MB` | `10` | Maximum allowed image upload size in megabytes. |

---

## 11. Database Setup and Migrations

The application requires a PostgreSQL database when running live.

### 1. Create the Database

Ensure PostgreSQL is running locally, then create the target database using `psql`:

```sql
CREATE DATABASE onion_quality;
```

### 2. Apply Database Migrations with Alembic

Alembic automatically provisions tables and indexes. Run migrations from the `backend/` directory with the virtual environment activated:

```powershell
cd backend
alembic upgrade head
```

This applies two verified migrations:
1. `20260925_0001_initial_tables`: Creates the initial schema (`inspections`, `images`, `onion_instances`, `defect_observations`, `grading_results`, `quality_reports`).
2. `20260925_0002_add_quality_reasons`: Adds the `quality_reasons` JSON column to the `images` table to persist quality-gate diagnostic messages.

### Database Schema Overview

```
 ┌─────────────────────────────────────────┐
 │               inspections               │
 ├─────────────────────────────────────────┤
 │ id (PK, String 36)                      │
 │ lot_id (String 100, Indexed)            │
 │ status (String 50, Indexed)             │
 │ grading_profile (String 100)            │
 │ created_at (DateTime with TZ)           │
 │ updated_at (DateTime with TZ)           │
 └───────┬─────────────────────────────────┘
         │ 1:N
         ├─────────────────────────────────┐
         │ 1:N                             │ 1:N
         ▼                                 ▼
 ┌─────────────────────────┐     ┌─────────────────────────┐
 │         images          │     │     onion_instances     │
 ├─────────────────────────┤     ├─────────────────────────┤
 │ id (PK, String 36)      │     │ id (PK, String 36)      │
 │ inspection_id (FK)      │     │ inspection_id (FK)      │
 │ file_path (String 500)  │◀──┐ │ image_id (FK, Nullable) │
 │ image_type (String 50)  │   │ │ bounding_box (JSON)     │
 │ capture_timestamp (DT)  │   │ │ segmentation_path (Str) │
 │ quality_status (Str 50) │   │ │ detection_conf (Float)  │
 │ quality_score (Float)   │   │ └───────────┬─────────────┘
 │ quality_reasons (JSON)  │   │             │ 1:N
 └─────────────────────────┘   │             ▼
                               │ ┌─────────────────────────┐
                               │ │   defect_observations   │
                               │ ├─────────────────────────┤
                               │ │ id (PK, String 36)      │
                               │ │ onion_id (FK)           │
                               │ │ defect_type (String 100)│
                               │ │ confidence (Float)      │
                               │ │ severity (String 50)    │
                               │ │ evidence_path (Str 500) │
                               │ └─────────────────────────┘
                               │
         ┌─────────────────────┴───────────┐
         │ 1:N                             │ 1:N
         ▼                                 ▼
 ┌─────────────────────────┐     ┌─────────────────────────┐
 │     grading_results     │     │     quality_reports     │
 ├─────────────────────────┤     ├─────────────────────────┤
 │ id (PK, String 36)      │     │ id (PK, String 36)      │
 │ inspection_id (FK)      │     │ inspection_id (FK)      │
 │ profile_name (Str 100)  │     │ report_path (Str 500)   │
 │ profile_version (Str 50)│     │ created_at (DT with TZ) │
 │ status (String 50)      │     └─────────────────────────┘
 │ overall_conf (Float)    │
 │ created_at (DT with TZ) │
 └─────────────────────────┘
```

---

## 12. Running the Backend

Start the FastAPI application using Uvicorn with auto-reload:

```powershell
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Once running, access the interactive API documentation:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 13. API Endpoints and Example Requests

All domain routes are served under the `/api/v1` prefix.

### Summary of Available Endpoints

| HTTP Method | Path | Summary | Status |
| :--- | :--- | :--- | :---: |
| `GET` | `/api/v1/health` | Service health status | ✅ Implemented |
| `POST` | `/api/v1/inspections` | Create a new inspection session | ✅ Implemented |
| `GET` | `/api/v1/inspections` | List inspections with pagination & lot ID filtering | ✅ Implemented |
| `GET` | `/api/v1/inspections/{inspection_id}` | Retrieve full inspection details with relationships | ✅ Implemented |
| `PATCH` | `/api/v1/inspections/{inspection_id}` | Update inspection status or grading profile | ✅ Implemented |
| `POST` | `/api/v1/inspections/{inspection_id}/images` | Upload produce image with automated quality validation | ✅ Implemented |
| `GET` | `/api/v1/inspections/{inspection_id}/images` | List all images attached to an inspection | ✅ Implemented |

---

### Endpoint Details & Examples

#### 1. Service Health Check

```http
GET /api/v1/health
```

**Example Request:**
```bash
curl -X GET http://127.0.0.1:8000/api/v1/health
```

**Response (`200 OK`):**
```json
{
  "status": "ok",
  "service": "onion-quality-backend",
  "version": "0.1.0"
}
```

---

#### 2. Create Inspection Session

```http
POST /api/v1/inspections
Content-Type: application/json
```

**Example Request:**
```bash
curl -X POST http://127.0.0.1:8000/api/v1/inspections \
  -H "Content-Type: application/json" \
  -d '{"lot_id": "LOT-MH-2026-001", "grading_profile": "AGMARK_2024_v1"}'
```

**Response (`201 Created`):**
```json
{
  "id": "c1f7b82e-9d2a-4f3b-8210-671234abcd56",
  "lot_id": "LOT-MH-2026-001",
  "status": "pending",
  "grading_profile": "AGMARK_2024_v1",
  "created_at": "2026-09-25T17:30:00Z",
  "updated_at": "2026-09-25T17:30:00Z"
}
```

---

#### 3. List Inspections

Supports optional query parameters: `skip` (default 0), `limit` (default 50, max 100), and `lot_id`.

```http
GET /api/v1/inspections?skip=0&limit=10&lot_id=LOT-MH-2026-001
```

**Example Request:**
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/inspections?skip=0&limit=10"
```

**Response (`200 OK`):**
```json
[
  {
    "id": "c1f7b82e-9d2a-4f3b-8210-671234abcd56",
    "lot_id": "LOT-MH-2026-001",
    "status": "pending",
    "grading_profile": "AGMARK_2024_v1",
    "created_at": "2026-09-25T17:30:00Z",
    "updated_at": "2026-09-25T17:30:00Z"
  }
]
```

---

#### 4. Get Inspection Details

```http
GET /api/v1/inspections/{inspection_id}
```

**Example Request:**
```bash
curl -X GET http://127.0.0.1:8000/api/v1/inspections/c1f7b82e-9d2a-4f3b-8210-671234abcd56
```

**Response (`200 OK`):**
```json
{
  "id": "c1f7b82e-9d2a-4f3b-8210-671234abcd56",
  "lot_id": "LOT-MH-2026-001",
  "status": "pending",
  "grading_profile": "AGMARK_2024_v1",
  "created_at": "2026-09-25T17:30:00Z",
  "updated_at": "2026-09-25T17:30:00Z",
  "images": [
    {
      "id": "e2d3c4b5-a6f7-4182-9345-abcdef123456",
      "inspection_id": "c1f7b82e-9d2a-4f3b-8210-671234abcd56",
      "file_path": "data/raw/inspections/c1f7b82e-9d2a-4f3b-8210-671234abcd56/20260925_173100_f8a9e7d6c5b4_capture.jpg",
      "image_type": "top_view",
      "capture_timestamp": "2026-09-25T17:31:00Z",
      "quality_status": "passed",
      "quality_score": 0.94,
      "quality_reasons": []
    }
  ],
  "onion_instances": [],
  "grading_results": [],
  "quality_reports": []
}
```

---

#### 5. Update Inspection Session

```http
PATCH /api/v1/inspections/{inspection_id}
Content-Type: application/json
```

**Example Request:**
```bash
curl -X PATCH http://127.0.0.1:8000/api/v1/inspections/c1f7b82e-9d2a-4f3b-8210-671234abcd56 \
  -H "Content-Type: application/json" \
  -d '{"status": "in_progress", "grading_profile": "NAFED_2025_v2"}'
```

**Response (`200 OK`):**
```json
{
  "id": "c1f7b82e-9d2a-4f3b-8210-671234abcd56",
  "lot_id": "LOT-MH-2026-001",
  "status": "in_progress",
  "grading_profile": "NAFED_2025_v2",
  "created_at": "2026-09-25T17:30:00Z",
  "updated_at": "2026-09-25T17:35:00Z"
}
```

---

#### 6. Upload Inspection Image & Quality Check

```http
POST /api/v1/inspections/{inspection_id}/images
Content-Type: multipart/form-data
```

**Example Request:**
```bash
curl -X POST http://127.0.0.1:8000/api/v1/inspections/c1f7b82e-9d2a-4f3b-8210-671234abcd56/images \
  -F "file=@sample_onion.jpg;type=image/jpeg" \
  -F "image_type=top_view"
```

**Response — Quality Check Passed (`201 Created`):**
```json
{
  "id": "e2d3c4b5-a6f7-4182-9345-abcdef123456",
  "inspection_id": "c1f7b82e-9d2a-4f3b-8210-671234abcd56",
  "file_path": "data/raw/inspections/c1f7b82e-9d2a-4f3b-8210-671234abcd56/20260925_173100_f8a9e7d6c5b4_sample_onion.jpg",
  "image_type": "top_view",
  "capture_timestamp": "2026-09-25T17:31:00Z",
  "quality_status": "passed",
  "quality_score": 0.94,
  "quality_reasons": []
}
```

**Response — Quality Check Failed / Recapture Recommended (`201 Created`):**
```json
{
  "id": "e2d3c4b5-a6f7-4182-9345-abcdef123456",
  "inspection_id": "c1f7b82e-9d2a-4f3b-8210-671234abcd56",
  "file_path": "data/raw/inspections/c1f7b82e-9d2a-4f3b-8210-671234abcd56/20260925_173100_f8a9e7d6c5b4_blurry_sample.jpg",
  "image_type": "top_view",
  "capture_timestamp": "2026-09-25T17:31:00Z",
  "quality_status": "recapture",
  "quality_score": 0.28,
  "quality_reasons": [
    "Image is excessively blurry (sharpness score: 18.4, min: 60.0). Please steady the camera and recapture."
  ]
}
```

---

#### 7. List Images for Inspection

```http
GET /api/v1/inspections/{inspection_id}/images
```

**Example Request:**
```bash
curl -X GET http://127.0.0.1:8000/api/v1/inspections/c1f7b82e-9d2a-4f3b-8210-671234abcd56/images
```

**Response (`200 OK`):**
```json
[
  {
    "id": "e2d3c4b5-a6f7-4182-9345-abcdef123456",
    "inspection_id": "c1f7b82e-9d2a-4f3b-8210-671234abcd56",
    "file_path": "data/raw/inspections/c1f7b82e-9d2a-4f3b-8210-671234abcd56/20260925_173100_f8a9e7d6c5b4_sample_onion.jpg",
    "image_type": "top_view",
    "capture_timestamp": "2026-09-25T17:31:00Z",
    "quality_status": "passed",
    "quality_score": 0.94,
    "quality_reasons": []
  }
]
```

---

## 14. Running Backend Tests

The test suite runs using `pytest` and `pytest-asyncio`. It is completely self-contained and does not require an active PostgreSQL server or Docker daemon:
- **Database Isolation**: Tests execute against an in-memory SQLite database (`sqlite+aiosqlite:///:memory:`).
- **Filesystem Isolation**: The `isolate_test_image_storage` autouse fixture in `conftest.py` redirects file uploads to pytest's temporary directory (`tmp_path`), guaranteeing no test artifacts pollute the repository's `data/raw` folder.

### Executing Tests on Windows

```powershell
cd backend

# Option A: Run directly through the virtual environment binary
.\.venv\Scripts\pytest -v

# Option B: Run within activated virtual environment
pytest -v
```

### Verified Test Results

The test suite currently includes **24 passing tests** across 3 test modules:

```text
tests/test_health.py::test_health_returns_200 PASSED                     [  4%]
tests/test_health.py::test_health_response_body PASSED                   [  8%]
tests/test_image_quality.py::test_sharp_image_passes_quality_gate PASSED [ 12%]
tests/test_image_quality.py::test_blurry_image_flags_recapture PASSED    [ 16%]
tests/test_image_quality.py::test_dark_image_flags_recapture PASSED      [ 20%]
tests/test_image_quality.py::test_bright_image_flags_recapture PASSED    [ 25%]
tests/test_image_quality.py::test_low_resolution_flags_recapture PASSED  [ 29%]
tests/test_image_quality.py::test_corrupted_data_handled_gracefully PASSED [ 33%]
tests/test_inspections.py::test_create_inspection PASSED                 [ 37%]
tests/test_inspections.py::test_get_inspection_by_id PASSED              [ 41%]
tests/test_inspections.py::test_get_inspection_not_found PASSED          [ 45%]
tests/test_inspections.py::test_list_inspections PASSED                  [ 50%]
tests/test_inspections.py::test_list_inspections_filter_by_lot PASSED    [ 54%]
tests/test_inspections.py::test_upload_image_multipart_success PASSED    [ 58%]
tests/test_inspections.py::test_upload_image_png_format PASSED           [ 62%]
tests/test_inspections.py::test_upload_image_poor_quality_advises_recapture PASSED [ 66%]
tests/test_inspections.py::test_upload_image_unsupported_type PASSED     [ 70%]
tests/test_inspections.py::test_upload_image_empty_file PASSED           [ 75%]
tests/test_inspections.py::test_upload_image_to_nonexistent_inspection PASSED [ 79%]
tests/test_inspections.py::test_update_inspection_status PASSED          [ 83%]
tests/test_inspections.py::test_update_inspection_grading_profile PASSED [ 87%]
tests/test_inspections.py::test_update_inspection_single_field_preserves_other PASSED [ 91%]
tests/test_inspections.py::test_update_inspection_not_found PASSED       [ 95%]
tests/test_inspections.py::test_update_inspection_empty_and_invalid_payload PASSED [100%]

============================= 24 passed in 2.88s ==============================
```

---

## 15. Flutter Frontend Setup and Execution

The `frontend/` directory contains the Flutter client application.

### Prerequisites for Frontend
- [Flutter SDK](https://docs.flutter.dev/get-started/install) (`>=3.0.0 <4.0.0`) installed and added to your `PATH`.
- Chrome (for web debugging) or an Android / iOS simulator.

### Setup and Running the App

```powershell
cd frontend

# 1. Fetch package dependencies
flutter pub get

# 2. Run the application
flutter run
```

### Running Frontend Tests

The frontend includes widget tests verifying the `HomeScreen` UI layout and navigation buttons:

```powershell
cd frontend
flutter test
```

> **Current Implementation Note**: The Flutter client currently renders the Home screen with buttons for "Start Inspection", "View Results", and "Reports". Tapping these buttons triggers an informative "Not implemented yet" notification. Detailed camera capture and inspection wizard screens are currently in the design phase.

---

## 16. Docker Setup

A complete `docker-compose.yml` configuration is provided for spinning up PostgreSQL and the FastAPI backend in synchronized containers.

### Services Defined in `docker-compose.yml`

- **`postgres`**: Runs `postgres:16-alpine` on port `5432`, configured with a persistent Docker volume (`pgdata`) and health check (`pg_isready -U postgres`).
- **`backend`**: Builds `backend/Dockerfile` using Python 3.11-slim, connects to the `postgres` service container, and mounts `./backend`, `./data`, `./models`, and `./reports` as bind mounts for live development.

### Starting the Docker Environment

```bash
# From the onion-quality-ai root directory:
docker compose up --build
```

To stop containers and tear down volumes:
```bash
docker compose down -v
```

> **Verification Status**: The Docker configuration files are verified syntactically and architecturally in the repository. Local Docker execution requires Docker Desktop / Docker Engine to be installed and running on the host machine.

---

## 17. Current Limitations and Unimplemented Features

To provide clear expectations, the following limitations are explicitly noted:

1. **Computer Vision & Inference**:
   - Model weights (`models/`) and training scripts (`ml/`) are currently scaffolding and placeholders.
   - Real-time onion bounding-box detection, instance segmentation masks, and defect classification models are **not yet wired into the API pipeline**.
2. **Physical Diameter Estimation**:
   - Spatial calibration (e.g. using reference markers or fixed camera focal distances) is planned but **not yet implemented**.
3. **Government Grading Engine**:
   - Routes under `/api/v1/grading` are stubs returning no evaluations. The formal AGMARK/NAFED specification decision logic is in design.
4. **Jev Decision Gating**:
   - The confidence thresholding and human-in-the-loop review workflow (`app/workflows/jev/`) is planned and not yet integrated.
5. **PDF Quality Report Generation**:
   - Routes under `/api/v1/reports` are stubs. Automated PDF generation with image evidence is scheduled for a future milestone.
6. **Mobile Field Client**:
   - Camera capture, image cropping, and inspection flow screens are not yet implemented in Flutter.

---

## 18. Development Roadmap

| Phase | Milestone | Focus Area | Status |
| :---: | :--- | :--- | :---: |
| **Phase 1** | Project Foundation & Architecture | Repository skeleton, Docker setup, Flutter skeleton | ✅ Completed |
| **Phase 2** | Database & Core Inspection CRUD | SQLAlchemy models, Alembic migrations, Inspection CRUD & PATCH | ✅ Completed |
| **Phase 3** | Image Ingestion & Quality Validation | Multipart upload, storage sanitization, optical quality gates | ✅ Completed |
| **Phase 4** | ML Pipeline: Detection & Segmentation | Ultralytics/YOLO onion localization and mask segmentation | ⏳ Planned |
| **Phase 5** | ML Pipeline: Defects & Diameter | Diameter sizing calibration, multi-label surface defect model | ⏳ Planned |
| **Phase 6** | Government Grading Rule Engine | Deterministic AGMARK, NAFED, and APMC grade calculation | ⏳ Planned |
| **Phase 7** | Jev Confidence & Evidence Gate | Confidence thresholding, recapture prompting, inspector audit | ⏳ Planned |
| **Phase 8** | LangGraph Workflow Orchestration | Agentic inspection workflow orchestration | ⏳ Planned |
| **Phase 9** | Digital Quality Certificates | Automated PDF generation with embedded images & signatures | ⏳ Planned |
| **Phase 10** | Flutter Field App Complete UI | Camera capture guide, inspection wizard, offline sync | ⏳ Planned |
| **Phase 11** | End-to-End Integration Testing | Integrated pipeline validation and load testing | ⏳ Planned |
| **Phase 12** | Production Deployment & Pilot | Edge mandi deployment and procurement pilot testing | ⏳ Planned |

---

## 19. Troubleshooting

### 1. `pytest : The term 'pytest' is not recognized`
- **Cause**: Pytest is installed in the project virtual environment, but the virtual environment has not been activated, or its `Scripts` directory is not in your system `PATH`.
- **Solution**: Run using the full virtual environment path:
  ```powershell
  .\.venv\Scripts\pytest -v
  ```
  Or activate the virtual environment first:
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```

### 2. Database Connection Errors on Startup
- **Cause**: The application attempted to connect to PostgreSQL at `DATABASE_URL`, but the server is not running or credentials in `.env` are mismatched.
- **Solution**:
  - Verify PostgreSQL is running: `pg_isready` or check Windows Services (`services.msc`).
  - Check that the username, password, host, port, and database name in `.env` match your PostgreSQL installation.
  - For automated testing, unit tests run against in-memory SQLite and do not require PostgreSQL.

### 3. Image Upload Returns `400 Bad Request` or `413 Payload Too Large`
- **Supported Formats**: Only `.jpg`, `.jpeg`, and `.png` are accepted. Files like `.pdf` or `.webp` will return HTTP 400.
- **File Size**: Uploads exceeding `MAX_IMAGE_SIZE_MB` (default 10 MB) return HTTP 413. Adjust `MAX_IMAGE_SIZE_MB` in `.env` if larger images must be supported.

### 4. Image Upload Response Advises `quality_status: "recapture"`
- This is an intended feature of the Image Quality Gate service. Check `quality_reasons` in the JSON response:
  - **Blurry**: Camera was moving or out of focus (sharpness variance < 60.0).
  - **Dark / Underexposed**: Insufficient ambient lighting (mean brightness < 40.0/255).
  - **Overexposed / Washed out**: Excessive flash or direct sunlight glare (mean brightness > 225.0/255).
  - **Low Resolution**: Image dimensions smaller than 480x480 pixels.

---

## 20. Contributing and License Information

### Contributing
Contributions to the project should adhere to the following principles:
1. Ensure all new endpoints include Pydantic schemas and are documented under `/api/v1`.
2. Maintain complete test isolation: tests must not depend on external databases or create uncleaned filesystem artifacts.
3. Keep ML models decoupled from core CRUD APIs via modular service interfaces.
4. Run `pytest -v` before committing any backend changes.

### License
This project's license is currently **Proprietary / Under Evaluation** pending pilot deployment agreements with procurement agencies. All rights reserved.
