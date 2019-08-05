import time
import numpy as np
import cv2


from Obj.Obs_Graph import Obs_Graph
from tools.prepare_data import prepare_data
from config import Config
from mot_func.mot_pre_association import mot_pre_association
from mot_func.MOT_Initialization_Tracklets import MOT_Initialization_Tracklets
from mot_func.MOT_Local_Association import MOT_Local_Association
from mot_func.MOT_Global_Association import MOT_Global_Association
from mot_func.MOT_Confidence_Update import MOT_Confidence_Update
from mot_func.MOT_Type_Update import MOT_Type_Update
from mot_func.MOT_State_Update import MOT_State_Update
from mot_func.MOT_Generation_Tracklets import MOT_Generation_Tracklets
from mot_func.MOT_Tracking_Results import MOT_Tracking_Results
print("config param generated...")
param  =  Config()
print('Loading detections...')
prepare_data(param)
detections  =  param.detections
img_List  =  param.img_List
# 1:ILDA, 0: No-ILDA (faster)
# To use ILDA, refer to README.
param.use_ILDA  =  0
frame_start = 0
if len(param.img_List) > 10:
    frame_end = len(detections)
else:
    frame_end = 10

All_Eval = []
cct = 0
Trk = []
Trk_sets = []
all_mot = []
Obs_grap = []
init_img_set = np.zeros((param.imgSeq_lenth,param.imgsize[0],param.imgsize[1],param.imgsize[2]))
## Initiailization Tracklet
tstart1  =  time.time()
init_frame = frame_start + param.show_scan + 1
#####################
"""
    Obs_grap:
        type:
            list
            the length equals the number of the frames
            every node record the current frame informations
        content:
                iso_idx:a list of which length equals bbx number in this frame
                child:
                iso_child
"""
for i in range(0,init_frame):
    obs_grap = Obs_Graph()
    Obs_grap.append(obs_grap)
    Obs_grap[i].iso_idx  =  np.ones(len(detections[i]))
    Obs_grap[i].child  =  []
    Obs_grap[i].iso_child  =  []

Obs_grap = mot_pre_association(detections,Obs_grap,frame_start,init_frame)
st_fr = 1
en_fr = init_frame
for fr in range(0,init_frame):
    filename  =  param.img_path + img_List[fr]
    print(filename)
    bgrimg = cv2.imread(filename)
    b,g,r = cv2.split(bgrimg)
    rgbimg = cv2.merge([r,g,b])
    init_img_set[fr] = rgbimg

Trk,param,Obs_grap = MOT_Initialization_Tracklets(init_img_set,Trk,detections,param,Obs_grap,init_frame)
for item in Trk:
    print(item.A_Model[0])
## Tracking
#for item in Trk:
#    print(item)
#    for state in item.state:
#        print(state)
for fr in range(init_frame,frame_end):
    if fr == 11:
        print(111111222)
    filename = param.img_path+param.img_List[fr]
    bgrimg = cv2.imread(filename)
    b,g,r = cv2.split(bgrimg)
    rgbimg = cv2.merge([r,g,b])
    init_img_set[fr] = rgbimg
    Trk,Obs_grap,Obs_info = MOT_Local_Association(Trk,detections,Obs_grap,param,fr,rgbimg,3)
    Trk,Obs_grap = MOT_Global_Association(Trk,Obs_grap,Obs_info,param,fr)
    Trk = MOT_Confidence_Update(Trk,param,fr,param.lambda_)
    Trk = MOT_Type_Update(rgbimg,Trk,param.type_thr,fr)
    Trk = MOT_State_Update(Trk,param,fr)
    Trk,param,Obs_grap = MOT_Generation_Tracklets(init_img_set,Trk,detections,param,Obs_grap,fr)
    if param.use_ILDA:
        ILDA = MOT_Online_Appearance_Learning(rgbimg,img_path,img_List,fr,Trk,param,ILDA)
    ## Tracking Results
    Trk_sets = MOT_Tracking_Results(Trk,Trk_sets,fr)
    print('Tracking:Frame_{}'.format(fr))

##
disp('Tracking done...')
TotalTime = toc(tstart1)
AverageTime = TotalTime / (frame_start + frame_end)
## Draw Tracking Results
out_path = './Results/ETH_Bahnhof/'
DrawOption.isdraw  =  copy(1)
DrawOption.iswrite  =  copy(1)
DrawOption.new_thr  =  copy(param.new_thr)
# Box colors indicate the confidences of tracked objects
# High (Red)-> Low (Blue)
all_mot = MOT_Draw_Tracking(Trk_sets,out_path,img_path,img_List,DrawOption)
close_('all')
disp(concat([sprintf('Average running time:%.3f(sec/frame)',AverageTime)]))
## Save tracking results
out_path = './Results/'
out_filename = strcat(out_path,'cmot_tracking_results.mat')
save(out_filename,'all_mot')
