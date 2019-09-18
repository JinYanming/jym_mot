import numpy as np
from mot_func.mot_color_similarity import mot_color_similarity
def cal_a_model_affinity(cur_a_model = None,prev_a_model = None,i = None):
    Affinity = []
    for a_model in prev_a_model:
        affinity = mot_color_similarity(cur_a_model[i],a_model)
        Affinity.append(affinity)
    Affinity = np.array(Affinity)
    return Affinity
