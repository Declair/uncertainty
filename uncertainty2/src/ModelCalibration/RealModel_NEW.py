import numpy
import CalculateMethod as ca
import CalibrationPanel as cp
import arg_order as ao
from compiler.ast import flatten
import numpy as np
import BuildMetaModel
import ShowNotebook as SNB



def run_real_model(inh_p, input_X):
    real_cog_p_r = BuildMetaModel.real_cog_p_r
    real_cog_p_r = real_cog_p_r.split(',')
    cog_p_r = list()
    for str1 in real_cog_p_r:
        v1 = float(str1)
        cog_p_r.append(v1)
    cog_p_r = np.mat(cog_p_r)
    print cog_p_r
    order = ao.get_order(cp.n_id)
    shape_inh = inh_p.shape
    ret = RunImportedModel(order, cog_p_r, inh_p[0], input_X)

    for i in range(shape_inh[0]):
        if i==0:
            continue
        tret = RunImportedModel(order, cog_p_r, inh_p[i], input_X)
        ret = ret + tret
    ret = ret/shape_inh[0]
    return ret


def RunImportedModel(order, cog_p_r, inh_p_r, input_X):
    shape_v = input_X.shape
    n = shape_v[0]
    cog_p_r_l = flatten(cog_p_r.tolist())
    inh_p_r_l = flatten(inh_p_r.tolist())
    inp_l = flatten(input_X[0].tolist())
    rans = ao.get_result(cp.n_id, order, inp_l, inh_p_r_l, cog_p_r_l)
    for i in range(n):
        if i == 0:
            continue
        inp_l = flatten(input_X[i].tolist())
        tans = ao.get_result(cp.n_id, order, inp_l, inh_p_r_l, cog_p_r_l)
        rans = np.row_stack((rans, tans))
    return np.mat(rans)
