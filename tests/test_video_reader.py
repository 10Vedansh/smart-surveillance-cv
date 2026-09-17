import cv2
import numpy as np
from input.video_reader import VideoReader


def test_video_reader(tmp_path):
    path = str(tmp_path / "sample.mp4")
    writer = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*"mp4v"), 10, (64, 48))
    assert writer.isOpened()
    frame = np.zeros((48, 64, 3), dtype=np.uint8)
    for _ in range(3):
        writer.write(frame)
    writer.release()

    reader = VideoReader(path)
    props = reader.get_properties()
    frames = list(reader.read_frames())
    reader.release()
    assert props["width"] == 64
    assert props["height"] == 48
    assert len(frames) == 3
