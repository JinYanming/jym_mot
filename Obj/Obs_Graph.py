class F_Motion(object):
    def __init__(self):
        self.X = None
        self.P = None
class Kalman_Filter(object):
    def __init__(self):
        #this attribute is used to record the information of this detection about kalman data:[XX PP] if this detection has never be  predicted by kalman then it will be []
        self.FMotion = F_Motion()
        self.FMotion_wh = F_Motion()
        #this attribute is used to record that th
        """
        -1      no relationship with kalman filter
        1       head part1 of kalman filter
        2       head part2 of kalman filter
        3,4,5,6       boday part of kalman filter
        """
        self.kalman_filter_role = -1
        #this attribute is used to record that whether this node is the last element of the kalman sequence
        self.kalman_end = False
        #this attribute is used to record the state predicted by kalman filter
        self.kalman_filter_predict_state = None
        self.has_son = False
        self.father_real_id = None
        self.son_real_id = None


class Obs_Graph(object):
    #####################
    """
        Obs_grap:
            type:
                list
                the length equals the number of the frames
                every node record the current frame informations
            content:
                    iso_idx:a list of which length equals bbx number in this frame
                    child:
                    iso_child
    """
    def __init__(self,num_det = None):
        self.iso_idx = []
        self.child = []
        self.iso_child = []
        #this attribute means the similarity between current detection and the father detection
        self.child_A_Model_affinity =[0]*num_det
        self.kalman_filters = []
        if num_det != None:
            for i in range(0,num_det):
                kalman_filter = Kalman_Filter()
                self.kalman_filters.append(kalman_filter)
