import numpy as np
class HYP(object):
    def __init__(self):
        self.score = None
        self.ystate = None
        self.new_tmpl = None
        self.ystates_id = None
        self.idsw = None
        self.idsw_count = None
class F_Motion(object):
    def __init__(self):
        self.X = None
        self.P = None
class B_Motion(object):
    def __init__(self):
        self.X = None
        self.P = None
class Tracklet(object):
    def __init__(self):
        self.Conf_prob= 0
        self.type = "Low"
        self.reliable = False
        self.isnew = True
        self.sub_img = []
        self.status = "none"
        self.label = "-1"
        self.ifr = 0
        self.efr = 0
        self.window_end = 0
        self.last_update = 0
        self.state = []
        self.A_model = np.zeros(144)
        self.A_model_head = np.zeros(144)
        self.A_model_tail = np.zeros(144)
        self.A_model_list = []
        self.FMotion = F_Motion()
        self.BMotion = B_Motion()
        self.hyp = HYP()
        self.detections_id_list = []
