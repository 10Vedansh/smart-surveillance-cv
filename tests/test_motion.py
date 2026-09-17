import numpy as np
from motion.motion_detector import MotionDetector


def test_first_frame_has_no_motion():
    detector = MotionDetector()
    frame = np.zeros((120, 160, 3), dtype=np.uint8)
    result = detector.detect(frame)
    assert result["motion_detected"] is False
    assert result["motion_pixels"] == 0


def test_changed_frame_detects_motion():
    detector = MotionDetector(threshold=10, pixel_threshold=50, min_flow=0.01)
    first = np.zeros((120, 160, 3), dtype=np.uint8)
    second = first.copy()
    second[30:90, 40:120] = 255
    detector.detect(first)
    result = detector.detect(second)
    assert result["motion_pixels"] > 0
    assert result["motion_detected"] is True
