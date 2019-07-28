import numpy as np
from Common.calc_overlap2 import calc_overlap2
def mot_pre_association(detections=None,Y=None,start_frame=None,end_frame=None,*args,**kwargs):

    cur_det=detections[1]
    for i in range(0,len(cur_det)):
        Y[start_frame].child.append([-1]) 
    for q in range(start_frame+1,end_frame):
        prev_det=np.array(detections[q - 1])
        cur_det=np.array(detections[q])
        asso_idx=np.array([])
        for i in range(0,len(cur_det)):
            ovs1,_,_ = calc_overlap2(cur_det,prev_det,i)
            inds1 = np.nonzero(ovs1 > 0.4)[0]#return the index of  prvious detections whose IOU with current Detection
            max_ovs1_location = np.where(ovs1 == np.max(ovs1))[0][0]
            inds1 = np.array([max_ovs1_location]) if (max_ovs1_location in inds1) else inds1#choose the detections from the privious frame whose IOU is max and <0.4

            ratio1=cur_det[i,5] / prev_det[inds1,5]#calculate the ratio in Demesion H betweend current detection and privious detections
            inds2=(np.minimum(ratio1,1.0 / ratio1) > 0.8)#select ratio1 > 0.8
            if ~np.all(inds1[inds2]==0):#if ratios > 0.8 exits then add these
                Y[q].child.append(inds1[inds2].tolist())
            else:
                Y[q].child.append([-1])
            asso_idx = np.concatenate((asso_idx,inds1[inds2]),axis=0)
        asso_idx = asso_idx.astype("int")
        Y[q - 1].iso_idx[asso_idx]=0
    
    return Y
    
if __name__ == '__main__':
    pass
    
