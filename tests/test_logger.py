import csv
from logging_module.event_logger import EventLogger


def test_event_logger(tmp_path):
    path = tmp_path / "events.csv"
    logger = EventLogger(str(path))
    logger.log_event(2, "Motion Detected", 7, "person", 0.91, 1200, 1.2)
    with path.open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    assert len(rows) == 1
    assert rows[0]["object_class"] == "person"
    assert rows[0]["object_id"] == "7"
    assert rows[0]["motion_pixels"] == "1200"
