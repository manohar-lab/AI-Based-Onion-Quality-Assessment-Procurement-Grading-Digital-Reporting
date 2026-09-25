# Evaluation Module

> **STATUS: NOT IMPLEMENTED YET**

## Responsibility

Evaluate trained models against held-out test sets and produce metrics reports.

## Metrics

- Detection: mAP@50, mAP@50:95, precision, recall
- Segmentation: IoU, Dice coefficient
- Defects: accuracy, F1 per class, confusion matrix
- Diameter: MAE (mm), RMSE (mm), correlation coefficient

## Future Files

- `evaluate.py` — Unified evaluation runner
- `metrics.py` — Metric computation functions
- `visualize.py` — Plots and qualitative result samples
