import os
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.widgets import Button  # Pour le bouton
import numpy as np

from src.core.mire import Mire
from src.core.observation import Observation

# --- CONFIGURATION ---
SAVE_GIF = False
curr_dir = os.path.dirname(__file__)

points_dict = {
    0: [0.0, 0.0, 0.0], 
    1: [100.0, 0.0, 0.0], 
    2: [0.0, 100.0, 0.0], 
    3: [100.0, 100.0, 0.0]
}

# Variable d'état pour la rotation
class RotationState:
    def __init__(self):
        self.active = False  # Par défaut, c'est toi qui tournes à la souris

state = RotationState()

ma_mire = Mire(points=list(points_dict.values()))
points_2d_seuls = [pt[:2] for pt in points_dict.values()]
mon_observation = Observation(points2d=points_2d_seuls) 

def get_coords(points_input, is_2d=False):
    if isinstance(points_input, dict):
        pts = np.array(list(points_input.values()), dtype=float)
    else:
        pts = np.asarray(points_input, dtype=float)
    if pts.size == 0: return [], [], []
    x, y = pts[:, 0], pts[:, 1]
    z = pts[:, 2] if (not is_2d and pts.shape[1] > 2) else np.zeros_like(x)
    return x, y, z

# --- PRÉPARATIF DE LA FIGURE ---
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
plt.subplots_adjust(bottom=0.2) # On laisse de la place pour le bouton

scatter_mire = ax.scatter([], [], [], color='blue', s=50, label='Mire 3D (Modèle)')
scatter_obs = ax.scatter([], [], [], color='red', marker='x', s=100, label='Observation (Écran)')

ax.set_xlim3d(-50, 150)
ax.set_ylim3d(-50, 150)
ax.set_zlim3d(-50, 150)
ax.legend()

# --- GESTION DU BOUTON ---
ax_button = plt.axes([0.1, 0.05, 0.2, 0.075]) # Position du bouton [gauche, bas, largeur, hauteur]
btn = Button(ax_button, 'Auto-Rotate: OFF', color='lightgray', hovercolor='skyblue')

def toggle_rotation(event):
    state.active = not state.active
    btn.label.set_text(f"Auto-Rotate: {'ON' if state.active else 'OFF'}")
    fig.canvas.draw_idle()

btn.on_clicked(toggle_rotation)

# --- ANIMATION ---
def animate(frame):
    angle = np.radians(frame)
    rotation_z = np.array([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle),  np.cos(angle), 0],
        [0, 0, 1]
    ])
    
    pts_base = np.array(list(points_dict.values()))
    pts_transfo = pts_base @ rotation_z.T
    mx, my, mz = get_coords(pts_transfo)
    
    obs_data = getattr(mon_observation, 'points2d', getattr(mon_observation, 'points', []))
    ox, oy, oz = get_coords(obs_data, is_2d=True)

    scatter_mire._offsets3d = (mx, my, mz)
    scatter_obs._offsets3d = (ox, oy, oz)

    # ON NE TOURNE QUE SI LE BOUTON EST SUR "ON"
    if state.active:
        ax.view_init(elev=20, azim=frame)
    
    ax.set_title(f"Kyniska - Mode {'Auto' if state.active else 'Manuel (Souris)'}")
    return scatter_mire, scatter_obs

anim = animation.FuncAnimation(fig, animate, frames=360, interval=30, blit=False)

print("💡 Utilise la souris pour tourner la vue. Clique sur le bouton pour l'auto-rotation.")
plt.show()