import numpy as np
from tools.ListGiant import ListInsert

def mot_tracklets_concat(init_tracklet,window_tracklet,cr_fr,param):
    concat_fr = cr_fr
    ListInsert(init_tracklet.state,concat_fr,window_tracklet.state[concat_fr],[])
    ListInsert(init_tracklet.hyp.score,concat_fr,window_tracklet.hyp.score[concat_fr],0)
    ListInsert(init_tracklet.hyp.ystate,concat_fr,window_tracklet.hyp.ystate[concat_fr],[])
    #ListInsert(init_tracklet.hyp.ystates_ids,concat_fr,window_tracklet.hyp.ystates_ids[concat_fr],[])
    init_tracklet.FMotion.X = np.c_[init_tracklet.FMotion.X,window_tracklet.FMotion.X[:,concat_fr]]
    init_tracklet.FMotion.P = np.concatenate((init_tracklet.FMotion.P,window_tracklet.FMotion.P[:,:,concat_fr][:,:,np.newaxis]),axis = 2)
    init_tracklet.A_Model  =  param.alpha*window_tracklet.A_Model + (1 - param.alpha)*init_tracklet.A_Model
    init_tracklet.last_update = concat_fr
    ListInsert(init_tracklet.A_model_list,concat_fr,window_tracklet.A_model_list,None)
    ListInsert(init_tracklet.hyp.ystates_id,concat_fr,window_tracklet.hyp.ystates_id,-1)
    if len(window_tracklet.state[concat_fr]) > 0:
        window_tracklet.ifr = concat_fr + 1
        
        #remove the detections which is already concat with existing init tracklets
        window_tracklet.state[concat_fr] = []
        window_tracklet.FMotion.X[:,concat_fr] = 0
        window_tracklet.FMotion.P[:,:,concat_fr] = 0
        window_tracklet.hyp.score[concat_fr] = 0
        window_tracklet.hyp.ystate[concat_fr] = []
