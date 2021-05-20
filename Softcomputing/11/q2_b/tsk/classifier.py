from typing import Any
import numpy as np
from scipy.special import softmax
from sklearn.linear_model import LogisticRegression
from tsk.clustering import CMeansClustering


def compute_firing_level(data: np.ndarray, centers: int, delta: float) -> np.ndarray:
    d = -(np.expand_dims(data, axis=2) - np.expand_dims(centers.T, axis=0)) ** 2 / (2 * delta.T)
    d = np.exp(np.sum(d, axis=1))
    d = np.fmax(d, np.finfo(np.float64).eps)
    return d / np.sum(d, axis=1, keepdims=True)


def apply_firing_level(x: np.ndarray, firing_levels: np.ndarray, order: int = 1) -> np.ndarray:
    if order == 0:
        return firing_levels
    else:
        n = x.shape[0]
        firing_levels = np.expand_dims(firing_levels, axis=1)
        x = np.expand_dims(np.concatenate((x, np.ones([n, 1])), axis=1), axis=2)
        x = np.repeat(x, repeats=firing_levels.shape[1], axis=2)
        output = x * firing_levels
        output = output.reshape([n, -1])

        return output


class Classifier:
    def __init__(self, c: float = 1., max_iters: int = 200, n_cluster: int = 2, order: int = 1):
        self._c = c
        self._max_iters = max_iters
        self._n_clusters = n_cluster
        self._order = order

        self._n_classes = None
        self._center = None
        self._variance = None
        self._regression = None

    def fit(self, x: np.ndarray, y: np.ndarray) -> Any:
        self._n_classes = len(np.unique(y))
        cluster = CMeansClustering(self._n_clusters).fit(x, y)
        self._center = cluster.center
        self._variance = cluster.delta
        mu_a = compute_firing_level(x, self._center, self._variance)
        computed_input = apply_firing_level(x, mu_a, self._order)
        self._regression = LogisticRegression(C=self._c, max_iter=self._max_iters)
        self._regression.fit(computed_input, y)
        return self

    def predict(self, x: np.ndarray) -> np.ndarray:
        firing_levels = compute_firing_level(x, self._center, self._variance)
        computed_input = apply_firing_level(x, firing_levels, self._order)
        logits = self._regression.decision_function(computed_input)
        return np.argmax(softmax(logits, axis=1), axis=1)
