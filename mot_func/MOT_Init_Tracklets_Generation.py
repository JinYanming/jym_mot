from Obj.Tracklet import Tracklet
from mot_func.mot_appearance_model_update import mot_appearance_model_update
def checkNone(tracklet):
    for item in tracklet.state:
        if len(item) > 0:
            return False
    return True
def MOT_Init_Tracklets_Generation(init_Trks,window_tracklets,cfr,param):
    for tracklet in window_tracklets:
        #if one tracklet in the window has never been matched for 5 frames above,cut this part of this window tracklet and make it a new init tracklet
        if cfr - tracklet.ifr +1 == 5:
            ifr = tracklet.ifr
            new_init_tracklet = Tracklet()
            new_init_tracklet.Conf_prob = tracklet.Conf_prob
            new_init_tracklet.type = tracklet.type
            new_init_tracklet.reliable = tracklet.reliable
            new_init_tracklet.isnew = 1
            new_init_tracklet.sub_img = []
            new_init_tracklet.status = tracklet.status
            new_init_tracklet.label = tracklet.label
            new_init_tracklet.ifr = ifr
            new_init_tracklet.efr = -1
            new_init_tracklet.last_update = cfr
            new_init_tracklet.state = [[]]*(cfr+1)
            new_init_tracklet.A_model_list = tracklet.A_model_list[:cfr]
            new_init_tracklet.FMotion.X = tracklet.FMotion.X[:,cfr].copy()
            new_init_tracklet.FMotion.P = tracklet.FMotion.P[:,:,cfr].copy()
            new_init_tracklet.hyp.score = tracklet.hyp.score[:cfr].copy()
            new_init_tracklet.hyp.ystate = tracklet.hyp.score[:cfr].copy()
            new_init_tracklet.state = tracklet.state[:cfr].copy()
            
            #remove the information of the part which has already become a new init_tracklet
            fr = cfr
            while 1:
                if len(tracklet.hyp.ystate[fr]) > 0:
                    tracklet.ifr = fr
                    break
                fr += 1
            for i in range(cfr+1-5,cfr+1):
                tracklet.state[i] = []
                tracklet.A_model_list[i] = None
                tracklet.FMotion.X[:,i] = 0
                tracklet.FMotion.P[:,:,i] = 0
                tracklet.hyp.score[i] = 0
                tracklet.hyp.ystate[i] = []
                tracklet.state[i] = []
            mot_appearance_model_update(new_init_tracklet)
            init_Trks.append(new_init_tracklet)

            #if the window_tracklet of which apart is concated with another init tracklet,and the rest tracklet is already empty,then delete it from the window tracklet list
            if checkNone(tracklet) == True:
                window_tracklets.remove(tracklet)
                print("delete 1 window tracklet...")
            print("Init Tracklet Generated:len(Trk)+1")
