import numpy as np
from mot_func.mot_return_ass_idx import mot_return_ass_idx
from mot_func.mot_search_association import mot_search_association
from mot_func.mot_tracklets_components_setup import mot_tracklets_components_setup
def mot_generation_tracklet(rgbimg=None,Trk=None,Obs_grap=None,detections=None,param=None,cfr=None,*args,**kwargs):

    
    ct=0
    non_iso = []
    new_thr = param.new_thr
    for j in range(0,param.window_length - param.window_min_length_tracklet_generated):
        fr = cfr - j
        for i in range(0,len(Obs_grap[fr].child)):
            #prt_idx is the end of a tracklet it cannot be -1
            prt_idx = Obs_grap[fr].child[i]
            if prt_idx != -1:
                child_idx = mot_search_association(Obs_grap,fr,prt_idx)
                ass_idx = mot_return_ass_idx(child_idx,prt_idx,i,fr)
                if len(np.where(np.array(ass_idx) != -1)[0]) >= new_thr:
                    #generate the tracklet
                    Trk,param = mot_tracklets_components_setup(rgbimg,Trk,detections,fr+1,ass_idx,param,None,Obs_grap)
    
    return Trk,param,Obs_grap
    
if __name__ == '__main__':
    pass
    

