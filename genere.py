from src.mire import Mire
import sys

if __name__ == "__main__":
    # la liste de arg est donner dans sys.argv, le premier etant le chemin du fichier python
    argc = len(sys.argv)
    if argc == 1 :
        print("Usage: program <type mire> <nb point> ...\n"
              " - <type mire> : {pave | cone tronque | }\n"
              " - <nb point> : un nombre ... ",
            file=sys.stderr)
        sys.exit(1)
    # TODO
    print("TODO : ecrire un mire en JSON et des observation...")
