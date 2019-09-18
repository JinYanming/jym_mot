import numpy as np
from Common.Idx2Types import Idx2Types
from Obj.Tracklet import Tracklet
from mot_func.mot_appearance_model_generation import mot_appearance_model_generation
from mot_func.mot_appearance_model_update import mot_appearance_model_update
from mot_func.mot_eval_association_matrix import mot_eval_association_matrix
from mot_func.mot_association_hungarian import mot_association_hungarian
from mot_func.mot_motion_model_generation import mot_motion_model_generation
from mot_func.mot_tracklets_concat import mot_tracklets_concat
from mot_func.mot_check_idsw import mot_check_idsw
from kf_func.km_estimation import km_estimation
from mot_func.mot_count_ids import mot_count_ids
from Obj.Z_item import Z_item
from Obj.Obs_Graph import Obs_Graph
from tools.ListGiant import ListInsert
#this functions is used to decline the calculation during the tracklets association
def getHeadAndTailTrk(tracklets):
    length = len(tracklets)
    head = []
    tail = []
    for i in range(0,length):
        for j in range(0,length):
            if i != j:
                if tracklets[i].last_update < tracklets[j].ifr:
                    if i not in head:
                        head.append(i)
                    if j not in tail:
                        tail.append(j)
    return head,tail
    
def MOT_Window_Association(Tracklets_window = None,param = None,fr = None,detections = None,Obs_grap_window = None,*args,**kwargs):
    #get the head and tail list of tracklet in order to decline the calculation
    head_index,tail_index = getHeadAndTailTrk(Tracklets_window)
    ILDA  =  param.ILDA
    all_indx_window = [i for i in range(0,len(Tracklets_window))]
    window_trk_head = []
    window_trk_tail = []
    High_trk = []
    Low_trk = []
    Y_set = []
    # For trackletin the window with head A_Model
    for jj in range(0,len(head_index)):
        j = head_index[jj]
        temp_Trk = Tracklet()
        temp_Trk.hist  =  Tracklets_window[j].A_model_tail
        temp_Trk.h  =  Tracklets_window[j].state[-1][3]
        temp_Trk.w  =  Tracklets_window[j].state[-1][2]
        temp_Trk.FMotion  =  Tracklets_window[j].FMotion
        XX,PP = mot_motion_model_generation(Tracklets_window[j],param,'Forward')
        temp_Trk.BMotion.X  =  XX
        temp_Trk.BMotion.P  =  PP
        temp_Trk.last_update  =  Tracklets_window[j].last_update
        temp_Trk.init_time  =  Tracklets_window[j].ifr
        temp_Trk.end_time = Tracklets_window[j].last_update
        window_trk_head.append(temp_Trk)
    iso_label = []
        
    # For trackletin the window with tail A_Model
    for jj in range(0,len(tail_index)):
        j = tail_index[jj]
        temp_Tracklets_window = Tracklet()
        temp_Tracklets_window.hist  =  Tracklets_window[j].A_model_head
        temp_Tracklets_window.h  =  Tracklets_window[j].state[Tracklets_window[j].ifr][3]
        temp_Tracklets_window.w  =  Tracklets_window[j].state[Tracklets_window[j].ifr][2]
        temp_Tracklets_window.FMotion  =  Tracklets_window[j].FMotion
        XX,PP = mot_motion_model_generation(Tracklets_window[j],param,'Backward')
        temp_Tracklets_window.BMotion.X  =  XX
        temp_Tracklets_window.BMotion.P  =  PP
        temp_Tracklets_window.last_update  =  Tracklets_window[j].last_update
        temp_Tracklets_window.init_time  =  Tracklets_window[j].ifr
        temp_Tracklets_window.end_time  =  Tracklets_window[j].last_update
        window_trk_tail.append(temp_Tracklets_window)
        
    thr = param.obs_thr
    print(1111)
    score_trk = mot_eval_association_matrix(window_trk_head,window_trk_tail,param,'Trk',ILDA)
    print(score_trk,"score_trk matrix:")
    matching,Affinity = mot_association_hungarian(score_trk,thr)
    alpha = param.alpha
    rm_idx = []
    print(matching,"matching matrix:")
    #association the tracklet in the window to init tracklets
    for m in range(0,len(Affinity)):
        head_idx = head_index[matching[0,m]]
        tail_idx = tail_index[matching[1,m]]
        print("concat the tracklets whose ids is {} and {}".format(head_idx,tail_idx),"----"*30)
        fr1 = Tracklets_window[tail_idx].ifr
        fr2 = Tracklets_window[tail_idx].last_update
        for kk in range(fr1,fr2):
            ListInsert(Tracklets_window[head_idx].state,kk,Tracklets_window[tail_idx].state[kk],[])
        numHyp = len(Tracklets_window[tail_idx].hyp.score)
        #copy hyp information from window_tracklets to init_tracklets
        for kk in range(fr1,numHyp):
            mot_tracklets_concat(Tracklets_window[head_idx],Tracklets_window[tail_idx],kk,param)
        mot_check_idsw(Tracklets_window[head_idx])
        XX = np.array([0,0,0,0])
        numState = len(Tracklets_window[head_idx].state)
        XX[0] = Tracklets_window[head_idx].state[fr1][0]
        XX[2] = Tracklets_window[head_idx].state[fr1][1]
        PP = param.P
        Tracklets_window[head_idx].type  =  'High'
        mot_appearance_model_update(Tracklets_window[head_idx],param)
        rm_idx.append(tail_idx)
    if len(rm_idx) != 0:
        print("removed tracklets ids of which are {}".format(rm_idx))
        for idx in sorted(rm_idx,reverse=True):
            Tracklets_window.pop(idx)
    
    return Tracklets_window,Obs_grap_window
    
if __name__=='__main__':
    pass
    

