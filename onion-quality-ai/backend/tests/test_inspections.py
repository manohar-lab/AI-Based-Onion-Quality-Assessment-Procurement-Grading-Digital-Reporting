"""Tests for Inspection and Image Ingestion API endpoints."""

import io
import numpy as np
from PIL import Image as PILImage
import pytest


def _create_test_image_bytes(width: int = 600, height: int = 600, format: str = "JPEG") -> bytes:
    """Helper creating high-contrast in-memory test image bytes."""
    img = PILImage.new("RGB", (width, height), color=(220, 220, 220))
    arr = np.array(img)
    for y in range(0, height, 40):
        for x in range(0, width, 40):
            if (x // 40 + y // 40) % 2 == 0:
                arr[y : y + 40, x : x + 40] = [100, 30, 30]
    out = io.BytesIO()
    PILImage.fromarray(arr).save(out, format=format)
    return out.getvalue()


@pytest.mark.asyncio
async def test_create_inspection(async_client):
    """POST /api/v1/inspections should create an inspection with status 201."""
    payload = {
        "lot_id": "LOT-MH-2026-001",
        "grading_profile": "AGMARK_2024_v1",
    }
    response = await async_client.post("/api/v1/inspections", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["lot_id"] == "LOT-MH-2026-001"
    assert data["grading_profile"] == "AGMARK_2024_v1"
    assert data["status"] == "pending"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_get_inspection_by_id(async_client):
    """GET /api/v1/inspections/{id} should return inspection detail with related entity arrays."""
    create_resp = await async_client.post(
        "/api/v1/inspections",
        json={"lot_id": "LOT-PUN-1002", "grading_profile": "NAFED_2025_v1"},
    )
    assert create_resp.status_code == 201
    inspection_id = create_resp.json()["id"]

    get_resp = await async_client.get(f"/api/v1/inspections/{inspection_id}")
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["id"] == inspection_id
    assert data["lot_id"] == "LOT-PUN-1002"
    assert data["grading_profile"] == "NAFED_2025_v1"
    assert isinstance(data["images"], list)
    assert isinstance(data["onion_instances"], list)
    assert isinstance(data["grading_results"], list)
    assert isinstance(data["quality_reports"], list)


@pytest.mark.asyncio
async def test_get_inspection_not_found(async_client):
    """GET /api/v1/inspections/{invalid_id} should return 404."""
    response = await async_client.get("/api/v1/inspections/non-existent-id-0000")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_list_inspections(async_client):
    """GET /api/v1/inspections should return list of inspections."""
    await async_client.post("/api/v1/inspections", json={"lot_id": "LOT-A"})
    await async_client.post("/api/v1/inspections", json={"lot_id": "LOT-B"})

    response = await async_client.get("/api/v1/inspections")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    lot_ids = [item["lot_id"] for item in data]
    assert "LOT-A" in lot_ids
    assert "LOT-B" in lot_ids


@pytest.mark.asyncio
async def test_list_inspections_filter_by_lot(async_client):
    """GET /api/v1/inspections?lot_id=... should filter inspections."""
    await async_client.post("/api/v1/inspections", json={"lot_id": "TARGET-LOT"})
    await async_client.post("/api/v1/inspections", json={"lot_id": "OTHER-LOT"})

    response = await async_client.get("/api/v1/inspections?lot_id=TARGET-LOT")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["lot_id"] == "TARGET-LOT"


@pytest.mark.asyncio
async def test_upload_image_multipart_success(async_client):
    """POST /api/v1/inspections/{id}/images with multipart JPEG file should pass quality gate."""
    # 1. Create inspection
    insp_resp = await async_client.post(
        "/api/v1/inspections",
        json={"lot_id": "LOT-UPLOAD-01"},
    )
    inspection_id = insp_resp.json()["id"]

    # 2. Upload valid image
    img_bytes = _create_test_image_bytes(width=600, height=600, format="JPEG")
    files = {"file": ("onion_sample.jpg", img_bytes, "image/jpeg")}
    data = {"image_type": "top_view"}

    upload_resp = await async_client.post(
        f"/api/v1/inspections/{inspection_id}/images",
        files=files,
        data=data,
    )
    assert upload_resp.status_code == 201
    img_data = upload_resp.json()
    assert img_data["inspection_id"] == inspection_id
    assert img_data["image_type"] == "top_view"
    assert img_data["quality_status"] == "passed"
    assert img_data["quality_score"] >= 0.85
    assert isinstance(img_data["quality_reasons"], list)
    assert len(img_data["quality_reasons"]) == 0
    assert "id" in img_data
    assert "file_path" in img_data

    # 3. List images
    list_resp = await async_client.get(f"/api/v1/inspections/{inspection_id}/images")
    assert list_resp.status_code == 200
    images = list_resp.json()
    assert len(images) == 1
    assert images[0]["id"] == img_data["id"]


@pytest.mark.asyncio
async def test_upload_image_png_format(async_client):
    """POST /api/v1/inspections/{id}/images supports PNG format."""
    insp_resp = await async_client.post(
        "/api/v1/inspections",
        json={"lot_id": "LOT-PNG-01"},
    )
    inspection_id = insp_resp.json()["id"]

    img_bytes = _create_test_image_bytes(width=500, height=500, format="PNG")
    files = {"file": ("sample_onion.png", img_bytes, "image/png")}

    upload_resp = await async_client.post(
        f"/api/v1/inspections/{inspection_id}/images",
        files=files,
    )
    assert upload_resp.status_code == 201
    assert upload_resp.json()["quality_status"] == "passed"


@pytest.mark.asyncio
async def test_upload_image_poor_quality_advises_recapture(async_client):
    """Low quality image must be saved but marked 'recapture' with explicit reasons."""
    insp_resp = await async_client.post(
        "/api/v1/inspections",
        json={"lot_id": "LOT-POOR-01"},
    )
    inspection_id = insp_resp.json()["id"]

    # Low resolution dark image (200x200)
    img = PILImage.new("RGB", (200, 200), color=(10, 10, 10))
    out = io.BytesIO()
    img.save(out, format="JPEG")

    files = {"file": ("poor_sample.jpg", out.getvalue(), "image/jpeg")}
    upload_resp = await async_client.post(
        f"/api/v1/inspections/{inspection_id}/images",
        files=files,
    )
    assert upload_resp.status_code == 201
    data = upload_resp.json()
    assert data["quality_status"] == "recapture"
    assert data["quality_score"] < 0.85
    assert len(data["quality_reasons"]) > 0
    assert any("resolution" in r.lower() or "dark" in r.lower() for r in data["quality_reasons"])


@pytest.mark.asyncio
async def test_upload_image_unsupported_type(async_client):
    """Uploading unsupported file format (e.g. .txt or .pdf) should return 400."""
    insp_resp = await async_client.post(
        "/api/v1/inspections",
        json={"lot_id": "LOT-INVALID-TYPE"},
    )
    inspection_id = insp_resp.json()["id"]

    files = {"file": ("document.pdf", b"%PDF-1.4 dummy content", "application/pdf")}
    upload_resp = await async_client.post(
        f"/api/v1/inspections/{inspection_id}/images",
        files=files,
    )
    assert upload_resp.status_code == 400
    assert "unsupported file type" in upload_resp.json()["detail"].lower()


@pytest.mark.asyncio
async def test_upload_image_empty_file(async_client):
    """Uploading an empty file should return 400."""
    insp_resp = await async_client.post(
        "/api/v1/inspections",
        json={"lot_id": "LOT-EMPTY"},
    )
    inspection_id = insp_resp.json()["id"]

    files = {"file": ("empty.jpg", b"", "image/jpeg")}
    upload_resp = await async_client.post(
        f"/api/v1/inspections/{inspection_id}/images",
        files=files,
    )
    assert upload_resp.status_code == 400
    assert "empty" in upload_resp.json()["detail"].lower()


@pytest.mark.asyncio
async def test_upload_image_to_nonexistent_inspection(async_client):
    """POST /api/v1/inspections/{id}/images with invalid inspection_id should return 404."""
    img_bytes = _create_test_image_bytes()
    files = {"file": ("phantom.jpg", img_bytes, "image/jpeg")}
    response = await async_client.post(
        "/api/v1/inspections/phantom-id-9999/images",
        files=files,
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_inspection_status(async_client):
    """PATCH /api/v1/inspections/{id} should update status and return 200."""
    create_resp = await async_client.post(
        "/api/v1/inspections",
        json={"lot_id": "LOT-UPDATE-01", "grading_profile": "AGMARK_2024_v1"},
    )
    assert create_resp.status_code == 201
    insp_id = create_resp.json()["id"]

    patch_resp = await async_client.patch(
        f"/api/v1/inspections/{insp_id}",
        json={"status": "in_progress"},
    )
    assert patch_resp.status_code == 200
    data = patch_resp.json()
    assert data["id"] == insp_id
    assert data["status"] == "in_progress"
    assert data["lot_id"] == "LOT-UPDATE-01"
    assert data["grading_profile"] == "AGMARK_2024_v1"


@pytest.mark.asyncio
async def test_update_inspection_grading_profile(async_client):
    """PATCH /api/v1/inspections/{id} should update grading_profile and return 200."""
    create_resp = await async_client.post(
        "/api/v1/inspections",
        json={"lot_id": "LOT-UPDATE-02", "grading_profile": "AGMARK_2024_v1"},
    )
    insp_id = create_resp.json()["id"]

    patch_resp = await async_client.patch(
        f"/api/v1/inspections/{insp_id}",
        json={"grading_profile": "NAFED_2025_v2"},
    )
    assert patch_resp.status_code == 200
    data = patch_resp.json()
    assert data["grading_profile"] == "NAFED_2025_v2"
    assert data["status"] == "pending"


@pytest.mark.asyncio
async def test_update_inspection_single_field_preserves_other(async_client):
    """Updating a single field must not overwrite or nullify the other field."""
    create_resp = await async_client.post(
        "/api/v1/inspections",
        json={"lot_id": "LOT-UPDATE-03", "grading_profile": "INITIAL_PROFILE"},
    )
    insp_id = create_resp.json()["id"]

    # Update only status
    patch_resp1 = await async_client.patch(
        f"/api/v1/inspections/{insp_id}",
        json={"status": "completed"},
    )
    assert patch_resp1.status_code == 200
    data1 = patch_resp1.json()
    assert data1["status"] == "completed"
    assert data1["grading_profile"] == "INITIAL_PROFILE"

    # Update only grading_profile
    patch_resp2 = await async_client.patch(
        f"/api/v1/inspections/{insp_id}",
        json={"grading_profile": "NEW_PROFILE"},
    )
    assert patch_resp2.status_code == 200
    data2 = patch_resp2.json()
    assert data2["status"] == "completed"
    assert data2["grading_profile"] == "NEW_PROFILE"


@pytest.mark.asyncio
async def test_update_inspection_not_found(async_client):
    """PATCH with non-existent inspection_id should return 404."""
    patch_resp = await async_client.patch(
        "/api/v1/inspections/phantom-id-9999",
        json={"status": "completed"},
    )
    assert patch_resp.status_code == 404
    assert "not found" in patch_resp.json()["detail"].lower()


@pytest.mark.asyncio
async def test_update_inspection_empty_and_invalid_payload(async_client):
    """Empty payload returns 200 with unchanged fields; invalid payload returns 422."""
    create_resp = await async_client.post(
        "/api/v1/inspections",
        json={"lot_id": "LOT-UPDATE-04", "grading_profile": "AGMARK_2024_v1"},
    )
    insp_id = create_resp.json()["id"]

    # Empty payload preserves existing fields
    empty_resp = await async_client.patch(
        f"/api/v1/inspections/{insp_id}",
        json={},
    )
    assert empty_resp.status_code == 200
    data = empty_resp.json()
    assert data["status"] == "pending"
    assert data["grading_profile"] == "AGMARK_2024_v1"

    # Invalid payload (wrong type for status) returns 422
    invalid_resp = await async_client.patch(
        f"/api/v1/inspections/{insp_id}",
        json={"status": 12345},
    )
    # Pydantic may coerce or reject; status is str, integer could be coerced or rejected.
    # Passing an object/dict into a string field will strictly fail with 422
    dict_as_str_resp = await async_client.patch(
        f"/api/v1/inspections/{insp_id}",
        json={"status": {"invalid": "object"}},
    )
    assert dict_as_str_resp.status_code == 422
