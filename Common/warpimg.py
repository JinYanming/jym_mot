import numpy as np
import scipy.ndimage    
def warpimg(img=None,p=None,sz=None,*args,**kwargs):
# function wimg = warpimg(img, p, sz)
    
#    img(h,w)
#    p(n,6) : mat format
#    sz(th,tw)
    
    
    if (sz == None):
        sz=img.shape
    
    #if (size(p,1) == 1):
    #   p=ravel(p)
    
    w=sz[1]
    h=sz[0]
    n= p.shape[0]
    x,y = np.meshgrid(np.arange(w)-w/2,np.arange(h)-h/2)
    item_1 = np.concatenate((np.ones((h*w,1)),x.reshape(-1,1),y.reshape(-1,1)),axis=1)
    item_2 = np.array([np.r_[p[:,0],p[:,1]],np.r_[p[:,2],p[:,3]],np.r_[p[:,3],p[:,4]]])
    pos = np.matmul(item_1,item_2)
    pos = pos.reshape((h,w,n,2))
    #x,y=np.meshgrid(concat([arange(1,w)]) - w / 2,concat([arange(1,h)]) - h / 2,nargout=2)
    #pos=reshape(dot(cat(2,ones(dot(h,w),1),ravel(x),ravel(y)),concat([[p(1,arange()),p(2,arange())],[p(arange(3,4),arange()),p(arange(5,6),arange())]])),concat([h,w,n,2]))
    target_sz = sz +[len(p)]
    wimg = scipy.ndimage.map_coordinates(img, [pos[:,:,:,0].ravel(), pos[:,:,:,1].ravel()], order=3, mode='nearest').reshape(target_sz)
#    wimg = scipy.ndimage.map_coordinates()
#    wimg=squeeze(interp2(img,pos(arange(),arange(),arange(),1),pos(arange(),arange(),arange(),2)))
    #wimg[find(isnan(wimg))]=0
    return wimg
