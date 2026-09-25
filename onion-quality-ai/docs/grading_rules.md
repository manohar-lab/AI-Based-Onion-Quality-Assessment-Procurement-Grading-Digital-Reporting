# Grading Rules Documentation

> **STATUS: PLACEHOLDER — to be expanded**

## Overview

Indian onion quality grading is governed by multiple agencies and standards:

- **AGMARK** — Agricultural Produce (Grading and Marking) Act
- **NAFED** — National Agricultural Cooperative Marketing Federation procurement specifications
- **State APMC** — Agricultural Produce Market Committee norms (vary by state)

## Design Principles

- Rules are **separate from AI models** (see `backend/app/rules/README.md`)
- Rules are **versioned** — each government notification creates a new version
- The **grading profile + version** is stored with every inspection result
- Rules are **auditable** — written in human-readable format (YAML/JSON)

## Future Sections

- Detailed AGMARK grading criteria for onions
- NAFED procurement quality parameters
- State-specific variations
- Mapping between ML outputs and grading inputs
- Rule validation test cases
