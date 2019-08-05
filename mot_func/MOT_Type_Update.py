import numpy as np
from mot_func.mot_is_reg import mot_is_reg
def MOT_Type_Update(rgbimg=None,Trk=None,type_thr=None,cfr=None,*args,**kwargs):

    
    del_idx=[]
    lb_idx=[]
    max_frame=50
    for i in range(0,len(Trk)):
        Conf_prob=Trk[i].Conf_prob
        type_=Trk[i].type
        if 'High' == type_:
            if Conf_prob < type_thr:
                Trk[i].type = 'Low'
                Trk[i].efr = cfr
        else:
            if 'Low' == type_:
                if Conf_prob > type_thr:
                    Trk[i].type = 'High'
                efr=Trk[i].efr
                if np.abs(cfr - efr) >= max_frame:
                    del_idx=concat([del_idx,i])
                    lb_idx=concat([lb_idx,Trk[i].label])
    
    R_pos = rgbimg.shape[:2]
    L_pos=np.array([0,0])
    margin=np.array([0,0])
    for i in range(0,len(Trk)):
        tstates=Trk[i].state[-1]
        if np.isnan(tstates[0]):
            del_idx = [del_idx,i]
        else:
            fmotion=Trk[i].state[-1]
            C_pos = np.array(fmotion[0:2])
            L_pos=L_pos + margin
            R_pos=R_pos - margin

            print("**"*80)
            print(C_pos,L_pos,R_pos)
            if not mot_is_reg(C_pos,L_pos,R_pos):
                del_idx.append(i)
    
    
    del_idx = np.array(del_idx)
    if not np.all(del_idx == 0):
        Trk[del_idx]=[]
    
    return Trk
    
if __name__ == '__main__':
    pass
    

