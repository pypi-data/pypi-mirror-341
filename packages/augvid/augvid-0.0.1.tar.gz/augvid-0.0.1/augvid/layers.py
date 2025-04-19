# Copyright (c) 2025 Viktor Fairuschin
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


import typing
import keras
import tensorflow as tf


class BaseAugmentationLayer(keras.layers.Layer):
    """
    Base class for video augmentation layer.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.input_spec = keras.layers.InputSpec(ndim=5, axes={4: 3})

    @staticmethod
    def apply_to_video(video: tf.Tensor, func: typing.Callable, **kwargs) -> tf.Tensor:
        """ Applies image op `func` to video. """
        t, h, w, c = video.shape.as_list()

        video = func(tf.reshape(video, [t * h, w, c]), **kwargs)
        return tf.reshape(video, [t, h, w, c])


class RandomVideoBrightness(BaseAugmentationLayer):
    """
    Adjusts the brightness of videos by a random factor.

    :param max_delta: This parameter controls the maximum relative
        change in brightness (must be non-negative).
    """

    def __init__(self, max_delta: float, **kwargs):
        super().__init__(**kwargs)
        self.max_delta = max_delta

    def call(self, inputs, training=False):
        def adjust(video):
            fn = lambda x: tf.image.random_brightness(x, max_delta=self.max_delta)
            return tf.map_fn(fn, video)

        if training:
            outputs = adjust(inputs)
            outputs.set_shape(inputs.shape)
            return outputs

        return inputs


class RandomVideoContrast(BaseAugmentationLayer):
    """
    Adjusts the contrast of videos by a random factor.

    :param lower: Lower bound for the random contrast factor.
    :param upper: Upper bound for the random contrast factor.
    """

    def __init__(self, lower: float, upper: float, **kwargs):
        super().__init__(**kwargs)
        self.lower = lower
        self.upper = upper

    def call(self, inputs, training=False):
        def adjust(video):
            fn = lambda x: tf.image.random_contrast(x, lower=self.lower, upper=self.upper)
            return tf.map_fn(fn, video)

        if training:
            outputs = adjust(inputs)
            outputs.set_shape(inputs.shape)
            return outputs

        return inputs


class RandomVideoHue(BaseAugmentationLayer):
    """
    Adjusts the hue of RGB videos by a random factor.

    :param max_delta: The maximum value for the random delta.
    """

    def __init__(self, max_delta: float, **kwargs):
        super().__init__(**kwargs)
        self.max_delta = max_delta

    def call(self, inputs, training=False):
        def adjust(video):
            fn = lambda x: tf.image.random_hue(x, max_delta=self.max_delta)
            return tf.map_fn(fn, video)

        if training:
            outputs = adjust(inputs)
            outputs.set_shape(inputs.shape)
            return outputs

        return inputs


class RandomVideoSaturation(BaseAugmentationLayer):
    """
    Adjusts the saturation of videos by a random factor.

    :param lower: Lower bound for the random saturation factor.
    :param upper: Upper bound for the random saturation factor.
    """

    def __init__(self, lower: float, upper: float,  **kwargs):
        super().__init__(**kwargs)
        self.lower = lower
        self.upper = upper

    def call(self, inputs, training=False):
        def adjust(video):
            fn = lambda x: tf.image.random_saturation(x, lower=self.lower, upper=self.upper)
            return tf.map_fn(fn, video)

        if training:
            outputs = adjust(inputs)
            outputs.set_shape(inputs.shape)
            return outputs

        return inputs


class RandomHorizontalVideoFlip(BaseAugmentationLayer):
    """
    Randomly flips videos horizontally.
    """

    def call(self, inputs, training=False):
        def adjust(video):
            fn = lambda x: self.apply_to_video(x, tf.image.random_flip_left_right)
            return tf.map_fn(fn, video)

        if training:
            outputs = adjust(inputs)
            outputs.set_shape(inputs.shape)
            return outputs

        return inputs


class RandomVerticalVideoFlip(BaseAugmentationLayer):
    """
    Randomly flips videos vertically.
    """

    def call(self, inputs, training=False):
        def adjust(video):
            fn = lambda x: self.apply_to_video(x, tf.image.random_flip_up_down)
            return tf.map_fn(fn, video)

        if training:
            outputs = adjust(inputs)
            outputs.set_shape(inputs.shape)
            return outputs

        return inputs

