# -*- coding: utf-8 -*-

import Sql
import numpy as np

#arg_type = 0取自变量   1取固有  2是认知
def get_samp(nid = 9, arg_type = 0):
    records = Sql.selectSql((nid, arg_type), Sql.get_samp2)
    flag = 0
    for record in records:
        samps = record[1].decode('utf-8')
        samps = samps.split(',')
        samps = [float(samp) for samp in samps]
        if flag == 0:
            mat = samps
            flag = 1
        else:
            mat = np.row_stack((mat, samps))
    mat = np.transpose(mat)
    print mat

if __name__ == '__main__':
    get_samp()