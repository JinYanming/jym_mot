import numpy as np    
def Labelling(param=None,*args,**kwargs):
    
    label=param.label
    label_array = np.array(label)
    zero_index = np.where(label_array == 0)[0]
    idx = np.min(zero_index)
    param.label[idx]=1
    return param,idx
