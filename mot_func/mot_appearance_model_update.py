import numpy as np
def mot_appearance_model_update(tracklet,param):
    length = len(tracklet.state)
    head_fr = tracklet.ifr
    head_A_Model = np.zeros(144)
    tail_A_Model = np.zeros(144)
    temp_fr = head_fr
    head_count = 0
    tail_count = 0
    checkNone = lambda x:False if isinstance(x,np.ndarray) else None
    while(head_count < param.head_tail_A_Model_length and temp_fr <length):
        tmp_A_model = tracklet.A_model_list[temp_fr]
        if checkNone(tmp_A_model) == False:
            head_A_Model = head_A_Model + tmp_A_model.squeeze()[:,np.newaxis]
            head_count += 1
        temp_fr += 1
    head_A_Model = head_A_Model/head_count
    
    temp_fr = -1
    while(tail_count < param.head_tail_A_Model_length and temp_fr > -length):
        tmp_A_model = tracklet.A_model_list[temp_fr]
        if checkNone(tmp_A_model) == False:
            tail_A_Model = tail_A_Model + tmp_A_model.squeeze()[:,np.newaxis]
            tail_count += 1
        temp_fr -= 1
    tail_A_Model = tail_A_Model/tail_count
    tracklet.A_model_head = head_A_Model
    tracklet.A_model_tail =  tail_A_Model
