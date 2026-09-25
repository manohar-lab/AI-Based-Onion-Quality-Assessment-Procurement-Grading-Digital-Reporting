# Data Directory

This directory contains all data assets for the project.

## Structure

| Directory      | Purpose                                              |
| -------------- | ---------------------------------------------------- |
| `raw/`         | Original, unprocessed images as captured              |
| `processed/`   | Pre-processed images ready for model input            |
| `annotations/` | Labels, bounding boxes, masks (COCO / YOLO format)   |
| `samples/`     | Small representative samples for quick testing        |

## Notes

- Large data files are excluded from Git (see `.gitignore`).
- Use DVC or similar for data versioning in production.
- Do NOT commit real training datasets to this repository.
