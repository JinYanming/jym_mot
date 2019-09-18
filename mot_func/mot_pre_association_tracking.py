import numpy as np
from mot_func.mot_appearance_model_generation import mot_appearance_model_generation
from kf_func.km_for_search import mot_motion_model_generation_for_search,km_state_predict,km_state_update_for_search
from Common.calc_overlap2 import calc_overlap2
from Common.cal_a_model_affinity import cal_a_model_affinity
from Obj.Obs_Graph import Obs_Graph
from tools.ListGiant import ListInsert,ListIndice1d
class Information(object):
    def __init__(self,obs_grap = None,detections = None,unmatched_detections = None,unmatched_detections_id = None,a_models = None):
        self.obs_grap = obs_grap
        self.detections = detections
        self.unmatched_detections = unmatched_detections
        self.unmatched_detections_id = unmatched_detections_id
        self.a_models = a_models
        self.a_models_unmatched = ListIndice1d(a_models,unmatched_detections_id)
def clear_break_family(Obs_grap = None,start_frame = None,end_frame = None,param = None):
    fr = end_frame
    for i in range(0,end_frame - start_frame):
        fr  = fr - 1
        for i in range(0,len(Obs_grap[fr].kalman_filters)):
            kalman_filter = Obs_grap[fr].kalman_filters[i]
            #if the end node of a kalman sequence is before the window end frame and it has no son ndoe,i remove its whole kalman family
            if kalman_filter.kalman_filter_role >= 2 and  kalman_filter.kalman_filter_role < param.window_min_length_tracklet_generated and kalman_filter.kalman_end == True and kalman_filter.has_son == False:
                count = 1
                now_node = kalman_filter
                now_real_id = i
                while now_node.father_real_id != None:
                    father_real_id = now_node.father_real_id
                    father = Obs_grap[fr - count].kalman_filters[father_real_id]
                    
                    Obs_grap[fr - count + 1].iso_idx[now_real_id] = now_real_id
                    Obs_grap[fr - count + 1].child[now_real_id] = -1
                    Obs_grap[fr - count + 1].child_A_Model_affinity[now_real_id] = 0
                    now_node.__init__()

                    now_node = father
                    now_real_id  = father_real_id
                    count += 1
                father_real_id = now_node.father_real_id
                Obs_grap[fr - count+1].iso_idx[now_real_id] = now_real_id
                Obs_grap[fr - count+1].child[now_real_id] = -1
                Obs_grap[fr - count+1].child_A_Model_affinity[now_real_id] = 0
                now_node.__init__()
                    
                    


def update_Obs_grap(Obs_grap = None,detections = None,cur_fr = None,father = None,current = None,father_real_id = None,real_id = None,param = None,a_model_affinity = None):
    #the father node find the son node so lable the attribute from False to True
    Obs_grap[cur_fr-1].kalman_filters[father_real_id].has_son = True
    Obs_grap[cur_fr-1].kalman_filters[father_real_id].son_real_id = real_id
    Obs_grap[cur_fr].kalman_filters[real_id].father_real_id = father_real_id

    #if the last kalman end node's role is 2
    if father.obs_grap.kalman_filters[father_real_id].kalman_filter_role >= 2:
        father_FMotion = Obs_grap[cur_fr-1].kalman_filters[father_real_id].FMotion
        father_FMotion_wh = Obs_grap[cur_fr-1].kalman_filters[father_real_id].FMotion_wh
                        
        
        ListInsert(Obs_grap[cur_fr].child,real_id,father_real_id,-1)
        Obs_grap[cur_fr-1].kalman_filters[father_real_id].kalman_end = False
        Obs_grap[cur_fr].kalman_filters[real_id].kalman_end = True
        Obs_grap[cur_fr].kalman_filters[real_id].kalman_filter_role = Obs_grap[cur_fr-1].kalman_filters[father_real_id].kalman_filter_role + 1
        Obs_grap[cur_fr].kalman_filters[real_id].FMotion,Obs_grap[cur_fr].kalman_filters[real_id].FMotion_wh =  km_state_update_for_search(father_FMotion,father_FMotion_wh,detections[cur_fr][real_id][2:-1] ,param)
        current_FMotion = Obs_grap[cur_fr].kalman_filters[real_id].FMotion
        current_FMotion_wh = Obs_grap[cur_fr].kalman_filters[real_id].FMotion_wh
        Obs_grap[cur_fr].kalman_filters[real_id].kalman_filter_predict_state = km_state_predict(current_FMotion,current_FMotion_wh,detections[cur_fr][real_id][2:-1],param)
        #print("body Fmotion is :",current_FMotion.X)
        if a_model_affinity != None:
            ListInsert(Obs_grap[cur_fr].child_A_Model_affinity,real_id,a_model_affinity,0)

    if father.obs_grap.kalman_filters[father_real_id].kalman_filter_role == -1:
        current_FMotion,current_FMotion_wh = mot_motion_model_generation_for_search(detections[cur_fr][real_id][2:-1],detections[cur_fr-1][father_real_id][2:-1],param)
        #print("head Fmotion is :",current_FMotion.X)
        ListInsert(Obs_grap[cur_fr].child,real_id,father_real_id,-1)
        Obs_grap[cur_fr-1].kalman_filters[father_real_id].kalman_end = False
        Obs_grap[cur_fr].kalman_filters[real_id].kalman_end = True
        Obs_grap[cur_fr-1].kalman_filters[father_real_id].kalman_filter_role = 1
        Obs_grap[cur_fr].kalman_filters[real_id].kalman_filter_role = 2
        Obs_grap[cur_fr].kalman_filters[real_id].FMotion = current_FMotion 
        Obs_grap[cur_fr].kalman_filters[real_id].FMotion_wh = current_FMotion_wh
        Obs_grap[cur_fr].kalman_filters[real_id].kalman_filter_predict_state = km_state_predict(current_FMotion,current_FMotion_wh,detections[cur_fr][real_id][2:-1],param)
        #ListInsert(Obs_grap[cur_fr].child_A_Model_affinity,real_id,a_model_affinity,0)



def mot_pre_association_tracking(img_list,a_model_list = None,detections = None,Obs_grap=None,start_frame=None,end_frame=None,param = None,*args,**kwargs):
    #for ii in range(start_frame,end_frame+1):
        #tttt = []
        #pp = []
        #for jj in Obs_grap[ii].kalman_filters:
        #    pp.append(jj.kalman_end)
        #    tttt.append(jj.kalman_filter_role)
        #print("role:",tttt,"kalman_end:",pp,"child:",Obs_grap[ii].child,"iso_idx",Obs_grap[ii].iso_idx,ii)
    unmatched_detections = []
    unmatched_detections_id = []
    for i in range(start_frame,end_frame+1):
        temp_detections = []
        temp_detections_id = []
        for j in range(0,len(Obs_grap[i].iso_idx)):
            idx = Obs_grap[i].iso_idx[j]
            role = Obs_grap[i].kalman_filters[j].kalman_filter_role
            whether_end = Obs_grap[i].kalman_filters[j].kalman_end
            if idx != -1 and (role == -1 or whether_end == True):
                temp_detections.append(detections[i][idx])
                temp_detections_id.append(idx)
        unmatched_detections_id.append(temp_detections_id)
        unmatched_detections.append(temp_detections)


    for qq in range(start_frame+1,end_frame+1):
        q = qq - start_frame
        #this line is used to avoid the empty situation
        getPiece = lambda detections,index: np.array(detections[index])[:,2:-1] if len(detections[index]) > 0 else np.array(detections[index])
        
        father = Information(Obs_grap[qq-1],detections[qq-1],getPiece(unmatched_detections,q-1),unmatched_detections_id[q-1],a_model_list[qq-1])
        current = Information(Obs_grap[qq],detections[qq],getPiece(unmatched_detections,q),unmatched_detections_id[q],a_model_list[qq])
        #to look for the head1 or body of the kalman filters
        father_kalmans = [item.kalman_filter_role for item in Obs_grap[q-1].kalman_filters]
        asso_idx = []
        father_kalman_end_predicted_states = np.zeros((0,4))
        father_kalman_end_real_ids = []
        father_kalman_end_predicted_state_a_models = []
        #in order to find the head1 and head2 at 2nd frame and this part functions should not work
        if qq > start_frame:
            #at first I will found the node that is alreadt connect by kalman filter who is the last node of that state sequence
            for i in range(0,len(father.obs_grap.kalman_filters)):
                if father.obs_grap.kalman_filters[i].kalman_end == True:

                    X = father.obs_grap.kalman_filters[i].FMotion.X
                    P = father.obs_grap.kalman_filters[i].FMotion.P
                
                    predicted_state = father.obs_grap.kalman_filters[i].kalman_filter_predict_state
                    father_a_model = mot_appearance_model_generation(img_list[qq],param,predicted_state)
                    father_kalman_end_predicted_states = np.r_[father_kalman_end_predicted_states,predicted_state[np.newaxis,:]]
                    father_kalman_end_real_ids.append(i)
                    father_kalman_end_predicted_state_a_models.append(father_a_model)
                    father_kalman_end_role = father.obs_grap.kalman_filters[i].kalman_filter_role
            for j in range(0,len(current.unmatched_detections)):
                #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #at first to find the detections in current detection that has relationship with existing detections
                a_model_affinity = cal_a_model_affinity(current.a_models_unmatched,father_kalman_end_predicted_state_a_models,j)
                ovs1,_,_=calc_overlap2(current.unmatched_detections,father_kalman_end_predicted_states,j)
                total_affinity = a_model_affinity*0.2*(ovs1>0.4)+ovs1*0.8*(a_model_affinity>0.5)
                
                inds1 = np.nonzero(total_affinity > 0.4)[0]
                
                real_id = current.unmatched_detections_id[j]
                
                fr = qq
                if qq >324:
                    print(total_affinity,a_model_affinity,qq,len(Obs_grap),ovs1)
                if len(inds1) != 0:
                    max_ovs1_location = np.where(total_affinity == np.max(total_affinity))[0][0]
                    #choose the detections from the privious frame whose IOU is max and <0.4
                    inds1 = np.array([max_ovs1_location])
                    #calculate the ratio in Demesion H betweend current detection and privious detections if (max_ovs1_location in inds1) else inds1
                    ratio1 = current.unmatched_detections[j,3] / father_kalman_end_predicted_states[inds1,3]
                    #select ratio1 > 0.8
                    inds2=(np.minimum(ratio1,1.0 / ratio1) > 0.8)
                    #if ratios > 0.8 exits then add these
                    if len(inds1[inds2]) > 0 and Obs_grap[fr].iso_idx[real_id] != -1:
                        father_real_id = father_kalman_end_real_ids[inds1[inds2][0]]
                        #modify the father element information
                        #modify the current element information
                        if current.obs_grap.kalman_filters[real_id].kalman_filter_role == -1:
                            update_Obs_grap(Obs_grap,detections,fr,father,current,father_real_id,real_id,param,a_model_affinity[max_ovs1_location])
            #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        #from now on to find a new pair of head1 and head2
        for j in range(0,len(current.unmatched_detections)):
            a_model_affinity = cal_a_model_affinity(current.a_models_unmatched,father.a_models_unmatched,j)
            ovs1,_,_=calc_overlap2(current.unmatched_detections,father.unmatched_detections,j)
            total_affinity = a_model_affinity*0.2*(ovs1>0.4)+ovs1*0.8*(a_model_affinity>0.5)
            
            inds1 = np.nonzero(total_affinity > 0.4)[0]
            
            real_id = current.unmatched_detections_id[j]
            
            fr = qq
            if len(inds1) != 0:
                max_ovs1_location = np.where(total_affinity == np.max(total_affinity))[0][0]
                #choose the detections from the privious frame whose IOU is max and <0.4
                inds1 = np.array([max_ovs1_location])
                #calculate the ratio in Demesion H betweend current detection and privious detectionsf (max_ovs1_location in inds1) else inds1
                ratio1 = current.unmatched_detections[j,3] / father.unmatched_detections[inds1,3]
                #select ratio1 > 0.8
                inds2=(np.minimum(ratio1,1.0 / ratio1) > 0.8)
                #if ratios > 0.8 exits then add these
                if len(inds1[inds2]) > 0 and Obs_grap[fr].iso_idx[real_id] != -1:
                    father_real_id = father.unmatched_detections_id[inds1[inds2][0]]
                    #modify the father element information
                    #modify the current element information
                    if father.obs_grap.kalman_filters[father_real_id].kalman_filter_role == -1 and current.obs_grap.kalman_filters[real_id].kalman_filter_role == -1:
                        update_Obs_grap(Obs_grap,detections,fr,father,current,father_real_id,real_id,param)
                asso_idx = np.concatenate((asso_idx,inds1[inds2]),axis=0)
    #clear_break_family(Obs_grap,start_frame,end_frame,param)
            
    return Obs_grap
    
if __name__ == '__main__':
    pass
    

