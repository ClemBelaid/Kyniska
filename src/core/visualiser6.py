import os
import json
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib import animation
from geometry import build_basis
from matplotlib.widgets import Button
import numpy as np

# --- CONFIGURATION DES CHEMINS ---
BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))

MIRE_PATH = os.path.join(BASE_DIR, "newMire")
if not os.path.exists(MIRE_PATH) and os.path.exists(MIRE_PATH + ".json"):
    MIRE_PATH += ".json"

OBS_PATH = os.path.join(BASE_DIR, "obs_ref")
if not os.path.exists(OBS_PATH) and os.path.exists(OBS_PATH + ".json"):
    OBS_PATH += ".json"

# Matrice de recalage (10° autour de Z + 30mm sur X)
tht = np.pi / 18
T_M_GENERER =mat = np.array([
    [1, 0, 0, 0],
    [0,1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
    ])
"""np.array([
    [np.cos(tht), -np.sin(tht), 0.0, 30.0],
    [np.sin(tht),  np.cos(tht), 0.0,  0.0],
    [0.0,          0.0,         1.0,  0.0],
    [0.0,          0.0,         0.0,  1.0]
])"""

def charger_points(json_path, est_2d=False):
    with open(json_path, 'r', encoding='utf-8') as f:
        content = json.load(f)
    points_dict = {}
    if isinstance(content, dict) and "points" in content:
        for pt in content["points"]:
            pid = int(pt["id"])
            if est_2d:
                points_dict[pid] = [float(pt["x"]), float(pt["y"])]
            else:
                points_dict[pid] = [float(pt["x"]), float(pt["y"]), float(pt.get("z", 0.0))]
    elif isinstance(content, dict):
        for k, v in content.items():
            pid = int(k)
            if est_2d:
                points_dict[pid] = [float(v[0]), float(v[1])]
            else:
                z_val = float(v[2]) if len(v) > 2 else 0.0
                points_dict[pid] = [float(v[0]), float(v[1]), z_val]
    return points_dict

# --- FONCTION PRINCIPALE ---
def visualiser_3D(mire_json, ecran_json, T_M):
    mire_dict = charger_points(mire_json, est_2d=False)
    ecran_dict = charger_points(ecran_json, est_2d=True)

    pts_mire = np.array(list(mire_dict.values()))
    pts_ecran = np.array(list(ecran_dict.values()))

# =========================
# DEFINITION VRAI ECRAN
# =========================

    vn = np.array([0, 0, 1]) # A REMPLACER PAR TON v2 REEL

    origin = np.array([0.0, 0.0, 0.0])

    u1, u2  = build_basis(vn)

    # Reconstruction 3D des observations
    pts_ecran_3d = []

    for obs in pts_ecran:
        u, v = obs

        pt3d = origin + u*u1 + v*u2

        pts_ecran_3d.append(pt3d)

    pts_ecran_3d = np.array(pts_ecran_3d)
    # Application de la transformation T_M sur la mire 3D
    ones = np.ones((pts_mire.shape[0], 1))
    pts_mire_homo = np.hstack((pts_mire, ones))
    pts_transformes = (T_M @ pts_mire_homo.T).T[:, :3]

    # --- GRAPHISME MATPLOTLIB ---
    fig = plt.figure(figsize=(11, 8))
    ax = fig.add_subplot(111, projection='3d')
    plt.subplots_adjust(bottom=0.2)

    ax.set_xlabel("X (mm)")
    ax.set_ylabel("Y (mm)")
    ax.set_zlabel("Z (mm)")

    # 1. Tracé de la mire transformée (Billes bleues)
    scatter_mire = ax.scatter(pts_transformes[:, 0], pts_transformes[:, 1], pts_transformes[:, 2], color='blue', s=60, label='Mire 3D ($T_M$)')
    
    # =========================
# AFFICHAGE VRAI PLAN ECRAN
# =========================

    s = 150

    corners = [
    origin + s*u1 + s*u2,
    origin + s*u1 - s*u2,
    origin - s*u1 - s*u2,
    origin - s*u1 + s*u2
    ]

    X_surface = np.array([
    [corners[0][0], corners[1][0]],
    [corners[3][0], corners[2][0]]
    ])

    Y_surface = np.array([
    [corners[0][1], corners[1][1]],
    [corners[3][1], corners[2][1]]
    ])

    Z_surface = np.array([
    [corners[0][2], corners[1][2]],
    [corners[3][2], corners[2][2]]
    ])

    ax.plot_surface(
    X_surface,
    Y_surface,
    Z_surface,
    color='gray',
    alpha=0.15,
    edgecolor='black'
    )

    # 3. Tracé des observations réelles (Croix rouges)
    scatter_obs = ax.scatter(
    pts_ecran_3d[:, 0],
    pts_ecran_3d[:, 1],
    pts_ecran_3d[:, 2], color='red', marker='x', s=120, label='Obs Écran')

    # 4. TRACÉ DES PROJECTIONS PARFAITEMENT PERPENDICULAIRES
    lignes = []
    for i in range(len(pts_transformes)):

        pt_3d = pts_transformes[i]

        dist = np.dot(pt_3d - origin, vn)

        proj = pt_3d - dist * vn

        line, = ax.plot(
        [pt_3d[0], proj[0]],
        [pt_3d[1], proj[1]],
        [pt_3d[2], proj[2]],
        color='darkorange',
        linestyle='--',
        alpha=0.7,
        linewidth=1.5
        )

        lignes.append(line)

        ax.scatter(
        proj[0],
        proj[1],
        proj[2],
        color='deepskyblue',
        s=20
        )

    ax.set_xlim3d(-50, 150)
    ax.set_ylim3d(-50, 150)
    ax.set_zlim3d(-50, 150)
    ax.legend()

    # Bouton d'interaction
    ax_btn = plt.axes([0.1, 0.05, 0.2, 0.06])
    btn = Button(ax_btn, 'Auto-Rotate: OFF', color='lightgray', hovercolor='skyblue')
    
    visualiser_3D.auto_rotate = False

    def toggle_rotation(event):
        visualiser_3D.auto_rotate = not visualiser_3D.auto_rotate
        btn.label.set_text(f"Auto-Rotate: {'ON' if visualiser_3D.auto_rotate else 'OFF'}")
        fig.canvas.draw_idle()
    btn.on_clicked(toggle_rotation)

    def animate(frame):
        if visualiser_3D.auto_rotate:
            ax.view_init(elev=20, azim=frame)
        ax.set_title("Kyniska V5 - Projection Orthogonale (Perpendiculaire)")
        return [scatter_mire, scatter_obs] + lignes

    anim = animation.FuncAnimation(fig, animate, frames=360, interval=30, blit=False)
    plt.show()
"""def visualiser_iteration(mire, observ, screen, angle=0, rms=0):

    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111, projection='3d')

    vn = screen["normal"]
    origin = screen["origin"]
    u1 = screen["u1"]
    u2 = screen["u2"]

    # =========================
    # MIRE 3D
    # =========================

    pts_mire = np.array(list(mire.pts.values()))

    ax.scatter(
        pts_mire[:,0],
        pts_mire[:,1],
        pts_mire[:,2],
        color='blue',
        s=60,
        label='Mire'
    )

    # =========================
    # PLAN ECRAN
    # =========================

    s = 150

    corners = [
        origin + s*u1 + s*u2,
        origin + s*u1 - s*u2,
        origin - s*u1 - s*u2,
        origin - s*u1 + s*u2
    ]

    X = np.array([
        [corners[0][0], corners[1][0]],
        [corners[3][0], corners[2][0]]
    ])

    Y = np.array([
        [corners[0][1], corners[1][1]],
        [corners[3][1], corners[2][1]]
    ])

    Z = np.array([
        [corners[0][2], corners[1][2]],
        [corners[3][2], corners[2][2]]
    ])

    ax.plot_surface(
        X, Y, Z,
        color='gray',
        alpha=0.2
    )

    # =========================
    # OBSERVATIONS
    # =========================

    obs_pts = []

    for pt2d in observ.points:

        x = pt2d[0]
        y = pt2d[1]

        pt3d = origin + x*u1 + y*u2

        obs_pts.append(pt3d)

    obs_pts = np.array(obs_pts)

    ax.scatter(
        obs_pts[:,0],
        obs_pts[:,1],
        obs_pts[:,2],
        color='red',
        marker='x',
        s=100,
        label='Projection'
    )

    # =========================
    # LIGNES DE PROJECTION
    # =========================

    for i, pt3d in enumerate(pts_mire):

        proj = obs_pts[i]

        ax.plot(
            [pt3d[0], proj[0]],
            [pt3d[1], proj[1]],
            [pt3d[2], proj[2]],
            '--',
            color='orange'
        )

    ax.set_title(f"Angle={angle:.3f} | RMS={rms:.6f}")

    ax.legend()

    plt.show()

if __name__ == '__main__':
    visualiser_3D(MIRE_PATH, OBS_PATH, T_M_GENERER)"""
