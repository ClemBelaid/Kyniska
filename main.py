from mire import Mire
import matplotlib.pyplot as plt

if __name__ == "__main__":
    pts = [
        [0,0,0],
        [1,0,0],
        [0,1,0]
    ]

    m = Mire(pts)
    print(m.points)
    print(m.ids)

    m.save_json("test.json")

    mire_cube = Mire.generer_cube(nb_billes=20, largeur=200.0, longueur=200.0, epaisseur=30.0)

    print("--- MIRE CUBE ---")
    print(f"Nombre de billes : {len(mire_cube)}")
    print(f"IDs générés : {mire_cube.ids}")

    mire_cube.save_json("mire_rectangle.json")


    mire_cone = Mire.generer_cone_tronque(nb_billes=25, rayon_base=100.0, rayon_sommet=50.0, hauteur=40.0)
    print("\n--- MIRE CÔNE ---")
    print(f"Nombre de billes : {len(mire_cone)}")

    mire_cone.save_json("mire_cone.json")


    m2 = Mire.load_json("test.json")
    print(m2)
    print(m2.points)
    m2.show()
    plt.show()

