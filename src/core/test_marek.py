import numpy as np


# Une mire de 3 points: A, B, C
A = np.array([0, 0, 0])
B = np.array([10, 3, -1])
C = np.array([0, -2, 7])

print(f'Mire 0 A=\n{A}')
print(f'Mire 0 B=\n{B}')
print(f'Mire 0 C=\n{C}')
print()
# A, B, C sont des coordonnées 3D (vecteurs 3x1)

# On va prendre une matrice de rotation 3x3 (90° selon l'axe Z)
R = np.array([[ 0, -1,  0],
              [+1,  0,  0],
              [ 0,  0,  1]])

# Les 3 vecteurs de la base World: x, y, z
x = np.array([1, 0, 0])
y = np.array([0, 1, 0])
z = np.array([0, 0, 1])

# R transforme ces vecteurs en ...
print(f'R(x)=\n{R.dot(x)}')  # x va pointer en +y
print(f'R(y)=\n{R.dot(y)}')  # y va pointer en -x
print(f'R(z)=\n{R.dot(z)}')  # z ne bouge pas, pointe en +z
print()

# R transforme les points A, B, C en ...
print(f'R(A)=\n{R.dot(A)}')  # A ne bouge pas car il est a l'origine
print(f'R(B)=\n{R.dot(B)}')  # B se fait rotater mais son z ne change pas
print(f'R(C)=\n{R.dot(C)}')  # C se fait rotater mais son z ne change pas
print()

# Maintenant on va ajouter une translation t
t = np.array([100, 200, 300])
print(f't=\n{t}')
print()

# Et on etend la matrice R pour obtenir la matrice T (avec R et t dedans)
T = np.hstack([R, t.reshape((3,1))])
print(f'En ajoutant t : T=\n{T}')
print()
#
zzz1 = np.array([0, 0, 0, 1])
T = np.vstack([T, zzz1.reshape((1,4))])
print(f'En ajoutant la ligne du bas : T=\n{T}')
print()

# Maintenant, pour faire les calculs avec les coordonnées homogenes
# il faut leur ajouter un 1 a la fin (4eme coordonnée)
Ah = np.hstack([A, [1]])
Bh = np.hstack([B, [1]])
Ch = np.hstack([C, [1]])

print(f'Mire 0 -- coord. homogenes Ah=\n{Ah}')
print(f'Mire 0 -- coord. homogenes Bh=\n{Bh}')
print(f'Mire 0 -- coord. homogenes Ch=\n{Ch}')
print()

# On applique T aux points A, B et C en coordonnees homogenes
Ah_2 = T.dot(Ah)
Bh_2 = T.dot(Bh)
Ch_2 = T.dot(Ch)
#
print(f'T(Ah)=\n{Ah_2}')
print(f'T(Bh)=\n{Bh_2}')
print(f'T(Ch)=\n{Ch_2}')
print()

# Et on extrait les coordonnees cartesiennes qui nous interessent (en oubliant le 1 a la fin)
A_2 = Ah_2[:3]
B_2 = Bh_2[:3]
C_2 = Ch_2[:3]

print(f'A_2=\n{A_2}')
print(f'B_2=\n{B_2}')
print(f'C_2=\n{C_2}')
print()
print(f'(A_2)x={A_2[0]}, (A_2)y={A_2[1]}, (A_2)z={A_2[2]}')
print(f'(B_2)x={B_2[0]}, (B_2)y={B_2[1]}, (B_2)z={B_2[2]}')
print(f'(C_2)x={C_2[0]}, (C_2)y={C_2[1]}, (C_2)z={C_2[2]}')
print()

# Exemple de tableau a 3 dimensions
data = np.random.randint(0, 10, (10,5,3))  # 10 valeurs de alpha, 5 billes, 3 coordonnees
print(f'data=\n{data}')
print()

# La bille N a l'angle A a pour coordonnees...
N = 3
A = 8
coord = data[A,N]
print(f'coord=\n{coord}')
print()
