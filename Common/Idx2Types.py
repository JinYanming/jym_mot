# Generated with SMOP  0.41
from libsmop import *
# /workspace/MOT/cmot-v1/Common/Idx2Types.m

    
@function
def Idx2Types(Trk=None,type_=None,*args,**kwargs):
    varargin = Idx2Types.varargin
    nargin = Idx2Types.nargin

    ## Copyright (C) 2014 Seung-Hwan Bae
## All rights reserved.
    
    indx=[]
# /workspace/MOT/cmot-v1/Common/Idx2Types.m:5
    reliable=[]
# /workspace/MOT/cmot-v1/Common/Idx2Types.m:6
    new=[]
# /workspace/MOT/cmot-v1/Common/Idx2Types.m:7
    for i in arange(1,length(Trk)).reshape(-1):
        if strcmp(Trk(i).type,type_):
            indx=concat([indx,i])
# /workspace/MOT/cmot-v1/Common/Idx2Types.m:10
            if Trk(i).reliable == 1:
                reliable=concat([reliable,i])
# /workspace/MOT/cmot-v1/Common/Idx2Types.m:12
            if Trk(i).isnew == 1:
                new=concat([new,i])
# /workspace/MOT/cmot-v1/Common/Idx2Types.m:15
    
    return indx,reliable,new
    
if __name__ == '__main__':
    pass
    