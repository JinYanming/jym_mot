import numpy as np

def mot_search_association(Obs_grap=None,fr=None,prt_idx=None,*args,**kwargs):
    """
    input:
            Obs_grap,fr,prt_idx
            Obs_grap:graph
            fr:the last init frame
            prt_idx:every child dectection list from the privious frame
    output:
        ass_idx
        ass_idx:the tracklet of this object
    """
    flg = 1
    ct= 0
    ass_idx=[]
    check_none = lambda x: True if len(x) >= 1 and x[0]!=-1 else False
    if prt_idx != -1:
        while flg == 1 :
            ct=ct + 1
            if Obs_grap[fr -ct].iso_idx[prt_idx] != -1:
                getMapped = lambda c_list,p_list:[j for i in c_list for j in p_list[i]]
                prt_idx = Obs_grap[fr-ct].child[prt_idx]
                ass_idx.append(prt_idx)
            else:
                flg = 0
            #when it comes to -1 means the tracklet suspend
            if prt_idx == -1:
                flg = 0

    
    ass_idx.reverse()
    return ass_idx
    
if __name__ == '__main__':
    pass
    

