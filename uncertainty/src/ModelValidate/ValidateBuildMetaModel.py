# -*- coding: utf-8 -*-
import numpy as np
import time

import sys
from wx.lib.mixins.listctrl import TextEditMixin

import ValidateRealModel_New as rm
import ValidateDoubleLoop
import mashi as ms
import oushi as ou
import manhadun as mh
import qiebixuefu as qbxf
import xuangduishang as kl
import zhi as zi
import pandas as pd
import wx.grid
from ModelCalibration import GetSample as gs
import ValidateUi as cp


from sklearn.gaussian_process.kernels import (RBF, Matern, RationalQuadratic, DotProduct,ConstantKernel)
import wx

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

    cog_p_all = gs.get_samp(nid=n_id, arg_type=2)  # 根据你选择的模型导入相应的数据
    inh_p = gs.get_samp(nid=n_id, arg_type=1)
    input_v = gs.get_samp(nid=n_id, arg_type=0)
    cog_p = cog_p_all[0:200, :]

    shape = input_v.shape
    d1 = shape[0] / 3
    input_v1 = input_v[0:d1 * 2, :]
    input_v2 = input_v[d1 * 2:, :]

    output1 = rm.run_real_model(inh_p, input_v1)
    output2 = rm.run_real_model(inh_p, input_v2)
    show_panel = snb.show_panel
    Cal_form = snb.Cal_form
    Comp_form = snb.Comp_form


    draw_table(3, 5,  output1, Cal_form, "计算输出")
    draw_table(3, 5,  output2, Comp_form, "对比输出")

    show_panel.SetupScrolling()
    show_panel.Layout()

    cp.sym1 = 1

    dlg = wx.MessageDialog(None, message='数据导入已经完成')
    dlg.ShowModal()

def buildoushidistance(snb,cog_p, inh_p, output1, input_v1):
    show_panel = snb.show_panel
    aa = ValidateDoubleLoop.outer_level_loop(cog_p, inh_p, output1, input_v1)
    yy = np.array(aa)
    y = yy[0]
    m = np.array(output1)
    n = len(m)
    d = ou.oushidistance(y, n, m)
    d1 = zi.Orang(d, len(d))


    show_panel = snb.show_panel
    grid = snb.grid_out
    grid.CreateGrid(1, len(d))
    grid.SetRowLabelValue(0, '欧式距离')
    grid.SetRowLabelAlignment(horiz=wx.ALIGN_TOP, vert=wx.ALIGN_TOP)
    for i in range(len(d)):
        grid.SetColLabelValue(i, '%d' % (i + 1))
        grid.SetCellValue(0, i, str(round(d[i], 3)))

    axes = snb.axes
    axes2 = snb.axes2
    canvas = snb.canvas
    canvas2 = snb.canvas2
    axes.clear()
  #  lpred, = axes.plot(y_pred, 'r', label='predict value')
    #ltest, = axes.plot(y_test, 'g', label='real value')
    axes.boxplot(d)
    axes.set(ylabel='Euclidean distance', title='Simulation of Euclidean distance')

    axes2.set(ylabel='Euclidean distance', title='data analysis')
    name_list = ['sum', 'var', '1/4', '3/4', 'median']
    axes2.bar(range(len(d1)), d1, color='black', tick_label=name_list,width = 0.6)


    #axes.legend(handles=[lpred, ltest], labels=['predict value', 'real value'])
    canvas.draw()
    canvas2.draw()
    show_panel.SetupScrolling()
    show_panel.Layout()




   # plt.figure("5")
    # plt.figure(2)#创建图表2

    #ax1 = plt.subplot(221)  # 在图表2中创建子图1
    #s1 = pd.Series(np.array(d))
   # data1 = pd.DataFrame({"Simulation of Euclidean distance": s1})
    # plt.ylabel("ylabel")
    # plt.xlabel("xlabel")
    #plt.title("Euclidean distance")
   # data1.boxplot()  # 这里，pandas自己有处理的过程，很方便哦
    #ax2 = plt.subplot(222)
    # make a histogram of the data array
  #  num_list1 = zi.Orang(d, len(d))
   # name_list = ['sum', 'var', '1/4', '3/4', 'median']
   # plt.title("data")
   # plt.bar(range(len(num_list1)), num_list1, color='black', tick_label=name_list)
   # plt.show()
    #show_panel = snb.show_panel
    #grid = snb.grid_out
    #grid.CreateGrid(1, len(d))
    #grid.SetRowLabelValue(0, '欧式距离')
   # grid.SetRowLabelAlignment(horiz=wx.ALIGN_TOP, vert=wx.ALIGN_TOP)
   # for i in range(len(d)):
        #grid.SetColLabelValue(i, '%d' % (i + 1))
       # grid.SetCellValue(0, i, str(round(d[i], 3)))

    #show_panel.SetupScrolling()
    #show_panel.Layout()

def buildmshidistance(snb,cog_p, inh_p, output1, input_v1):
    show_panel = snb.show_panel
    aa = ValidateDoubleLoop.outer_level_loop(cog_p, inh_p, output1, input_v1)
    yy = np.array(aa)
    y = yy[0]
    m = np.array(output1)
    n = len(m)
    d = ms.mashidistance(y, n, m)
    d1 = zi.Orang(d, len(d))

    show_panel = snb.show_panel
    grid = snb.grid_out
    grid.CreateGrid(1, len(d))
    grid.SetRowLabelValue(0, '马氏距离')
    grid.SetRowLabelAlignment(horiz=wx.ALIGN_TOP, vert=wx.ALIGN_TOP)
    for i in range(len(d)):
        grid.SetColLabelValue(i, '%d' % (i + 1))
        grid.SetCellValue(0, i, str(round(d[i], 3)))

    axes = snb.axes
    axes2 = snb.axes2
    canvas = snb.canvas
    canvas2 = snb.canvas2
    axes.clear()
    #  lpred, = axes.plot(y_pred, 'r', label='predict value')
    # ltest, = axes.plot(y_test, 'g', label='real value')
    print "========================"
    x = []
    for i in range(len(d)):
        x.append(float(str(round(d[i],8))))
    print x
    print "========================"
    d = x
    axes.boxplot(d)
    axes.set(ylabel='Markov distance', title='Simulation of Markov distance')

    axes2.set(ylabel='Markov distance', title='data analysis')
    name_list = ['sum', 'var', '1/4', '3/4', 'median']
    axes2.bar(range(len(d1)), d1, color='black', tick_label=name_list, width=0.6)

    # axes.legend(handles=[lpred, ltest], labels=['predict value', 'real value'])
    canvas.draw()
    canvas2.draw()
    show_panel.SetupScrolling()
    show_panel.Layout()


def buildqiebixuefudistance(snb,cog_p, inh_p, output1, input_v1):
    show_panel = snb.show_panel
    aa = ValidateDoubleLoop.outer_level_loop(cog_p, inh_p, output1, input_v1)
    yy = np.array(aa)
    y = yy[0]
    m = np.array(output1)
    n = len(m)
    d = qbxf.qiebixuefudistance(y, n, m)
    d1 = zi.Orang(d, len(d))

    show_panel = snb.show_panel
    grid = snb.grid_out
    grid.CreateGrid(1, len(d))
    grid.SetRowLabelValue(0, '切比雪夫距离')
    grid.SetRowLabelAlignment(horiz=wx.ALIGN_TOP, vert=wx.ALIGN_TOP)
    for i in range(len(d)):
        grid.SetColLabelValue(i, '%d' % (i + 1))
        grid.SetCellValue(0, i, str(round(d[i], 3)))

    axes = snb.axes
    axes2 = snb.axes2
    canvas = snb.canvas
    canvas2 = snb.canvas2
    axes.clear()
    #  lpred, = axes.plot(y_pred, 'r', label='predict value')
    # ltest, = axes.plot(y_test, 'g', label='real value')
    print "2========================"
    print d
    print "========================"
    axes.boxplot(d)
    axes.set(ylabel='Chebyshev distance', title='Simulation of Chebyshev distance')

    axes2.set(ylabel='Chebyshev distance', title='data analysis')
    name_list = ['sum', 'var', '1/4', '3/4', 'median']
    axes2.bar(range(len(d1)), d1, color='black', tick_label=name_list, width=0.6)

    # axes.legend(handles=[lpred, ltest], labels=['predict value', 'real value'])
    canvas.draw()
    canvas2.draw()
    show_panel.SetupScrolling()
    show_panel.Layout()





def buildmanhadundistance(snb,cog_p, inh_p, output1, input_v1):
    show_panel = snb.show_panel
    aa = ValidateDoubleLoop.outer_level_loop(cog_p, inh_p, output1, input_v1)
    yy = np.array(aa)
    y = yy[0]
    m = np.array(output1)
    n = len(m)
    d = mh.manhadundistance(y, n, m)
    d1 = zi.Orang(d, len(d))

    show_panel = snb.show_panel
    grid = snb.grid_out
    grid.CreateGrid(1, len(d))
    grid.SetRowLabelValue(0, '曼哈顿距离')
    grid.SetRowLabelAlignment(horiz=wx.ALIGN_TOP, vert=wx.ALIGN_TOP)
    for i in range(len(d)):
        grid.SetColLabelValue(i, '%d' % (i + 1))
        grid.SetCellValue(0, i, str(round(d[i], 3)))

    axes = snb.axes
    axes2 = snb.axes2
    canvas = snb.canvas
    canvas2 = snb.canvas2
    axes.clear()
    #  lpred, = axes.plot(y_pred, 'r', label='predict value')
    # ltest, = axes.plot(y_test, 'g', label='real value')
    print "3========================"
    print d
    print "========================"
    axes.boxplot(d)
    axes.set(ylabel='Manhattan  distance', title='Simulation of Manhattan distance')

    axes2.set(ylabel='Manhattan  distance', title='data analysis')
    name_list = ['sum', 'var', '1/4', '3/4', 'median']
    axes2.bar(range(len(d1)), d1, color='black', tick_label=name_list, width=0.6)

    # axes.legend(handles=[lpred, ltest], labels=['predict value', 'real value'])
    canvas.draw()
    canvas2.draw()
    show_panel.SetupScrolling()
    show_panel.Layout()


def buildKLdistance(snb,cog_p, inh_p, output1, input_v1):
    aa = ValidateDoubleLoop.outer_level_loop(cog_p, inh_p, output1, input_v1)
    m = np.array(output1)  # cankao
    y = np.array(aa) #fahgnzhen
    d = kl.KLdistanse(y,m)

    show_panel = snb.show_panel
    grid = snb.grid_out
    grid.CreateGrid(1, len(d))
    grid.SetRowLabelValue(0, 'kl')
    grid.SetRowLabelAlignment(horiz=wx.ALIGN_TOP, vert=wx.ALIGN_TOP)
    for i in range(len(d)):
        grid.SetColLabelValue(i, '%d' % (i + 1))
        grid.SetCellValue(0, i, str(round(d[i], 3)))

    show_panel.Layout()
    show_panel.SetupScrolling()

def draw_table(x, y, show, form, text):

    row, cloumn = show.shape
    # grid.CreateGrid(row, cloumn)
    # for i in range(row):
    #     grid.SetRowLabelValue(i, '%dth抽样' % (i + 1))
    #     for j in range(cloumn):
    #         if i == 0:
    #             grid.SetColLabelValue(j, )
    #             grid.SetColSize(j, -1)
    #         grid.SetCellValue(i, j, str(round(show[i, j], 3)))

    for i in range(cloumn):
         form.InsertColumn(i, text+'_%d' % (i + 1), width=160)
    # 初始化表格
    for i in range(row):
         index = form.InsertItem(sys.maxint, 0)
         print(str(i)+":"+str(index))

    # 设置内容
    for i in range(cloumn):
         for j in range(row):
            # 截段输出 numpy 抽样结果过长
            form.SetItem(j, i, str(round(show[j, i], 3)))
            print(str(i)+":"+str(j))
    #         i = i + 1
    #     j += 1
    #
    #
    # self.gbSizer_show.Add(form, wx.GBPosition(x, y), wx.GBSpan(1, 3), wx.ALL, 5)
    # return y + size_of_par

    # for i in range(cloumn):
    #     form.InsertRow(i, '%dth抽样' % (i + 1), width=160)
    #     for j in range(cloumn):
    #         if (i == 0):
    #             form.InsertItem(j, text + '_%d' % (j + 1))
    #         form.SetItem(i, j, str(("%.3f" % row)))

class EditMixin(wx.ListCtrl, TextEditMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
        TextEditMixin.__init__(self)