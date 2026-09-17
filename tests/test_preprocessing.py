import numpy as np
from preprocessing.image_processor import ImageProcessor


def test_processing_outputs():
    image = np.zeros((480, 640, 3), dtype=np.uint8)
    image[100:200, 100:300] = 180
    processor = ImageProcessor(320)
    result = processor.process(image)
    assert result["resized"].shape == (240, 320, 3)
    assert result["enhanced"].shape == (240, 320)
    assert result["edges"].shape == (240, 320)
    assert result["edges"].dtype == np.uint8
