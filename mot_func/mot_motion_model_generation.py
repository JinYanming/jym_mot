import numpy as np
from Common.state_list2array import state_lists2array 
def mot_motion_model_generation(Trk=None,param=None,type_=None,*args,**kwargs):
    
    if 'Forward' == type_:
        Y=state_lists2array(Trk.state)
        X[0,:]=Y[0,0]
        X[1,:]=0
        X[2,:]=Y[1,0]
        X[3,:]=0
        Y[2:3,:]=np.array([])
        Yr=Y
    else:
        if 'Backward' == type_:
            Y=state_lists2array(Trk.state)
            X[0,:] = Y[1,-1]
            X[1,:] = 0
            X[2,:] = Y[2,-1]
            X[3,:] = 0
            Y[2:3,:] = np.array([])
            Yr = Y[:,::-1]
    
    XX,PP=km_state_est(X,Yr,param,nargout=2)
    return XX,PP
    
if __name__ == '__main__':
    pass
    

