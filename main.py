from mire import Mire


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

    m2 = Mire.load_json("test.json")
    print(m2.points)
