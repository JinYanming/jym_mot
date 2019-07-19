# Generated with SMOP  0.41
from libsmop import *
# /workspace/MOT/cmot-v1/Common/affparam2mat.m

    
@function
def affparam2mat(p=None,*args,**kwargs):
    varargin = affparam2mat.varargin
    nargin = affparam2mat.nargin

    # function q = affparam2mat(p)
    
    # The functions affparam2geom and affparam2mat convert a 'geometric'
# affine parameter to/from a matrix form (2x3 matrix).
# 
# affparam2geom converts a 2x3 matrix to 6 affine parameters
# (x, y, th, scale, aspect, skew), and affparam2mat does the inverse.
    
    #    p(6,n) : [dx dy sc th sr phi]'
#    q(6,n) : [q(1) q(3) q(4); q(2) q(5) q(6)]
    
    # Reference "Multiple View Geometry in Computer Vision" by Richard
# Hartley and Andrew Zisserman.
    
    # Copyright (C) Jongwoo Lim and David Ross.  All rights reserved.
    
    sz=size(p)
# /workspace/MOT/cmot-v1/Common/affparam2mat.m:19
    if (length(ravel(p)) == 6):
        p=ravel(p)
# /workspace/MOT/cmot-v1/Common/affparam2mat.m:21
    
    s=p(3,arange())
# /workspace/MOT/cmot-v1/Common/affparam2mat.m:23
    th=p(4,arange())
# /workspace/MOT/cmot-v1/Common/affparam2mat.m:23
    r=p(5,arange())
# /workspace/MOT/cmot-v1/Common/affparam2mat.m:23
    phi=p(6,arange())
# /workspace/MOT/cmot-v1/Common/affparam2mat.m:23
    cth=cos(th)
# /workspace/MOT/cmot-v1/Common/affparam2mat.m:24
    sth=sin(th)
# /workspace/MOT/cmot-v1/Common/affparam2mat.m:24
    cph=cos(phi)
# /workspace/MOT/cmot-v1/Common/affparam2mat.m:24
    sph=sin(phi)
# /workspace/MOT/cmot-v1/Common/affparam2mat.m:24
    ccc=multiply(multiply(cth,cph),cph)
# /workspace/MOT/cmot-v1/Common/affparam2mat.m:25
    ccs=multiply(multiply(cth,cph),sph)
# /workspace/MOT/cmot-v1/Common/affparam2mat.m:25
    css=multiply(multiply(cth,sph),sph)
# /workspace/MOT/cmot-v1/Common/affparam2mat.m:25
    scc=multiply(multiply(sth,cph),cph)
# /workspace/MOT/cmot-v1/Common/affparam2mat.m:26
    scs=multiply(multiply(sth,cph),sph)
# /workspace/MOT/cmot-v1/Common/affparam2mat.m:26
    sss=multiply(multiply(sth,sph),sph)
# /workspace/MOT/cmot-v1/Common/affparam2mat.m:26
    q[1,arange()]=p(1,arange())
# /workspace/MOT/cmot-v1/Common/affparam2mat.m:27
    q[2,arange()]=p(2,arange())
# /workspace/MOT/cmot-v1/Common/affparam2mat.m:27
    q[3,arange()]=multiply(s,(ccc + scs + multiply(r,(css - scs))))
# /workspace/MOT/cmot-v1/Common/affparam2mat.m:28
    q[4,arange()]=multiply(s,(multiply(r,(ccs - scc)) - ccs - sss))
# /workspace/MOT/cmot-v1/Common/affparam2mat.m:28
    q[5,arange()]=multiply(s,(scc - ccs + multiply(r,(ccs + sss))))
# /workspace/MOT/cmot-v1/Common/affparam2mat.m:29
    q[6,arange()]=multiply(s,(multiply(r,(ccc + scs)) - scs + css))
# /workspace/MOT/cmot-v1/Common/affparam2mat.m:29
    q=reshape(q,sz)
# /workspace/MOT/cmot-v1/Common/affparam2mat.m:30