# Generated with SMOP  0.41
from libsmop import *
# /workspace/MOT/cmot-v1/Common/estimation_size.m

    
@function
def estimation_size(Trk=None,ystate=None,fr=None,*args,**kwargs):
    varargin = estimation_size.varargin
    nargin = estimation_size.nargin

    ## Copyright (C) 2014 Seung-Hwan Bae
## All rights reserved.
    
    init_time=Trk.ifr
# /workspace/MOT/cmot-v1/Common/estimation_size.m:6
    nof_s=4
# /workspace/MOT/cmot-v1/Common/estimation_size.m:7
    sum_size=Trk.state[end()](arange(3,4))
# /workspace/MOT/cmot-v1/Common/estimation_size.m:9
    if fr == Trk.last_update:
        size_state=ystate(arange(3,4))
# /workspace/MOT/cmot-v1/Common/estimation_size.m:11
    else:
        if fr > init_time + 3:
            for j in arange(1,nof_s).reshape(-1):
                sum_size=sum_size + Trk.state[end() - j](arange(3,4))
# /workspace/MOT/cmot-v1/Common/estimation_size.m:15
            size_state=sum_size / (nof_s + 1)
# /workspace/MOT/cmot-v1/Common/estimation_size.m:17
        else:
            all_est=cell2mat(Trk.state)
# /workspace/MOT/cmot-v1/Common/estimation_size.m:19
            sum_size=sum_size + sum(all_est(arange(3,4),arange()),2)
# /workspace/MOT/cmot-v1/Common/estimation_size.m:20
            size_state=sum_size / (size(all_est,2) + 1)
# /workspace/MOT/cmot-v1/Common/estimation_size.m:21
    
    return size_state
    
if __name__ == '__main__':
    pass
    