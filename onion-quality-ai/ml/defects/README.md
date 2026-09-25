# Defect Classification Module

> **STATUS: NOT IMPLEMENTED YET**

## Responsibility

Classify surface and internal defects on individual onions. Defect categories may include:

- Sprouting
- Rotting (bacterial / fungal)
- Mechanical damage (cuts, bruises)
- Skin splitting
- Sunscald / discoloration
- Insect damage

## Expected Outputs

- Defect type labels with confidence scores.
- Defect area as a percentage of total onion surface.

## Future Files

- `model.py` — Classification model wrapper
- `taxonomy.py` — Defect type definitions (aligned with Government specifications)
- `visualization.py` — Overlay defect regions on source images
