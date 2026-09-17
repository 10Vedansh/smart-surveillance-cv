class ObjectTracker:
    """Persistent multi-object tracking using Ultralytics YOLO tracking."""

    def __init__(self, model_name="yolo11n.pt", confidence=0.35):
        try:
            from ultralytics import YOLO
        except ImportError as exc:
            raise ImportError(
                "Ultralytics is required for tracking. Install with "
                "python -m pip install ultralytics."
            ) from exc
        self.model = YOLO(model_name)
        self.confidence = confidence

    def track(self, frame):
        results = self.model.track(
            frame,
            persist=True,
            conf=self.confidence,
            verbose=False,
        )
        return results[0]

    @staticmethod
    def get_tracks(result):
        tracks = []
        if result.boxes is None or result.boxes.id is None:
            return tracks

        for box, track_id, cls, conf in zip(
            result.boxes.xyxy,
            result.boxes.id,
            result.boxes.cls,
            result.boxes.conf,
        ):
            class_id = int(cls)
            tracks.append({
                "track_id": int(track_id),
                "class_id": class_id,
                "class_name": result.names[class_id],
                "confidence": float(conf),
                "box": box.tolist(),
            })
        return tracks
