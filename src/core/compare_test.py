#1. Bibliothèques standard
import os

#Bibliothèques tierces
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.widgets import Button
from scipy.optimize import minimize
from scipy.spatial.distance import cdist

#Modules locaux
from src.core.dichotomie import optimisation_dichotomie
from src.core.geometry import build_basis
from src.core.mire import Mire
from src.core.observation import Observation
from src.core.process import frst_process, scd_process, thd_process
from src.core.projection import project_pt_to_plane
from src.core.transformation import calcul_matrice_rotation

#Configuration / Variables globales
curr_dir = os.path.dirname(__file__) # Current directory

# Save animation to GIF?
SAVE_GIF = False

#--------------------------------
# 3D scene -- Data
#--------------------------------


mire = Mire.load_json("Mire_tr") #notre mire non roté et l'algo va déterminer cette rotation qui colle avec les observations de obs_ref
obs_ref = Observation.load_json("obs_ref")
obs_pts = obs_ref.points

##################################################
# Tout ce qui concerne l'écran : origine, vect normal et vect directeurs
vn = np.array([0,0,1])
u1,u2=build_basis(vn)



#center = np.mean(mire.points, axis=0)

origin = np.array([
    0.,
    0.,
    0.
])
screen = {
    "origin": origin,
    "normal": vn,
    "u1": u1,
    "u2": u2
    }
###################################################
#Reconstruction des points 2D dans le repère monde: ils se retrouveront alors bien sur l'écran
obs_3d = np.array([
    screen["origin"] + p[0]*u1 + p[1]*u2
    for p in obs_pts
]) 
pts =  mire.points

####################################################
#Param dynamiques de stockage: les points de la mire et les points 3D projections à toutes les frames
data = np.zeros((360, len(pts), 3), dtype=float)
data_proj = np.zeros((360,len(pts),3),dtype=float)


########################################"
#Les pts pour l'axe de rotation fixés et ym_xm pour la construction de la matrice de rotation 
ym_xm = mire.points[0] - mire.points[1]
xm2_rote=mire.points[0]
ym2_rote=mire.points[1]

########################################################


#Rotation autour de Z

#########################################################
#Boucle pour le stockage des param dynamiques: points 3D mire et projections converties 3D écran 
for i in range(360):

    theta = np.deg2rad(i)
    axis = ym_xm / np.linalg.norm(ym_xm)
    mR = calcul_matrice_rotation(axis, theta)
    """R = np.array([
        [np.cos(theta), -np.sin(theta), 0],
        [np.sin(theta),  np.cos(theta), 0],
        [0,              0,             1]
    ])"""

    for j in range(len(pts)):

        pt_rot = mR @ (pts[j] - xm2_rote) + xm2_rote
        pt_proj = project_pt_to_plane(pt_rot,screen)
        pt_p3D = screen["origin"] + pt_proj[0]*u1 + pt_proj[1]*u2 #la conversion 3D 
        data[i, j] = pt_rot
        data_proj[i,j]=pt_p3D

#########################################################

###########################################################
#Boucle pour les scores 


def evaluer_angle(theta_deg):
    theta_rad = np.deg2rad(theta_deg[0])
    mR_test = calcul_matrice_rotation(axis, theta_rad)
    
    # On projette temporairement la mire pour cet angle précis
    pts_projetes_test = []
    for p in pts:
        pt_rot = mR_test @ (p - xm2_rote) + xm2_rote
        pt_proj = project_pt_to_plane(pt_rot, screen)
        pt_p3D = screen["origin"] + pt_proj[0]*u1 + pt_proj[1]*u2
        pts_projetes_test.append(pt_p3D)
        
    # Calcul de la distance max avec les observations réelles
    erreurs = np.linalg.norm(np.array(pts_projetes_test) - obs_3d, axis=1)
    return np.max(erreurs)

#Lancement de l'optimisation par la dichotomie
print("\n--- Optimisation par Dichotomie en cours ---")
best_angle_exact = optimisation_dichotomie(pts, obs_3d, axis, xm2_rote, screen, u1, u2)

#récupération du résultat pour l'affichage (on réutilise leur fonction d'évaluation pour le score)
best_frame = int(np.round(best_angle_exact)) % 360  # Arrondi pour l'index de l'animation
best_score = evaluer_angle([best_angle_exact])

print(f"Angle exact trouvé par le modèle : {best_angle_exact:.3f}°")
print(f"Index d'affichage correspondant : {best_frame}")
print(f"Best score (Erreur résiduelle) : {best_score:.6f} mm")
print("==========================================\n")

#############################################################
# Sécurise toute l'animation au-dessus de l'écran

margin = 20

global_min_z = np.min(data[:,:,2])

if global_min_z < margin:

    dz = margin - global_min_z

    data[:,:,2] += dz

    xm2_rote[2] += dz
    ym2_rote[2] += dz

###############################################################

#Points pour l'axe de rotation 
pt_1 = xm2_rote + 3*(ym2_rote-xm2_rote)
pt_2= xm2_rote - 2*(ym2_rote-xm2_rote)

#################################################################

#--------------------------------
# Create 3D figure
#--------------------------------


#Tout ce qui est lié à la création du box 3D, axes et autres. Normalement pas besoin d'y toucher

figure = plt.figure(figsize=(10, 10))
#

axes = plt.axes(projection="3d")
axes.plot((pt_1[0],pt_2[0]),(pt_1[1],pt_2[1]),(pt_1[2],pt_2[2]))
axes.scatter(
    obs_3d[:,0],
    obs_3d[:,1],
    obs_3d[:,2],
    color='red',
    marker='x',
    s=100
)
axes.set_xlabel("millimeters")
axes.set_ylabel("millimeters")
axes.set_zlabel("millimeters")

# Set-up camera --- axes.view_init(elev=10., azim=10)
axes.elev = 50  # Elevation
axes.azim = 45  # Azimuth
axes.dist = 100 # Distance

# Set bbox
xmin = np.min(data[:,:,0])
xmax = np.max(data[:,:,0])

ymin = np.min(data[:,:,1])
ymax = np.max(data[:,:,1])

zmin = np.min(data[:,:,2])
zmax = np.max(data[:,:,2])

pad = 90
#Ce truc joue un role dans la représentation de l'écran à 0 l'écran se retouve très grand et en dessous du box 3D autre valeur plus petit et dans le box 

axes.set_xlim(xmin - pad, xmax + pad)
axes.set_ylim(ymin - pad, ymax + pad)
axes.set_zlim(zmin - pad, zmax + pad)
"""axes.set_xlim3d(min(data_x), max(data_x))
axes.set_ylim3d(min(data_y), max(data_y))
axes.set_zlim3d(min(data_z), max(data_z))"""


axes.set_box_aspect((1, 1, 1))


scale = np.max(np.abs(mire.points)) * 1.5

s = scale
###################################################

#Tout ce barratin c'est juste pour que l'écran soit un peu propre. Pas besoin d'y toucher normalement 


origin = screen["origin"]

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

axes.plot_surface(
    X_surface,
    Y_surface,
    Z_surface,
    color='gray',
    alpha=0.15,
    edgecolor='black'
    )

######################################################

#--------------------------------
# Scatter data
#--------------------------------

# Animated data = subset of 3D scene data
x = []
y = []
z = []

x_proj = [] 
y_proj = [] 
z_proj = []

# Commit data to 3D renderer
scatter = axes.scatter(x, y, z, color='r', s=80)
scatter_proj = axes.scatter(
    x_proj,
    y_proj,
    z_proj,
    facecolors='none',
    edgecolors='blue',
    marker='o',
    s=40,
    linewidths=2
)
proj_lines = []

#TRACÉ DES ORBITES DE TRAJECTOIRE AU SOL ---
#On trace la trajectoire complète projetée pour chaque point de la mire..
angles_full = np.linspace(0, 2 * np.pi, 360)
for pt_index in range(len(pts)):
    trajectoire_x = []
    trajectoire_y = []
    trajectoire_z = []
    # On simule les 360 positions projetées pour ce point précis
    for i in range(360):
        trajectoire_x.append(data_proj[i, pt_index, 0])
        trajectoire_y.append(data_proj[i, pt_index, 1])
        trajectoire_z.append(data_proj[i, pt_index, 2])
        
    axes.plot(trajectoire_x, trajectoire_y, trajectoire_z, 
              color='deepskyblue', linestyle='-', alpha=0.3, linewidth=1)
# -------------------------------------------------------

#--------------------------------
# Animation function
#--------------------------------

def animate(in_angle: int):
  """
  Update 3D scene to reflect frame
  """
  # Use global x, y and z
  global x, y, z
  global x_proj, y_proj, z_proj

  # Log
  # print(f'Animating frame {in_frame}')

  # Reset animated data
  x = []
  y = []
  z = []

  x_proj = [] 
  y_proj = [] 
  z_proj = []
   
  # Set timestamp in title
  axes.set_title('{:.3f}'.format(in_angle))

  """# Move camera
  axes.elev += 0.2
  axes.azim += 0.1"""

  # Add new position
  x = data[in_angle,:,0]
  y = data[in_angle,:,1]
  z = data[in_angle,:,2]
  x_proj = data_proj[in_angle,:,0] 
  y_proj = data_proj[in_angle,:,1] 
  z_proj = data_proj[in_angle,:,2] 

  # Update scatter plot
  scatter._offsets3d = (x, y, z)
  scatter_proj._offsets3d = (x_proj, y_proj, z_proj)
 
  if abs(in_angle - best_frame) <= 2:
    scatter_proj.set_edgecolor('green')
  else:
    scatter_proj.set_edgecolor('blue')
 
  is_best = (in_angle == best_frame)

  # supprimer anciennes lignes
  for ln in proj_lines:
    ln.remove()
  proj_lines.clear()

  # ajouter nouvelles lignes de projection
  for i in range(len(x)):
    color = 'green' if is_best else 'blue'

    ln = axes.plot(
    [x[i], x_proj[i]],
    [y[i], y_proj[i]],
    [z[i], z_proj[i]],
    color=color,
    linestyle='--',
    linewidth = 2 if is_best else 1,
    alpha = 1.0 if is_best else 0.5
    )
    proj_lines.append(ln[0])

  # --- AJOUT : GESTION DE LA CAMÉRA ET DU TITRE ---
  global auto_rotate_cam
  if auto_rotate_cam:
      axes.view_init(elev=50, azim=in_angle) # La caméra tourne

  # Titre dynamique
  if in_angle == best_frame:
      axes.set_title(f"Angle Optimal : {best_angle_exact:.3f}° (Frame {in_angle})", color='green', fontsize=14, fontweight='bold')
  else:
      axes.set_title(f"Recherche... {in_angle}° | Cible : {best_angle_exact:.1f}°", color='black')
  # ------------------------------------------------

  return scatter, scatter_proj

#--------------------------------
# AJOUT : BOUTON INTERACTIF AUTO-ROTATE
#--------------------------------
auto_rotate_cam = False
ax_btn = plt.axes([0.1, 0.05, 0.2, 0.06])
btn_rotate = Button(ax_btn, 'Caméra: OFF', color='lightgray', hovercolor='skyblue')

def toggle_rotation(event):
    global auto_rotate_cam
    auto_rotate_cam = not auto_rotate_cam
    btn_rotate.label.set_text(f"Caméra: {'ON' if auto_rotate_cam else 'OFF'}")
    figure.canvas.draw_idle()

btn_rotate.on_clicked(toggle_rotation)

#--------------------------------
# Generate animation, save, show
#--------------------------------

# Generate
anim = animation.FuncAnimation(figure, animate,
                               frames=360,
                               interval=50,
                               repeat=True)

# Show 3D animation
plt.show()