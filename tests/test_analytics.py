import csv
import json
from analytics.analytics import SurveillanceAnalytics


def test_analytics_and_json(tmp_path):
    csv_path = tmp_path / "events.csv"
    json_path = tmp_path / "summary.json"
    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(SurveillanceAnalytics.__module__ and [
            "timestamp", "frame_number", "event_type", "object_id",
            "object_class", "confidence", "motion_pixels", "mean_flow"
        ])
        writer.writerow(["2026-09-17T10:00:00", 1, "Motion Detected", 1, "person", 0.9, 100, 1.0])
        writer.writerow(["2026-09-17T10:00:01", 2, "Motion Detected", 1, "person", 0.8, 200, 1.4])
        writer.writerow(["2026-09-17T10:00:02", 3, "Motion Detected", 2, "car", 0.7, 300, 0.8])

    analytics = SurveillanceAnalytics(str(csv_path))
    summary = analytics.analyze()
    assert summary["total_events"] == 3
    assert summary["unique_objects"] == 2
    assert summary["object_types"] == {"person": 2, "car": 1}
    assert summary["average_confidence"] == 0.8
    analytics.save_json(str(json_path), summary, 10, 1.25)
    data = json.loads(json_path.read_text(encoding="utf-8"))
    assert data["frames_processed"] == 10
    assert data["total_events"] == 3
