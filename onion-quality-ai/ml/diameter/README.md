# Diameter Estimation Module

> **STATUS: NOT IMPLEMENTED YET**

## Responsibility

Estimate the physical diameter (in mm) of each detected onion from its segmentation mask and a known reference scale.

## Approach

- Use segmentation contour + calibration reference (coin, ruler, or known-size card placed in the image).
- Convert pixel measurements to millimetres.
- Report minimum and maximum diameter for non-circular onions.

## Expected Outputs

- Diameter in mm (min, max, average).
- Pixel-to-mm conversion factor used.

## Future Files

- `estimator.py` — Core diameter computation
- `calibration.py` — Reference-object-based pixel-to-mm calibration
