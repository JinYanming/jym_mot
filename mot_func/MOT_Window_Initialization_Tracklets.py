import numpy as np
import time
from mot_func.mot_search_association import mot_search_association
from mot_func.mot_return_ass_idx import mot_return_ass_idx
from mot_func.mot_tracklets_components_setup import mot_tracklets_components_setup
def MOT_Window_Initialization_Tracklets(rgbimg=None,Trk=None,detections=None,param=None,Obs_grap=None,window_start_frame=None,window_end_frame = None,*args,**kwargs):
    print("MOT_Window_Initialization_Tracklets.py start")
    min_length = param.window_min_length_tracklet_generated 
    new_thr = param.new_thr
    window_length = param.window_length
    for j in range(0,window_length-min_length):
        tail_frame = window_end_frame-j
        #backup to init the initial tracklet
        for i in range(0,len(Obs_grap[tail_frame].child)):
            prt_idx = Obs_grap[tail_frame].child[i]
            #child_idx:the init tracklet
            child_idx = mot_search_association(Obs_grap,tail_frame,prt_idx)
            ass_idx = mot_return_ass_idx(child_idx,prt_idx,i,tail_frame)
            #if the length of init tracketlet >4 then generate the tracklet
            if len(np.where(np.array(ass_idx) != -1)[0]) >= new_thr:
                time1 = time.time()
                Trk,param = mot_tracklets_components_setup(rgbimg,Trk,detections,window_end_frame-j+1,ass_idx,param,None,Obs_grap)
                time2 = time.time()
                #print("after tracklets generate",time2-time1)
                for h in range(0,len(np.where(np.array(ass_idx) != -1)[0])):
                    Obs_grap[tail_frame - h].child[ass_idx[-1 - h]] = -1
    
    print("MOT_Window_Initialization_Tracklets over")
    return Trk,param,Obs_grap
    
if __name__ == '__main__':
    pass
    
