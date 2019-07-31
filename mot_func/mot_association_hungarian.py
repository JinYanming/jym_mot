import numpy as np
from Common.munkres import munkres    
def mot_association_hungarian(score_mat=None,thr=None,*args,**kwargs):

    
    if score_mat.shape[0] == 1:
        assignment,cost=munkres(- (score_mat.T))
        assignment=assignment.T
        ass_row,ass_col=np.where(assignment == 1)[0]
    else:
        assignment,cost=munkres(- (score_mat))
        ass_row,ass_col=np.where(assignment == 1)[0]
    
    match_cost=score_mat[assignment]
    midx=np.where(match_cost > thr)[0]
    matching=[ass_row(midx),ass_col(midx)]
    score=match_cost[midx]
    return matching,score
    
if __name__ == '__main__':
    pass
    

