# -*- coding: utf-8 -*-
import cal_f as ca
import simu_model as sm
import CalibrationPanel as cp

def inner_level_loop(cog_p_r, inh_p, input_X, sym=0):
    output_m = sm.run_simu_model(cog_p_r, inh_p[0], input_X)
    shape_va = inh_p.shape
    M_v = shape_va[0]
    for i in range(M_v):
        if i == 0:
            continue
        inh_p_r = inh_p[i]  # 每一组固有不确定参数
        if sym==0:   #如果是0，说明运行自测试的仿真软件，否则说明运行的是导入的仿真软件
            output_ma = sm.run_simu_model(cog_p_r, inh_p_r, input_X)  # output_m为仿真模型在固定认知和固有不确定参数下的输出矩阵1*p
        else:
            output_ma = RunImportedModel(nid=cp.n_id)
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

    shape_v = cog_p.shape
    N_v = shape_v[0]  # 认知不确定性参数的组数
    list_t = list()
    for i in range(N_v):  # 每一组认知不确定参数
        a_mat = inner_level_loop(cog_p[i], inh_p, input_X, sym=sym)
        #         # print('获得的仿真输出:')
        #         # print(a_mat)
        #         # print('认知不确定参数:')
        #         # print(cog_p[i])
        y_out = ca.Euclid_distance(a_mat, output)  # 将获得的输出特征矩阵和参考数据组成的矩阵进行运算获得马氏距离   他们都是每一行代表一个输出
        # print('一致性度量为:')
        # print(y_out)
        list_t.append(y_out)  # 将获得的马氏距离添加到输出向量中
    return list_t