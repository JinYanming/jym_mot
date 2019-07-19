# Generated with SMOP  0.41
from libsmop import *
# /workspace/MOT/cmot-v1/Common/warpimg.m

    
@function
def warpimg(img=None,p=None,sz=None,*args,**kwargs):
    varargin = warpimg.varargin
    nargin = warpimg.nargin

    # function wimg = warpimg(img, p, sz)
    
    #    img(h,w)
#    p(6,n) : mat format
#    sz(th,tw)
    
    ## Copyright (C) 2005 Jongwoo Lim and David Ross.
## All rights reserved.
    
    if (nargin < 3):
        sz=size(img)
# /workspace/MOT/cmot-v1/Common/warpimg.m:14
    
    if (size(p,1) == 1):
        p=ravel(p)
# /workspace/MOT/cmot-v1/Common/warpimg.m:17
    
    w=sz(2)
# /workspace/MOT/cmot-v1/Common/warpimg.m:19
    h=sz(1)
# /workspace/MOT/cmot-v1/Common/warpimg.m:19
    n=size(p,2)
# /workspace/MOT/cmot-v1/Common/warpimg.m:19
    #[x,y] = meshgrid(1:w, 1:h);
    x,y=meshgrid(concat([arange(1,w)]) - w / 2,concat([arange(1,h)]) - h / 2,nargout=2)
# /workspace/MOT/cmot-v1/Common/warpimg.m:21
    pos=reshape(dot(cat(2,ones(dot(h,w),1),ravel(x),ravel(y)),concat([[p(1,arange()),p(2,arange())],[p(arange(3,4),arange()),p(arange(5,6),arange())]])),concat([h,w,n,2]))
# /workspace/MOT/cmot-v1/Common/warpimg.m:22
    wimg=squeeze(interp2(img,pos(arange(),arange(),arange(),1),pos(arange(),arange(),arange(),2)))
# /workspace/MOT/cmot-v1/Common/warpimg.m:24
    wimg[find(isnan(wimg))]=0
# /workspace/MOT/cmot-v1/Common/warpimg.m:25