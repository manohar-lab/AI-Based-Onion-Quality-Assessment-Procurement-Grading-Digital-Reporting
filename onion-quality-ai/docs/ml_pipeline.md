# ML Pipeline Documentation

> **AI-Based Onion Quality Assessment Pipeline**

## Pipeline Stages

```
1. Image Capture (Mobile / Camera)
         │
         ▼
2. Image Quality Gate (Blur, Exposure, Resolution) ──[Recapture?]──▶ Immediate Inspector Feedback
         │ (Passed)
         ▼
3. Preprocessing (Normalization, Standardisation) [Next Phase]
         │
         ▼
4. Object Detection (Bounding Boxes per Onion) [Next Phase]
         │
         ▼
5. Instance Segmentation (Pixel-level Contours) [Next Phase]
         │
         ▼
6. Physical Measurement (Diameter, Area, Shape in mm) [Next Phase]
         │
         ▼
7. Defect Classification (Rot, Sprouting, Cuts, Discoloration) [Next Phase]
         │
         ▼
8. Government Grading Rule Engine (AGMARK / NAFED / APMC) [Next Phase]
         │
         ▼
9. Decision & Confidence Gate (Jev) [Next Phase]
         │
         ▼
10. Lot Aggregation & Digital Report [Next Phase]
```

---

## Stage 2: Automated Pre-Inference Quality Validation

Before executing computer vision models, incoming images pass through the deterministic quality pipeline implemented in `app/services/image_quality_service.py`.

### Quality Metrics & Thresholds

| Metric | Algorithm | Passing Threshold | Recapture Trigger |
| :--- | :--- | :--- | :--- |
| **Sharpness / Blur** | Discrete Laplacian variance on grayscale intensity | $\sigma^2_{\nabla^2} \ge 60.0$ | $\sigma^2_{\nabla^2} < 60.0$ (motion blur, defocus) |
| **Underexposure** | Mean pixel luminance ($\mu_L$) | $\mu_L \ge 40.0$ | $\mu_L < 40.0$ (excessively dark, shadows) |
| **Overexposure** | Mean pixel luminance ($\mu_L$) | $\mu_L \le 225.0$ | $\mu_L > 225.0$ (glare, flash washout) |
| **Resolution** | Image dimensions $(W \times H)$ | $W \ge 480$ and $H \ge 480$ | Either dimension $< 480$ px |

### Recapture Protocol
- If any check fails, the API sets `quality_status: "recapture"` and returns an actionable `quality_reasons` array directly to the client.
- Low-quality images are preserved for auditability but are flagged so subsequent AI measurement stages do not produce inaccurate results from corrupted or out-of-focus inputs.
