import numpy as np
def lists2array(state,c = None):
    """
    state:a list which consist of list
    """
    state_array = np.zeros((c,0))
    for list in state:
        if len(list) !=0:
            state_array = np.c_[state_array,np.array(list)[:,np.newaxis]]
    return state_array
            
