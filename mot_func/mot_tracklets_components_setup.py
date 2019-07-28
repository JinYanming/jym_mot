import numpy as np
from Obj.Tracklet import Tracklet
from Common.Labelling import Labelling

from mot_func.mot_motion_model_generation import mot_motion_model_generation
from mot_func.mot_appearance_model_generation import mot_appearance_model_generation
def mot_tracklets_components_setup(img=None,Trk=None,detections=None,cfr=None,y_idx=None,param=None,tmp_label=None,*args,**kwargs):
    #y_idx the tracklet state
    ass_idx=y_idx
    nofa=len(np.nonzero(y_idx)[0])
    tracklet = Tracklet()#genenrate a new tracklet
    tracklet.Conf_prob = param.init_prob
    tracklet.type = 'High'
    tracklet.reliable = 'False'
    tracklet.isnew = 1
    tracklet.sub_img = []
    tracklet.status = 'none'
    if tmp_label != None :
        tracklet.label = tmp_label
    else:
        param,idx=Labelling(param,nargout=2)
        tracklet.label = idx
    
    tracklet.ifr = cfr - nofa + 1
    tracklet.efr = 0
    tracklet.last_update = cfr
    Acc_tmpl = np.zeros(((param.Bin*3),param.subregion))
    for i in range(0,nofa):#from crruent frame to  track the len(ass_idx) privious frames detections
        tmp_idx=cfr - i -1
        state = np.array((4))
        temp_state = detections[tmp_idx][ass_idx[tmp_idx][0]][2:6]
        tracklet.state.append(temp_state)
        #tracklet.state[tmp_idx][3,1]=detections(tmp_idx).h(ass_idx(tmp_idx))
        tmpl=mot_appearance_model_generation(img[tmp_idx],param,temp_state,False)
        Acc_tmpl=Acc_tmpl + tmpl
    tracklet.state.reverse()
    
    # Appearnce Model
    tracklet.A_Model = Acc_tmpl / nofa
    # Forward Motion Model
    XX,PP=mot_motion_model_generation(tracklet,param,'Forward',nargout=2)
    lt=size(XX,2)
    tracklet.FMotion.X[arange(),arange(cfr - lt + 1,cfr)]=XX
    tracklet.FMotion.P[arange(),arange(),arange(cfr - lt + 1,cfr)]=PP
    tracklet.BMotion.X = []
    tracklet.BMotion.P = []
    tracklet.hyp.score[cfr]=0
    tracklet.hyp.ystate[cfr]=[]
    return tracklet,param
    
if __name__ == '__main__':
    pass
    

