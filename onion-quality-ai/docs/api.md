# API Documentation

> **Onion Quality Assessment & Procurement Grading API**

## Base URL

```
http://localhost:8000/api/v1
```

Interactive documentation:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

---

## Endpoints Summary

| Method | Path | Description | Status |
| :--- | :--- | :--- | :--- |
| `GET` | `/health` | Service health status | ✅ Implemented |
| `POST` | `/inspections` | Initialize new inspection session | ✅ Implemented |
| `GET` | `/inspections` | List inspections with pagination & filters | ✅ Implemented |
| `GET` | `/inspections/{inspection_id}` | Get inspection detail with all related entities | ✅ Implemented |
| `POST` | `/inspections/{inspection_id}/images` | Upload produce image with automated quality validation | ✅ Implemented |
| `GET` | `/inspections/{inspection_id}/images` | List images attached to an inspection | ✅ Implemented |
| `POST` | `/grading/evaluate` | Evaluate inspection against grading rules | ⏳ Next Phase |
| `POST` | `/reports/generate` | Generate PDF / digital report | ⏳ Next Phase |

---

## Detailed Endpoint Specifications

### 1. Health Check

```http
GET /api/v1/health
```

#### Response (200 OK)
```json
{
  "status": "ok",
  "service": "onion-quality-backend",
  "version": "0.1.0"
}
```

---

### 2. Create Inspection

```http
POST /api/v1/inspections
```

#### Request Body (JSON)
```json
{
  "lot_id": "LOT-MH-2026-001",
  "grading_profile": "AGMARK_2024_v1"
}
```

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `lot_id` | string | Yes | Unique identifier of the procurement lot/batch. |
| `grading_profile` | string | No (default: `"AGMARK_2024_v1"`) | Versioned Government or APMC grading specification to apply. |

#### Response (201 Created)
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

### 3. List Inspections

```http
GET /api/v1/inspections?skip=0&limit=50&lot_id=LOT-MH-2026-001
```

#### Query Parameters
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `skip` | integer | `0` | Number of items to skip for pagination (≥ 0). |
| `limit` | integer | `50` | Maximum items to return (1 - 100). |
| `lot_id` | string | `null` | Optional filter by exact lot identifier. |

#### Response (200 OK)
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

### 4. Get Inspection Details

```http
GET /api/v1/inspections/{inspection_id}
```

Retrieves full inspection state including attached images with quality assessments, detected onion instances, defect observations, grading outcomes, and generated quality reports.

#### Response (200 OK)
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
      "id": "f8a9e7d6-c5b4-4a39-9210-123456789abc",
      "inspection_id": "c1f7b82e-9d2a-4f3b-8210-671234abcd56",
      "file_path": "/data/raw/inspections/c1f7b82e-9d2a-4f3b-8210-671234abcd56/20260925_173005_a1b2c3d4e5f6_img_01.jpg",
      "image_type": "top_view",
      "capture_timestamp": "2026-09-25T17:30:05Z",
      "quality_status": "passed",
      "quality_score": 0.95,
      "quality_reasons": []
    }
  ],
  "onion_instances": [],
  "grading_results": [],
  "quality_reports": []
}
```

#### Response (404 Not Found)
```json
{
  "detail": "Inspection 'invalid-id' not found"
}
```

---

### 5. Upload Image & Quality Validation

```http
POST /api/v1/inspections/{inspection_id}/images
Content-Type: multipart/form-data
```

Uploads a produce image from a camera or mobile capture. The backend executes the following pipeline:
1. **Type Validation**: Accepts only `JPEG`, `JPG`, and `PNG` formats.
2. **Size Validation**: Rejects files exceeding `MAX_IMAGE_SIZE_MB` (default 10 MB).
3. **Safe Storage**: Generates a collision-resistant, sanitized unique filename and stores the raw file in `data/raw/inspections/{inspection_id}/`.
4. **Quality Gates**: Computes optical and structural quality metrics:
   - **Blur detection**: Discrete Laplacian variance (minimum sharpness score: 60.0).
   - **Darkness check**: Mean grayscale pixel luminance (minimum threshold: 40.0/255).
   - **Brightness check**: Mean grayscale pixel luminance (maximum threshold: 225.0/255).
   - **Resolution check**: Minimum resolution of 480x480 pixels.
5. **Metadata Persistence**: Records image metadata, quality score, and feedback in PostgreSQL.

#### Request Parameters (multipart/form-data)
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `file` | file | Yes | Image binary (`image/jpeg` or `image/png`). |
| `image_type` | string | No (default: `"capture"`) | Capture angle or setting (`top_view`, `tray`, `single`). |

#### Response — Quality Check Passed (201 Created)
```json
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
```

#### Response — Quality Check Failed / Recapture Recommended (201 Created)
```json
{
  "id": "e2d3c4b5-a6f7-4182-9345-abcdef123456",
  "inspection_id": "c1f7b82e-9d2a-4f3b-8210-671234abcd56",
  "file_path": "data/raw/inspections/c1f7b82e-9d2a-4f3b-8210-671234abcd56/20260925_173100_f8a9e7d6c5b4_capture.jpg",
  "image_type": "top_view",
  "capture_timestamp": "2026-09-25T17:31:00Z",
  "quality_status": "recapture",
  "quality_score": 0.32,
  "quality_reasons": [
    "Image is excessively blurry (sharpness score: 18.4, min: 60.0). Please steady the camera and recapture.",
    "Image is extremely dark / underexposed (brightness: 22.1/255). Please ensure adequate lighting and recapture."
  ]
}
```

#### Error Responses
- **400 Bad Request**: Unsupported file type or empty file.
  ```json
  {"detail": "Unsupported file type '.pdf'. Supported formats: JPEG, JPG, PNG."}
  ```
- **413 Payload Too Large**: File size exceeds maximum limit.
  ```json
  {"detail": "File size (14.2 MB) exceeds maximum allowed limit of 10 MB."}
  ```
- **404 Not Found**: Inspection session does not exist.
  ```json
  {"detail": "Inspection 'invalid-id' not found"}
  ```

---

### 6. List Images for Inspection

```http
GET /api/v1/inspections/{inspection_id}/images
```

#### Response (200 OK)
```json
[
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
]
```
