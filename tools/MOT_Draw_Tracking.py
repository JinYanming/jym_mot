import os
import sys
import cv2
import numpy as np
base_dir = "/workspace/MOT/jym_cmot"
sys.path.append(base_dir)
from config import Config
def draw_frame(img_url,save_url,img_name,fr_detecions):
    img = cv2.imread(img_url + "/" + img_name)#read image
    for detection in fr_detecions:#iterate detections in this frame
        ####draw the bbx on image
        cv2.rectangle(
                img,
                (detection[2], detection[3]),
                (detection[2]+detection[4], detection[3]+detection[5]),
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

def MOT_Tracking_Results(Trk,Trk_sets,fr,param):
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
    img_name = "000001.jpg"
    fr_detections = np.array([
            [1,12,1359.1,413.27,120.26,362.77,2.3092],
            [1,33,571.03,402.13,104.56,315.68,1.5028],
            [1,1,650.8,455.86,63.98,193.94,0.33276],
            [1,34,721.23,446.86,41.871,127.61,0.27401],
            [1,2,454.06,434.36,97.492,294.47,0.20818],
            [1,4,1254.6,446.72,33.822,103.47,0.14776],
            [1,5,1301.1,237.38,195.98,589.95,0.051818],
            [1,1,1480.3,413.27,120.26,362.77,-0.020474],
            [1,12,552.72,473.9,29.314,89.943,-0.087553],
            [1,23,1097,433,39,119,-0.17964],
            [1,42,543.19,442.1,44.948,136.84,-0.3683],
            [1,4,1017,425,39,119,-0.41789]
            ],np.float32)
    draw_frame("/workspace/MOT/jym_cmot/tools","./",img_name,fr_detections)
