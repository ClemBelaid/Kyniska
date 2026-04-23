"""a simple python script to create figures for the raport"""

import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt
from pathlib import Path
import sys
import math
import subprocess
import os
from matplotlib.patches import FancyArrowPatch


def cross_ratio(A,B,C,D):
    return float((norm(A - C) * norm(B - D)) / (norm(A - D) * norm(B - C)))

def ortho_proj(x, p0, v):
    # projection orthogonal sur la ligne { p0 + t*v }
    v_unit = v / norm(v)
    return p0 + np.dot(x - p0, v_unit) * v_unit

# credit : claude code
def draw_right_angle(ax, P, u, v, size=0.2, **kwargs):
    """
    Draw a right-angle marker at point P between directions u and v.

    Parameters
    ----------
    ax : matplotlib Axes
        Target axes.
    P : array-like, shape (2,)
        Vertex of the angle.
    u, v : array-like, shape (2,)
        Direction vectors (must be perpendicular).
    size : float
        Marker size in data units.
    kwargs :
        Passed to ax.plot (e.g. color, linewidth).
    """
    P = np.asarray(P, dtype=float)
    u = np.asarray(u, dtype=float)
    v = np.asarray(v, dtype=float)

    u /= np.linalg.norm(u)
    v /= np.linalg.norm(v)

    pts = np.vstack([
        P + size * u,
        P + size * (u + v),
        P + size * v
    ])

    ax.plot(pts[:, 0], pts[:, 1], **kwargs)


def draw_projection_ray(ax, P, P2, back=0.1, forward=0.25, **kwargs):
    """
    Draw a projection ray as an arrow from P toward P2,
    starting slightly before P2.

    Parameters
    ----------
    ax : matplotlib Axes
    P : ndarray (2,)
        Original point.
    P2 : ndarray (2,)
        Projected point.
    back : float
        How much the arrow starts before P2 (data units).
    forward : float
        Arrow length past the start point.
    kwargs :
        Passed to FancyArrowPatch (color, linewidth, etc.)
    """
    d = P2 - P
    d /= np.linalg.norm(d)

    start = P2 - back * d
    end   = start + forward * d

    arrow = FancyArrowPatch(
        start, end,
        arrowstyle='->',
        shrinkA=0, shrinkB=0,
        mutation_scale=10,
        **kwargs
    )
    ax.add_patch(arrow)

# parametrage de la droite
angle = math.pi / 5
p = np.array([0.8, 0.4])
u = np.array([np.cos(angle), np.sin(angle)])

# choix de quatre points
t = np.array([-1.5, -0.2, 0.7, 2.1])
A, B, C, D = [p + ti * u for ti in t]

angle_proj = math.pi / 7
v = np.array([np.cos(angle_proj), np.sin(angle_proj)])

p0 = np.array([1, -1.1])
A2, B2, C2, D2 = [ortho_proj(pt, p0, v) for pt in [A, B, C, D]]

fig, ax = plt.subplots()

# ligne source
tt = np.linspace(t.min() - 0.5, t.max() + 0.5, 100)
src_line = p + tt[:, None] * u
ax.plot(src_line[:, 0], src_line[:, 1], label="ligne source")

# ligne projection
v_unit = v / norm(v)
s_vals = [np.dot(pt - p, v_unit) for pt in [A2, B2, C2, D2]]
smin, smax = min(s_vals), max(s_vals)
ss = np.linspace(smin - 0.8, smax + 0.8, 100)
proj_line = p0 + ss[:, None] * v_unit
ax.plot(proj_line[:, 0], proj_line[:, 1], label="linge de projection")

pts = [A, B, C, D]
pts2 = [A2, B2, C2, D2]
labels = ["A", "B", "C", "D"]

for P, P2, lab in zip(pts, pts2, labels):
    ax.scatter([P[0]], [P[1]], color="red")
    ax.text(P[0], P[1], f" {lab}", va="bottom", ha="left")
    ax.scatter([P2[0]], [P2[1]], color="red")
    ax.text(P2[0], P2[1], f" {lab}'", va="top", ha="left")

    draw_right_angle(ax, P2, P-P2, p0-P2,color="black", linewidth=0.6)

    ax.plot([P[0], P2[0]], [P[1], P2[1]], color="gray", linestyle="--", linewidth=1)
    # doesn't do what I want, to lazy to fix...
    # draw_projection_ray(
    #     ax, P, P2,
    #     back=0.08,
    #     forward=0.25,
    #     color="grey",
    #     linewidth=0.8
    # )

ax.set_aspect("equal", adjustable="box")
ax.set_title("Invariance projective du Bi-rapport avec projection orthogonal")
ax.legend()
ax.grid(True, linewidth=0.5)

fig_path = Path(__file__).resolve().parent / "figures" / "proj_ortho.png"
fig_path.parent.mkdir(parents=True, exist_ok=True)

plt.savefig(fig_path, dpi=200, bbox_inches="tight")

DRAW = os.getenv("DRAW")
if DRAW :
    subprocess.run(["kitty", "+kitten", "icat", str(fig_path)])
