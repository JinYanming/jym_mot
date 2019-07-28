import numpy as np
def state_lists2array(state):
    """
    state:a list which consist of list
    """
    state_array = np.zeros((4,0))
    print(state)
    for list in state:
        if len(list) !=0:
            state_array = np.c_[state_array,np.array(list)[:,np.newaxis]]
    print(state_array)
    return state_array
            
