from tools.ListGiant import ListInsert
def mot_check_idsw(tracklet = None):
    id_list = tracklet.hyp.ystates_id

    count = 0
    prev_id = id_list[0]
    length = len(id_list)
    tracklet.hyp.idsw = [0]*length
    for i in range(1,length):
        cur_id = id_list[i]
        if cur_id != prev_id and cur_id != -1:
            count +=1
            ListInsert(tracklet.hyp.idsw,i,1,0)
            prev_id = cur_id
    tracklet.hyp.idsw_count = count
