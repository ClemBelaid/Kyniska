from src.core import Mire
from src.core import Observation
from src.core.matching import identification
import sys

if __name__ == "__main__":
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

    print("TODO : identifier les billes des projections")
