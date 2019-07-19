# Generated with SMOP  0.41
from libsmop import *
# /workspace/MOT/cmot-v1/Common/motion_affinity.m

    
@function
def motion_affinity(x=None,mean=None,var=None,*args,**kwargs):
    varargin = motion_affinity.varargin
    nargin = motion_affinity.nargin

    ## Copyright (C) 2014 Seung-Hwan Bae
## All rights reserved.
    
    prob_pdf=exp(dot(dot(dot(- 0.5,(x - mean).T),inv(var)),(x - mean)))
# /workspace/MOT/cmot-v1/Common/motion_affinity.m:5