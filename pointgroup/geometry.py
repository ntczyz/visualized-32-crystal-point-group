from __future__ import annotations

import numpy as np

from .operations import normalize_axis


def axis_endpoints(axis, length: float = 4.0) -> tuple[np.ndarray, np.ndarray]:
    unit = normalize_axis(axis)
    return -0.5 * length * unit, 0.5 * length * unit


def mirror_plane_rotation(normal) -> tuple[float, np.ndarray]:
    """Return an angle/axis pair rotating the xy plane to the requested normal."""
    target = normalize_axis(normal)
    source = np.array([0.0, 0.0, 1.0])
    dot = float(np.clip(np.dot(source, target), -1.0, 1.0))
    if np.isclose(dot, 1.0):
        return 0.0, np.array([0.0, 0.0, 1.0])
    if np.isclose(dot, -1.0):
        return np.pi, np.array([1.0, 0.0, 0.0])
    axis = np.cross(source, target)
    angle = float(np.arccos(dot))
    return angle, normalize_axis(axis)

