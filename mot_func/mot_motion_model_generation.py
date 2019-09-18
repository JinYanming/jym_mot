import numpy as np
from Common.list2array import lists2array 
from kf_func.km_state_est import km_state_est
#this functions is used to generate a motion model for a new generated tracklet
def mot_motion_model_generation(Trk=None,param=None,type_=None,*args,**kwargs):
    
    if 'Forward' == type_:
        Y=lists2array(Trk.state,4)
        X = np.array([0]*4)
        X = X[:,np.newaxis]
        X[0,:]=Y[0,0]
        X[2,:]=Y[1,0]
        Y = np.delete(Y,[2,3],0)
        #Y[2:3,:]=np.array([])
        Yr=Y
    else:
        if 'Backward' == type_:
            Y=lists2array(Trk.state,4)
            X = np.array([0]*4)
            X = X[:,np.newaxis]
            X[0,:]=Y[0,-1]
            X[2,:]=Y[1,-1]
            Y = np.delete(Y,[2,3],0)
            Yr = Y[:,::-1]
    
    XX,PP=km_state_est(X,Yr,param)
    
    return XX,PP
    
if __name__ == '__main__':
    pass
    

