"""
Collision helpers:
- point-in-triangle test (barycentric)
- segment collision test by sampling points along a segment
"""

from __future__ import annotations
import numpy as np

def point_in_triangle(p, a, b, c) -> bool:
    """
    Return True if point p is inside triangle (a,b,c)
    Uses barycentric technique with a small tolerance
    p, a, b, c: (x,y)
    """
    px, py = p
    ax, ay = a
    bx, by = b
    cx, cy = c

    v0 = (cx - ax, cy - ay)
    v1 = (bx - ax, by - ay)
    v2 = (px - ax, py - ay)

    dot00 = v0[0] * v0[0] + v0[1] * v0[1]
    dot01 = v0[0] * v1[0] + v0[1] * v1[1]
    dot02 = v0[0] * v2[0] + v0[1] * v2[1]
    dot11 = v1[0] * v1[0] + v1[1] * v1[1]
    dot12 = v1[0] * v2[0] + v1[1] * v2[1]

    denom = dot00 * dot11 - dot01 * dot01
    if abs(denom) < 1e-12:
        return False  # degenerate triangle

    inv = 1.0 / denom
    u = (dot11 * dot02 - dot01 * dot12) * inv
    v = (dot00 * dot12 - dot01 * dot02) * inv

    eps = 1e-9
    return (u >= -eps) and (v >= -eps) and (u + v <= 1.0 + eps)


def segment_is_collision_free(env, p1, p2, step: float = 0.05) -> bool:
    """
    Sample points along segment p1->p2 and ensure all are collision-free
    step: approximate spacing between samples (smaller = safer but slower)
    """
    x1, y1 = p1
    x2, y2 = p2
    dist = float(np.hypot(x2 - x1, y2 - y1))

    if dist == 0.0:
        return not env.check_collision(x1, y1)

    n = max(2, int(np.ceil(dist / step)) + 1)
    xs = np.linspace(x1, x2, n)
    ys = np.linspace(y1, y2, n)

    for x, y in zip(xs, ys):
        if env.check_collision(float(x), float(y)):
            return False
    return True
