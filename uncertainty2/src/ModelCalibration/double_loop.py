# -*- coding: utf-8 -*-
import cal_f as ca
import simu_model as sm
import CalibrationPanel as cp
import arg_order as ao
from compiler.ast import flatten
import numpy as np

def RunImportedModel(order, cog_p_r, inh_p_r, input_X):
    shape_v = input_X.shape
    n = shape_v[0]

    cog_p_r_l = flatten(cog_p_r.tolist())
    inh_p_r_l = flatten(inh_p_r.tolist())
    inp_l = flatten(input_X[0].tolist())

    rans = ao.get_result(cp.n_id, order, inp_l, inh_p_r_l, cog_p_r_l)
    #rans = run_simu_model_inner(cog_p_r, inh_p_r, input_X[0])
    for i in range(n):
        if i == 0:
            continue

        inp_l = flatten(input_X[i].tolist())
        tans = ao.get_result(cp.n_id, order, inp_l, inh_p_r_l, cog_p_r_l)
        #tans = run_simu_model_inner(cog_p_r, inh_p_r, input_X[i])
        rans = np.row_stack((rans, tans))
    return np.mat(rans)


def inner_level_loop(cog_p_r, inh_p, input_X, order=0, sym=0):
    if sym==0:
        output_m = sm.run_simu_model(cog_p_r, inh_p[0], input_X)
    else:
        output_m = RunImportedModel(order, cog_p_r, inh_p[0], input_X)

    # print 'output_m:'
    # print output_m
    shape_va = inh_p.shape
    M_v = shape_va[0]
    for i in range(M_v):
        if i == 0:
            continue
        inh_p_r = inh_p[i]  # 每一组固有不确定参数
        if sym==0:   #如果是0，说明运行自测试的仿真软件，否则说明运行的是导入的仿真软件
            output_ma = sm.run_simu_model(cog_p_r, inh_p_r, input_X)  # output_m为仿真模型在固定认知和固有不确定参数下的输出矩阵1*p
        else:
            output_ma = RunImportedModel(order, cog_p_r, inh_p_r, input_X)
        # output_m = numpy.vstack((output_m, output_ma))
        output_m = output_m + output_ma

    # print('内层循环输出:')
    # print(output_m)
    output_m = output_m/M_v
    return output_m  # 是一个在该认知不确定参数下得到的输出特征矩阵M*p  p为输出个数

def outer_level_loop(cog_p, inh_p, output, input_X, sym=0):  # Es_p为认知不确定参数矩阵N*nr  N为组数，nr为每组的认知不确定性参数个数   Er_p为固有不确定性参数矩阵M*mr M为固有不确定性参数组数，mr为每组固有不确定性参数个数
    # print('认知不确定参数:')
    # print(Es_p)
    # print('固有不确定参数:')
    # print(Er_p)
    # print('输入为:')
    # print(input_X)

    order = 0
    if sym == 1:
        order = ao.get_order(cp.n_id)

    shape_v = cog_p.shape
    N_v = shape_v[0]  # 认知不确定性参数的组数
    list_t = list()
    for i in range(N_v):  # 每一组认知不确定参数
        a_mat = inner_level_loop(cog_p[i], inh_p, input_X, order, sym=sym)
        #         # print('获得的仿真输出:')
        #         # print(a_mat)
        #         # print('认知不确定参数:')
        #         # print(cog_p[i])
        y_out = ca.Euclid_distance(a_mat, output)  # 将获得的输出特征矩阵和参考数据组成的矩阵进行运算获得马氏距离   他们都是每一行代表一个输出
        # print('一致性度量为:')
        # print(y_out)
        list_t.append(y_out)  # 将获得的马氏距离添加到输出向量中
    return list_t