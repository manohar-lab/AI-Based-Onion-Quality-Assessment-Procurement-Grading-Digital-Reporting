# Preprocessing Module

> **STATUS: NOT IMPLEMENTED YET**

## Responsibility

Prepare raw images for the ML pipeline:

- Resize / pad to model input dimensions
- Colour normalization
- White-balance correction
- Background removal or standardization
- Image quality assessment (blur, exposure, resolution)

## Future Files

- `transforms.py` — Reusable image transforms
- `quality.py` — Image quality scoring (blur detection, exposure check)
- `augmentation.py` — Training-time augmentations
