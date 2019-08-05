import numpy as np
    
def mot_generation_tracklet(rgbimg=None,Trk=None,Obs_grap=None,detections=None,param=None,Y_set=None,fr=None,*args,**kwargs):

    
    ct=0
    non_iso=[]
    new_thr=param.new_thr
    for i in range(0,len(Y_set[fr])):
        prt_idx=Y_set(fr).child[i]
        if len(prt_idx) <= 1:
            child_idx=mot_search_association(Y_set,fr,prt_idx)
            ass_idx=mot_return_ass_idx(child_idx,prt_idx,i,fr)
        else:
            child_idx=[]
            tmp_ass_idx=[]
            ass_ln=[]
            for j in range(0,len(prt_idx)):
                child_idx[j]=mot_search_association(Y_set,fr,prt_idx(j))
                tmp_ass_idx[j]=mot_return_ass_idx(child_idx[j],prt_idx(j),i,fr)
                ass_ln[j]=len(find(tmp_ass_idx[j] != 0))
            __,pid=max(ass_ln,nargout=2)
            ass_idx=tmp_ass_idx[pid]
        if len(find(ass_idx != 0)) >= new_thr:
            ct=ct + 1
            Trk,param=mot_tracklets_components_setup(rgbimg,Trk,detections,fr,ass_idx,param,[],nargout=2)
            idx=[]
            nT=len(find(ass_idx != 0))
            for h in range(0,nT):
                idx1=find(Obs_grap(fr + h - nT).iso_idx == 1)
                idx2=idx1(ass_idx(end() + h - nT))
                idx=concat([idx,idx2])
            non_iso[ct,range()]=idx
    for j in range(0,len(non_iso)):
        setr=unique(non_iso(range(),j))
        if Obs_grap(fr + j - nT).iso_idx(setr) == 0:
            puase
        Obs_grap(fr + j - nT).iso_idx[setr]=0
    
    
    return Trk,param,Obs_grap
    
if __name__ == '__main__':
    pass
    

