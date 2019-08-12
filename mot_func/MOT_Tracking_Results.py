import numpy as np
from Common.Idx2Types import Idx2Types
from Obj.Trk_Sets import Trk_Set
from tools.ListGiant import ListIndice1d
def MOT_Tracking_Results(Trk=None,Trk_sets=None,fr=None,*args,**kwargs):

    
    hg_indx,_,_=Idx2Types(Trk,'High')
    low_indx,_,_=Idx2Types(Trk,'Low')
    del_indx=[]
    for i in range(0,len(low_indx)):
        efr=Trk[low_indx[i]].efr
        if abs(efr - fr) > 5:
            del_indx.append(i)
    if len(Trk_sets) == 0:
        for i in range(0,fr):
            Trk_sets.append(Trk_Set())
    if len(Trk_sets) == fr:
        Trk_sets.append(Trk_Set())

    Trk_sets[fr].high = hg_indx
    Trk_sets[fr].low = np.setdiff1d(low_indx,ListIndice1d(low_indx,del_indx))
    for i in range(0,len(Trk)):
        Trk_sets[fr].states.append(Trk[i].state)
        Trk_sets[fr].conf.append(Trk[i].Conf_prob)
        Trk_sets[fr].label.append(Trk[i].label)
    
    return Trk_sets
