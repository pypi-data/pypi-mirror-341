"""
Image Schema Module
-------------------
This module defines type annotations for image processing.

Attributes
----------
ColorPatchType : numpy.typing.NDArray[np.uint8]
    Represents a color patch extracted from an image,
    typically the mean of a region patch.

    Example
    -------
    ```python
    np.array(
        [68, 82, 115],  # 1. Dark skin
    )
    ```
ImageType : numpy.typing.NDArray[np.uint8]
    Represents a 3D image array with shape (H, W, C) in uint8 format.
ImageBGR : numpy.typing.NDArray[np.uint8]
    Represents an image in BGR format (OpenCV default).
ImageRGB : numpy.typing.NDArray[np.uint8]
    Represents an image in RGB format.
ImageGray : numpy.typing.NDArray[np.uint8]
    Represents a grayscale image.
BoundingBox : tuple[int, int, int, int]
    Represents a bounding box as (x1, y1, x2, y2).
    The top-left and bottom-right corners of the detection.
MatrixWeightLeastSquare : numpy.typing.NDArray[np.float64]
    Represents the matrix of weights for the least squares regression.
TrainedCorrection : MatrixWeightLeastSquare | LinearRegression | Pipeline
    Represents the trained model for color correction.

"""

from typing import Literal

import numpy as np
from numpy.typing import NDArray
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline

LiteralModelCorrection = Literal[
    "least_squares",
    "polynomial",
    "linear_reg",
    "affine_reg",
]

LiteralModelDetection = Literal["yolov8", "mcc"]

ColorPatchType = NDArray[np.uint8]
ImageType = NDArray[np.uint8]
ImageBGR = NDArray[np.uint8]
ImageRGB = NDArray[np.uint8]
ImageGray = NDArray[np.uint8]
BoundingBox = tuple[int, int, int, int]
SegmentPoint = list[tuple[int, int]]
MatrixWeightLeastSquare = NDArray[np.float64]

TrainedCorrection = MatrixWeightLeastSquare | LinearRegression | Pipeline
