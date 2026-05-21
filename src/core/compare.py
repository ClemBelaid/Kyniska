import os
curr_dir = os.path.dirname(__file__) # Current directory
#
import matplotlib.pyplot as plt
from matplotlib import animation
from src.core.geometry import build_basis
import numpy as np


# Save animation to GIF?
SAVE_GIF = False

#--------------------------------
# 3D scene -- Data
#--------------------------------

# My 3D scene data
"""t = np.linspace(0, 4*np.pi, 100)
data_x = 50 * np.cos(t)
data_y = 50 * np.sin(t)
data_z = 10 * t"""
data = np.zeros((360,3,3), dtype=float)
pts = np.array([
    [1, 5, 7],   # point 0
    [1, 3, 4],   # point 1
    [1, 2, 2]    # point 2
])

#Rotation autour de Z
for i in range(360):

    theta = np.deg2rad(i)

    R = np.array([
        [np.cos(theta), -np.sin(theta), 0],
        [np.sin(theta),  np.cos(theta), 0],
        [0,              0,             1]
    ])

    for j in range(3):

        pt_rot = R @ pts[j]

        data[i, j] = pt_rot



#--------------------------------
# Create 3D figure
#--------------------------------

figure = plt.figure(figsize=(10, 10))
#
axes = plt.axes(projection="3d")
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

pad = 5 #Ce truc joue un role dans la représentation de l'écran à 0 l'écran se retouve très grand et en dessous du box 3D autre valeur plus petit et dans le box 

axes.set_xlim(xmin - pad, xmax + pad)
axes.set_ylim(ymin - pad, ymax + pad)
axes.set_zlim(zmin - pad, zmax + pad)
"""axes.set_xlim3d(min(data_x), max(data_x))
axes.set_ylim3d(min(data_y), max(data_y))
axes.set_zlim3d(min(data_z), max(data_z))"""

# Set aspect ratio using "peak to peak" in dataset
#static parameters 
axes.set_box_aspect((1, 1, 1))

vn = np.array([0,0,1])
u1,u2=build_basis(vn)
screen = {
    "origin": np.array([0.,0.,0.]),
    "normal": vn,
    "u1": u1,
    "u2": u2
    }

s = 10
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


#--------------------------------
# Scatter data
#--------------------------------

# Animated data = subset of 3D scene data
x = []
y = []
z = []


# Commit data to 3D renderer
scatter = axes.scatter(x, y, z, color='r', s=80)
#--------------------------------
# Animation function
#--------------------------------

def animate(in_angle: int):
  """
  Update 3D scene to reflect frame
  """
  # Use global x, y and z
  global x, y, z

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
   

  # Set timestamp in title
  axes.set_title('{:.3f}'.format(in_angle))

  """# Move camera
  axes.elev += 0.2
  axes.azim += 0.1"""

  # Add new position
  x = data[in_angle,:,0]
  y = data[in_angle,:,1]
  z = data[in_angle,:,2]
 

  # Update scatter plot
  scatter._offsets3d = (x, y, z)

  return scatter,

#--------------------------------
# Generate animation, save, show
#--------------------------------

# Generate
anim = animation.FuncAnimation(figure, animate,
                               frames=360,
                               interval=30,
                               repeat=True)

# Save?
"""if SAVE_GIF:
  gif_path = os.path.join(curr_dir, '__ANIM__.gif')
  anim.save(gif_path)

  # Log
  print(f'Saved animation to "{gif_path}"')"""

# Show 3D animation
plt.show()