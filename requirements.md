# Software Requirements Specification

## 1. Functional Requirements

- **FR-1:** Accept a compatible video path through the command line.
- **FR-2:** Validate video availability and readable properties.
- **FR-3:** Resize frames while preserving aspect ratio.
- **FR-4:** Apply Gaussian denoising, CLAHE contrast enhancement and Canny edge extraction.
- **FR-5:** Detect and track objects using a pretrained YOLO model.
- **FR-6:** Estimate motion using frame differencing and dense optical flow.
- **FR-7:** Log motion-associated tracked-object events with confidence and motion metrics.
- **FR-8:** Generate an annotated output video unless disabled.
- **FR-9:** Generate CSV and JSON analytics.
- **FR-10:** Expose processing parameters through command-line options.

## 2. Non-Functional Requirements

- **Performance:** processing width and frame limit are configurable.
- **Reliability:** invalid input and output initialization failures produce clear exceptions and resources are released.
- **Maintainability:** each major responsibility is isolated in a module.
- **Usability:** the project runs from a terminal with documented commands.
- **Resource efficiency:** frames are resized before expensive analysis.
- **Testability:** deterministic modules are covered by pytest.
- **Observability:** console summaries and machine-readable reports are generated.

## 3. Hardware / Software

- Python 3.11+ recommended.
- 8 GB RAM or more recommended.
- CPU supported; compatible GPU may accelerate YOLO inference.
- OpenCV, NumPy, Ultralytics and pytest.

## 4. Inputs / Outputs

**Input:** recorded video file.

**Outputs:** annotated MP4, event CSV and summary JSON.

## 5. Constraints

The project does not train a new model, identify individuals, determine intent, or provide real-time security decisions.
