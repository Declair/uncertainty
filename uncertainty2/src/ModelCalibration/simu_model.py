# -*- coding: utf-8 -*-
import numpy
def run_simu_model_inner(cog_p_r, inh_p_r, input_Xi):
    shape_v1 = cog_p_r.shape
    shape_v2 = inh_p_r.shape
    s = 0
    sa = 0
    for i in range(shape_v1[1]):
        s = s+cog_p_r[0,i]*input_Xi[0,i]**1
        sa = sa+cog_p_r[0, i]*input_Xi[0, i]**2
    ts = 0
    for i in range(shape_v2[1]):
        ts = ts+inh_p_r[0, i]

    s = s+ts
    sa = sa+ts
    return s, sa

def run_simu_model_inner_arr(p, input_Xi):
    s = 0
    sa = 0
    for i in range(3):
        s = s+p[i]*input_Xi[i]**1
        sa = sa+p[i]*input_Xi[i]**2
    ts = 0
    for i in range(3):
        ts = ts+p[i+3]

    s = s+ts
    sa = sa+ts
    return s, sa

def description():
    param = [];
    param.append(['参数1', 'cog_p1', '无量纲']);
    param.append(['参数2', 'cog_p2', '无量纲']);
    param.append(['参数3', 'cog_p3', '无量纲']);
    param.append(['参数4', 'inh_p1', '无量纲']);
    param.append(['参数5', 'inh_p2', '无量纲']);
    param.append(['参数6', 'inh_p3', '无量纲']);
    return param;

def descr_var():
    var = [];
    var.append(['变量1', 'input_x1', '无量纲']);
    var.append(['变量2', 'input_x2', '无量纲']);
    var.append(['变量3', 'input_x3', '无量纲']);
    return var;

def run_simu_model(cog_p_r, inh_p_r, input_X):
    shape_v = input_X.shape
    n = shape_v[0]
    rans = run_simu_model_inner(cog_p_r, inh_p_r, input_X[0])
    for i in range(n):
        if i == 0:
            continue
        tans = run_simu_model_inner(cog_p_r, inh_p_r, input_X[i])
        rans = numpy.row_stack((rans, tans))
    return numpy.mat(rans)
