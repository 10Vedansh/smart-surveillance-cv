# Testing and Validation

## Test Strategy

The project separates deterministic image-processing, motion, logging and analytics logic from the YOLO dependency. This permits automated tests to run quickly without downloading a model. A small smoke test is also provided for the CLI entry point.

## Automated Tests

Run from the repository root:

```bash
python -m pytest -q
```

The suite checks:
- frame resizing, grayscale conversion, CLAHE output and edge extraction;
- frame-difference/optical-flow motion behavior on synthetic frames;
- event CSV creation and fields;
- analytics aggregation and JSON export;
- video reader validation using a generated temporary video;
- command-line parser defaults and validation.

## End-to-End Run

After installing dependencies and confirming `yolo11n.pt` is present:

```bash
python main.py --input input/test_video.mp4 --output-dir output --max-frames 30
```

For a complete run:

```bash
python main.py --input input/test_video.mp4 --output-dir output
```

To avoid writing the annotated video:

```bash
python main.py --input input/test_video.mp4 --no-video
```

## Validation Criteria

A successful run should:
1. print a final surveillance summary;
2. create `output/events.csv`;
3. create `output/summary.json`;
4. create `output/surveillance_output.mp4` unless `--no-video` is supplied;
5. preserve the number and dimensions of written frames for the configured output size.

## Observed Results

Results below are from the student's own run on this machine.

### Quick validation run (first 30 frames)

```bash
python main.py --input input/test_video.mp4 --output-dir output --max-frames 30
```

- Frames processed: 30
- Processing time: 24.18 s
- Total logged events: 16
- Unique tracked IDs: 10
- Average confidence: 0.732
- Average motion pixels: 101146.25
- Average optical-flow magnitude: 2.653
- Object classes: car (2), person (12), traffic light (2)

### Full run

```bash
python main.py --input input/test_video.mp4 --output-dir output
```

- Frames processed: 186
- Processing time: 65.43 s
- Total logged events: 101
- Unique tracked IDs: 23
- Average confidence: 0.675
- Average motion pixels: 150243.95
- Average optical-flow magnitude: 4.301
- Object classes: person (72), traffic light (13), car (13), bicycle (3)

All outputs (`output/events.csv`, `output/summary.json` and `output/surveillance_output.mp4`) were created successfully.

## Limitations of Evaluation

Detection/tracking results depend on the pretrained YOLO model, input video, confidence threshold and hardware. Therefore, exact event counts and processing times should be reported from the student's own run rather than copied from another environment.
