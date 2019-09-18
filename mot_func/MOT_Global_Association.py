import numpy as np
from Common.Idx2Types import Idx2Types
from Obj.Tracklet import Tracklet
from mot_func.mot_appearance_model_generation import mot_appearance_model_generation
from mot_func.mot_appearance_model_update import mot_appearance_model_update
from mot_func.mot_eval_association_matrix import mot_eval_association_matrix
from mot_func.mot_association_hungarian import mot_association_hungarian
from mot_func.mot_motion_model_generation import mot_motion_model_generation
from mot_func.mot_tracklets_concat import mot_tracklets_concat
from kf_func.km_estimation import km_estimation
from mot_func.mot_count_ids import mot_count_ids
from Obj.Z_item import Z_item
from Obj.Obs_Graph import Obs_Graph
from tools.ListGiant import ListInsert
def MOT_Global_Association(Trk = None,Tracklets_window = None,param = None,fr = None,Obs_grap_window = None,detections = None,*args,**kwargs):

    obs_grap = Obs_Graph()
    Obs_grap_window.append(obs_grap)
    Obs_grap_window[fr].iso_idx = np.ones((len(detections[fr])))
    ILDA  =  param.ILDA
    Refer = []
    Test = []
    all_indx = [i for i in range(0,len(Trk))]
    all_indx_window = [i for i in range(0,len(Tracklets_window))]
    low_indx,_,_ = Idx2Types(Tracklets_window,'Low')
    high_indx = np.setdiff1d(all_indx_window,low_indx)
    init_indx = all_indx
    init_trk = []
    High_trk = []
    Low_trk = []
    window_trk = []
    Y_set = []
    if len(high_indx) !=0:
        # For tracklets with low confidence in the window
        for ii in range(0,len(low_indx)):
            i = low_indx[ii]
            temp_Trk_low = Tracklet()
            temp_Trk_low.hist  =  Tracklets_window[i].A_Model
            temp_Trk_low.FMotion  =  Tracklets_window[i].FMotion
            temp_Trk_low.last_update  =  Tracklets_window[i].last_update
            temp_Trk_low.h  =  Tracklets_window[i].state[-1][3]
            temp_Trk_low.w  =  Tracklets_window[i].state[-1][2]
            temp_Trk_low.type  =  Tracklets_window[i].type
            temp_Trk_low.end_time = Tracklets_window[i].efr
            Low_trk.append(temp_Trk_low)
        # For tracklet with high confidence in the window
        for jj in range(0,len(all_indx_window)):
            j = all_indx_window[jj]
            temp_Trk_high = Tracklet()
            temp_Trk_high.hist  =  Tracklets_window[j].A_model_tail
            print(jj,j,len(Tracklets_window[j].state),Tracklets_window[j].state)
            temp_Trk_high.h  =  Tracklets_window[j].state[-1][3]
            temp_Trk_high.w  =  Tracklets_window[j].state[-1][2]
            temp_Trk_high.FMotion  =  Tracklets_window[j].FMotion
            XX,PP = mot_motion_model_generation(Tracklets_window[j],param,'Backward',nargout = 2)
            temp_Trk_high.BMotion.X  =  XX
            temp_Trk_high.BMotion.P  =  PP
            temp_Trk_high.last_update  =  Tracklets_window[j].last_update
            temp_Trk_high.init_time  =  Tracklets_window[j].ifr
            temp_Trk_high.end_time = Tracklets_window[j].efr
            window_trk.append(temp_Trk_high)
        iso_label = []
        
    for jj in range(0,len(all_indx)):
        j = all_indx[jj]
        temp_init_trk = Tracklet()
        temp_init_trk.hist  =  Trk[j].A_model_tail
        temp_init_trk.h  =  Trk[j].state[-1][3]
        temp_init_trk.w  =  Trk[j].state[-1][2]
        temp_init_trk.FMotion  =  Trk[j].FMotion
        XX,PP = mot_motion_model_generation(Trk[j],param,'Backward',nargout = 2)
        temp_init_trk.BMotion.X  =  XX
        temp_init_trk.BMotion.P  =  PP
        temp_init_trk.last_update  =  Trk[j].last_update
        temp_init_trk.init_time  =  Trk[j].ifr
        temp_init_trk.end_time  =  Trk[j].last_update
        init_trk.append(temp_init_trk)
        
    thr = param.obs_thr
    score_trk = mot_eval_association_matrix(init_trk,window_trk,param,'Trk',ILDA)
    print("score_trk matrix:",score_trk)
    matching,Affinity = mot_association_hungarian(score_trk,thr)
    alpha = param.alpha
    rm_idx = []
    print("matching matrix:",matching)
    #association the tracklet in the window to init tracklets
    for m in range(0,len(Affinity)):
        w_idx = all_indx_window[matching[0,m]]
        init_idx = all_indx[matching[1,m]]
        fr1 = Tracklets_window[w_idx].ifr
        fr2 = Tracklets_window[w_idx].last_update
        for kk in range(fr1,fr2):
            
            ListInsert(Trk[init_idx].state,kk,Tracklets_window[w_idx].state[kk],[])
        numHyp = len(Tracklets_window[w_idx].hyp.score)
        #copy hyp information from window_tracklets to init_tracklets
        for kk in range(fr1,numHyp):
            mot_tracklets_concat(Trk[init_idx],Tracklets_window[w_idx],kk,param)
        XX = np.array([0,0,0,0])
        numState = len(Trk[init_idx].state)
        XX[0] = Trk[init_idx].state[fr1][0]
        XX[2] = Trk[init_idx].state[fr1][1]
        PP = param.P
        Trk[init_idx].type  =  'High'
        mot_appearance_model_update(Trk[init_idx])
        rm_idx.append(w_idx)
    if len(rm_idx) != 0:
        print("removed tracklets ids of which are {}".format(rm_idx))
        for idx in sorted(rm_idx,reverse=True):
            #mot_count_ids(tracklets_window[idx],param)
            Tracklets_window.pop(idx)
    
    return Trk
    
if __name__=='__main__':
    pass
    
