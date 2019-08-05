import numpy as np
def ListIndice1d(raw_list,indice_list):
    result_list = []
    for item in indice_list:
        result_list.append(raw_list[i])
    return result_list
def ListIndice2d(raw_list = None,indice_list_row = None,indice_list_col = None):
    result_list = []
    if indice_list_row == None:
        indice_list_row = [0,len(raw_list)]
    for i in range(indice_list_row[0],indice_list_row[1]):
        result_list.append(raw_list[i][indice_list_col[0]:indice_list_col[1]])
    return result_list
