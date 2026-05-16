from src.core import Mire
from src.core import Observation 
import src.core.process as prc
import sys
import numpy as np 

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

    mire = Mire.load_json(sys.argv[1])
    #nb_proj = sys.argv[2]
    obs_ref = Observation.load_json(sys.argv[2])
    v2 = np.array([0, 0.5, np.sqrt(3)/2])
    #p2 = sys.argv[4]
    #p3 = sys.argv[5]
    (mire_1,xm_rote,ym_rote,lst_xm)=prc.frst_process(mire,v2,obs_ref.points[0],obs_ref.points[1])
    (mire_2,xm2_rote,ym2_rote,lst2_xm)=prc.scd_process(mire_1,v2,lst_xm,xm_rote,ym_rote,obs_ref.points[0],obs_ref.points[1])
    (mire_3,rms,agl)=prc.thd_process(mire_2,v2,obs_ref,xm2_rote,ym2_rote,360)
    print(f"Angle : {np.degrees(agl):.2f}° avec un RMS de {rms:.4f}")
    #print(xm_rote)
    #print(ym_rote)

