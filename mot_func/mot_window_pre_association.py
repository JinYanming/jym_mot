import numpy as np
from Common.calc_overlap2 import calc_overlap2
from Common.cal_a_model_affinity import cal_a_model_affinity
from tools.ListGiant import ListIndice2d
def mot_window_pre_association(a_model_list = None,img_sets = None,detections=None,Obs_grap=None,start_frame=None,end_frame=None,*args,**kwargs):

    cur_det = detections[start_frame]
    for i in range(0,len(cur_det)):
        Obs_grap[start_frame].child.append(-1)
    for q in range(start_frame+1,end_frame+1):
        prev_det = np.array(detections[q - 1])
        cur_det = np.array(detections[q])

        cur_a_models = a_model_list[q]
        prev_a_models = a_model_list[q-1]

        asso_idx = np.array([])
        for i in range(0,len(cur_det)):
            a_model_affinity = cal_a_model_affinity(cur_a_models,prev_a_models,i )
            ovs1,_,_ = calc_overlap2(ListIndice2d(cur_det,None,[2,6]),ListIndice2d(prev_det,None,[2,6]),i)
            #return the index of  prvious detections whose IOU with current Detection
            total_affinity = a_model_affinity*0.2*(ovs1>0.4)+ovs1*0.8*(a_model_affinity>0.5)
            inds1 = np.nonzero(total_affinity > 0.4)[0]
            max_ovs1_location = np.where(ovs1 == np.max(ovs1))[0][0]
            #choose the detections from the privious frame whose IOU is max and <0.4
            inds1 = np.array([max_ovs1_location]) if (max_ovs1_location in inds1) else inds1

            #calculate the ratio in Demesion H betweend current detection and privious detections
            ratio1 = cur_det[i,5] / prev_det[inds1,5]
            #select ratio1 > 0.8
            inds2 = (np.minimum(ratio1,1.0 / ratio1) > 0.8)
            #if ratios > 0.8 exits then add these
            if len(inds1[inds2]) > 0:
                
                Obs_grap[q].child.append(inds1[inds2][0])
                Obs_grap[q].child_A_Model_affinity.append(a_model_affinity[max_ovs1_location])
            else:
                Obs_grap[q].child.append(-1)
                Obs_grap[q].child_A_Model_affinity.append(0)
            asso_idx = np.concatenate((asso_idx,inds1[inds2]),axis=0)
        #asso_idx = asso_idx.astype("int")
        #Obs_grap[q - 1].iso_idx[asso_idx] = -1
    
    return Obs_grap
    
if __name__ == '__main__':
    pass
    
