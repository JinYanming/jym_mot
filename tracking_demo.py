import time,datetime
import numpy as np
import cv2
import pickle as pk
from Obj.Obs_Graph import Obs_Graph
from tools.prepare_data import prepare_data
from config import Config
from image2video import img2mp4
from mot_func.mot_pre_association import mot_pre_association
from mot_func.mot_window_pre_association import mot_window_pre_association
from mot_func.MOT_Initialization_Tracklets import MOT_Initialization_Tracklets
from mot_func.MOT_Window_Initialization_Tracklets import MOT_Window_Initialization_Tracklets
from mot_func.MOT_Window_Association import MOT_Window_Association
from mot_func.MOT_Global_Association import MOT_Global_Association
from mot_func.MOT_Confidence_Update import MOT_Confidence_Update
from mot_func.MOT_Type_Update import MOT_Type_Update
from mot_func.MOT_State_Update import MOT_State_Update
from mot_func.MOT_Generation_Tracklets import MOT_Generation_Tracklets
from mot_func.MOT_Tracking_Results import MOT_Tracking_Results
from mot_func.mot_count_ids import mot_count_ids
from mot_func.MOT_Init_Tracklets_Generation import MOT_Init_Tracklets_Generation
from mot_func.mot_appearance_model_generation import mot_appearance_model_generation

from tools.MOT_Draw_Tracking import MOT_Tracking_Reauslt_Realtime
from tools.fileGiant import clear_subfile
from tools.ListGiant import ListInsert

from Obj.Obs_Graph import Kalman_Filter

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
#this variable is used to record every state of tracklets in every frame and finally use Trk_sets to draw and show the tracklets
Trk_sets = []
all_mot = []
#to record relations between detections in current and privious frames
#Obs_grap = []
init_img_set = np.zeros((param.imgSeq_lenth,param.imgsize[0],param.imgsize[1],param.imgsize[2]))
a_model_list = []
#window information
Obs_grap_window = []
Tracklets_window = []
## Initiailization Tracklet
start_time  =  time.time()
init_frame = frame_start + param.show_scan + 1
#window tracklet generated
window_start_frame = param.tracking_start_frame
window_end_frame = window_start_frame+param.window_length-1
for fr in range(0,window_end_frame+1):
    filename  =  param.img_path + img_List[fr]
    bgrimg = cv2.imread(filename)
    b,g,r = cv2.split(bgrimg)
    rgbimg = cv2.merge([r,g,b])
    init_img_set[fr] = rgbimg
    frame_a_models = []
    if fr > window_start_frame-1:
        for i in range(0,len(detections[fr])):
            det = detections[fr][i]
            det_a_model = mot_appearance_model_generation(rgbimg,param,det[2:-1])
            frame_a_models.append(det_a_model)
    #a_model_list.append(frame_a_models)
    ListInsert(a_model_list,fr,frame_a_models,[])
print(window_start_frame,window_end_frame)
for i in range(0,window_end_frame+1):
    num_det = len(detections[i])
    obs_grap = Obs_Graph(num_det)
    Obs_grap_window.append(obs_grap)
    Obs_grap_window[i].iso_idx  =  np.array(np.arange(0,len(detections[i])))
    Obs_grap_window[i].kalman_filter  =  [Kalman_Filter()]*len(detections[i])
    Obs_grap_window[i].child  =  [-1]*num_det
    Obs_grap_window[i].iso_child  =  []
num_det = len(detections[0])
Obs_grap_window[0].child = [-1]*num_det

print("Tracklets_window number is:",len(Tracklets_window))
#clear ./result subfiles
clear_subfile("./result/")
#define current frame and window_frame
## Tracking
for fr in range(window_end_frame,frame_end):
    print('Tracking:Frame_{}'.format(fr))
    if fr == 329:
        print(11111)
    filename = param.img_path+param.img_List[fr]
    bgrimg = cv2.imread(filename)
    b,g,r = cv2.split(bgrimg)
    rgbimg = cv2.merge([r,g,b])
    init_img_set[fr] = rgbimg
    frame_a_models = []
    for i in range(0,len(detections[fr])):
        det = detections[fr][i]
        det_a_model = mot_appearance_model_generation(rgbimg,param,det[2:-1])
        frame_a_models.append(det_a_model)
    ListInsert(a_model_list,fr,frame_a_models,[])
    #a_model_list.append(frame_a_models)
    
    if fr+1 > len(Obs_grap_window):
        num_det = len(detections[fr])
        obs_grap = Obs_Graph(num_det)
        obs_grap.child  =  [-1]*num_det 
        Obs_grap_window.append(obs_grap)
        Obs_grap_window[fr].iso_idx  =  np.array(np.arange(0,num_det))
        #Obs_grap_window[fr].child  =  [-1]*len(num_det)
    """***************Window Move*******************"""
    #generate new tracklet in the window
    Tracklets_window,param,Obs_grap_window = MOT_Generation_Tracklets(a_model_list,init_img_set,Tracklets_window,detections,param,Obs_grap_window,fr)
    Tracklets_window = MOT_State_Update(Tracklets_window,param,fr)
    Tracklets_window = MOT_Type_Update(rgbimg,Tracklets_window,param,fr)
    #Tracklets_window = MOT_Confidence_Update(Tracklets_window,param,fr)
    """^^^^^^^^^^^^^^^Window Tracklets Association^^^^^^^^^^^^^^^^^^^"""
    #after tracklet generated in the window,we start to do association between tracklet before and tracklet in window
    Tracklets_window,Obs_grap_window = MOT_Window_Association(Tracklets_window,param,fr,detections,Obs_grap_window)
    """**********************************"""
    if param.use_ILDA:
        ILDA = MOT_Online_Appearance_Learning(rgbimg,img_path,img_List,fr,Trk,param,ILDA)
    ## Tracking Results
    Trk_sets = MOT_Tracking_Results(Tracklets_window,Trk_sets,fr-param.window_length+1,param)
    if param.draw_while_track:
        MOT_Tracking_Reauslt_Realtime(Trk_sets,fr-param.window_length+1,param)

##count the ids of the rest Tracklet
for tracklet in Tracklets_window:
    mot_count_ids(tracklet,param)
print("Tracking Done...")
end_time = time.time()
spend_time = end_time-start_time
print("Tracking: Total Time:{}|FPS :{}".format(spend_time,len(param.img_List)/spend_time))
print("Total Tracklet:{}   |Total Object:{}".format(param.total_tracklet_count,param.object_count))
print("TT-TO:  {}".format(param.total_tracklet_count-param.object_count))
print("IDS:{}".format(param.ids))

print("mp4 result is generating.....")
img2mp4(param)
print("mp4 result is completed!")
if param.draw_while_track == False:
    pass
