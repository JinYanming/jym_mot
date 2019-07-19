# Generated with SMOP  0.41
from libsmop import *
# /workspace/MOT/cmot-v1/Common/Labelling.m

    
@function
def Labelling(param=None,*args,**kwargs):
    varargin = Labelling.varargin
    nargin = Labelling.nargin

    ## Copyright (C) 2014 Seung-Hwan Bae
## All rights reserved.
    
    label=param.label
# /workspace/MOT/cmot-v1/Common/Labelling.m:5
    idx=min(find(label == 0))
# /workspace/MOT/cmot-v1/Common/Labelling.m:6
    param.label[idx]=1
# /workspace/MOT/cmot-v1/Common/Labelling.m:7