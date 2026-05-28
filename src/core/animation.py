import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from src.core.projection import project_pt_to_plane
from src.core.transformation import calcul_matrice_rotation


def compute_animation_data(mire, screen, xm, ym):
    """
    Entrée :
        - mire : objet contenant les points 3D de la mire (mire.pts)
        - screen : dictionnaire contenant 'origin', 'u1', 'u2'
        - xm, ym : points définissant l’axe de rotation

    Sortie :
        - data : tableau (360, N, 3) des points de la mire tournés
        - data_proj : tableau (360, N, 3) des points projetés sur l'écran en 3D
    """

    u1 = screen["u1"]
    u2 = screen["u2"]

    points = mire.points

    data = np.zeros((360, len(points), 3))
    data_proj = np.zeros((360, len(points), 3))

    axis = ym - xm
    axis = axis / np.linalg.norm(axis)

    for angle in range(360):

        theta = np.deg2rad(angle)
        rotation_matrix = calcul_matrice_rotation(axis, theta)

        for j in range(len(points)):

            pt_rot = rotation_matrix @ (points[j] - xm) + xm

            pt_proj = project_pt_to_plane(pt_rot, screen)

            pt_proj_3d = (
                screen["origin"]
                + pt_proj[0] * u1
                + pt_proj[1] * u2
            )

            data[angle, j] = pt_rot
            data_proj[angle, j] = pt_proj_3d

    return data, data_proj


def lift_above_screen(data, xm, ym, margin=20):
    """
    Entrée :
        - data : positions 3D de la mire sur toutes les frames
        - xm, ym : points définissant l'axe (modifiés si besoin)
        - margin : marge minimale en z

    Sortie :
        - None (modifie data, xm et ym en place)
    """
    global_min_z = np.min(data[:, :, 2])

    if global_min_z < margin:
        dz = margin - global_min_z
        data[:, :, 2] += dz
        xm[2] += dz
        ym[2] += dz


def setup_axes(axes, data, mire):
    """
    Entrée :
        - axes : axe matplotlib 3D
        - data : positions 3D de la mire sur toutes les frames
        - mire : objet contenant les points (pour échelle)

    Sortie :
        - None (modifie directement les axes)
    """

    axes.set_xlabel("millimeters")
    axes.set_ylabel("millimeters")
    axes.set_zlabel("millimeters")

    axes.elev = 50
    axes.azim = 45
    axes.dist = 100

    xmin = np.min(data[:, :, 0])
    xmax = np.max(data[:, :, 0])

    ymin = np.min(data[:, :, 1])
    ymax = np.max(data[:, :, 1])

    zmin = np.min(data[:, :, 2])
    zmax = np.max(data[:, :, 2])

    pad = 90

    axes.set_xlim(xmin - pad, xmax + pad)
    axes.set_ylim(ymin - pad, ymax + pad)
    axes.set_zlim(zmin - pad, zmax + pad)

    axes.set_box_aspect((1, 1, 1))


def draw_screen_surface(axes, screen, mire):
    """
    Entrée :
        - axes : axe matplotlib 3D
        - screen : dictionnaire contenant origin, u1, u2
        - mire : utilisé pour l'échelle

    Sortie :
        - None (dessine directement sur les axes)
    """

    origin = screen["origin"]

    u1 = screen["u1"]
    u2 = screen["u2"]

    scale = np.max(np.abs(mire.points)) * 1.5
    s = scale

    corners = [
        origin + s * u1 + s * u2,
        origin + s * u1 - s * u2,
        origin - s * u1 - s * u2,
        origin - s * u1 + s * u2
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


def animate_rotation(mire, obs_3d, screen, xm, ym, xo, yo, best_frame):
    """
    Entrée :
        - mire : objet contenant les points de la mire
        - obs_3d : points observés en 3D (scatter rouge)
        - screen : repère de projection (origin, u1, u2)
        - xm, ym : points définissant l’axe de rotation
        - xo, yo : points de repère choisis dans l'observation de référence
        - best_frame : frame à mettre en évidence

    Sortie :
        - None (affiche une animation matplotlib)
    """

    data, data_proj = compute_animation_data(
        mire,
        screen,
        xm,
        ym
    )

    lift_above_screen(data, xm, ym)

    pt_1 = xm + 3 * (ym - xm)
    pt_2 = xm - 2 * (ym - xm)

    # On reconvertit xo et yo dans le repère écran
    xo = screen["origin"] + xo[0]*screen["u1"] + xo[1]*screen["u2"]
    yo = screen["origin"] + yo[0]*screen["u1"] + yo[1]*screen["u2"]

    figure = plt.figure(figsize=(10, 10))

    axes = plt.axes(projection="3d")

    axes.plot(
        (pt_1[0], pt_2[0]),
        (pt_1[1], pt_2[1]),
        (pt_1[2], pt_2[2])
    )

    axes.scatter(
        obs_3d[:, 0],
        obs_3d[:, 1],
        obs_3d[:, 2],
        color='red',
        marker='x',
        s=100
    )


    axes.scatter(
        xm[0], xm[1], xm[2],
        color='black',
        marker='X',
        s=120,
    )

    axes.scatter(
        xo[0], xo[1], xo[2],
        color='black',
        marker='o',
        s=80,
    )

    axes.scatter(
        ym[0], ym[1], ym[2],
        color='green',
        marker='X',
        s=120,
    )

    axes.scatter(
        yo[0], yo[1], yo[2],
        color='green',
        marker='o',
        s=80,
    )

    setup_axes(axes, data, mire)

    draw_screen_surface(axes, screen, mire)

    scatter = axes.scatter([], [], [], color='r', s=80)

    scatter_proj = axes.scatter(
        [],
        [],
        [],
        facecolors='none',
        edgecolors='blue',
        marker='o',
        s=40,
        linewidths=2
    )

    proj_lines = []

    def animate(angle):

        axes.set_title(f"{angle:.3f}")

        x = data[angle, :, 0]
        y = data[angle, :, 1]
        z = data[angle, :, 2]

        x_proj = data_proj[angle, :, 0]
        y_proj = data_proj[angle, :, 1]
        z_proj = data_proj[angle, :, 2]

        scatter._offsets3d = (x, y, z)

        scatter_proj._offsets3d = (
            x_proj,
            y_proj,
            z_proj
        )

        is_best = (angle == best_frame)

        scatter_proj.set_edgecolor(
            'green' if is_best else 'blue'
        )

        for line in proj_lines:
            line.remove()

        proj_lines.clear()

        for i in range(len(x)):

            line = axes.plot(
                [x[i], x_proj[i]],
                [y[i], y_proj[i]],
                [z[i], z_proj[i]],
                color='green' if is_best else 'blue',
                linestyle='--',
                linewidth=2 if is_best else 1,
                alpha=1.0 if is_best else 0.5
            )

            proj_lines.append(line[0])

        return scatter, scatter_proj

    anim = animation.FuncAnimation(
        figure,
        animate,
        frames=360,
        interval=50,
        repeat=True
    )

    plt.show()

    return data, data_proj