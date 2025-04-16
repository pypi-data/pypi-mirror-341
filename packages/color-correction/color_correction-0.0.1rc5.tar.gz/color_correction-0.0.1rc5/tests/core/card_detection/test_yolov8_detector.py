import numpy as np
import pytest

from color_correction.core.card_detection.det_yv8_onnx import YOLOv8CardDetector

@pytest.mark.skip(reason="Test is not implemented")
def test_detector_init(sample_image: np.ndarray) -> None:
    detector = YOLOv8CardDetector(use_gpu=False)
    result = detector.detect(sample_image)
    assert result is not None
    assert len(result.boxes) == 0  # Expect no detections on empty image
