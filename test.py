from mire import Mire
from mire import Observation 
from mire import project_mire_to_plane
import numpy as np
import matplotlib.pyplot as plt

mire = Mire.load_json("test.json") #récupérer l'objet mire 
v=np.array([3,3,4]) #Le vecteur normal au plan 
cliches2D, vect_proj= project_mire_to_plane(mire,v) #les clichés et les projections 2D sur le plan dans les figures 3D 
vect_proj = np.array(vect_proj)
n = vect_proj.shape[0]
print(n) #notre vect_proj contenant toutes les projections dans le plan 2D selon les différents angles de vue donc 9 points pour notre exemple
# Création de la figure 3D
fig = plt.figure(figsize=(16, 10))
#boucle pour les 3 projections 3D 
for i in range(3):
    ax = fig.add_subplot(1, 6, i+1, projection='3d')
    plt.xlabel("X")
    plt.ylabel("Y")
    #Pour la représentation des billes et leurs projections 2D 
    ax.scatter(mire.points[:,0],mire.points[:,1],mire.points[:,2], c=mire.points[:,2], cmap='viridis', edgecolor='k')
    subset = vect_proj[i*3:(i+1)*3]
    ax.scatter(subset[:,0],subset[:,1],subset[:,2],c="red",edgecolor='k')
    #Pour le tracé du plan 2D où les projections 2D se situent 
    xx, yy = np.meshgrid(np.linspace(0,1,20), np.linspace(0,1,20))
    zz = (-v[0] * xx - v[1] * yy) * 1. / v[2] # z = (-ax -by)/c
    ax.plot_surface(xx, yy, zz, alpha=0.2)

# pour les 3 plans 2D 
for k in range(3):
    ax_k = fig.add_subplot(1,6,k+4)
    ax_k.plot(cliches2D[k].points[:,0],cliches2D[k].points[:,1], 'ro')
plt.show()

