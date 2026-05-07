from src.core import Mire
import src.core.observation as obs
import sys

if __name__ == "__main__":
    argc = len(sys.argv)
    if argc == 1 :
        print("Usage: program <mire> <nb projections> <projections...>\n"
              " - <mire> : fichier JSON de la mire\n"
              " - <nb projections> : int\n"
              " - <proj 1> : JSON \n"
              " - <proj 2> : JSON \n"
              " - <proj 3> : JSON \n"
              "    ...\n",
            file=sys.stderr)
        sys.exit(1)

    m = Mire.load_json(sys.argv[1])
    nb_proj = sys.argv[2]
    p1 = sys.argv[3]
    p2 = sys.argv[4]
    p3 = sys.argv[5]
