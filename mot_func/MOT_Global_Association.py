import numpy as np
from Common.Idx2Types import Idx2Types
def MOT_Global_Association(Trk = None,Obs_grap = None,Obs_info = None,param = None,fr = None,*args,**kwargs):

    ILDA  =  param.ILDA
    Refer = []
    Test = []
    all_indx = [i for i in range(0,len(Trk))]
    low_indx,_,_ = Idx2Types(Trk,'Low')
    high_indx = np.setdiff1d(all_indx,low_indx)
    yidx = np.where(Obs_grap[fr].iso_idx  ==  1)
    yhist = Obs_info.yhist
    ystate = Obs_info.ystate
    High_trk = []
    Low_trk = []
    Y_set = []
    if not (np.all(low_indx ==0 )):
        # For tracklets with low confidence
        for ii in range(0,len(low_indx)):
            i = low_indx[ii]
            Low_trk[ii].hist  =  Trk[i].A_Model
            Low_trk[ii].FMotion  =  Trk[i].FMotion
            Low_trk[ii].h  =  Trk[i].state[-1][3]
            Low_trk[ii].w  =  Trk[i].state[-1][2]
            Low_trk[ii].last_update  =  Trk[i].last_update
            Low_trk[ii].end_time  =  Trk[i].efr
            Low_trk[ii].type  =  Trk[i].type
        # For tracklet with high confidence
        for jj in range(1,len(high_indx)):
            j = high_indx[jj]
            High_trk[jj].hist  =  Trk[j].A_Model
            High_trk[jj].h  =  Trk[j].state[-1][3]
            High_trk[jj].w  =  Trk[j].state[-1][2]
            High_trk[jj].FMotion  =  Trk[j].FMotion
            XX,PP = mot_motion_model_generation(Trk[j],param,'Backward',nargout = 2)
            High_trk[jj].BMotion.X  =  XX
            High_trk[jj].BMotion.P  =  PP
            High_trk[jj].last_update  =  Trk[j].last_update
            High_trk[jj].init_time  =  Trk[j].ifr
        iso_label = []
        if logical_not(isempty(yidx)):
            # For detections
            for jj in range(1,len(yidx)):
                j = yidx[jj]
                Y_set[jj].hist  =  yhist[:,:,j]
                Y_set[jj].pos  =  concat([[ystate(1,j)],[ystate(2,j)]])
                Y_set[jj].h  =  ystate[4,j]
                Y_set[jj].w  =  ystate[3,j]
                iso_label = j
        thr = param.obs_thr
        score_trk = mot_eval_association_matrix(Low_trk,High_trk,param,'Trk',ILDA)
        score_obs = mot_eval_association_matrix(Low_trk,Y_set,param,'Obs',ILDA)
        score_mat = concat([score_trk,score_obs])
        matching,Affinity = mot_association_hungarian(score_mat,thr,nargout = 2)
        alpha = param.alpha
        rm_idx = []
        for m in range(1,len(Affinity)):
            mat_idx = matching(m,2)
            if mat_idx <=  len(high_indx):
                t_idx = low_indx(matching(m,1))
                y_idx = high_indx(matching(m,2))
                Trk(y_idx).ifr  =  copy(Trk[t_idx].ifr)
                fr1 = Trk[t_idx].ifr
                fr2 = Trk[t_idx].efr
                for kk in range(fr1,fr2):
                    Trk(y_idx).state[kk] = Trk[t_idx].state[kk]
                numHyp = len(Trk[t_idx].hyp.score)
                for kk in range(fr1,numHyp):
                    Trk(y_idx).hyp.score[kk] = Trk[t_idx].hyp.score(kk)
                    Trk(y_idx).hyp.ystate[kk] = Trk[t_idx].hyp.ystate[kk]
                for kk in range(numHyp + 1,fr - 1):
                    Trk(y_idx).hyp.score[kk] = param.init_prob
                    Trk(y_idx).hyp.ystate[kk] = []
                Trk(y_idx).A_Model  =  copy(dot(alpha,(Trk[t_idx].A_Model)) + dot((1 - alpha),(Trk(y_idx).A_Model)))
                XX = []
                numState = len(Trk(y_idx).state)
                XX[1,:] = Trk(y_idx).state[fr1](1)
                XX[3,:] = Trk(y_idx).state[fr1](2)
                XX[2,:] = 0
                XX[4,:] = 0
                PP = param.P
                for ff in range(fr1,numState):
                    tState = Trk(y_idx).state[ff]
                    if logical_not(isempty(tState)):
                        XX,PP = km_estimation(XX,tState(range(1,2)),param,PP,nargout = 2)
                    else:
                        tState = Trk(y_idx).state[fr2]
                        XX,PP = km_estimation(XX,[],param,PP,nargout = 2)
                        Trk(y_idx).state[ff][range(1,2),:] = concat([[XX(1)],[XX(3)]])
                        Trk(y_idx).state[ff][range(3,4),:] = concat([[tState(1)],[tState(3)]])
                    Trk(y_idx).FMotion.X[:,ff] = XX
                    Trk(y_idx).FMotion.P[:,:,ff] = PP
                Trk(y_idx).label  =  copy(Trk[t_idx].label)
                Trk(y_idx).type  =  copy('High')
                rm_idx = concat([rm_idx,t_idx])
            else:
                m_idx = matching(m,2) - len(high_indx)
                t_idx = low_indx(matching(m,1))
                y_idx = yidx(m_idx)
                Trk[t_idx].hyp.score[fr] = Affinity(m)
                Trk[t_idx].hyp.ystate[fr] = ystate[:,y_idx]
                Trk[t_idx].hyp.new_tmpl  =  yhist[:,:,y_idx]
                Trk[t_idx].last_update  =  fr
                Obs_grap(fr).iso_idx[y_idx] = 0
        if logical_not(isempty(rm_idx)):
            Trk[rm_idx] = []
    
    return Trk,Obs_grap
    
if __name__=='__main__':
    pass
    
