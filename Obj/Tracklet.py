import numpy as np
class HYP(object):
    def __init__(self):
        self.score = None
        self.ystate = None
        self.new_tmpl = None
class FMotion(object):
    def __init__(self):
        self.X = None
        self.P = None
class BMotion(object):
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
        self.last_update = 0
        self.state = []
        self.A_model = np.zeros(144)
        self.F_Motion = FMotion()
        self.B_Motion = BMotion()
        self.hyp = HYP()
