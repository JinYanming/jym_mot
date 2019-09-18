from Common.cal_a_model_affinity import cal_a_model_affinity
from Common.Labelling import Labelling

from Obj.Tracklet import Tracklet
from mot_func.mot_motion_model_generation import mot_motion_model_generation
from mot_func.mot_motion_similarity import mot_motion_similarity
def mot_get_label(tracklets,new_tracklet,param):
    #look for the tracklet before new tracklet
    affinity = []
    for trk in tracklets:
            temp_Trk = Tracklet()
            temp_Trk.FMotion  =  trk.FMotion
            XX,PP = mot_motion_model_generation(trk,param,'Backward')
            temp_Trk.BMotion.X  =  XX
            temp_Trk.BMotion.P  =  PP
            temp_Trk.init_time  =  trk.ifr
            temp_Trk.end_time = trk.last_update
            
            
            new_Trk = Tracklet()
            new_Trk.FMotion  =  new_tracklet.FMotion
            XX,PP = mot_motion_model_generation(new_tracklet,param,'Backward')
            new_Trk.BMotion.X  =  XX
            new_Trk.BMotion.P  =  PP
            new_Trk.init_time  = new_tracklet.ifr
            new_Trk.end_time = new_tracklet.last_update


            if trk.last_update < new_tracklet.ifr:
                motion_similarity = mot_motion_similarity(temp_Trk,new_Trk,param,"Trk")
                a_model_affinity = cal_a_model_affinity([trk.A_model_tail],[new_tracklet.A_model_head],0)[0]
                final_affinity = motion_similarity*a_model_affinity
                affinity.append([final_affinity,trk.label])
            if trk.ifr < new_tracklet.last_update:
                motion_similarity = mot_motion_similarity(new_Trk,temp_Trk,param,"Trk")
                a_model_affinity = cal_a_model_affinity([trk.A_model_head],[new_tracklet.A_model_tail],0)[0]
                final_affinity = motion_similarity*a_model_affinity
                affinity.append([final_affinity,trk.label])
    if len(affinity) > 0:
        print(affinity,1213123123123123)
        affinity = sorted(affinity,key=(lambda x:x[0]),reverse=True)
        max_affinity = affinity[0]
        if max_affinity[0] > param.similar_thresh:
            new_tracklet.label =  max_affinity[1]
        else:
            new_tracklet.label =  Labelling(param)
    else:
        new_tracklet.label =  Labelling(param)
