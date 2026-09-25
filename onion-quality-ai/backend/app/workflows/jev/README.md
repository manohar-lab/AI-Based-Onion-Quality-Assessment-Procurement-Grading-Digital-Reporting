# Jev — Confidence / Evidence Decision Gate

> **STATUS: NOT IMPLEMENTED YET**

## Purpose

Jev will act as a **confidence and evidence decision gate** within the inspection workflow. After the ML pipeline produces measurements and the government rule engine produces a tentative grade, Jev evaluates:

- **Confidence levels** of each ML prediction (detection, segmentation, defect classification, diameter estimation).
- **Evidence sufficiency** — whether enough images were captured, whether image quality was adequate, and whether all required measurements are present.
- **Decision routing** — based on confidence thresholds, Jev will route the inspection to one of:
  - ✅ **Accept** — all predictions are high-confidence; the grade stands.
  - 🔄 **Recapture** — one or more images were low-quality or ambiguous; request new capture.
  - 👤 **Human Review** — confidence is below threshold; flag for manual inspection.

## Critical Constraint

Jev **must NOT redefine or override Government grading rules**. It operates purely on the confidence/evidence dimension. The grading rules are the sole authority on what constitutes Grade A vs. Grade B etc. Jev only decides whether the system is *confident enough* in the measurements to apply those rules automatically.

## Planned Interface

```python
class JevDecision:
    action: Literal["accept", "recapture", "human_review"]
    confidence_scores: dict[str, float]
    reasons: list[str]
```

## Integration Point

Jev sits between the government rule engine output and the final result:

```
ML Pipeline → Government Rules → Jev → Final Decision
```
