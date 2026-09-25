# LangGraph — Inspection Workflow Orchestration

> **STATUS: NOT IMPLEMENTED YET**

## Purpose

LangGraph will orchestrate the full inspection pipeline as a directed graph of processing nodes. Each node is a discrete, testable step.

## Planned Workflow

```
┌─────────┐
│ Capture  │  ← Image(s) from camera
└────┬─────┘
     ▼
┌──────────────┐
│ Image Quality │  ← Blur / exposure / resolution check
└────┬─────────┘
     ▼
┌───────────┐
│ Detection  │  ← Locate individual onions in the image
└────┬──────┘
     ▼
┌──────────────┐
│ Segmentation  │  ← Pixel-level mask for each onion
└────┬─────────┘
     ▼
┌──────────────┐
│ Measurements  │  ← Diameter, area, shape metrics
└────┬─────────┘
     ▼
┌─────────────────┐
│ Defect Analysis  │  ← Classify surface defects (rot, sprouting, cuts, etc.)
└────┬────────────┘
     ▼
┌───────────────────┐
│ Government Rules   │  ← Apply versioned grading specifications
└────┬──────────────┘
     ▼
┌──────┐
│ Jev   │  ← Confidence / evidence gate
└────┬──┘
     ▼
┌─────────────────────────────────────┐
│ Accept  /  Recapture  /  Human Review │
└────┬────────────────────────────────┘
     ▼
┌──────────────────┐
│ Lot Aggregation   │  ← Combine per-onion results into lot-level summary
└────┬─────────────┘
     ▼
┌─────────┐
│ Report   │  ← Generate PDF / digital report
└──────────┘
```

## Design Notes

- Each node receives a shared `InspectionState` and returns an updated state.
- Conditional edges (e.g., recapture loop) are modelled as LangGraph edges.
- The graph definition will live in this directory; individual node implementations will reference services and ML modules.
- The graph must be serialisable for debugging and audit purposes.
