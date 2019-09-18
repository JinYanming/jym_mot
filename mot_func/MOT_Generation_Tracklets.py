import numpy as np
from mot_func.mot_generation_tracklet import mot_generation_tracklet
from mot_func.mot_non_associated import mot_non_associated
from mot_func.mot_pre_association_tracking import mot_pre_association_tracking 
from Obj.ISO import ISO

def MOT_Generation_Tracklets(a_model_list = None,init_img_set=None,Trk=None,detections=None,param=None,Obs_grap=None,cfr=None,*args,**kwargs):

    
    start_fr=cfr - param.window_length +1
    end_fr=cfr
    #use iso to record the unmatched detections in every frames
    #look for the relationship betweend these detections by IOU
    Obs_grap=mot_pre_association_tracking(init_img_set,a_model_list,detections,Obs_grap,start_fr,end_fr,param)
    Trk,param,Obs_grap=mot_generation_tracklet(init_img_set,Trk,Obs_grap,detections,param,cfr)
    print("length of Trk is :",len(Trk))
    
    return Trk ,param, Obs_grap
