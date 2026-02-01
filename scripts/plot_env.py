import os
import matplotlib.pyplot as plt
from src.environment_2d import Environment2D

def main():
    env = Environment2D(width=10, height=6, n_obs=5, seed=4)
    ax = env.plot()

    pts = [env.sample_free() for _ in range(50)]
    xs = [p[0] for p in pts if p is not None]
    ys = [p[1] for p in pts if p is not None]
    ax.scatter(xs, ys, s=10)

    os.makedirs("outputs/plots", exist_ok=True)
    outpath = "outputs/plots/env_debug.png"
    plt.savefig(outpath, dpi=200)
    print(f"Saved plot to: {outpath}")

    # Optional: keep show (might still not pop up)
    # plt.show()

if __name__ == "__main__":
    main()
