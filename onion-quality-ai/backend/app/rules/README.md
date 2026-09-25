# Government Grading Rule Engine

> **STATUS: NOT IMPLEMENTED YET**

This directory will contain versioned Government grading specifications for Indian onion procurement.

## Design Principles

1. **Separation from AI Models**
   Government grading rules must be kept completely separate from the ML/AI models. AI models produce *measurements* (diameter, defect percentage, colour metrics). The rule engine applies *government specifications* to those measurements to arrive at a grade. This separation ensures that:
   - Changing a government specification does not require retraining a model.
   - AI model improvements do not accidentally alter grading outcomes.

2. **Versioning**
   Every rule set must be versioned (e.g., `AGMARK_2024_v1`, `NAFED_2025_v2`). When a new government notification changes grading thresholds, a new version is created — old versions are never deleted, so that past inspections remain auditable against the rules that were in effect at the time.

3. **Traceability**
   The grading profile (name + version) used during an inspection must be stored alongside the inspection result. This creates a complete audit trail from image → measurements → applied rules → final grade.

4. **Auditability**
   Rule definitions should be human-readable (YAML / JSON / structured Python) so that regulators, auditors, or domain experts can review them without needing to understand ML code.

5. **No Hard-Coded Decisions**
   Grading thresholds (e.g., maximum allowable defect percentages, minimum diameters for grade A) must **never** be embedded inside ML model logic. They belong here, in the rule engine, and are applied as a post-processing step.

## Planned Structure

```
rules/
├── __init__.py
├── engine.py              # Rule evaluation logic
├── profiles/
│   ├── agmark_2024.yaml   # AGMARK grading thresholds
│   ├── nafed_2025.yaml    # NAFED procurement specs
│   └── ...
└── README.md              # This file
```

## References

- AGMARK grading standards for onions (Directorate of Marketing & Inspection)
- NAFED procurement quality specifications
- State-level APMC grading norms
