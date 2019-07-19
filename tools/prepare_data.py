import os
import sys
import numpy as np
base_dir = "/workspace/MOT/jym_cmot"
sys.path.append(base_dir)
from config import Config
def get_sub_files(rootdir):    
    sub_files = []    
    for root, dirs, files in os.walk(rootdir,topdown = True):
        for name in files: 
            _, ending = os.path.splitext(name)
            if ending == ".jpg":
                sub_files.append(name)   
    return sub_files
def prepare_data(param):
    ##### path config
    det_file = open(param.dataset_path+"/det/det.txt")
    detlines = det_file.readlines()
    detections = []
    fr_detections = []
    fr_prev = 1
    deal = lambda x:x.strip("\n").split(",")#seperate the lines with ", " and remove the "\n"
    ###get detections
    for detection in detlines:
        detection = deal(detection)
        if detection[0] == fr_prev:
            fr_detections.append(detection)
        else:
            detections.append(fr_detections)
            fr_detections.clear()
            fr_detections.append(detection)
        fr_prev = detection[0]
    param.detections = np.array(detections)
    det_file.close()
    print("shape: {} |||detections get from txt!".format(param.detections.shape))
    img_dir = param.dataset_path+"/img1"
    img_list = get_sub_files(img_dir)
    param.img_List = img_list
    print("frames: {} ||||img_list generate over!".format(len(param.img_List)))
if __name__ == '__main__':
    param = Config()
    prepare_data(param)
