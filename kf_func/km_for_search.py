import numpy as np
from Common.list2array import lists2array 
from kf_func.km_state_est import km_state_est
from Common.estimation_size import estimation_size
from kf_func.km_estimation import km_estimation
from Obj.Obs_Graph import F_Motion
#this functions is used to generate a motion model for pre_association to search the relationship between detections
def mot_motion_model_generation_for_search(head1_state,head2_state,param):
    
    FMotion = F_Motion()
    FMotion_wh = F_Motion()
    states = []
    states.append(head1_state)
    states.append(head2_state)
    Y=lists2array(states,4)
    X = np.array([0]*4)
    X = X[:,np.newaxis]
    X[0,:]=Y[0,0]
    X[2,:]=Y[1,0]
    Y = np.delete(Y,[2,3],0)
    Yr=Y
    XX,PP=km_state_est(X,Yr,param)
    FMotion.X = XX
    FMotion.P = PP


    if param.wh_predict == True:
        #for w and h
        Y=lists2array(states,4)
        X = np.array([0]*4)
        X = X[:,np.newaxis]
        X[0,:]=Y[2,0]
        X[2,:]=Y[3,0]
        Y = np.delete(Y,[0,1],0)
        Yr=Y
        XX,PP=km_state_est(X,Yr,param)
        FMotion_wh.X = XX
        FMotion_wh.P = PP
    
    return FMotion,FMotion_wh

def km_state_predict(FMotion = None,FMotion_wh = None,cur_det = None,param = None,*args,**kwargs):

    XX=FMotion.X[:,-1]
    PP=FMotion.P[:,:,-1]
    XX,PP=km_estimation(XX,[],param,PP)
    
    pos_state = np.r_[XX[0],XX[2]]
    #predict wh
    if param.wh_predict == True:
        XX=FMotion_wh.X[:,-1]
        PP=FMotion_wh.P[:,:,-1]
        XX,PP=km_estimation(XX,[],param,PP)
    
        size_state = np.r_[XX[0],XX[2]]
    else:
        size_state = np.r_[cur_det[2],cur_det[3]]
    predict_state = np.r_[pos_state[:,np.newaxis],size_state[:,np.newaxis]].squeeze()
    return predict_state

def km_state_update_for_search(FMotion = None,FMotion_wh = None,det_pos = None,param = None,*args,**kwargs):

    
    size_state = det_pos
    XX=FMotion.X[:,-1]
    PP=FMotion.P[:,:,-1]
    XX,PP=km_estimation(XX,det_pos[0:2],param,PP)
    #np.c_[FMotion.X,XX]
    FMotion.X = XX
    #np.concatenate((FMotion.P,PP),axis = 2)
    FMotion.P = PP
    
    if param.wh_predict == True:
        #update wh kalman filter
        XX=FMotion_wh.X[:,-1]
        PP=FMotion_wh.P[:,:,-1]
        XX,PP=km_estimation(XX,det_pos[2:],param,PP)
        #np.c_[FMotion.X,XX]
        FMotion_wh.X = XX
        #np.concatenate((FMotion.P,PP),axis = 2)
        FMotion_wh.P = PP
    return FMotion,FMotion_wh
