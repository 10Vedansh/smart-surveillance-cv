# Smart Surveillance and Motion Analysis using Computer Vision

A command-line Computer Vision pipeline for **object detection, persistent tracking, motion estimation, event logging and analytics** on recorded video.

## Why this project fits Computer Vision

The pipeline applies practical CV operations including image resizing, Gaussian convolution/denoising, CLAHE contrast enhancement, Canny edge extraction, frame differencing and dense optical flow. A pretrained YOLO model provides object detection and persistent tracking IDs.

## Major Functional Modules

1. **Input & preprocessing** — validates video, reads frames, resizes, denoises, enhances contrast and extracts edges.
2. **Detection & tracking** — detects objects and maintains IDs across frames using YOLO tracking.
3. **Motion analysis** — combines changed-pixel masks with Farneback optical-flow magnitude.
4. **Event logging & analytics** — cooldown-based CSV event logging plus JSON summary generation.

## Features

- Fully terminal-based execution; no GUI interaction is required.
- Configurable input/output paths and CV thresholds.
- Persistent object IDs and confidence values.
- Motion mask and optical-flow measurements.
- Duplicate-event reduction through a per-track cooldown.
- Annotated MP4 output.
- CSV event log and JSON run summary.
- Automated pytest suite for deterministic modules.
- Mermaid architecture, use-case, sequence and component diagrams in `design.md`.

## Technologies

- Python 3.11+
- OpenCV
- NumPy
- Ultralytics YOLO
- pytest
- Git / GitHub

## Repository Structure

```text
smart-surveillance-cv/
├── analytics/analytics.py
├── config/config.py
├── detection/object_detector.py
├── input/video_reader.py
├── logging_module/event_logger.py
├── motion/motion_detector.py
├── preprocessing/image_processor.py
├── tracking/object_tracker.py
├── tests/                  # pytest test suite
├── input/test_video.mp4
├── yolo11n.pt
├── main.py
├── README.md
├── statement.md
├── requirements.md
├── design.md
└── testing.md
```

## Setup

### 1. Clone

```bash
git clone <YOUR_PUBLIC_REPOSITORY_URL>
cd smart-surveillance-cv
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The repository includes `yolo11n.pt`, so no separate model download is required for the included model file.

## Run

Show all options:

```bash
python main.py --help
```

Quick validation run on 30 frames:

```bash
python main.py --input input/test_video.mp4 --output-dir output --max-frames 30
```

Full run:

```bash
python main.py --input input/test_video.mp4 --output-dir output
```

Run without creating an annotated MP4:

```bash
python main.py --input input/test_video.mp4 --output-dir output --no-video
```

Example of changing CV/model parameters:

```bash
python main.py --input input/test_video.mp4 --conf 0.45 --motion-threshold 30 --motion-pixels 800 --cooldown 20
```

## Output

| File | Description |
|---|---|
| `output/surveillance_output.mp4` | Annotated video with boxes, IDs and motion metrics. |
| `output/events.csv` | Motion-associated tracked-object events. |
| `output/summary.json` | Frames, runtime, event count, class counts and averages. |

The exact event count and runtime depend on the input video, thresholds and hardware. Do not treat sample values from another machine as benchmark results.

## Testing

```bash
python -m pytest -q
```

The tests focus on deterministic modules so they do not require model inference. For the full end-to-end pipeline, install the requirements and run the command above with the included model/video.

## Documentation

- `statement.md` — problem statement, scope, target users and features.
- `requirements.md` — functional and non-functional requirements.
- `design.md` — architecture, workflow, UML-style diagrams, storage design and rationale.
- `testing.md` — test strategy and validation procedure.

## Privacy / Safety Scope

This is an academic video-analysis project. It does not perform facial recognition, infer identity, or decide whether a person is suspicious. It only records object classes, tracking IDs, confidence and motion measurements from the supplied video.

## Author

**Student Name:** Vedansh Taparia  
**Registration Number:** 24BAI10419  
**Course:** Computer Vision  
**Institution:** VIT Bhopal University
