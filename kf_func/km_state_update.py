# Generated with SMOP  0.41
from libsmop import *
# /workspace/MOT/cmot-v1/kf_func/km_state_update.m

    
@function
def km_state_update(Trk=None,ymeas=None,param=None,fr=None,*args,**kwargs):
    varargin = km_state_update.varargin
    nargin = km_state_update.nargin

    ## Copyright (C) 2014 Seung-Hwan Bae
## All rights reserved.
    
    size_state=estimation_size(Trk,ymeas,fr)
# /workspace/MOT/cmot-v1/kf_func/km_state_update.m:5
    XX=Trk.FMotion.X(arange(),end())
# /workspace/MOT/cmot-v1/kf_func/km_state_update.m:7
    PP=Trk.FMotion.P(arange(),arange(),end())
# /workspace/MOT/cmot-v1/kf_func/km_state_update.m:8
    if logical_not(isempty(ymeas)):
        XX,PP=km_estimation(XX,ymeas(arange(1,2)),param,PP,nargout=2)
# /workspace/MOT/cmot-v1/kf_func/km_state_update.m:11
    else:
        XX,PP=km_estimation(XX,[],param,PP,nargout=2)
# /workspace/MOT/cmot-v1/kf_func/km_state_update.m:13
    
    pos_state=concat([[XX(1)],[XX(3)]])
# /workspace/MOT/cmot-v1/kf_func/km_state_update.m:16
    Trk.state[fr]=concat([[pos_state],[size_state]])
# /workspace/MOT/cmot-v1/kf_func/km_state_update.m:17
    Trk.FMotion.X[arange(),fr]=XX
# /workspace/MOT/cmot-v1/kf_func/km_state_update.m:19
    Trk.FMotion.P[arange(),arange(),fr]=PP
# /workspace/MOT/cmot-v1/kf_func/km_state_update.m:20