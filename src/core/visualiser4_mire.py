import os
import json
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.widgets import Button
import numpy as np

# Importation sécurisée de tes classes
try:
    from src.core.mire import Mire
    from src.core.observation import Observation
except ImportError:
    # Fallback pour le mode standalone si exécuté en dehors de la structure
    class Mire:
        def __init__(self, points): self.points = points
    class Observation:
        def __init__(self, points2d): self.points2d = points2d

# --- CONFIGURATION DES FICHIERS ---
SAVE_GIF = False
curr_dir = os.path.dirname(__file__)

# Chemins par défaut pour les fichiers JSON issus de la génération
MIRE_JSON_PATH = os.path.join(curr_dir, 'mire.json')
OBS_JSON_PATH = os.path.join(curr_dir, 'observation.json')

def charger_donnees_json():
    """ Charge les fichiers JSON de génération ou génère des données par défaut s'ils n'existent pas """
    # Données par défaut au cas où la génération n'a pas encore écrit les fichiers
    default_mire = {0: [0.0, 0.0, 0.0], 1: [100.0, 0.0, 0.0], 2: [0.0, 100.0, 0.0], 3: [100.0, 100.0, 0.0]}
    default_obs = {0: [10.0, 12.0], 1: [110.0, 15.0], 2: [8.0, 95.0], 3: [105.0, 108.0]}

    # Chargement Mire 3D
    if os.path.exists(MIRE_JSON_PATH):
        with open(MIRE_JSON_PATH, 'r') as f:
            data = json.load(f)
            # Gestion des clés str issues du JSON -> conversion en int
            mire_data = {int(k): v for k, v in data.items()} if isinstance(data, dict) else {i: v for i, v in enumerate(data)}
    else:
        mire_data = default_mire

    # Chargement Observation 2D
    if os.path.exists(OBS_JSON_PATH):
        with open(OBS_JSON_PATH, 'r') as f:
            data = json.load(f)
            obs_data = {int(k): v for k, v in data.items()} if isinstance(data, dict) else {i: v for i, v in enumerate(data)}
    else:
        obs_data = default_obs

    return mire_data, obs_data

# Chargement initial
points_mire_dict, points_obs_dict = charger_donnees_json()

# Instanciation des objets selon ton architecture stricte
ma_mire = Mire(points=list(points_mire_dict.values()))
mon_observation = Observation(points2d=list(points_obs_dict.values()))

# Matrice numpy de base pour les calculs géométriques
PTS_BASE = np.array(list(points_mire_dict.values()), dtype=float)

# --- AXE DE ROTATION SPÉCIFIQUE (RODRIGUES) ---
# Définis ici l'axe de rotation demandé par Marc (ex: incliné à 45° ou selon un vecteur propre)
AXE_ROTATION = np.array([1.0, 1.0, 0.0]) # Exemple : Axe diagonal dans le plan XY
AXE_ROTATION = AXE_ROTATION / np.linalg.norm(AXE_ROTATION) # Normalisation de l'axe

def matrice_rotation_axe_quelconque(axe, angle_rad):
    """ Formule de Rodrigues pour tourner autour d'un axe spécifique quelconque """
    ux, uy, uz = axe
    cos_a = np.cos(angle_rad)
    sin_a = np.sin(angle_rad)
    one_minus_cos = 1.0 - cos_a
    
    R = np.array([
        [cos_a + ux**2 * one_minus_cos,     ux * uy * one_minus_cos - uz * sin_a, ux * uz * one_minus_cos + uy * sin_a],
        [uy * ux * one_minus_cos + uz * sin_a, cos_a + uy**2 * one_minus_cos,     uy * uz * one_minus_cos - ux * sin_a],
        [uz * ux * one_minus_cos - uy * sin_a, uz * uy * one_minus_cos + ux * sin_a, cos_a + uz**2 * one_minus_cos]
    ])
    return R

class RotationState:
    def __init__(self):
        self.active = False

state = RotationState()

def get_coords(points_input, is_2d=False):
    pts = np.array(list(points_input.values())) if isinstance(points_input, dict) else np.asarray(points_input)
    if pts.size == 0: return [], [], []
    x, y = pts[:, 0], pts[:, 1]
    z = pts[:, 2] if (not is_2d and pts.shape[1] > 2) else np.zeros_like(x)
    return x, y, z

# --- PRÉPARATIF DE LA FIGURE ---
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')
plt.subplots_adjust(bottom=0.2)

ax.set_xlabel("X (mm)")
ax.set_ylabel("Y (mm)")
ax.set_zlabel("Z (mm)")

# LE MEILLEUR AFFICHAGE : 
# 1. Le modèle 3D original (Mire) en bleu
scatter_mire = ax.scatter([], [], [], color='blue', s=60, label='Mire 3D (Modèle)')
# 2. Les points cibles réels capturés par l'écran (Observation de référence) en croix rouges fixes au sol (Z=-50)
scatter_obs = ax.scatter([], [], [], color='red', marker='x', s=120, linewidths=2, label='Observation de Réf (Écran)')
# 3. NOUVEAUTÉ : La projection virtuelle en direct de la mire sur l'écran (en petits ronds verts transparents)
scatter_proj = ax.scatter([], [], [], color='limegreen', alpha=0.6, s=40, edgecolors='g', label='Projection Virtuelle')

# 4. AFFICHAGE DE L'AXE DE ROTATION (Ligne noire en pointillés pour la réunion de 14h30)
t_line = np.linspace(-100, 200, 100)
axe_ligne_x = t_line * AXE_ROTATION[0]
axe_ligne_y = t_line * AXE_ROTATION[1]
axe_ligne_z = t_line * AXE_ROTATION[2]
ax.plot(axe_ligne_x, axe_ligne_y, axe_ligne_z, 'k--', alpha=0.7, label=f'Axe spécifique [{AXE_ROTATION[0]:.2f}, {AXE_ROTATION[1]:.2f}, {AXE_ROTATION[2]:.2f}]')

# Fixation des limites géométriques adaptées à l'axe et à la Mire
ax.set_xlim3d(-100, 200)
ax.set_ylim3d(-100, 200)
ax.set_zlim3d(-50, 150)
ax.legend(loc='upper right')

# Bouton d'interaction
ax_button = plt.axes([0.1, 0.05, 0.2, 0.06])
btn = Button(ax_button, 'Auto-Rotate: OFF', color='lightgray', hovercolor='skyblue')

def toggle_rotation(event):
    state.active = not state.active
    btn.label.set_text(f"Auto-Rotate: {'ON' if state.active else 'OFF'}")
    fig.canvas.draw_idle()

btn.on_clicked(toggle_rotation)

def animate(frame):
    angle = np.radians(frame)
    
    # Application de la rotation autour de l'axe spécifique choisi par Marc
    R = matrice_rotation_axe_quelconque(AXE_ROTATION, angle)
    pts_transfo = PTS_BASE @ R.T
    
    # Extraction des coordonnées pour la mire 3D
    mx, my, mz = get_coords(pts_transfo)
    
    # Extraction des coordonnées de l'observation 2D de référence (on la fixe graphiquement à la base Z=-50 pour l'effet écran)
    obs_data = getattr(mon_observation, 'points2d', getattr(mon_observation, 'points', []))
    ox, oy, _ = get_coords(obs_data, is_2d=True)
    oz = np.full_like(ox, -50) # Positionnement sur le "sol" ou plan de l'écran virtuel
    
    # LA PROJECTION VIRTUELLE : on projette la mire 3D sur le même plan écran (Z=-50) pour analyser le recalage
    px, py = mx, my # Projection orthogonale simple (ou perspective si Rayan a fini sa matrice)
    pz = np.full_like(px, -50)

    # Mise à jour des objets graphiques
    scatter_mire._offsets3d = (mx, my, mz)
    scatter_obs._offsets3d = (ox, oy, oz)
    scatter_proj._offsets3d = (px, py, pz)

    if state.active:
        ax.view_init(elev=25, azim=frame/2)
    
    ax.set_title(f"Kyniska - Rotation Axe Spécifique - Frame {frame}")
    return scatter_mire, scatter_obs, scatter_proj

anim = animation.FuncAnimation(fig, animate, frames=360, interval=30, blit=False)
print("🚀 Prêt pour la démo de 14h30 avec le chargement JSON et la projection active !")
plt.show()