import csv
import os
from datetime import datetime


class EventLogger:
    """Writes structured motion/object events to CSV."""

    FIELDS = [
        "timestamp", "frame_number", "event_type", "object_id",
        "object_class", "confidence", "motion_pixels", "mean_flow"
    ]

    def __init__(self, file_path="output/events.csv", reset=True):
        self.file_path = file_path
        directory = os.path.dirname(file_path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        if reset or not os.path.exists(file_path):
            self._create_new_file()

    def _create_new_file(self):
        with open(self.file_path, "w", newline="", encoding="utf-8") as file:
            csv.writer(file).writerow(self.FIELDS)

    def log_event(self, frame_number, event_type, object_id, object_class,
                  confidence, motion_pixels=0, mean_flow=0.0):
        timestamp = datetime.now().isoformat(timespec="seconds")
        with open(self.file_path, "a", newline="", encoding="utf-8") as file:
            csv.writer(file).writerow([
                timestamp, frame_number, event_type, object_id,
                object_class, round(confidence, 3), motion_pixels,
                round(mean_flow, 3),
            ])
