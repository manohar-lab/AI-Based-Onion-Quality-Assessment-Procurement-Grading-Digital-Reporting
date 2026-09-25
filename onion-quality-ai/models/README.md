# Trained Model Weights

> **STATUS: NOT IMPLEMENTED YET**

This directory stores trained model weight files.

## Structure

| Directory        | Model Type                          |
| ---------------- | ----------------------------------- |
| `detection/`     | Object detection weights            |
| `segmentation/`  | Instance segmentation weights       |
| `defects/`       | Defect classification weights       |

## Notes

- Model files (`.pt`, `.onnx`, `.tflite`) are excluded from Git via `.gitignore`.
- Use a model registry or cloud storage for production weight management.
- Every model file should be versioned and traceable to a training run.
