# Copyright (c) 2025 Viktor Fairuschin
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


import os
import typing

import cv2
import numpy as np

from decord import VideoReader, cpu


def load_video(
        filepath: typing.Union[str, os.PathLike],
        height: int = -1,
        width: int = -1,
) -> np.ndarray:
    """
    Loads a video.

    :param filepath: Path to the video.
    :param height: Desired output height of the video, unchanged if -1 is specified.
    :param width: Desired output width of the video, unchanged if -1 is specified.
    """
    if not os.path.isfile(filepath):
        raise FileNotFoundError(filepath)

    vr = VideoReader(filepath, height=height, width=width, num_threads=-1, ctx=cpu(0))
    return vr[:].asnumpy()


def show_video(video: np.ndarray) -> None:
    """
    Shows a video.
    """
    cv2.destroyAllWindows()

    for frame in video:
        cv2.imshow('video', cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
        cv2.waitKey(1)

    cv2.destroyAllWindows()


