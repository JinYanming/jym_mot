import numpy as np
from Obj.Tracklet import Tracklet
from Common.Labelling import Labelling
from tools.ListGiant import ListInsert
from mot_func.mot_motion_model_generation import mot_motion_model_generation
from mot_func.mot_appearance_model_generation import mot_appearance_model_generation
from mot_func.mot_tracklet_confidence_update import mot_tracklet_confidence_update
from mot_func.mot_appearance_model_update import mot_appearance_model_update
from mot_func.mot_check_idsw import mot_check_idsw
from mot_func.mot_label_resign import mot_get_label
def mot_tracklets_components_setup(img=None,Trk=None,detections=None,cfr=None,ass_idx=None,param=None,tmp_label=None,Obs_grap=None,*args,**kwargs):
    #ass_idx the tracklet state
    nofa=len(np.where(np.array(ass_idx) != -1)[0])
    #record the detections id which refer to the object
    ystate_id_list = [-1]*cfr
    tracklet = Tracklet()#genenrate a new tracklet
    tracklet.Conf_prob = param.init_prob
    tracklet.type = 'High'
    tracklet.reliable = 'False'
    tracklet.isnew = 1
    tracklet.sub_img = []
    tracklet.status = 'none'
    tracklet.hyp.score = []

    tracklet.ifr = cfr - nofa
    tracklet.efr = 0
    tracklet.last_update = cfr - 1
    tracklet.window_end = cfr - 1
    Acc_tmpl = np.zeros(((param.Bin*3),param.subregion))
    A_Model_list = [None]*(cfr-nofa)
    #from crruent frame to  track the len(ass_idx) privious frames detection
    for i in range(0,nofa):
        state = np.array((4))
        tmp_idx=cfr - i -1
        temp_state = np.array(detections[tmp_idx][ass_idx[tmp_idx]][2:6].copy())
        temp_affinity = Obs_grap[tmp_idx].child_A_Model_affinity[ass_idx[tmp_idx]]
        ystate_id_list.append(detections[tmp_idx][ass_idx[tmp_idx]][1])
        ListInsert(tracklet.hyp.score,tmp_idx,temp_affinity,0)
        ListInsert(tracklet.state,tmp_idx,temp_state,[])
        ListInsert(tracklet.detections_id_list,tmp_idx,ass_idx[tmp_idx],None)
        tmpl=mot_appearance_model_generation(img[tmp_idx],param,temp_state,False).squeeze()
        A_Model_list.append(tmpl)
    tracklet.A_model_list = A_Model_list
    ystate_id_list.reverse()
    
    # Appearnce Model
    tracklet.A_Model = Acc_tmpl / nofa
    # Forward Motion Model
    # XX [4,frames]
    XX,PP=mot_motion_model_generation(tracklet,param,'Forward')
    lt=XX.shape[1]
    tracklet.FMotion.X = np.zeros((4,cfr))
    tracklet.FMotion.P = np.zeros((4,4,cfr))
    tracklet.FMotion.X[:,cfr -lt:]=XX
    tracklet.FMotion.P[:,:,cfr - lt:]=PP
    tracklet.BMotion.X = []
    tracklet.BMotion.P = []
    tracklet.hyp.ystates_id = [0]*cfr
    tracklet.hyp.ystate = [item for item in tracklet.state]
    tracklet.hyp.ystates_id = ystate_id_list

    mot_check_idsw(tracklet)
    mot_get_label(Trk,tracklet,param)
    Trk.append(tracklet)
    #count the number of the total tracklets
    param.total_tracklet_count += 1
    if (tracklet.window_end-tracklet.ifr +1) > 5:
        mot_tracklet_confidence_update(tracklet,param,param.lambda_)
    mot_appearance_model_update(tracklet,param)
    
    #label the used detections as -1 in iso_idx and child
    used_idx = []
    nT = len(np.where(np.array(ass_idx) != -1)[0])
    for hh in range(0,nT):
        h = -nT+hh
        used_idx.append(ass_idx[h])
    for i in range(0,len(used_idx)):
        iden = used_idx[i]
        Obs_grap[cfr + i - nT].iso_idx[iden] = -1
        Obs_grap[cfr + i - nT].child[iden] = -1

    print("Window Tracklet Generated:len(Trk_Window)+1",ass_idx[-nofa-2:])
    return Trk,param
    
if __name__ == '__main__':
    pass
    

