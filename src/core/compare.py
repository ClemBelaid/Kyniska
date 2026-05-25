import os
curr_dir = os.path.dirname(__file__) # Current directory
#
import matplotlib.pyplot as plt
from matplotlib import animation
from src.core.geometry import build_basis
from src.core.process import frst_process
from src.core.projection import project_pt_to_plane
from scipy.spatial.distance import cdist
from src.core.process import scd_process
from src.core.process import thd_process
from src.core.process import app_proc
from src.core.transformation import calcul_matrice_rotation
from src.core.mire import Mire 
from src.core.observation import Observation 
import numpy as np


# Save animation to GIF?
SAVE_GIF = False

#--------------------------------
# 3D scene -- Data
#--------------------------------


mire = Mire.load_json("newMire") #notre mire non roté et l'algo va déterminer cette rotation qui colle avec les observations de obs_ref
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
#(mire_1,xm_rote,ym_rote,lst_xm)=frst_process(mire,screen,obs_ref.points[0],obs_ref.points[1])
#(mire_2,xm2_rote,ym2_rote,lst2_xm)=scd_process(mire_1,screen,lst_xm,xm_rote,ym_rote,obs_ref.points[0],obs_ref.points[1])
(bst_mire, bst_xm , bst_ym , bst_score , bst_agl ) = app_proc(mire,obs_ref,screen,obs_ref.points[0],obs_ref.points[1])

pts =  mire.points

####################################################
#Param dynamiques de stockage: les points de la mire et les points 3D projections à toutes les frames
data = np.zeros((360, len(pts), 3), dtype=float)
data_proj = np.zeros((360,len(pts),3),dtype=float)

#####################################################


#ym_xm = (ym2_rote - xm2_rote)

########################################"
#Les pts pour l'axe de rotation fixés et ym_xm pour la construction de la matrice de rotation 
ym_xm = bst_ym - bst_xm
xm2_rote=bst_xm
ym2_rote=bst_ym

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
#scores = []

"""for i in range(360):

    err = np.linalg.norm(data_proj[i] - obs_3d, axis=1)

    # erreur du pire point
    score = np.max(err)

    scores.append(score)""" 

best_frame = int(np.rad2deg(bst_agl)) % 360

print("Best angle  :", best_frame)
#print("Best score:", scores[best_frame]) 
print("Best score:", bst_score)

#############################################################

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

#################################################################

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

pad = 90#Ce truc joue un role dans la représentation de l'écran à 0 l'écran se retouve très grand et en dessous du box 3D autre valeur plus petit et dans le box 

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

  # Reset if starting frame
  """if in_angle == 0:
    # Reset camera
    axes.elev = 50
    axes.azim = 45"""

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
 
  if in_angle == best_frame:
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

  return scatter, scatter_proj
#--------------------------------
# Generate animation, save, show
#--------------------------------

# Generate
anim = animation.FuncAnimation(figure, animate,
                               frames=360,
                               interval=50,
                               repeat=True)

# Save?
"""if SAVE_GIF:
  gif_path = os.path.join(curr_dir, '__ANIM__.gif')
  anim.save(gif_path)

  # Log
  print(f'Saved animation to "{gif_path}"')"""

# Show 3D animation
plt.show()