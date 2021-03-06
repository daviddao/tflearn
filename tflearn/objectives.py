from __future__ import division, print_function, absolute_import

import tensorflow as tf

from .config import _EPSILON, _FLOATX
from .utils import get_from_module


def get(identifier):
    return get_from_module(identifier, globals(), 'objective')


def softmax_categorical_crossentropy(y_pred, y_true):
    """ Softmax Categorical Crossentropy.

    Computes softmax cross entropy between y_pred (logits) and
    y_true (labels).

    Measures the probability error in discrete classification tasks in which
    the classes are mutually exclusive (each entry is in exactly one class).
    For example, each CIFAR-10 image is labeled with one and only one label:
    an image can be a dog or a truck, but not both.

    **WARNING:** This op expects unscaled logits, since it performs a `softmax`
    on `y_pred` internally for efficiency.  Do not call this op with the
    output of `softmax`, as it will produce incorrect results.

    `y_pred` and `y_true` must have the same shape `[batch_size, num_classes]`
    and the same dtype (either `float32` or `float64`). It is also required
    that `y_true` (labels) are binary arrays (For example, class 2 out of a
    total of 5 different classes, will be define as [0., 1., 0., 0., 0.])

    Arguments:
        y_pred: `Tensor`. Predicted values.
        y_true: `Tensor` . Targets (labels), a probability distribution.

    """
    with tf.name_scope("SoftmaxCrossentropy"):
        return tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(y_pred,
                                                                      y_true))


def categorical_crossentropy(y_pred, y_true):
    """ Categorical Crossentropy.

    Computes cross entropy between y_pred (logits) and y_true (labels).

    Measures the probability error in discrete classification tasks in which
    the classes are mutually exclusive (each entry is in exactly one class).
    For example, each CIFAR-10 image is labeled with one and only one label:
    an image can be a dog or a truck, but not both.

    `y_pred` and `y_true` must have the same shape `[batch_size, num_classes]`
    and the same dtype (either `float32` or `float64`). It is also required
    that `y_true` (labels) are binary arrays (For example, class 2 out of a
    total of 5 different classes, will be define as [0., 1., 0., 0., 0.])

    Arguments:
        y_pred: `Tensor`. Predicted values.
        y_true: `Tensor` . Targets (labels), a probability distribution.

    """
    with tf.name_scope("Crossentropy"):
        y_pred /= tf.reduce_sum(y_pred,
                                reduction_indices=len(y_pred.get_shape())-1,
                                keep_dims=True)
        # manual computation of crossentropy
        y_pred = tf.clip_by_value(y_pred, tf.cast(_EPSILON, dtype=_FLOATX),
                                  tf.cast(1.-_EPSILON, dtype=_FLOATX))
        cross_entropy = - tf.reduce_sum(y_true * tf.log(y_pred),
                               reduction_indices=len(y_pred.get_shape())-1)
        return tf.reduce_mean(cross_entropy)


def binary_crossentropy(y_pred, y_true):
    """ Binary Crossentropy.

    Computes sigmoid cross entropy between y_pred (logits) and y_true
    (labels).

    Measures the probability error in discrete classification tasks in which
    each class is independent and not mutually exclusive. For instance,
    one could perform multilabel classification where a picture can contain
    both an elephant and a dog at the same time.

    For brevity, let `x = logits`, `z = targets`.  The logistic loss is

      x - x * z + log(1 + exp(-x))

    To ensure stability and avoid overflow, the implementation uses

      max(x, 0) - x * z + log(1 + exp(-abs(x)))

    `y_pred` and `y_true` must have the same type and shape.

    Arguments:
        y_pred: `Tensor` of `float` type. Predicted values.
        y_true: `Tensor` of `float` type. Targets (labels).

    """
    with tf.name_scope("BinaryCrossentropy"):
        return tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(y_pred,
                                                                      y_true))


def mean_square(y_pred, y_true):
    """ Mean Square Loss.

    Arguments:
        y_pred: `Tensor` of `float` type. Predicted values.
        y_true: `Tensor` of `float` type. Targets (labels).

    """
    with tf.name_scope("MeanSquare"):
        return tf.reduce_mean(tf.square(y_pred - y_true))


def hinge_loss(y_pred, y_true):
    """ Hinge Loss.

    Arguments:
        y_pred: `Tensor` of `float` type. Predicted values.
        y_true: `Tensor` of `float` type. Targets (labels).

    """
    with tf.name_scope("HingeLoss"):
        return tf.reduce_mean(tf.maximum(1. - y_true * y_pred, 0.))
