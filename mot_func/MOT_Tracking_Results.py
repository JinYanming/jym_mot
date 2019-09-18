import numpy as np
from Common.Idx2Types import Idx2Types
from Obj.Trk_Sets import Trk_Set
from tools.ListGiant import ListIndice1d
def MOT_Tracking_Results(Trk=None,Trk_sets=None,fr=None,param = None,*args,**kwargs):

    hg_indx,_,_=Idx2Types(Trk,'High')
    low_indx,_,_=Idx2Types(Trk,'Low')
    del_indx=[]
    for i in range(0,len(low_indx)):
        efr=Trk[low_indx[i]].efr
        if abs(efr - fr) > 5:
            del_indx.append(i)
    #when the length of the Trk_set is zero,save the information about the init state
    #    if len(Trk_sets) == 0:
    #        for i in range(0,fr):
    #            Trk_sets.append(Trk_Set())
    #            for j in range(0,len(Trk)):
    #                Trk_sets[i].states.append(Trk[j].state[i].copy())
    #                Trk_sets[i].conf.append(Trk[j].Conf_prob)
    #                Trk_sets[i].label.append(Trk[j].label)
    #                Trk_sets[i].ystates_ids.append(Trk[j].hyp.ystates_ids[i])
    if len(Trk_sets) == fr:
        Trk_sets.append(Trk_Set())
    else:
        Trk_sets = [None]*fr
        Trk_sets.append(Trk_Set())

    Trk_sets[fr].high = hg_indx
    Trk_sets[fr].low = np.setdiff1d(low_indx,ListIndice1d(low_indx,del_indx))
    for i in range(0,len(Trk)):
        if Trk[i].last_update > fr:
            Trk_sets[fr].idsw.append(Trk[i].hyp.idsw[fr])
            if param.show_background_track == True:
                if len(Trk[i].state[fr]) != 0:
                    Trk_sets[fr].states.append(Trk[i].state[fr].copy())
                    Trk_sets[fr].conf.append(Trk[i].Conf_prob)
                    Trk_sets[fr].label.append(Trk[i].label)
            else:
                if len(Trk[i].hyp.ystate[fr]) != 0:
                    Trk_sets[fr].states.append(Trk[i].hyp.ystate[fr].copy())
                    Trk_sets[fr].conf.append(Trk[i].Conf_prob)
                    Trk_sets[fr].label.append(Trk[i].label)
    
    return Trk_sets
