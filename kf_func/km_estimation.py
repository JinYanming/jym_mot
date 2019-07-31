# Generated with SMOP  0.41
from libsmop import *
# /workspace/MOT/cmot-v1/kf_func/km_estimation.m

    
@function
def km_estimation(X=None,Y=None,param=None,P=None,*args,**kwargs):
    varargin = km_estimation.varargin
    nargin = km_estimation.nargin

    # X: object motion state, (x_pos, x_vel, y_pos, y_vel)
# Y: measurements, (x_pos, y_pos)
    
    ## Copyright (C) 2014 Seung-Hwan Bae
## All rights reserved.
    
    if nargin < 4:
        P=param.P
# /workspace/MOT/cmot-v1/kf_func/km_estimation.m:9
    
    H=param.H
# /workspace/MOT/cmot-v1/kf_func/km_estimation.m:12
    R=param.R
# /workspace/MOT/cmot-v1/kf_func/km_estimation.m:13
    Ts=param.Ts
# /workspace/MOT/cmot-v1/kf_func/km_estimation.m:16
    F1=concat([[1,Ts],[0,1]])
# /workspace/MOT/cmot-v1/kf_func/km_estimation.m:17
    Fz=zeros(2,2)
# /workspace/MOT/cmot-v1/kf_func/km_estimation.m:18
    param.F = copy(concat([[F1,Fz],[Fz,F1]]))
# /workspace/MOT/cmot-v1/kf_func/km_estimation.m:19
    A=param.F
# /workspace/MOT/cmot-v1/kf_func/km_estimation.m:22
    Q=param.Q
# /workspace/MOT/cmot-v1/kf_func/km_estimation.m:23
    if logical_not(isempty(Y)):
        MM,PP=kf_loop(X,P,H,R,Y,A,Q,nargout=2)
# /workspace/MOT/cmot-v1/kf_func/km_estimation.m:26
    else:
        MM,PP=kf_predict(X,P,A,Q,nargout=2)
# /workspace/MOT/cmot-v1/kf_func/km_estimation.m:28
    
    return MM,PP
    
if __name__ == '__main__':
    pass
    