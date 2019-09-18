class Node(object):
    def __init__(self):
        self.child = []
class ISO(object):
    def __init__(self):
        #meas save the detections that is unmatched 
        self.meas = None
        #node save the detections id that is unmatched
        self.node = None
        self.ystates_ids = None
