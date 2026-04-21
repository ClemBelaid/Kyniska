import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math

pi = math.pi

# n le nombre de billes à générer
n = 15

# Genère n points (x,y,z) aléatoires
np.random.seed(42)
x = np.random.rand(n)
y = np.random.rand(n)
z = np.random.rand(n)

# Tailles s aléatoires
s = np.random.rand(n)*60 + 30

# Projection d'un vecteur u sur un plan P de vecteur normal n
def proj(v, n):
    n_norm = np.sqrt(sum(n**2))
    v_prime = np.dot(v,n)/np.dot(n,n)*n
    return v - v_prime

# Création de la figure 3D
fig = plt.figure(figsize=(16, 10))
ax = fig.add_subplot(1, 2, 1, projection='3d')
plt.xlabel("X")
plt.ylabel("Y")

# Création d'un scatter plot
ax.scatter(x, y, z, c=z, cmap='viridis', s = s, edgecolor='k')

# Vecteur normal à un plan P quelconque (pour tester)
normal = np.array([1, 1, 1])

# Calcul des coordonnées du plan
d = 0 # Ou bien d = 0

xx, yy = np.meshgrid(np.linspace(0,1,20), np.linspace(0,1,20))
zz = (-normal[0] * xx - normal[1] * yy - d) * 1. / normal[2] # z = (-ax -by)/c
ax.plot_surface(xx, yy, zz, alpha=0.2)

for i in range(n):
    v = (x[i], y[i], z[i])
    v_proj = proj(v,normal)
    ax.scatter(v_proj[0], v_proj[1], v_proj[2], c ="red", s = s[i], edgecolor='k')

plt.show()
