import csv
import json
import os
from collections import Counter


class SurveillanceAnalytics:
    """Calculates reproducible summary statistics from the event CSV."""

    def __init__(self, event_file="output/events.csv"):
        self.event_file = event_file

    def analyze(self):
        total_events = 0
        object_types = Counter()
        object_ids = set()
        confidences = []
        motion_pixels = []
        flow_values = []

        if not os.path.exists(self.event_file):
            return {
                "total_events": 0,
                "unique_objects": 0,
                "object_types": {},
                "average_confidence": 0.0,
                "average_motion_pixels": 0.0,
                "average_flow": 0.0,
            }

        with open(self.event_file, "r", newline="", encoding="utf-8") as file:
            for row in csv.DictReader(file):
                total_events += 1
                object_types[row["object_class"]] += 1
                object_ids.add(row["object_id"])
                confidences.append(float(row["confidence"]))
                motion_pixels.append(float(row.get("motion_pixels", 0)))
                flow_values.append(float(row.get("mean_flow", 0)))

        mean = lambda values: sum(values) / len(values) if values else 0.0
        return {
            "total_events": total_events,
            "unique_objects": len(object_ids),
            "object_types": dict(object_types),
            "average_confidence": round(mean(confidences), 3),
            "average_motion_pixels": round(mean(motion_pixels), 2),
            "average_flow": round(mean(flow_values), 3),
        }

    def save_json(self, output_path, summary, frames_processed=0, elapsed_seconds=0.0):
        payload = {
            "frames_processed": frames_processed,
            "elapsed_seconds": round(elapsed_seconds, 3),
            **summary,
        }
        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(payload, file, indent=2)
        return payload
