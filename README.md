# path-planning-prm

This repository implements the **Probabilistic Roadmap (PRM)** algorithm for solving a **2D motion planning problem with polygonal (triangular) obstacles**, following the standard sampling-based planning exercise.

The exercise demonstrates:
- Sampling collision-free configurations
- Building a roadmap in configuration space
- Connecting start and goal via graph search
- Visualizing the environment, roadmap, and final path

---


## How to Run

### 1. Install dependencies
pip install -r requirements.txt
### 2. Run PRM
python -m scripts.run_prm


### Notes
- **`scripts/run_prm.py`** is the main entry point to reproduce results.
- **`plots/`** contains pre-generated figures


