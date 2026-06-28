from __future__ import annotations

from math import cos, radians, sin
from typing import Iterable

import numpy as np


Vector = Iterable[float]


def normalize_axis(axis: Vector) -> np.ndarray:
    vector = np.array(axis, dtype=float)
    norm = np.linalg.norm(vector)
    if norm == 0:
        raise ValueError("axis must be non-zero")
    return vector / norm


def rotation_matrix(axis: Vector, angle_degrees: float) -> np.ndarray:
    """Return a 3x3 Rodrigues rotation matrix."""
    x, y, z = normalize_axis(axis)
    angle = radians(angle_degrees)
    c = cos(angle)
    s = sin(angle)
    one_minus_c = 1 - c
    return np.array(
        [
            [c + x * x * one_minus_c, x * y * one_minus_c - z * s, x * z * one_minus_c + y * s],
            [y * x * one_minus_c + z * s, c + y * y * one_minus_c, y * z * one_minus_c - x * s],
            [z * x * one_minus_c - y * s, z * y * one_minus_c + x * s, c + z * z * one_minus_c],
        ],
        dtype=float,
    )


def reflection_matrix(normal: Vector) -> np.ndarray:
    """Return the matrix for reflection through the plane normal to `normal`."""
    unit = normalize_axis(normal)
    return np.identity(3) - 2 * np.outer(unit, unit)


def inversion_matrix() -> np.ndarray:
    """Return the matrix for inversion through the origin."""
    return -np.identity(3)


def rotoinversion_matrix(axis: Vector, angle_degrees: float) -> np.ndarray:
    """Return the matrix for rotation followed by inversion through the origin."""
    return -rotation_matrix(axis, angle_degrees)


def generate_cyclic_rotations(axis: Vector, order: int) -> list[np.ndarray]:
    if order < 1:
        raise ValueError("order must be positive")
    step = 360 / order
    return [rotation_matrix(axis, step * i) for i in range(order)]


def operation_label(operation: dict) -> str:
    kind = operation.get("kind", "operation")
    if kind == "identity":
        return "E"
    if kind == "rotation":
        return operation.get("label") or f"C{operation['order']}"
    if kind == "mirror":
        return operation.get("label", "mirror")
    if kind == "inversion":
        return "inversion"
    if kind == "rotoinversion":
        return operation.get("label") or f"S{operation['order']}"
    return operation.get("label", kind)
