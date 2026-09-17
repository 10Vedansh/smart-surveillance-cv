import os
import cv2


class VideoReader:
    """Safely opens a video and yields valid frames sequentially."""

    def __init__(self, video_path: str):
        self.video_path = video_path
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            raise ValueError(f"Could not open video: {video_path}")

    def get_properties(self):
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = float(self.cap.get(cv2.CAP_PROP_FPS))
        frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

        if width <= 0 or height <= 0 or fps <= 0:
            raise ValueError("Invalid video properties.")

        return {
            "width": width,
            "height": height,
            "fps": fps,
            "frame_count": frame_count,
        }

    def read_frames(self):
        while True:
            success, frame = self.cap.read()
            if not success:
                break
            if frame is not None and frame.size > 0:
                yield frame

    def release(self):
        if self.cap is not None:
            self.cap.release()
