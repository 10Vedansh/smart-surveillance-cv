"""Default configuration for the command-line surveillance pipeline."""

VIDEO_PATH = "input/test_video.mp4"
OUTPUT_DIR = "output"
MODEL_PATH = "yolo11n.pt"

OUTPUT_WIDTH = 640
CONFIDENCE_THRESHOLD = 0.35

# Frame-difference motion parameters.
MOTION_THRESHOLD = 25
MOTION_PIXEL_THRESHOLD = 500
MOTION_MIN_FLOW = 0.8

# Avoid writing the same tracked object on every consecutive frame.
EVENT_COOLDOWN_FRAMES = 15

# Set to False to run faster when an annotated video is not required.
SAVE_VIDEO = True
