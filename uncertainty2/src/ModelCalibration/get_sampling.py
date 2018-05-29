# -*- coding: utf-8 -*-

import Sql
import numpy as np

def get_input():
    records = Sql.selectSql((9, 0), Sql.get_samp2)
    mat = None
    for record in records:
        samps = record[1].decode('utf-8')
        samps = samps.split(',')
        samps = [float(samp) for samp in samps]
        if mat == None:
            mat = samps
        else:
            mat = np.row_stack((mat, samps))
    print mat

if __name__ == '__main__':
    get_input()