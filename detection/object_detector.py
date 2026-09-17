class ObjectDetector:
    """YOLO object detector with lazy dependency loading."""

    def __init__(self, model_name="yolo11n.pt", confidence=0.35):
        try:
            from ultralytics import YOLO
        except ImportError as exc:
            raise ImportError(
                "Ultralytics is required for detection. Install with "
                "python -m pip install ultralytics."
            ) from exc
        self.model = YOLO(model_name)
        self.confidence = confidence

    def detect(self, frame):
        results = self.model(frame, conf=self.confidence, verbose=False)
        return results[0]

    @staticmethod
    def get_detections(result):
        detections = []
        if result.boxes is None:
            return detections
        for box in result.boxes:
            class_id = int(box.cls[0])
            detections.append({
                "class_id": class_id,
                "class_name": result.names[class_id],
                "confidence": float(box.conf[0]),
                "box": box.xyxy[0].tolist(),
            })
        return detections
