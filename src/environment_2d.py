"""
2D environment with triangular obstacles

Provides:
- random triangle obstacles (seeded)
- check_collision(x, y): True if point is inside any triangle or outside bounds
- plot(): visualize obstacles + start/goal + roadmap/tree
"""

from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
from src.collision import point_in_triangle


class Environment2D:
    def __init__(self, width: float = 10.0, height: float = 6.0, n_obs: int = 5, seed: int | None = None):
        self.width = float(width)
        self.height = float(height)
        self.n_obs = int(n_obs)
        self.rng = np.random.default_rng(seed)
        self.obstacles: list[tuple[tuple[float, float], tuple[float, float], tuple[float, float]]] = []
        self._generate_random_triangles()

    def _generate_random_triangles(self):
        """
        Generate n_obs random triangles
        Method: pick 3 random points near a random center
        """
        self.obstacles.clear()

        for _ in range(self.n_obs):
            # pick a center away from borders
            cx = float(self.rng.uniform(1.0, self.width - 1.0))
            cy = float(self.rng.uniform(1.0, self.height - 1.0))

            # random triangle "radius"
            r = float(self.rng.uniform(0.4, 1.1))

            pts = []
            for _k in range(3):
                ang = float(self.rng.uniform(0, 2 * np.pi))
                rad = float(self.rng.uniform(0.2 * r, r))
                x = cx + rad * np.cos(ang)
                y = cy + rad * np.sin(ang)

                # clamp into bounds
                x = float(np.clip(x, 0.0, self.width))
                y = float(np.clip(y, 0.0, self.height))
                pts.append((x, y))

            a, b, c = pts[0], pts[1], pts[2]
            self.obstacles.append((a, b, c))

    def check_collision(self, x: float, y: float) -> bool:
        """
        True if (x,y) is in obstacle OR outside the environment box
        False means free space (C_free)
        """
        # outside bounds treated as collision
        if x < 0.0 or x > self.width or y < 0.0 or y > self.height:
            return True

        p = (x, y)
        for (a, b, c) in self.obstacles:
            if point_in_triangle(p, a, b, c):
                return True
        return False

    def sample_free(self, max_tries: int = 5000) -> tuple[float, float] | None:
        """
        Sample a random collision-free point in [0,width]x[0,height]
        """
        for _ in range(max_tries):
            x = float(self.rng.uniform(0.0, self.width))
            y = float(self.rng.uniform(0.0, self.height))
            if not self.check_collision(x, y):
                return (x, y)
        return None

    def plot(self, ax=None):
        if ax is None:
            fig, ax = plt.subplots()

        # draw border
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)
        ax.set_aspect("equal", adjustable="box")

        # draw triangles
        for (a, b, c) in self.obstacles:
            xs = [a[0], b[0], c[0], a[0]]
            ys = [a[1], b[1], c[1], a[1]]
            ax.plot(xs, ys)

        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title("Environment2D (triangular obstacles)")
        return ax
