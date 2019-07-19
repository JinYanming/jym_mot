import numpy as np
from mot_func import *
from tools import *
print('Loading detections...')
data_path = './Det/'
seq_name = 'ETH_Bahnhof_Demo_Det.mat'

file_name = strcat(data_path,seq_name)
file = open(file_name)

param = config()
# 1:ILDA, 0: No-ILDA (faster)
# To use ILDA, refer to README.
param.use_ILDA = 0 
Detections = np.random.rand(600,random.randint(2,4),4)


frame_start = 1
if length(img_List) > 10:
    frame_end = length(detections)
else
    frame_end = 10    
end

All_Eval = []
cct = 0
Trk = [] Trk_sets = [] all_mot =[]

## Initiailization Tracklet
tstart1 = tic
init_frame = frame_start + param.show_scan

for i=1:init_frame
    print(detections)
    Obs_grap(i).iso_idx = np.ones((Detections.shape)[1])
    Obs_grap(i).child = [] 
    Obs_grap(i).iso_child =[]
end


[Obs_grap] = mot_pre_association(detections,Obs_grap,frame_start,init_frame)
st_fr = 1
en_fr = init_frame

for fr = 1:init_frame
    filename = strcat(img_path,img_List(fr).name)
    rgbimg = imread(filename)
    init_img_set{fr} = rgbimg
end

[Trk,param,Obs_grap] = MOT_Initialization_Tracklets(init_img_set,Trk,detections,param,...
            Obs_grap,init_frame)
print(Trk)        
## Tracking 
print('Tracking objects...')
for fr = init_frame+1:frame_end
    filename = strcat(img_path,img_List(fr).name)
    rgbimg = imread(filename)
    init_img_set{fr} = rgbimg

    ## Local Association
    [Trk, Obs_grap, Obs_info] = MOT_Local_Association(Trk, detections, Obs_grap, param, ILDA, fr, rgbimg)
    ## Global Association
    [Trk, Obs_grap] = MOT_Global_Association(Trk, Obs_grap, Obs_info, param, ILDA, fr)
    ## Tracklet Confidence Update
    [Trk] = MOT_Confidence_Update(Trk,param,fr, param.lambda)
    [Trk] = MOT_Type_Update(rgbimg,Trk,param.type_thr,fr)
    ## Tracklet State Update & Tracklet Model Update
    [Trk] = MOT_State_Update(Trk, param, fr)
    ## New Tracklet Generation 
    [Trk, param, Obs_grap] = MOT_Generation_Tracklets(init_img_set,Trk,detections,param,...
    Obs_grap,fr)

    ## Incremental subspace learning
    if param.use_ILDA
        [ILDA] = MOT_Online_Appearance_Learning(rgbimg, img_path, img_List, fr, Trk, param, ILDA)
    end
    
    ## Tracking Results
    [Trk_sets] = MOT_Tracking_Results(Trk,Trk_sets,fr)
    print([sprintf('Tracking:Frame_#04d',fr)])
end
## 
print('Tracking done...')
TotalTime = toc(tstart1)
AverageTime = TotalTime/(frame_start + frame_end)

## Draw Tracking Results
out_path = './Results/ETH_Bahnhof/'

DrawOption.isdraw = 1
DrawOption.iswrite = 1
DrawOption.new_thr = param.new_thr

# Box colors indicate the confidences of tracked objects
# High (Red)-> Low (Blue)
[all_mot] = MOT_Draw_Tracking(Trk_sets, out_path, img_path, img_List, DrawOption) 
close all
print([sprintf('Average running time:#.3f(sec/frame)', AverageTime)])

## Save tracking results
out_path = '.\Results\'
out_filename = strcat(out_path, 'cmot_tracking_results.mat')
save(out_filename, 'all_mot')


