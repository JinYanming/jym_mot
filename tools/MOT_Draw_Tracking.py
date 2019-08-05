import os
import sys
import cv2
import numpy as np
base_dir = "/workspace/MOT/jym_cmot"
sys.path.append(base_dir)
from config import Config
from prepare_data import prepare_data
from Common.list2array import lists2array
def draw_frame_for_state(img_url,save_url,img_name,Trk_set,xy_center = False):
    detections = lists2array(Trk_set.state,4)
    confidence = Trk_set.conf
    label = Trk_set.label
    if xy_center:
        detections[:,0] = detections[:,0] - detections[:,2]/2
        detections[:,1] = detections[:,1] - detections[:,3]/2
    img = cv2.imread(img_url + "/" + img_name)#read image
    for i in range(0,len(detections[i]s)):#iterate detections[i]s in this frame
        ####draw the bbx on image
        x1 = int(detections[i][0])
        y1 = int(detections[i][1])
        x2 = int(detections[i][0] + detections[i][2])
        y2 = int(detections[i][1] + detections[i][3])
        cv2.rectangle(
                img,
                (x1 , y1),
                (x2 , y2),
                (128+96*(-confidence[i]), 0, 128+96*(confidence[i])),
                4
                )
        cv2.putText(
            img,
            str(label[i]),
            (int(detections[i][0]+detections[i][2]/2-30), int(detections[i][1]+detections[i][3]/2+25)),
            cv2.FONT_HERSHEY_COMPLEX,
            1.2,
            (0, 255, 0),
            thickness=4)
    cv2.imwrite(save_url+'/'+"tracked"+img_name, img)
def draw_frame(img_url,save_url,img_name,fr_detections,xy_center = False):
    fr_detections = lists2array(fr_detections,7)
    fr_detections = np.swapaxes(fr_detections,0,1)
    if xy_center:
        fr_detections[:,2] = fr_detections[:,2] - fr_detections[:,4]/2
        fr_detections[:,3] = fr_detections[:,3] - fr_detections[:,5]/2
    img = cv2.imread(img_url + "/" + img_name)#read image
    for detection in fr_detections:#iterate detections in this frame
        ####draw the bbx on image
        x1 = int(detection[2])
        y1 = int(detection[3])
        x2 = int(detection[2] + detection[4])
        y2 = int(detection[3] + detection[5])
        cv2.rectangle(
                img,
                (x1 , y1),
                (x2 , y2),
                (128+96*(-detection[6]), 0, 128+96*(detection[6])),
                4
                )
        cv2.putText(
            img,
            str(detection[1]),
            (int(detection[2]+detection[4]/2-30), int(detection[3]+detection[5]/2+25)),
            cv2.FONT_HERSHEY_COMPLEX,
            1.2,
            (0, 255, 0),
            thickness=4)
    cv2.imwrite(save_url+'/'+"tracked"+img_name, img)
def MOT_Tracking_Reauslt_Realtime(Trk_sets,fr,param):
    img_path = param.img_path
    save_path = "./result"
    current_Trks_states = Trk_sets[fr]
    imgName = param.img_List[fr]
    draw_frame(img_path,save_path,imgName,Trk_set[fr],True)

def MOT_Tracking_Results(Trk_sets,fr,param):
    print("MOT_Tracking_Results start")
    root_path = param.dataset_path
    img_list = param.img_List
    detections = param.detections
    for fr in range(param.imgSeq_lenth):
        removeZeros  = lambda array3d:array3d[~np.all(array3d==0,axis=2)]
        for det in removeZeros(detections[fr,:,:]):
            print(det)
    Trk_sets = 0
    print("MOT_Tracking_Results over")
    return Trk_sets
if __name__ == "__main__":
    img_name = "image_00000000_0.png"
    param = Config()
    prepare_data(param)
    detections = param.detections
    print(detections[0])
    imgName_list = param.img_List
    for item in zip(detections,imgName_list):
        fr_detections = item[0]
        imgName = item[1]
        draw_frame(param.img_path,"./mark",imgName,fr_detections,True)
