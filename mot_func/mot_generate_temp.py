import numpy as np
from Common.affparam2mat import affparam2mat
from Common.warpimg import warpimg
def mot_generate_temp(img=None,state=None,sz=None,*args,**kwargs):

    #if (sz == None):
    #    sz = img.shape
    
    #if (len(state) == 1):
    #   state = state[:]
    
    N = len(state)
    """
    AEF:
        shape:[num,6]
            element:x , y, w/sz[0], 0, h/w, 0
    """
    AFF_Generate = lambda states:[[item[0],item[1],item[2]/sz[0],0,item[3]/item[2],0]for item in states]
    AFF = AFF_Generate(state)
    #AFF=concat([[state(1,arange())],[state(2,arange())],[state(3,arange()) / sz(1)],[zeros(1,N)],[state(4,arange()) / state(3,arange())],[zeros(1,N)]])
    AFF=affparam2mat(AFF)
    tmpl=warpimg(img,AFF,sz)
    tmpl=tmpl.reshape([sz[0]*sz[1],N])
    return tmpl

