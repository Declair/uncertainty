# -*- coding: utf-8 -*-
import numpy as np
import ValidateRealModel as rm
import ValidateDoubleLoop
import mashi as ms
import oushi as ou
import manhadun as mh
import qiebixuefu as qbxf
import xuangduishang as kl

import matplotlib.pyplot as plt

from sklearn.gaussian_process.kernels import (RBF, Matern, RationalQuadratic,
                                              ExpSineSquared, DotProduct,
                                              ConstantKernel)
import ValidateGetSample as gs
import ValidateUi as cp

cog_p_all = 0
cog_p = 0
inh_p = 0
input_v = 0
input_v1 = 0
input_v2 = 0
output1 = 0
output2 = 0

def importData(snb, n_id):
    global cog_p_all
    global cog_p
    global inh_p
    global input_v
    global input_v1
    global input_v2
    global output1
    global output2

    cog_p_all = gs.get_samp(nid = n_id, arg_type=2)   # 根据你选择的模型导入相应的数据
    inh_p = gs.get_samp(nid = n_id, arg_type=1)
    input_v = gs.get_samp(nid = n_id, arg_type=0)

    cog_p = cog_p_all[0:200, :]

    shape = input_v.shape
    d1 = shape[0]/3
    input_v1 = input_v[0:d1*2, :]
    input_v2 = input_v[d1*2:, :]

    output1 = rm.run_real_model(inh_p, input_v1)
    output2 = rm.run_real_model(inh_p, input_v2)

    show_log = ''

    show_log = show_log + str(cog_p_all.shape) + '\n'
    print '认知不确定参数:'
    show_log = show_log + '认知不确定参数' + '\n'
    print cog_p.shape
    show_log = show_log + str(cog_p.shape) + '\n'
    print cog_p
    show_log = show_log + '%r'%(cog_p) + '\n'
    print '固有不确定参数:'
    show_log = show_log + '固有不确定参数:' + '\n'
    print inh_p.shape
    show_log = show_log + str(inh_p.shape) + '\n'
    print inh_p
    show_log = show_log + '%r'%(inh_p) + '\n'
   #print '训练输入:'
   # show_log = show_log + '训练输入:' + '\n'
   # print input_v1.shape
   # show_log = show_log + str(input_v1.shape) + '\n'
   # print input_v1
  #  show_log = show_log + '%r'%(input_v1) + '\n'
  #  print '对比输入:'
   # show_log = show_log + '对比输入:' + '\n'
   # print input_v2.shape
    #show_log = show_log + str(input_v2.shape) + '\n'
   # print input_v2
   # show_log = show_log + '%r'%(input_v2) + '\n'
    print '训练输出:'
    show_log = show_log + '训练输出:' + '\n'
    print output1.shape
    show_log = show_log + str(output1.shape) + '\n'
    print output1
    show_log = show_log + '%r'%(output1) + '\n'
    print '对比输出:'
    show_log = show_log + '对比输出:' + '\n'
    print output2.shape
    show_log = show_log + str(output2.shape) + '\n'
    print output2
    show_log = show_log + '%r'%(output2) + '\n'




    show_panel = snb.panel_import
    csw = snb.sw
    csw.text_ctrl.SetValue(show_log)
    show_panel.Layout()
    return output1.shape,output2.shape



if __name__ == '__main__':
    importData()


def buildoushidistance(cog_p, inh_p, output1, input_v1):
    aa = ValidateDoubleLoop.outer_level_loop(cog_p, inh_p, output1, input_v1)
    yy = np.array(aa)
    y = yy[0]
    m = np.array(output1)
    n = len(m)
    ou.figure_ou(y, n, m)

def buildmshidistance(cog_p, inh_p, output1, input_v1):
    aa = ValidateDoubleLoop.outer_level_loop(cog_p, inh_p, output1, input_v1)
    yy = np.array(aa)
    y = yy[0]
    m = np.array(output1)
    n = len(m)
    ms.figure_ms(y, n, m)


def buildqiebixuefudistance(cog_p, inh_p, output1, input_v1):
    aa = ValidateDoubleLoop.outer_level_loop(cog_p, inh_p, output1, input_v1)
    yy = np.array(aa)
    y = yy[0]
    m = np.array(output1)
    n = len(m)
    qbxf.figure_qbxf(y, n, m)





def buildmanhadundistance(cog_p, inh_p, output1, input_v1):
    aa = ValidateDoubleLoop.outer_level_loop(cog_p, inh_p, output1, input_v1)
    yy = np.array(aa)
    y = yy[0]
    m = np.array(output1)
    n = len(m)
    mh.figure_mh(y, n, m)


def buildKLdistance(cog_p, inh_p, output1, input_v1):
    aa = ValidateDoubleLoop.outer_level_loop(cog_p, inh_p, output1, input_v1)

    m = np.array(output1)  # cankao
    y = np.array(aa) #fahgnzhen


    kl.figure_kl(y,m)