import numpy as np
from Common.list2array import lists2array
from Common.Idx2Types import Idx2Types
from Obj.Obs_Graph import Obs_Graph
from Obj.Obs_info import Obs_info
from Obj.Tracklet import Tracklet
from Obj.Z_item import Z_item

from mot_func.mot_appearance_model_generation import mot_appearance_model_generation
from mot_func.mot_eval_association_matrix import mot_eval_association_matrix
from mot_func.mot_association_hungarian import mot_association_hungarian


def MOT_Local_Association(Trk = None,detections = None,Obs_grap = None,param = None,fr = None,rgbimg = None,nargout1 = None,*args,**kwargs):
    print("MOT_Local_Association start")
    ILDA  =  param.ILDA
    ## Copyright (C) 2014 Seung-Hwan Bae
## All rights reserved.
    
    Z_meas = detections[fr]
    Z_meas = [detection[2:6] for detection in Z_meas]
    ystate = Z_meas
    obs_grap = Obs_Graph()
    Obs_grap.append(obs_grap)
    Obs_grap[fr].iso_idx  =  np.ones((len(detections[fr])))
    obs_info = Obs_info()
    obs_info.ystate  =  []
    obs_info.yhist  =  []
    if ~(np.all(ystate == 0)):
        yhist = mot_appearance_model_generation(rgbimg,param,ystate,True)
        obs_info.ystate  =  ystate
        obs_info.yhist  =  yhist
        tidx,_,_ = Idx2Types(Trk,'High')
        yidx = np.where(Obs_grap[fr].iso_idx  ==  1)[0]
        if len(tidx) != 0 and len(yidx) != 0:
            Trk_high = []
            Z_set = []
            trk_label = []
            conf_set = []
            for ii in range(0,len(tidx)):
                i = tidx[ii]
                temp_Trk_high = Tracklet()
                temp_Trk_high.hist  =  Trk[i].A_Model
                temp_Trk_high.FMotion  =  Trk[i].FMotion
                temp_Trk_high.last_update  =  Trk[i].last_update
                temp_Trk_high.h  =  Trk[i].state[-1][3]
                temp_Trk_high.w  =  Trk[i].state[-1][2]
                temp_Trk_high.type  =  Trk[i].type
                Trk_high.append(temp_Trk_high)
                trk_label.append(Trk[i].label)
                conf_set.append(Trk[i].Conf_prob)
            # For detections
            meas_label = []
            for jj in range(0,len(yidx)):
                j = yidx[jj]
                z_item = Z_item()
                z_item.hist  =  yhist[:,:,j]
                z_item.pos  =  [ystate[j][0],ystate[j][1]]
                z_item.h  =  ystate[j][3]
                z_item.w  =  ystate[j][2]
                Z_set.append(z_item)
                meas_label.append(j)
            thr = param.obs_thr

            score_mat = mot_eval_association_matrix(Trk_high,Z_set,param,'Obs',ILDA)
            matching,__ = mot_association_hungarian(score_mat,thr,nargout = 2)
            if logical_not(isempty(matching)):
                for i in arange(1,size(matching,1)).reshape(-1):
                    ass_idx_row = matching(i,1)
                    ta_idx = tidx(ass_idx_row)
                    ass_idx_col = matching(i,2)
                    ya_idx = yidx(ass_idx_col)
                    Trk(ta_idx).hyp.score[fr] = score_mat(matching(i,1),matching(i,2))
                    Trk(ta_idx).hyp.ystate[fr] = ystate(arange(),ya_idx)
                    Trk(ta_idx).hyp.new_tmpl  =  copy(yhist(arange(),arange(),ya_idx))
                    Trk(ta_idx).last_update  =  copy[fr]
                    Obs_grap[fr].iso_idx[ya_idx] = 0
    print("MOT_Local_Association obver")
    
    return Trk,Obs_grap,Obs_info
    
if __name__  ==  '__main__':
    pass
    

