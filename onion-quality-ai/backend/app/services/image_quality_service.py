"""Image Quality Assessment Service.

Evaluates raw incoming onion capture images across essential quality gates:
1. Sharpness / Blur detection (discrete Laplacian variance)
2. Darkness / Underexposure check (mean luminance)
3. Brightness / Glare / Overexposure check (mean luminance)
4. Minimum resolution check (width and height thresholds)

Flags low-quality images with status 'recapture' and detailed reasons so the
frontend/inspector can immediately recapture the produce.
"""

from dataclasses import dataclass, field
import io
from typing import Any, Dict, List
import numpy as np
from PIL import Image as PILImage


# Tunable quality gate thresholds
MIN_WIDTH_PX: int = 480
MIN_HEIGHT_PX: int = 480
MIN_SHARPNESS_SCORE: float = 60.0
MIN_MEAN_BRIGHTNESS: float = 40.0
MAX_MEAN_BRIGHTNESS: float = 225.0


@dataclass
class ImageQualityResult:
    """Outcome of automated image quality analysis."""
    quality_status: str  # "passed" | "recapture"
    quality_score: float  # 0.0 to 1.0
    quality_reasons: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)


class ImageQualityService:
    """Service providing pre-inference quality validation for captured onion images."""

    @classmethod
    def evaluate(cls, image_bytes: bytes) -> ImageQualityResult:
        """Evaluate raw image bytes and return quality verdict, score, and reasons."""
        try:
            image = PILImage.open(io.BytesIO(image_bytes))
            image.verify()  # Ensure file is uncorrupted
            # Reopen after verify() because verify() empties buffer
            image = PILImage.open(io.BytesIO(image_bytes))
        except Exception as exc:
            return ImageQualityResult(
                quality_status="recapture",
                quality_score=0.0,
                quality_reasons=[f"Invalid or corrupted image data: {str(exc)}"],
                metrics={"corrupted": True},
            )

        width, height = image.size
        reasons: List[str] = []
        penalties: List[float] = []

        # 1. Resolution Check
        if width < MIN_WIDTH_PX or height < MIN_HEIGHT_PX:
            reasons.append(
                f"Insufficient resolution: {width}x{height} px. "
                f"Minimum required is {MIN_WIDTH_PX}x{MIN_HEIGHT_PX} px for accurate measurement. Please recapture."
            )
            dim_ratio = min(width / MIN_WIDTH_PX, height / MIN_HEIGHT_PX)
            penalties.append(max(0.2, dim_ratio))

        # Convert to grayscale for optical metrics
        gray_image = image.convert("L")
        gray = np.array(gray_image, dtype=np.float64)

        # 2. Brightness Check
        mean_brightness = float(np.mean(gray))
        if mean_brightness < MIN_MEAN_BRIGHTNESS:
            reasons.append(
                f"Image is extremely dark / underexposed (brightness: {mean_brightness:.1f}/255). "
                f"Please ensure adequate lighting and recapture."
            )
            penalties.append(max(0.1, mean_brightness / MIN_MEAN_BRIGHTNESS))
        elif mean_brightness > MAX_MEAN_BRIGHTNESS:
            reasons.append(
                f"Image is extremely bright / washed out (brightness: {mean_brightness:.1f}/255). "
                f"Please avoid direct flash/glare and recapture."
            )
            penalties.append(max(0.1, (255.0 - mean_brightness) / (255.0 - MAX_MEAN_BRIGHTNESS)))

        # 3. Blur / Sharpness Check (Laplacian Variance)
        # Compute discrete Laplacian using finite differences on inner grid
        if gray.shape[0] > 2 and gray.shape[1] > 2:
            laplacian = (
                gray[:-2, 1:-1]
                + gray[2:, 1:-1]
                + gray[1:-1, :-2]
                + gray[1:-1, 2:]
                - 4.0 * gray[1:-1, 1:-1]
            )
            sharpness_score = float(np.var(laplacian))
        else:
            sharpness_score = 0.0

        if sharpness_score < MIN_SHARPNESS_SCORE:
            reasons.append(
                f"Image is excessively blurry (sharpness score: {sharpness_score:.1f}, "
                f"min: {MIN_SHARPNESS_SCORE:.1f}). Please steady the camera and recapture."
            )
            penalties.append(max(0.1, sharpness_score / MIN_SHARPNESS_SCORE))

        # Compute overall quality score (0.0 to 1.0)
        if penalties:
            # Score reduced by the most severe defect
            quality_score = round(float(np.prod(penalties)), 2)
            quality_status = "recapture"
        else:
            # Passed - calculate high-confidence quality score
            # Scaled between 0.85 and 1.0 based on margin above thresholds
            sharpness_factor = min(1.0, sharpness_score / (MIN_SHARPNESS_SCORE * 3.0))
            quality_score = round(0.85 + (0.15 * sharpness_factor), 2)
            quality_status = "passed"

        metrics = {
            "width": width,
            "height": height,
            "mean_brightness": round(mean_brightness, 2),
            "sharpness_score": round(sharpness_score, 2),
        }

        return ImageQualityResult(
            quality_status=quality_status,
            quality_score=quality_score,
            quality_reasons=reasons,
            metrics=metrics,
        )
