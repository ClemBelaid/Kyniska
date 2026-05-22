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
def visualiser_3D(mire_json, ecran_json):
    mire_dict = charger_points(mire_json, est_2d=False)
    ecran_dict = charger_points(ecran_json, est_2d=True)

    pts_mire = np.array(list(mire_dict.values()))
    pts_ecran = np.array(list(ecran_dict.values()))


    centre_obs = pts_ecran[0] 
    centre_mire_brute = pts_mire.mean(axis=0)

    # On téléporte la mire au-dessus des croix rouges à 100 mm de haut
    T_M_DEMO = np.array([
        [1.0, 0.0, 0.0, centre_obs[0] - centre_mire_brute[0]],
        [0.0, 1.0, 0.0, centre_obs[1] - centre_mire_brute[1]],
        [0.0, 0.0, 1.0, 100.0 - centre_mire_brute[2]],
        [0.0, 0.0, 0.0, 1.0]
    ])

    ones = np.ones((pts_mire.shape[0], 1))
    pts_mire_homo = np.hstack((pts_mire, ones))
    pts_transformes = (T_M_DEMO @ pts_mire_homo.T).T[:, :3]

    # --- GRAPHISME MATPLOTLIB ---
    fig = plt.figure(figsize=(11, 8))
    ax = fig.add_subplot(111, projection='3d')
    plt.subplots_adjust(bottom=0.2)

    ax.set_xlabel("X (mm)")
    ax.set_ylabel("Y (mm)")
    ax.set_zlabel("Z (mm)")

    z_sol = -20
    
    # Plaque grise (Écran)
    x_min, x_max = pts_ecran[:, 0].min() - 20, pts_ecran[:, 0].max() + 20
    y_min, y_max = pts_ecran[:, 1].min() - 20, pts_ecran[:, 1].max() + 20
    X_surface, Y_surface = np.meshgrid([x_min, x_max], [y_min, y_max])
    Z_surface = np.full_like(X_surface, z_sol)
    ax.plot_surface(X_surface, Y_surface, Z_surface, color='gray', alpha=0.15, edgecolor='black', linewidth=1.2)

    # Croix Rouges
    ax.scatter(pts_ecran[:, 0], pts_ecran[:, 1], np.full_like(pts_ecran[:, 0], z_sol), color='red', marker='x', s=120, label='Obs Écran')

    # Nouveau centre de rotation
    x_center = pts_transformes[:, 0].mean()
    y_center = pts_transformes[:, 1].mean()
    centre_rotation = np.array([x_center, y_center, 0.0])

    # Tracé des cercles de trajectoire
    angles_full = np.linspace(0, 2 * np.pi, 360)
    for pt_3d in pts_transformes:
        trajectoire_x = []
        trajectoire_y = []
        pt_relatif = pt_3d - centre_rotation
        for a in angles_full:
            x_rot = pt_relatif[0] * np.cos(a) - pt_relatif[1] * np.sin(a) + x_center
            y_rot = pt_relatif[0] * np.sin(a) + pt_relatif[1] * np.cos(a) + y_center
            trajectoire_x.append(x_rot)
            trajectoire_y.append(y_rot)
        ax.plot(trajectoire_x, trajectoire_y, z_sol, color='deepskyblue', linestyle='-', alpha=0.2, linewidth=1)

    # Objets dynamiques
    scatter_mire = ax.scatter([], [], [], color='blue', s=60, label='Mire 3D Dynamique')
    lignes = [ax.plot([], [], [], color='darkorange', linestyle='--', alpha=0.7, linewidth=1.5)[0] for _ in range(len(pts_transformes))]
    scatter_pieds = ax.scatter([], [], [], color='deepskyblue', s=20, alpha=0.6)

    # On centre la caméra DE FORCE sur la zone du paquet de croix rouges
    ax.set_xlim3d(centre_obs[0] - 100, centre_obs[0] + 100)
    ax.set_ylim3d(centre_obs[1] - 100, centre_obs[1] + 100)
    ax.set_zlim3d(-50, 150)
    ax.legend()

    auto_rotate = False
    ax_btn = plt.axes([0.1, 0.05, 0.2, 0.06])
    btn = Button(ax_btn, 'Auto-Rotate: OFF', color='lightgray', hovercolor='skyblue')

    def toggle_rotation(event):
        nonlocal auto_rotate
        auto_rotate = not auto_rotate
        btn.label.set_text(f"Auto-Rotate: {'ON' if auto_rotate else 'OFF'}")
        if auto_rotate:
            anim.event_source.start()
        else:
            anim.event_source.stop()
        fig.canvas.draw_idle()
    btn.on_clicked(toggle_rotation)

    # --- MOTEUR D'ANIMATION ---
    def animate(frame):
        nonlocal auto_rotate
        alpha_rad = np.radians(frame)
        
        R_dynamic = np.array([
            [np.cos(alpha_rad), -np.sin(alpha_rad), 0],
            [np.sin(alpha_rad),  np.cos(alpha_rad), 0],
            [0,                  0,                 1]
        ])
        
        pts_relatifs = pts_transformes - centre_rotation
        pts_rotates = (R_dynamic @ pts_relatifs.T).T
        pts_courants = pts_rotates + centre_rotation
        
        scatter_mire._offsets3d = (pts_courants[:, 0], pts_courants[:, 1], pts_courants[:, 2])
        
        pieds_x, pieds_y = [], []
        for i, pt_3d in enumerate(pts_courants):
            x1, y1, z1 = pt_3d[0], pt_3d[1], pt_3d[2]
            
            # LA CORRECTION DES LIGNES ORANGE EST ICI
            x0, y0, z0 = x1, y1, z_sol
            
            lignes[i].set_data([x0, x1], [y0, y1])
            lignes[i].set_3d_properties([z0, z1])
            
            pieds_x.append(x0)
            pieds_y.append(y0)
            
        scatter_pieds._offsets3d = (pieds_x, pieds_y, np.full_like(pieds_x, z_sol))

        if auto_rotate:
            ax.view_init(elev=20, azim=frame)
            
        ax.set_title(f"Kyniska V6 (DÉMO FIXÉE) - Angle : {frame}°")
        return [scatter_mire, scatter_pieds] + lignes

    anim = animation.FuncAnimation(fig, animate, frames=360, interval=30, blit=False)
    anim.event_source.stop()
    
    plt.show()

if __name__ == '__main__':
    visualiser_3D(MIRE_PATH, OBS_PATH)