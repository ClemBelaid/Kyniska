from src.mire import Mire
import sys

if __name__ == "__main__":
    # la liste de arg est donner dans sys.argv, le premier etant le chemin du fichier python
    argc = len(sys.argv)
    if argc == 1 :
        print("Usage: program <mire> <nb projections> <projections...>\n"
              " - <mire> : fichier JSON de la mire\n"
              " - <nb projections> : int\n"
              " - <proj 1> : JSON \n"
              " - <proj 2> : JSON \n"
              "    ...\n",
            file=sys.stderr)
        sys.exit(1)
    # TODO
    print("TODO : identifier les billes des projections")
