import numpy as np
from Common.color_tools import rgb2hsv
from mot_func.mot_generate_temp import mot_generate_temp
def mot_appearance_model_generation(img=None,param=None,state=None,state_list=False,*args,**kwargs):

    # input :
    # img: a color image
    # state: [Center(X), Center(Y), Width, Height]
    # output : 
    # tmpl_hist: color histograms

    if param.color=='HSV':
        h,s,v = rgb2hsv(img[0],img[1],img[2])
        hsv_img = [h,s,w]
    else:
        hsv_img = img
    
    h_img=hsv_img[0,:,:] / np.max(img[0,:,:])
    s_img=hsv_img[1,:,:] / np.max(img[1,:,:])
    v_img=hsv_img[2,:,:] / np.max(img[2,:,:])
    #v_img=double(hsv_img(arange(),arange(),3)) / double(max(max(img(arange(),arange(),3))))
    initS = state if state_list else [state]
    h_tmpl=mot_generate_temp(h_img,initS,param.tmplsize)
    s_tmpl=mot_generate_temp(s_img,initS,param.tmplsize)
    v_tmpl=mot_generate_temp(v_img,initS,param.tmplsize)
    
    Nd=len(initS)
    h_tmpl = h_tmpl.reshape([param.subvec,param.subregion,Nd])
    s_tmpl = s_tmpl.reshape([param.subvec,param.subregion,Nd])
    v_tmpl = v_tmpl.reshape([param.subvec,param.subregion,Nd])
    all_tmpl = np.ones([3,param.subvec, param.subregion,Nd])
    all_tmpl[0]=h_tmpl
    all_tmpl[1]=s_tmpl
    all_tmpl[2]=v_tmpl
    nbins=param.Bin
    tmpl_hist=[]
    temp_hist=[]
    for j in range(1,Nd):
        temp_hist=[]
        for i in arange(1,3).reshape(-1):
            max_val=max(max(all_tmpl[i](arange(),arange(),j)))
            cb_tmpl=all_tmpl[i](arange(),arange(),j)
            cb_tmpl=dot(cb_tmpl / max_val,nbins)
            if param.subregion == 1:
                cb_tmpl_hist=(hist(cb_tmpl,nbins) / param.subvec).T
            else:
                cb_tmpl_hist=(hist(cb_tmpl,nbins) / param.subvec)
            temp_hist=concat([[temp_hist],[cb_tmpl_hist]])
        tmpl_hist[arange(),arange(),j]=temp_hist / 3
    return tmpl_hist

