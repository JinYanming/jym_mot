# Generated with SMOP  0.41
from libsmop import *
# /workspace/MOT/cmot-v1/Common/calc_overlap2.m

    
@function
def calc_overlap2(cur_det=None,prev_det=None,fr=None,*args,**kwargs):
    varargin = calc_overlap2.varargin
    nargin = calc_overlap2.nargin

    ##f2 can be an array and f1 should be a scalar.
### this will find the overlap between dres1(f1) (only one) and all detection windows in dres2(f2(:))
    
    ## Calculate overlap
    n2=length(prev_det.x)
# /workspace/MOT/cmot-v1/Common/calc_overlap2.m:6
    cx1=cur_det.x(fr)
# /workspace/MOT/cmot-v1/Common/calc_overlap2.m:8
    cx2=cur_det.x(fr) + cur_det.w(fr) - 1
# /workspace/MOT/cmot-v1/Common/calc_overlap2.m:9
    cy1=cur_det.y(fr)
# /workspace/MOT/cmot-v1/Common/calc_overlap2.m:10
    cy2=cur_det.y(fr) + cur_det.h(fr) - 1
# /workspace/MOT/cmot-v1/Common/calc_overlap2.m:11
    gx1=prev_det.x
# /workspace/MOT/cmot-v1/Common/calc_overlap2.m:13
    gx2=prev_det.x + prev_det.w - 1
# /workspace/MOT/cmot-v1/Common/calc_overlap2.m:14
    gy1=prev_det.y
# /workspace/MOT/cmot-v1/Common/calc_overlap2.m:15
    gy2=prev_det.y + prev_det.h - 1
# /workspace/MOT/cmot-v1/Common/calc_overlap2.m:16
    ca=multiply((cur_det.w(fr)),(cur_det.h(fr)))
# /workspace/MOT/cmot-v1/Common/calc_overlap2.m:18
    
    ga=multiply((prev_det.w),(prev_det.h))
# /workspace/MOT/cmot-v1/Common/calc_overlap2.m:19
    xx1=max(cx1,gx1)
# /workspace/MOT/cmot-v1/Common/calc_overlap2.m:23
    yy1=max(cy1,gy1)
# /workspace/MOT/cmot-v1/Common/calc_overlap2.m:24
    xx2=min(cx2,gx2)
# /workspace/MOT/cmot-v1/Common/calc_overlap2.m:25
    yy2=min(cy2,gy2)
# /workspace/MOT/cmot-v1/Common/calc_overlap2.m:26
    w=xx2 - xx1 + 1
# /workspace/MOT/cmot-v1/Common/calc_overlap2.m:27
    h=yy2 - yy1 + 1
# /workspace/MOT/cmot-v1/Common/calc_overlap2.m:28
    inds=find(multiply((w > 0),(h > 0)))
# /workspace/MOT/cmot-v1/Common/calc_overlap2.m:30
    ov=zeros(1,n2)
# /workspace/MOT/cmot-v1/Common/calc_overlap2.m:31
    ov_n1=zeros(1,n2)
# /workspace/MOT/cmot-v1/Common/calc_overlap2.m:32
    ov_n2=zeros(1,n2)
# /workspace/MOT/cmot-v1/Common/calc_overlap2.m:33
    inter=multiply(w(inds),h(inds))
# /workspace/MOT/cmot-v1/Common/calc_overlap2.m:34
    
    u=ca + ga(inds) - multiply(w(inds),h(inds))
# /workspace/MOT/cmot-v1/Common/calc_overlap2.m:35
    
    ov[inds]=inter / u
# /workspace/MOT/cmot-v1/Common/calc_overlap2.m:36
    
    ov_n1[inds]=inter / ca
# /workspace/MOT/cmot-v1/Common/calc_overlap2.m:37
    ov_n2[inds]=inter / ga(inds)
# /workspace/MOT/cmot-v1/Common/calc_overlap2.m:38
    return ov,ov_n1,ov_n2
    
if __name__ == '__main__':
    pass
    