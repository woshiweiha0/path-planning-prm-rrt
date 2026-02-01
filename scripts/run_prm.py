import os
import time
import matplotlib.pyplot as plt

from src.environment_2d import Environment2D
from src.prm import prm_plan
from src.postprocess import shortcut_path, path_length


def main():
    seed = 4
    env = Environment2D(width = 10, height = 6, n_obs = 5, seed = seed)

    # sample two free points
    start = env.sample_free()
    goal = env.sample_free()
    if start is None or goal is None:
        print("Failed to sample start/goal.")
        return

    t0 = time.perf_counter()
    res = prm_plan(env, start, goal, n_samples = 250, k = 12, step = 0.05)
    dt = time.perf_counter() - t0

    # plot
    ax = env.plot()

    # draw edges lightly
    nodes = res.nodes
    for i, nbrs in res.edges.items():
        xi, yi = nodes[i]
        for j in nbrs:
            # draw each undirected edge once
            if j < i:
                continue
            xj, yj = nodes[j]
            ax.plot([xi, xj], [yi, yj], color = "limegreen", alpha = 0.25, linewidth = 0.8)

    # draw nodes
    xs = [p[0] for p in nodes]
    ys = [p[1] for p in nodes]
    ax.scatter(xs, ys, s = 12, color = "green")

    # draw start/goal
    ax.scatter([start[0]], [start[1]], marker = "s", s = 80, color = "blue")
    ax.scatter([goal[0]], [goal[1]], marker = "*", s = 120, color = "gold")


    # draw path if found
    if res.path is not None:
        raw_path = res.path
        raw_len = path_length(raw_path)

        # post-process
        short_path = shortcut_path(env, raw_path, maxrep = 800, segment_step = 0.05, seed = seed)
        short_len = path_length(short_path)

        # 1) plot original PRM path (thin red)
        rx = [p[0] for p in raw_path]
        ry = [p[1] for p in raw_path]
        ax.plot(rx, ry, color = "red", linewidth = 2, alpha = 0.5)

        # 2) plot shortcut path (thick red)
        sx = [p[0] for p in short_path]
        sy = [p[1] for p in short_path]
        ax.plot(sx, sy, color = "red", linewidth = 3.5, alpha = 1.0)

        print(f"PRM raw path length       = {raw_len:.3f}")
        print(f"PRM shortcut path length  = {short_len:.3f}")
    else:
        print("PRM did not find a path.")



    # stats
    # count edges (undirected count)
    edge_count = sum(len(v) for v in res.edges.values()) // 2
    print(f"nodes = {len(res.nodes)}, edges = {edge_count}, runtime = {dt * 1000:.1f} ms")

    os.makedirs("outputs/plots", exist_ok = True)
    out = f"outputs/plots/prm_seed{seed}_shortcut.png"
    plt.savefig(out, dpi = 200, bbox_inches = "tight")
    plt.close()
    print(f"Saved plot to: {out}")


if __name__ == "__main__":
    main()
