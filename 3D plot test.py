import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Genère 50 points (x,y,z) aléatoires
np.random.seed(42)
x = np.random.rand(50)
y = np.random.rand(50)
z = np.random.rand(50)

# Tailles n aléatoire
n = np.random.rand(50)*50

# Creating a 3D figure
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(1, 2, 1, projection='3d')


# Creating a 3D scatter plot
scatter = ax.scatter(x, y, z, c=z, cmap='viridis', s=n, edgecolor='k')

plt.plot(x,y, 0,'o')

# Display the plot (rotate manually with mouse)
plt.show()