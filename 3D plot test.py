import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Genère 50 points (x,y,z) aléatoires
np.random.seed(42)
x = np.random.rand(50)
y = np.random.rand(50)
z = np.random.rand(50)

# Tailles n aléatoire
n = 50 # np.random.rand(50)*50

fig = plt.figure(figsize=(12, 6))

# Left: Creating a 3D figure

ax1 = fig.add_subplot(1, 2, 1, projection='3d')
# Creating a 3D scatter plot
ax1.scatter(x, y, z, c=z, cmap='viridis', s=n, edgecolor='k')
ax1.set_title("3D points")



# Rigth: projection 2D

# plt.plot(x,y, 0,'o')

ax2 = fig.add_subplot(1, 2, 2)
ax2.scatter(x, y, c=z, cmap='viridis', s=n, edgecolor='k')
ax2.set_title("Projection XY")
ax2.set_xlabel("x")
ax2.set_ylabel("y")
ax2.axis("equal")

if __name__ == "__main__":
    # Display the plot (rotate manually with mouse)
    plt.tight_layout()
    plt.show()
