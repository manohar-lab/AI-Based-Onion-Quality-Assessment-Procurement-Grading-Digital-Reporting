# Detection Module

> **STATUS: NOT IMPLEMENTED YET**

## Responsibility

Locate individual onions within an image using object detection models (e.g., YOLOv8, Faster R-CNN).

## Expected Outputs

- Bounding boxes with confidence scores for each detected onion.
- Count of onions per image.

## Future Files

- `model.py` — Model loading and inference wrapper
- `config.py` — Detection hyperparameters and thresholds
- `postprocess.py` — NMS, filtering, and coordinate normalization
