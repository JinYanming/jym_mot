import numpy as np
from Common.calc_overlap2 import calc_overlap2
def mot_pre_association_tracking(ISO=None,start_frame=None,end_frame=None,*args,**kwargs):

    #ISO.node : [[child][child]]
    for i in range(0,end_frame):
        ISO.node.append([])
    
    init_det=ISO.meas[start_frame]
    #ISO.node[start_frame]:[[0],[0],[0]]
    for i in range(0,len(init_det)):
        ISO.node[start_frame].append(0)
    if len(init_det) != 0:
        detections=ISO.meas
        for q in range(start_frame + 1,end_frame):
            prev_det=detections[q - 1]
            cur_det=detections[q]
            for i in range(0,len(cur_det)):
                ISO.node[q].append(0)
            asso_idx=[]
            for i in range(0,len(cur_det)):
                ovs1,_,_=calc_overlap2(cur_det,prev_det,i)
                inds1 = np.nonzero(ovs1 > 0.4)[0]#return the index of  prvious detections whose IOU with current Detection
                if len(ovs1) != 0:
                    max_ovs1_location = np.where(ovs1 == np.max(ovs1))[0][0]
                    inds1 = np.array([max_ovs1_location]) if (max_ovs1_location in inds1) else inds1#choose the detections from the privious frame whose IOU is max and <0.4
                    ratio1=cur_det[i,5] / prev_det[inds1,5]#calculate the ratio in Demesion H betweend current detection and privious detections
                    inds2=(np.minimum(ratio1,1.0 / ratio1) > 0.8)#select ratio1 > 0.8
                    if len(inds1[inds2]) > 0:#if ratios > 0.8 exits then add these
                        ISO.node[q].child[i]=inds1(inds2)
                    else:
                        ISO.node[q].child[i]=0
                    asso_idx = np.concatenate((asso_idx,inds1[inds2]),axis=0)
                else:
                    ISO.node[q][i]=0
    
    return ISO
    
if __name__ == '__main__':
    pass
    

