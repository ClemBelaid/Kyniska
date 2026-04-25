from mire import Mire
from mire import Observation 
from mire import project_mire_to_plane
import numpy as np
import matplotlib.pyplot as plt

mire = Mire.load_json("test.json")
v=np.array([3,3,4])
cliches2D = project_mire_to_plane(mire,v)

# Création de la figure 3D
fig = plt.figure(figsize=(16, 10))
ax = fig.add_subplot(1, 4, 1, projection='3d')
plt.xlabel("X")
plt.ylabel("Y")

# Création d'un scatter plot
ax.scatter(mire.points[0],mire.points[1],mire.points[2], c=mire.points[2], cmap='viridis', edgecolor='k')
xx, yy = np.meshgrid(np.linspace(0,1,20), np.linspace(0,1,20))
zz = (-v[0] * xx - v[1] * yy) * 1. / v[2] # z = (-ax -by)/c
ax.plot_surface(xx, yy, zz, alpha=0.2)
for k in range(2,5):
    ax_k = fig.add_subplot(1,2,k)
    ax_k.plot(cliches2D[k-2].points[0],cliches2D[k-2].points[1], 'ro')
plt.show()

