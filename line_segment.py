import numpy as np

class LineSegment:
    def __init__(self, point_a, point_b):
        self._support_vector = np.array(point_a)
        diff_vector = np.subtract(point_b, point_a)
        self._length = np.linalg.norm(diff_vector)
        self._direction_vector = normalize_vector(diff_vector)

    def get_length(self):
        return self._length

    def get_point(self, parameter):
        return self._support_vector + parameter * self._direction_vector

    def is_parallel_to(self, other, tolerance=1e-7):
        a = self._direction_vector
        b = other._direction_vector
        return 1 - np.abs(np.dot(a, b)) < tolerance

    def get_intersection_parameter(self, other):
        if self.is_parallel_to(other):
            print('parallel')
            return None
        b = np.subtract(self._support_vector, other._support_vector)
        A = np.array([-self._direction_vector, other._direction_vector]).T
        x = np.linalg.solve(A, b)
        if x[0] < 0 or x[0] > self._length:
            return None
        if x[1] < 0 or x[1] > other._length:
            return None
        return x[0]

    def get_intersection_point(self, other):
        t = self.get_intersection_parameter(other)
        if t is None:
            return None
        return self.get_point(t)


def normalize_vector(v):
    norm = np.linalg.norm(v)
    if norm > 0:
        v = np.divide(v, norm)
    return v