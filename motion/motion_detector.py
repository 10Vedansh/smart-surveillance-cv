import cv2
import numpy as np


class MotionDetector:
    """Combines frame differencing with dense optical-flow magnitude."""

    def __init__(self, threshold=25, pixel_threshold=500, min_flow=0.8):
        if threshold < 0 or pixel_threshold < 0 or min_flow < 0:
            raise ValueError("Motion parameters must be non-negative")
        self.threshold = threshold
        self.pixel_threshold = pixel_threshold
        self.min_flow = min_flow
        self.previous_gray = None

    def detect(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        if self.previous_gray is None:
            self.previous_gray = gray
            return {
                "motion_detected": False,
                "motion_pixels": 0,
                "mean_flow": 0.0,
                "mask": np.zeros_like(gray),
            }

        difference = cv2.absdiff(self.previous_gray, gray)
        _, mask = cv2.threshold(difference, self.threshold, 255, cv2.THRESH_BINARY)
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.dilate(mask, kernel, iterations=1)

        motion_pixels = int(cv2.countNonZero(mask))

        flow = cv2.calcOpticalFlowFarneback(
            self.previous_gray,
            gray,
            None,
            pyr_scale=0.5,
            levels=3,
            winsize=15,
            iterations=3,
            poly_n=5,
            poly_sigma=1.2,
            flags=0,
        )
        magnitude, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        mean_flow = float(np.mean(magnitude))

        motion_detected = (
            motion_pixels > self.pixel_threshold
            or mean_flow >= self.min_flow
        )
        self.previous_gray = gray

        return {
            "motion_detected": motion_detected,
            "motion_pixels": motion_pixels,
            "mean_flow": mean_flow,
            "mask": mask,
        }
