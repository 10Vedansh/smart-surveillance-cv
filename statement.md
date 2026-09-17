# Project Statement

## Project Title
Smart Surveillance and Motion Analysis using Computer Vision

## Problem Statement
Manual review of surveillance footage is time-consuming because an operator must repeatedly inspect frames to locate moving objects and understand when events occurred. The project addresses this problem with a command-line computer vision pipeline that detects objects, assigns persistent tracking IDs, estimates motion, and produces machine-readable event records.

## Objectives
1. Process a stored surveillance video frame by frame.
2. Apply image preprocessing techniques before analysis.
3. Detect and track objects using a pretrained YOLO model.
4. Detect motion using frame differencing and dense optical flow.
5. Log motion-associated object observations with timestamps and confidence values.
6. Produce summary analytics and an annotated output video without requiring a GUI.

## Major Functional Modules
- **Input & preprocessing:** video validation, frame extraction, resizing, Gaussian denoising, CLAHE contrast enhancement and Canny edge extraction.
- **Detection & tracking:** YOLO object detection and persistent multi-object tracking.
- **Motion analysis:** frame-difference mask plus Farneback dense optical flow.
- **Event logging & analytics:** cooldown-based event logging, CSV records and JSON summary statistics.

## Scope
### In scope
- Static video-file input.
- Object detection and persistent tracking.
- Motion estimation and event logging.
- Command-line execution and structured outputs.
- Automated unit/integration-style tests for deterministic modules.

### Out of scope
- Facial recognition or identity inference.
- Automatic judgment of whether a person is suspicious.
- Live CCTV deployment, cloud deployment and notification services.
- Training a new detection model.

## Target Users
- Computer vision students and researchers demonstrating a practical pipeline.
- Security-system prototyping teams evaluating detection/tracking workflows.
- Developers who need structured event data from recorded video.

## Inputs and Outputs
**Input:** MP4/compatible video file.

**Outputs:**
- `output/surveillance_output.mp4` — annotated video.
- `output/events.csv` — motion-associated tracked-object events.
- `output/summary.json` — run-level analytics.

## Academic Relevance
The implementation applies image preprocessing, convolution-based Gaussian filtering, contrast enhancement, edge detection, frame differencing, optical flow, object detection, tracking, and quantitative evaluation concepts from Computer Vision.
