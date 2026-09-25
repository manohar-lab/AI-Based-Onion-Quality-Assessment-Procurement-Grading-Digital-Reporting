"""Unit tests for ImageQualityService."""

import io
import numpy as np
from PIL import Image as PILImage, ImageFilter

from app.services.image_quality_service import ImageQualityService


def _generate_sharp_image(width: int = 600, height: int = 600) -> bytes:
    """Generate high-contrast, structured image with sharp edges."""
    img = PILImage.new("RGB", (width, height), color=(240, 240, 240))
    arr = np.array(img)
    # Add checkerboard high-contrast patterns
    for y in range(0, height, 40):
        for x in range(0, width, 40):
            if (x // 40 + y // 40) % 2 == 0:
                arr[y : y + 40, x : x + 40] = [120, 40, 40]
    out = io.BytesIO()
    PILImage.fromarray(arr).save(out, format="JPEG", quality=95)
    return out.getvalue()


def _generate_blurry_image(width: int = 600, height: int = 600) -> bytes:
    """Generate a severely blurred image."""
    sharp_bytes = _generate_sharp_image(width, height)
    img = PILImage.open(io.BytesIO(sharp_bytes))
    blurry = img.filter(ImageFilter.GaussianBlur(radius=15))
    out = io.BytesIO()
    blurry.save(out, format="JPEG")
    return out.getvalue()


def _generate_dark_image(width: int = 600, height: int = 600) -> bytes:
    """Generate an underexposed dark image."""
    img = PILImage.fromarray(np.full((height, width, 3), 15, dtype=np.uint8))
    out = io.BytesIO()
    img.save(out, format="JPEG")
    return out.getvalue()


def _generate_bright_image(width: int = 600, height: int = 600) -> bytes:
    """Generate an overexposed washed out image."""
    img = PILImage.fromarray(np.full((height, width, 3), 248, dtype=np.uint8))
    out = io.BytesIO()
    img.save(out, format="JPEG")
    return out.getvalue()


def _generate_low_res_image(width: int = 240, height: int = 240) -> bytes:
    """Generate an image below required resolution thresholds."""
    img = PILImage.new("RGB", (width, height), color=(150, 100, 100))
    out = io.BytesIO()
    img.save(out, format="PNG")
    return out.getvalue()


def test_sharp_image_passes_quality_gate():
    """Sharp, well-exposed, adequate-resolution image must pass quality check."""
    image_bytes = _generate_sharp_image()
    result = ImageQualityService.evaluate(image_bytes)

    assert result.quality_status == "passed"
    assert result.quality_score >= 0.85
    assert len(result.quality_reasons) == 0
    assert result.metrics["width"] == 600
    assert result.metrics["height"] == 600


def test_blurry_image_flags_recapture():
    """Blurry image must be rejected with status 'recapture' and explicit reason."""
    image_bytes = _generate_blurry_image()
    result = ImageQualityService.evaluate(image_bytes)

    assert result.quality_status == "recapture"
    assert result.quality_score < 0.85
    assert any("blurry" in r.lower() for r in result.quality_reasons)


def test_dark_image_flags_recapture():
    """Underexposed image must be rejected with status 'recapture' and dark reason."""
    image_bytes = _generate_dark_image()
    result = ImageQualityService.evaluate(image_bytes)

    assert result.quality_status == "recapture"
    assert any("dark" in r.lower() or "underexposed" in r.lower() for r in result.quality_reasons)


def test_bright_image_flags_recapture():
    """Overexposed/washed-out image must be rejected with status 'recapture' and bright reason."""
    image_bytes = _generate_bright_image()
    result = ImageQualityService.evaluate(image_bytes)

    assert result.quality_status == "recapture"
    assert any("bright" in r.lower() or "washed out" in r.lower() for r in result.quality_reasons)


def test_low_resolution_flags_recapture():
    """Image below minimum resolution must be rejected with resolution reason."""
    image_bytes = _generate_low_res_image(320, 240)
    result = ImageQualityService.evaluate(image_bytes)

    assert result.quality_status == "recapture"
    assert any("resolution" in r.lower() for r in result.quality_reasons)


def test_corrupted_data_handled_gracefully():
    """Invalid image bytes should return recapture without crashing."""
    corrupted_bytes = b"not-a-valid-image-content"
    result = ImageQualityService.evaluate(corrupted_bytes)

    assert result.quality_status == "recapture"
    assert result.quality_score == 0.0
    assert any("corrupted" in r.lower() or "invalid" in r.lower() for r in result.quality_reasons)
