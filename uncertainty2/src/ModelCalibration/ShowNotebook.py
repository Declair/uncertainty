# -*- coding: utf-8 -*-

from __future__ import division
from wx import aui
from wx import grid
import Import_file
import Run
import Sql

import numpy
import wx
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn import linear_model
import mysql.connector
from mysql.connector import Error
import real_model as rm
import simu_model as sm
import cal_f as ca

def inner_level_loop(Es_pi, Er_p, input_X):
    output_m = sm.run_simu_model(Es_pi, Er_p[0], input_X)
    shape_va = Er_p.shape
    M_v = shape_va[0]
    for i in range(M_v):
        if i == 0:
            continue
        Er_pi = Er_p[i]  # 每一组固有不确定参数
        output_ma = sm.run_simu_model(Es_pi, Er_pi, input_X)  # output_m为仿真模型在固定认知和固有不确定参数下的输出矩阵1*p
        # output_m = numpy.vstack((output_m, output_ma))
        output_m = output_m + output_ma

    # print('内层循环输出:')
    # print(output_m)
    output_m = output_m/M_v
    return output_m  # 是一个在该认知不确定参数下得到的输出特征矩阵M*p  p为输出个数

def outer_level_loop(Es_p, Er_p, Er, input_X):  # Es_p为认知不确定参数矩阵N*nr  N为组数，nr为每组的认知不确定性参数个数   Er_p为固有不确定性参数矩阵M*mr M为固有不确定性参数组数，mr为每组固有不确定性参数个数
    # print('认知不确定参数:')
    # print(Es_p)
    # print('固有不确定参数:')
    # print(Er_p)
    # print('输入为:')
    # print(input_X)

    shape_v = Es_p.shape
    N_v = shape_v[0]  # 认知不确定性参数的组数
    list_t = list()
    for i in range(N_v):  # 每一组认知不确定参数
        a_mat = inner_level_loop(Es_p[i], Er_p, input_X)
        # print('获得的仿真输出:')
        # print(a_mat)
        print('认知不确定参数:')
        print(Es_p[i])
        y_out = ca.Mahalanobis_2(a_mat, Er)  # 将获得的输出特征矩阵和参考数据组成的矩阵进行运算获得马氏距离   他们都是每一行代表一个输出
        print('马氏距离为:')
        print(y_out)
        list_t.append(y_out[0, 0])  # 将获得的马氏距离添加到输出向量中
    return list_t

def GA_1(Er_p, svr):  # 产生种群中每个个体的适应度,是一个累计概率列表
    shape_v = Er_p.shape
    population_num = shape_v[0]
    output_l = list()
    pro_l = list()
    tot_o = 0
    tot_dis = 0
    for i in range(population_num):
        input_x_v = Er_p[i]
        # print("输入:", end=" ")
        # print(input_x_v, end= " ")
        output_t = svr.predict(input_x_v)
        # print(output_t, end=" ")
        output_l.append(output_t[0])
        tot_o = tot_o + 1 / output_t[0]
        tot_dis = tot_dis + output_t[0]

    print "平均马氏距离:",
    print tot_dis / population_num,
    avg_dif.append(tot_dis/population_num)
    # print("种群大小:", end=" ")
    # print(population_num, end=" ")
    sum = 0
    max = 0
    min = 2
    reci = 0
    recia = 0
    for i in range(population_num):
        if max < 1 / output_l[i] / tot_o:
            max = 1 / output_l[i] / tot_o
            reci = i
        if min > 1 / output_l[i] / tot_o:
            min = 1 / output_l[i] / tot_o
            recia = i
        sum = 1 / output_l[i] / tot_o + sum
        pro_l.append(sum)
    print "最优解:",
    print Er_p[reci],
    print "该最优解对应马氏距离:",
    print output_l[reci]
    min_dif.append(output_l[reci])
    max_dif.append(output_l[recia])
    y_v = outer_level_loop(Er_p[reci], test_cmp_Er_p, test_cmp_Er, test_cmp_input)
    cmp_dif.append(y_v[0])
    return pro_l

def retIndex(pro_l, len, r_v):  # 随机选取一个个体的下标  按照概率的大小
    i = 0
    for i in range(len):
        if pro_l[i] >= r_v:
            return i
    return i

def cross_op(individual_1, individual_2):
    shape_v = individual_1.shape
    len = shape_v[1]
    cross_point = numpy.random.randint(1, len)
    ret_indi = numpy.mat(numpy.full(individual_1.shape, 0))
    for i in range(shape_v[1]):
        if i <= cross_point:
            ret_indi[0, i] = individual_1[0, i]
        else:
            ret_indi[0, i] = individual_2[0, i]
    return ret_indi

def mut_op(indi):
    shape_v = indi.shape
    r_v = numpy.random.randint(1, shape_v[1])
    r_v_a = numpy.random.rand()
    if r_v_a >= 0.5:
        indi[0, r_v] = indi[0, r_v] + 0.5
    else:
        indi[0, r_v] = indi[0, r_v] - 0.5
    return indi

def GA_2(pro_l, Er_p, cross_p, mut_p):  # 产生新种群
    shape_v = Er_p.shape
    num_iter = shape_v[0]
    row_t = Er_p[retIndex(pro_l, num_iter, numpy.random.rand())]
    new_Er_p = numpy.mat(numpy.full(row_t.shape, 0))
    shape_va = row_t.shape
    for i in range(shape_va[1]):
        new_Er_p[0, i] = row_t[0, i]
    i = 1
    while i <= num_iter - 1:
        rand_c = numpy.random.rand()
        if rand_c >= 0 and rand_c < cross_p:  # 交叉成立
            r_1 = numpy.random.rand()
            r_2 = numpy.random.rand()
            index_1 = retIndex(pro_l, num_iter, r_1)
            index_2 = retIndex(pro_l, num_iter, r_2)
            while index_2 == index_1:
                r_2 = numpy.random.rand()
                index_2 = retIndex(pro_l, num_iter, r_2)
            individual_1 = Er_p[index_1]
            individual_2 = Er_p[index_2]
            new_indi = cross_op(individual_1, individual_2)
            r_3 = numpy.random.rand()
            if r_3 >= 0 and r_3 < mut_p:
                new_indi = mut_op(new_indi)
            new_Er_p = numpy.row_stack((new_Er_p, new_indi))
            i = i + 1
        else:
            r = numpy.random.rand()
            index = retIndex(pro_l, num_iter, r)
            new_indi = Er_p[index]
            r_3 = numpy.random.rand()
            if r_3 >= 0 and r_3 < mut_p:
                new_indi = mut_op(new_indi)
            new_Er_p = numpy.row_stack((new_Er_p, new_indi))
            i = i + 1
    return new_Er_p

test_Es_p = 1
test_Er_p = 1
test_input = 1
test_cmp_input = 1
test_Er = 1
test_cmp_Er = 1
test_cmp_Er_p =1

def initData(Es_p_gn=400, Es_p_n=4, Er_p_gn=20, Er_p_n=1, c_data_n=30, cmp_data_n=20):
    global test_Es_p
    test_Es_p = numpy.mat(numpy.random.randint(2, 7, (Es_p_gn, Es_p_n)))  # 认知不确定参数 实际应该通过抽样获得
    global test_Er_p
    test_Er_p = numpy.mat(numpy.random.randn(Er_p_gn, Er_p_n))  # 固有不确定参数  实际应该通过抽样获得
    global test_cmp_Er_p
    test_cmp_Er_p = test_Er_p
    global test_input
    test_input = numpy.mat(
        numpy.random.randint(6, 9, (c_data_n, 3)))  # 这个输入是为了让实际系统和仿真系统在不确定参数确定的情况下获得相应的输出，进而可以比较获得马氏距离，进而来训练SVR模型

    global test_cmp_input
    test_cmp_input = numpy.mat(
        numpy.random.randint(6, 9, (cmp_data_n, 3)))  # 这个输入是在每一次优化中获得的最优参数下仿真模型的输出和实际系统在这个输入下的输出的比较，进而可以看见优化参数的效果

    global test_Er
    test_Er = rm.run_real_model(test_Er_p, test_input)  # 实际应该通过运行实际系统获得

    global test_cmp_Er
    test_cmp_Er = rm.run_real_model(test_Er_p, test_cmp_input)

def buildSVR1(test_Es_p, test_Er_p, test_Er, test_input, cus_C, cus_epsilon, cus_kernel):
    # print("SVR建模方法，C: %f，epsilon：%f，kernel：%s"%(cus_C, cus_epsilon, cus_kernel))

    print('认知不确定参数矩阵:')
    print(test_Es_p)
    print('固有不确定参数')
    print(test_Er_p)
    print('参考输入:')
    print(test_input)
    print('参考输出矩阵:')
    print(test_Er)
    print('对比输入:')
    print(test_cmp_input)
    print('对比输出矩阵')
    print(test_cmp_Er)
    y_v = outer_level_loop(test_Es_p, test_Er_p, test_Er, test_input)  # 运行仿真系统获得输出向量，即马氏距离的向量  该输出和认知不确定参数Es_p共同构成训练数据集
    y_va = numpy.array(y_v)
    print('训练输出:')
    print(y_va)
    test_Es_pa = numpy.array(test_Es_p)
    svr = svm.SVR(kernel=cus_kernel, C=cus_C, epsilon=cus_epsilon).fit(test_Es_pa, y_va)
    return svr

def buildSVR2(test_Es_p, test_Er_p, test_Er, test_input, cus_alpha):
    print ("GPR建模方法，alpha：%f"%(cus_alpha))
    print('认知不确定参数矩阵:')
    print(test_Es_p)
    print('固有不确定参数')
    print(test_Er_p)
    print('参考输入:')
    print(test_input)
    print('参考输出矩阵:')
    print(test_Er)
    print('对比输入:')
    print(test_cmp_input)
    print('对比输出矩阵')
    print(test_cmp_Er)
    y_v = outer_level_loop(test_Es_p, test_Er_p, test_Er, test_input)  # 运行仿真系统获得输出向量，即马氏距离的向量  该输出和认知不确定参数Es_p共同构成训练数据集
    y_va = numpy.array(y_v)
    print('训练输出:')
    print(y_va)
    test_Es_pa = numpy.array(test_Es_p)
    gpr = GaussianProcessRegressor(alpha=cus_alpha).fit(test_Es_pa, y_va)
    return gpr

def buildSVR3(test_Es_p, test_Er_p, test_Er, test_input, cus_n_iter, cus_tol ):
    print("Bayes建模方法，iter：%d，tol：%d"%(cus_n_iter, cus_tol))
    print('认知不确定参数矩阵:')
    print(test_Es_p)
    print('固有不确定参数')
    print(test_Er_p)
    print('参考输入:')
    print(test_input)
    print('参考输出矩阵:')
    print(test_Er)
    print('对比输入:')
    print(test_cmp_input)
    print('对比输出矩阵')
    print(test_cmp_Er)
    y_v = outer_level_loop(test_Es_p, test_Er_p, test_Er, test_input)  # 运行仿真系统获得输出向量，即马氏距离的向量  该输出和认知不确定参数Es_p共同构成训练数据集
    y_va = numpy.array(y_v)
    print('训练输出:')
    print(y_va)
    test_Es_pa = numpy.array(test_Es_p)
    bayes = linear_model.BayesianRidge(n_iter=cus_n_iter, tol=cus_tol).fit(test_Es_pa, y_va)
    return bayes

avg_dif = list()
max_dif = list()
min_dif = list()
cmp_dif = list()

def GA(bmodel, pn=100, itn=50, cp=0.3, mp=0.05, Es_p_n=4):
    population_num = pn  # 种群大小
    iter_num = itn  # 迭代次数
    cross_p = cp  # 交叉概率
    mut_p = mp  # 变异概率
    print '种群大小: %d' % (population_num),
    print '迭代次数: %d' % (iter_num),
    print '交叉概率: %f' % (cross_p),
    print '变异概率: %f' % (mut_p)
    Er_p = numpy.mat(numpy.random.randint(2, 7, (population_num, Es_p_n)))  # 初始种群
    for i in range(iter_num):
        print "第%d次迭代" % (i),
        pro_l = GA_1(Er_p, bmodel)
        Er_p = GA_2(pro_l, Er_p, cross_p, mut_p)

    print(avg_dif)
    print(cmp_dif)

    plt.figure(num=1, figsize=(6, 3))
    x = len(avg_dif)
    x= range(x)
    plt.plot(x, avg_dif)
    plt.plot(x, max_dif)
    plt.plot(x, min_dif)
    plt.xlabel('iter num')
    plt.ylabel('measure size')
    plt.title('average measure size trend')
    plt.figure(num=2, figsize=(6, 3))
    plt.plot(x, cmp_dif)
    plt.xlabel('iter num')
    plt.ylabel('measure size')
    plt.title('verify trend')
    plt.show()

class ShowNotebook(aui.AuiNotebook):
    
    def __init__(self, parent = None):
        
        aui.AuiNotebook.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, 
                                 wx.DefaultSize, aui.AUI_NB_DEFAULT_STYLE)

    def NewProj0(self, pProj = 0):
        self.show_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
                                   wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.AddPage(self.show_panel, u"数据库连接", True, wx.NullBitmap)
        show_panel = self.show_panel
        self.button_db = wx.Button(show_panel, label="导入数据")
        self.button_db.Bind(wx.EVT_BUTTON, self.onClick_button_db)
        self.text_ctrl_db = wx.TextCtrl(show_panel, -1, "连接id")

        box_sizer = wx.BoxSizer(orient=wx.VERTICAL)
        box_sizer_db = wx.BoxSizer(orient=wx.HORIZONTAL)
        box_sizer_db.Add(self.button_db)
        box_sizer_db.Add(self.text_ctrl_db)
        box_sizer.Add(box_sizer_db, flag=wx.EXPAND, proportion=wx.EXPAND)

        show_panel.SetSizer(box_sizer)
        self.Show(True)

        show_panel.Layout()

    def NewProj1(self, pProj = 0):
        self.show_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
                                   wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.AddPage(self.show_panel, u"参数设置", True, wx.NullBitmap)
        show_panel = self.show_panel

        self.static_text_1a = wx.StaticText(show_panel,-1,label="认知不确定参数个数：")
        self.text_ctrl_1a = wx.TextCtrl(show_panel, -1)
        self.button_t1a = wx.Button(show_panel, label='确定')
        self.button_t1a.Bind(wx.EVT_BUTTON, self.onClick_button_t1a)
        self.static_text_2a = wx.StaticText(show_panel, -1, label="认知不确定参数抽样组数：")
        self.text_ctrl_2a = wx.TextCtrl(show_panel, -1)
        self.button_t2a = wx.Button(show_panel, label='导入')
        self.button_t2a.Bind(wx.EVT_BUTTON, self.onClick_button_t2a)
        self.static_text_3a = wx.StaticText(show_panel, -1, label="固有不确定参数个数：")
        self.text_ctrl_3a = wx.TextCtrl(show_panel, -1)
        self.button_t3a = wx.Button(show_panel, label='确定')
        self.button_t3a.Bind(wx.EVT_BUTTON, self.onClick_button_t3a)
        self.static_text_4a = wx.StaticText(show_panel, -1, label="固有不确定参数抽样组数：")
        self.text_ctrl_4a = wx.TextCtrl(show_panel, -1)
        self.button_t4a = wx.Button(show_panel, label='导入')
        self.button_t4a.Bind(wx.EVT_BUTTON, self.onClick_button_t4a)
        self.static_text_input = wx.StaticText(show_panel, -1, label="模型输入类型个数：")
        self.text_ctrl_input = wx.TextCtrl(show_panel, -1)
        self.button_input = wx.Button(show_panel, label="确认")
        self.button_input.Bind(wx.EVT_BUTTON, self.onClick_button_input)
        self.static_text_5a = wx.StaticText(show_panel, -1, label="参考模型输入个数：")
        self.text_ctrl_5a = wx.TextCtrl(show_panel, -1)
        self.static_text_6a = wx.StaticText(show_panel, -1, label="对比输入个数：")
        self.text_ctrl_6a = wx.TextCtrl(show_panel, -1)
        self.button_ok_input = wx.Button(show_panel, -1, "输入确认")
        self.button_ok_input.Bind(wx.EVT_BUTTON, self.onClick_button_ok_input)

        box_sizer = wx.BoxSizer(orient=wx.VERTICAL)

        box_sizer_c1 = wx.BoxSizer(orient=wx.HORIZONTAL)
        box_sizer_c1.Add(self.static_text_1a)
        box_sizer_c1.Add(self.text_ctrl_1a)

        box_sizer.Add(box_sizer_c1)
        box_sizer.Add(self.button_t1a)

        box_sizer_c2 = wx.BoxSizer(orient=wx.HORIZONTAL)
        box_sizer_c2.Add(self.static_text_2a)
        box_sizer_c2.Add(self.text_ctrl_2a)

        box_sizer.Add(box_sizer_c2)
        box_sizer.Add(self.button_t2a)

        box_sizer_c3 = wx.BoxSizer(orient=wx.HORIZONTAL)
        box_sizer_c3.Add(self.static_text_3a)
        box_sizer_c3.Add(self.text_ctrl_3a)

        box_sizer.Add(box_sizer_c3)
        box_sizer.Add(self.button_t3a)

        box_sizer_c4 = wx.BoxSizer(orient=wx.HORIZONTAL)
        box_sizer_c4.Add(self.static_text_4a)
        box_sizer_c4.Add(self.text_ctrl_4a)

        box_sizer.Add(box_sizer_c4)
        box_sizer.Add(self.button_t4a)

        box_sizer_input = wx.BoxSizer(orient=wx.HORIZONTAL)
        box_sizer_input.Add(self.static_text_input)
        box_sizer_input.Add(self.text_ctrl_input)

        box_sizer.Add(box_sizer_input)
        box_sizer.Add(self.button_input)

        box_sizer_c5 = wx.BoxSizer(orient=wx.HORIZONTAL)
        box_sizer_c5.Add(self.static_text_5a)
        box_sizer_c5.Add(self.text_ctrl_5a)
        box_sizer.Add(box_sizer_c5)

        box_sizer_c6 = wx.BoxSizer(orient=wx.HORIZONTAL)
        box_sizer_c6.Add(self.static_text_6a)
        box_sizer_c6.Add(self.text_ctrl_6a)
        box_sizer.Add(box_sizer_c6)


        box_sizer.Add(self.button_ok_input)

        show_panel.SetSizer(box_sizer)
        self.Show(True)

        show_panel.Layout()

    def NewProj2(self, pProj = 0):
        self.show_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, 
                                   wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.AddPage(self.show_panel, u"元模型建模", True, wx.NullBitmap)
        show_panel = self.show_panel

        self.static_text_a = wx.StaticText(show_panel, -1, label="建模方法（SVR或者GPR或者Bayes）：")
        self.text_ctrl_a = wx.TextCtrl(show_panel, -1)
        self.button_a = wx.Button(show_panel, label="确定")
        box_sizer_a = wx.BoxSizer(orient=wx.HORIZONTAL)
        box_sizer_a.Add(self.static_text_a)
        box_sizer_a.Add(self.text_ctrl_a)
        box_sizer_a.Add(self.button_a)
        self.button_a.Bind(wx.EVT_BUTTON, self.onClick_button_a)

        # self.button_1a = wx.Button(show_panel, label="元模型建模")
        # self.button_1a.Bind(wx.EVT_BUTTON, self.onClick_button_1a)

        # lblList = ['SVR', 'GPR', 'Bayes']
        #
        # self.rbox = wx.RadioBox(show_panel, label='构建方法', choices=lblList,
        #                         majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        # self.rbox.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        # self.rbox.Enable(True)
        # self.rbox.SetSelection(self.rbox.GetSelection())


        box_sizer = wx.BoxSizer(orient=wx.VERTICAL)

        # box_sizer.Add(self.rbox)
        box_sizer.Add(box_sizer_a)
        # box_sizer.Add(self.button_1a)

        show_panel.SetSizer(box_sizer)
        self.Show(True)
        show_panel.Layout()

    def NewProj3(self, pProj = 0):
        self.show_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
                                   wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.AddPage(self.show_panel, u"优化设置", True, wx.NullBitmap)
        show_panel = self.show_panel

        self.static_text_1 = wx.StaticText(show_panel, -1, label="群体总数：")
        self.text_ctrl_1 = wx.TextCtrl(show_panel, -1)
        self.static_text_2 = wx.StaticText(show_panel, -1, label="交叉概率：")
        self.text_ctrl_2 = wx.TextCtrl(show_panel, -1)
        self.static_text_3 = wx.StaticText(show_panel, -1, label="变异概率：")
        self.text_ctrl_3 = wx.TextCtrl(show_panel, -1)
        self.static_text_4 = wx.StaticText(show_panel, -1, label="迭代次数：")
        self.text_ctrl_4 = wx.TextCtrl(show_panel, -1)

        self.button_1 = wx.Button(show_panel, label="点击开始校准")
        self.button_1.Bind(wx.EVT_BUTTON, self.onClick_button_1)

        box_sizer = wx.BoxSizer(orient=wx.VERTICAL)

        box_sizer_1 = wx.BoxSizer(orient=wx.HORIZONTAL)
        box_sizer_1.Add(self.static_text_1)
        box_sizer_1.Add(self.text_ctrl_1)

        box_sizer_2 = wx.BoxSizer(orient=wx.HORIZONTAL)
        box_sizer_2.Add(self.static_text_2)
        box_sizer_2.Add(self.text_ctrl_2)

        box_sizer_3 = wx.BoxSizer(orient=wx.HORIZONTAL)
        box_sizer_3.Add(self.static_text_3)
        box_sizer_3.Add(self.text_ctrl_3)

        box_sizer_4 = wx.BoxSizer(orient=wx.HORIZONTAL)
        box_sizer_4.Add(self.static_text_4)
        box_sizer_4.Add(self.text_ctrl_4)

        box_sizer.Add(box_sizer_1)
        box_sizer.Add(box_sizer_2)
        box_sizer.Add(box_sizer_3)
        box_sizer.Add(box_sizer_4)

        box_sizer.Add(self.button_1)

        show_panel.SetSizer(box_sizer)
        self.Show(True)

        show_panel.Layout()


    def onClick_button_a(self, event):
        methoda = self.text_ctrl_a.GetLineText(0)
        if methoda == "SVR":
            print ("SVR")
            self.sym = 1
            show_panel = self.show_panel
            sizer = show_panel.GetSizer()

            sizer_p1 = wx.BoxSizer(orient=wx.HORIZONTAL)
            self.static_text_p1 = wx.StaticText(show_panel, -1, label="惩罚参数（1.0）：")
            self.text_ctrl_p1 = wx.TextCtrl(show_panel, -1)
            sizer_p1.Add(self.static_text_p1)
            sizer_p1.Add(self.text_ctrl_p1)

            sizer_p2 = wx.BoxSizer(orient=wx.HORIZONTAL)
            self.static_text_p2 = wx.StaticText(show_panel, -1, label="小量（0.1）：")
            self.text_ctrl_p2 = wx.TextCtrl(show_panel, -1)
            sizer_p2.Add(self.static_text_p2)
            sizer_p2.Add(self.text_ctrl_p2)

            sizer_p3 = wx.BoxSizer(orient=wx.HORIZONTAL)
            self.static_text_p3 = wx.StaticText(show_panel, -1, label="内核方法（linear或者poly或者rbf或者sigmoid）：")
            self.text_ctrl_p3 = wx.TextCtrl(show_panel, -1)
            sizer_p3.Add(self.static_text_p3)
            sizer_p3.Add(self.text_ctrl_p3)

            sizer.Add(sizer_p1)
            sizer.Add(sizer_p2)
            sizer.Add(sizer_p3)

            self.button_1a = wx.Button(show_panel, label="元模型建模")
            self.button_1a.Bind(wx.EVT_BUTTON, self.onClick_button_1a)

            sizer.Add(self.button_1a)

            show_panel.Layout()
        elif methoda == "GPR":
            print ("GPR")
            self.sym = 2

            show_panel = self.show_panel
            sizer = show_panel.GetSizer()

            sizer_p1 = wx.BoxSizer(orient=wx.HORIZONTAL)
            self.static_text_p1 = wx.StaticText(show_panel, -1, label="alpha（1e-10）：")
            self.text_ctrl_p1 = wx.TextCtrl(show_panel, -1)
            sizer_p1.Add(self.static_text_p1)
            sizer_p1.Add(self.text_ctrl_p1)

            sizer.Add(sizer_p1)

            self.button_1a = wx.Button(show_panel, label="元模型建模")
            self.button_1a.Bind(wx.EVT_BUTTON, self.onClick_button_1a)

            sizer.Add(self.button_1a)

            show_panel.Layout()
        else:
            print ("Bayes")
            self.sym = 3

            show_panel = self.show_panel
            sizer = show_panel.GetSizer()

            sizer_p1 = wx.BoxSizer(orient=wx.HORIZONTAL)
            self.static_text_p1 = wx.StaticText(show_panel, -1, label="n_iter（300）：")
            self.text_ctrl_p1 = wx.TextCtrl(show_panel, -1)
            sizer_p1.Add(self.static_text_p1)
            sizer_p1.Add(self.text_ctrl_p1)

            sizer_p2 = wx.BoxSizer(orient=wx.HORIZONTAL)
            self.static_text_p2 = wx.StaticText(show_panel, -1, label="tol（0.001）：")
            self.text_ctrl_p2 = wx.TextCtrl(show_panel, -1)
            sizer_p2.Add(self.static_text_p2)
            sizer_p2.Add(self.text_ctrl_p2)

            sizer.Add(sizer_p1)
            sizer.Add(sizer_p2)

            self.button_1a = wx.Button(show_panel, label="元模型建模")
            self.button_1a.Bind(wx.EVT_BUTTON, self.onClick_button_1a)

            sizer.Add(self.button_1a)
            show_panel.Layout()



    # def onRadioBox(self, event):
    #     choice = self.rbox.GetStringSelection()
    #     if choice == 'SVR':
    #         print ('SVR')
    #         show_panel = self.show_panel
    #         sizer = show_panel.GetSizer()
    #         sizer_1 = wx.BoxSizer(orient=wx.HORIZONTAL)
    #         self.static_text_1 = wx.StaticText(show_panel, -1, label="惩罚参数：")
    #         self.text_ctrl_1 = wx.TextCtrl(show_panel, -1)
    #         sizer_1.Add(self.static_text_1)
    #         sizer_1.Add(self.text_ctrl_1)
    #         sizer.Add(sizer_1)
    #         show_panel.Layout()
    #     elif choice == 'GPR':
    #         print ('GPR')
    #     else:
    #         print ('Bayes')

    def onClick_button_db(self, event):
        db_config = {
            'host': '118.89.198.205',
            'user': 'certainty',
            'password': 'Nuaa666',
            'port': 3306,
            'database': 'work',
            'charset': 'utf8'
        }

        # db_config = {
        #     'user': 'test_user1',
        #     'password': '1234',
        #     'database': 'test1',
        #     'charset': 'utf8'
        # }

        try:
            self.conn = mysql.connector.connect(**db_config)
            self.text_ctrl_db.SetLabelText(str(self.conn.connection_id))
        except Error as e:
            print(e)
        finally:
            print '导入数据'

    def onClick_button_1a(self, event):
        # cursor = self.conn.cursor()
        # sql_create_table = 'create table test_table2 (' \
        #                    'size int,' \
        #                    'distribution varchar(20))'
        # cursor.execute(sql_create_table)
        # self.conn.commit()
        self.Es_p_n = int(self.text_ctrl_1a.GetLineText(0))
        self.Es_p_gn = int(self.text_ctrl_2a.GetLineText(0))
        self.Er_p_n = int(self.text_ctrl_3a.GetLineText(0))
        self.Er_p_gn = int(self.text_ctrl_4a.GetLineText(0))
        self.c_data_n = int(self.text_ctrl_5a.GetLineText(0))
        self.cmp_data_n = int(self.text_ctrl_6a.GetLineText(0))


        initData(self.Es_p_gn, self.Es_p_n, self.Er_p_gn, self.Er_p_n, self.c_data_n, self.cmp_data_n)
        if self.sym == 1:
            cus_C = float(self.text_ctrl_p1.GetLineText(0))
            cus_epsilon = float(self.text_ctrl_p2.GetLineText(0))
            cus_kernel = self.text_ctrl_p3.GetLineText(0)
            self.svr = buildSVR1(test_Es_p, test_Er_p, test_Er, test_input, cus_C, cus_epsilon, cus_kernel)
        elif self.sym == 2:
            cus_alpha = float(self.text_ctrl_p1.GetLineText(0))
            self.gpr = buildSVR2(test_Es_p, test_Er_p, test_Er, test_input, cus_alpha)
        else:
            cus_n_iter = int(self.text_ctrl_p1.GetLineText(0))
            cus_tol = float(self.text_ctrl_p2.GetLineText(0))
            self.bayes = buildSVR3(test_Es_p, test_Er_p, test_Er, test_input, cus_n_iter, cus_tol)

    def onClick_button_1(self, event):
        # print(self.text_ctrl_1.GetLineText(0))
        pn = int(self.text_ctrl_1.GetLineText(0))
        itn = int(self.text_ctrl_4.GetLineText(0))
        cp = float(self.text_ctrl_2.GetLineText(0))
        mp = float(self.text_ctrl_3.GetLineText(0))
        if self.sym == 1:
            GA(self.svr, pn, itn, cp, mp, self.Es_p_n)
        elif self.sym == 2:
            GA(self.gpr, pn, itn, cp, mp, self.Es_p_n)
        else:
            GA(self.bayes, pn, itn, cp, mp, self.Es_p_n)


    def onClick_button_t1a(self, event):
        p_n1 = int(self.text_ctrl_1a.GetLineText(0))
        self.p1_l = list()
        i = 1
        while i <= p_n1:
            dlg = wx.TextEntryDialog(None, "请输入第%d个认知不确定参数的分布特征" % (i))
            if dlg.ShowModal() == wx.ID_OK:
                response = dlg.GetValue()
                self.p1_l.append(response)
            i = i + 1
        print '认知不确定分布特征输入成功'

    def onClick_button_t2a(self, event):
        pg_n1 = int(self.text_ctrl_2a.GetLineText(0))
        self.pl_2 = list()
        l1 = len(self.p1_l)
        i = 0
        while i < l1:
            self.pl_2.append(pg_n1)
            i = i+1
        self.zip_1 = zip(self.pl_2, self.p1_l)
        try:
            cursor = self.conn.cursor()
            sql_create_table = 'create table test_table1 (' \
                               'size int,' \
                               'distribution varchar(20))'
            cursor.execute(sql_create_table)
        except Error as e:
            print(e)
        finally:
            print '导入数据'
        i = 0
        sql_deleteall = 'truncate table test_table1'
        cursor.execute(sql_deleteall)
        while i < l1:
            sql_insert = 'insert into test_table1 values (%s, %s)'
            data = self.zip_1[i]
            cursor.execute(sql_insert, data)
            i = i+1
        self.conn.commit()
        cursor.close()
        print '认知不确定个数导入成功'
    def onClick_button_t3a(self, event):
        p_n2 = int(self.text_ctrl_3a.GetLineText(0))
        self.p3_l = list()
        i = 1
        while i <= p_n2:
            dlg = wx.TextEntryDialog(None, "请输入第%d个固有不确定参数的分布特征" % (i))
            if dlg.ShowModal() == wx.ID_OK:
                response = dlg.GetValue()
                self.p3_l.append(response)
            i = i + 1
        print '固有不确定分布特征输入成功'

    def onClick_button_t4a(self, event):
        pg_n2 = int(self.text_ctrl_4a.GetLineText(0))
        self.p4_l = list()
        l3 = len(self.p3_l)
        i = 0
        while i < l3:
            self.p4_l.append(pg_n2)
            i = i + 1
        self.zip_2 = zip(self.p4_l, self.p3_l)
        try:
            cursor = self.conn.cursor()
            sql_create_table = 'create table test_table2 (' \
                               'size int,' \
                               'distribution varchar(20))'
            cursor.execute(sql_create_table)
        except Error as e:
            print(e)
        finally:
            print '导入数据'
        i = 0
        sql_deleteall = 'truncate table test_table2'
        cursor.execute(sql_deleteall)
        while i < l3:
            sql_insert = 'insert into test_table2 values (%s, %s)'
            data = self.zip_2[i]
            cursor.execute(sql_insert, data)
            i = i + 1
        print '固有不确定参数个数导入成功'
        self.conn.commit()
        cursor.close()

    def onClick_button_input(self, event):
        self.input_n = int(self.text_ctrl_input.GetLineText(0))
        self.pl_input = list()
        i = 0
        while i < self.input_n:
            dlg = wx.TextEntryDialog(None, "请输入第%d个输入的取值范围" % (i+1))
            if dlg.ShowModal() == wx.ID_OK:
                response = dlg.GetValue()
                self.pl_input.append(response)
            i = i + 1
        print '输入范围输入成功'

    def onClick_button_ok_input(self, event):
        input_n1 = int(self.text_ctrl_5a.GetLineText(0))
        input_n2 = int(self.text_ctrl_6a.GetLineText(0))
        input_l1 = list()
        i = 0
        while i < self.input_n:
            input_l1.append(input_n1+input_n2)
            i = i+1

        zip_a = zip(input_l1, self.pl_input)
        try:
            sql_create_table = 'create table test_table3 (' \
                               'size int,' \
                               'distribution varchar(20))'
            cursor = self.conn.cursor()
            cursor.execute(sql_create_table)
        except Error as e:
            print(e)
        finally:
            print '导入数据'

        i = 0
        sql_deleteall = 'truncate table test_table3'
        cursor.execute(sql_deleteall)
        while i < self.input_n:
            data = zip_a[i]
            sql_insert = 'insert into test_table3 values(%s, %s)'
            cursor.execute(sql_insert, data)
            i = i+1
        print '输入的个数导入成功'
        self.conn.commit()
        cursor.close()

    #点击导入模型事件
    # def ClickImport(self, event):
    #     show_panel = self.GetCurrentPage()
    #     proj_name = show_panel.textCtrl1.GetValue()
    #     if proj_name == '':
    #         return
    #     proj_descr = show_panel.textCtrl2.GetValue()
    #     record = Sql.selectSql((proj_name, show_panel.pid), Sql.selectProj)
    #     if record != []:
    #         show_panel.staticText3.Show(show=True)
    #         show_panel.Layout()
    #         return
    #     show_panel.staticText3.Show(show=False)
    #     dlg = wx.DirDialog(self,u"选择文件夹",style=wx.DD_DEFAULT_STYLE)
    #     if dlg.ShowModal() == wx.ID_OK:
    #         proj = Import_file.insert_blob(proj_name, show_panel.pid,
    #                                        proj_descr, dlg.GetPath())
    #         show_panel.textCtrl1.Disable() #导入成功后控件变为不可编辑
    #         show_panel.textCtrl2.Disable()
    #         show_panel.button1.Disable()
    #         self.GetParent().GetParent().navTree.updateTree()
    #         self.genInParams(proj, show_panel)
    #     dlg.Destroy()
    #
    # #导入成功后生成输入参数控件
    # def genInParams(self, proj, show_panel):
    #     Run.read_blob(proj)
    #     params = Run.read_param(proj)
    #     scrollPanel = show_panel.scrolledWindow
    #     show_panel.staticText4 = wx.StaticText(scrollPanel, wx.ID_ANY,
    #                             u"模型输入参数共" + str(len(params)) + u"个：",
    #                             wx.DefaultPosition, wx.DefaultSize, 0)
    #     show_panel.gbSizer.Add(show_panel.staticText4, wx.GBPosition(7, 4),
    #                            wx.GBSpan(1, 2), wx.ALL, 5)
    #     show_panel.staticText5 = wx.StaticText(scrollPanel, wx.ID_ANY,
    #                             u"参数描述", wx.DefaultPosition, wx.DefaultSize, 0)
    #     show_panel.gbSizer.Add(show_panel.staticText5, wx.GBPosition(7, 4),
    #                            wx.GBSpan(1, 2), wx.ALL, 5)
    #     show_panel.Layout()
