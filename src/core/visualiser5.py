import os
import json
import matplotlib.pyplot as plt
from matplotlib import animation
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
T_M_GENERER = np.array([
    [np.cos(tht), -np.sin(tht), 0.0, 30.0],
    [np.sin(tht),  np.cos(tht), 0.0,  0.0],
    [0.0,          0.0,         1.0,  0.0],
    [0.0,          0.0,         0.0,  1.0]
])

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
    
    # Altitude de l'écran
    z_sol = -20
    
    # 2. MODÉLISATION ET AFFICHAGE DE L'ÉCRAN PHYSIQUE (Rectangle gris)
    x_min, x_max = pts_ecran[:, 0].min() - 20, pts_ecran[:, 0].max() + 20
    y_min, y_max = pts_ecran[:, 1].min() - 20, pts_ecran[:, 1].max() + 20
    X_surface, Y_surface = np.meshgrid([x_min, x_max], [y_min, y_max])
    Z_surface = np.full_like(X_surface, z_sol)
    ax.plot_surface(X_surface, Y_surface, Z_surface, color='gray', alpha=0.15, edgecolor='black', linewidth=1.2)

    # 3. Tracé des observations (Croix rouges) sur l'écran
    scatter_obs = ax.scatter(pts_ecran[:, 0], pts_ecran[:, 1], np.full_like(pts_ecran[:, 0], z_sol), color='red', marker='x', s=120, label='Obs Écran')

    # 4. Association par proximité (Lignes oranges)
    lignes = []
    for i in range(len(pts_transformes)):
        pt_3d = pts_transformes[i]
        distances = np.sum((pts_ecran - pt_3d[:2])**2, axis=1)
        index_plus_proche = np.argmin(distances)
        pt_ecran_cible = pts_ecran[index_plus_proche]

        line, = ax.plot(
            [pt_3d[0], pt_ecran_cible[0]],
            [pt_3d[1], pt_ecran_cible[1]],
            [pt_3d[2], z_sol],
            color='darkorange', linestyle='--', alpha=0.6, linewidth=1.5
        )
        lignes.append(line)

    ax.set_xlim3d(-50, 150)
    ax.set_ylim3d(-50, 150)
    ax.set_zlim3d(-50, 150)
    ax.legend()

    # Bouton de rotation
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
        ax.set_title("Kyniska V5 - Écran Physique Modélisé")
        return [scatter_mire, scatter_obs] + lignes

    anim = animation.FuncAnimation(fig, animate, frames=360, interval=30, blit=False)
    plt.show()

if __name__ == '__main__':
    visualiser_3D(MIRE_PATH, OBS_PATH, T_M_GENERER)