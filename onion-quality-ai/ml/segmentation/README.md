# Segmentation Module

> **STATUS: NOT IMPLEMENTED YET**

## Responsibility

Generate pixel-level masks for each detected onion using instance segmentation (e.g., Mask R-CNN, SAM).

## Expected Outputs

- Binary or instance segmentation masks per onion.
- Contour polygons for area and shape computation.

## Future Files

- `model.py` — Segmentation model wrapper
- `postprocess.py` — Mask refinement and contour extraction
