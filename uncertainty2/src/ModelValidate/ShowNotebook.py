# -*- coding: utf-8 -*-
from __future__ import division

import thread

import time
import wx
import wx.grid
import wx.lib.scrolledpanel as scrolled
import wx.lib.newevent
from matplotlib.figure import Figure
#from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import zhi as zi
import pandas as pd
from wx import aui
from wx import grid
import Sql
import config
import ValidateDoubleLoop
import mysql.connector
import run as ru
from mysql.connector import Error
import numpy as np
import matplotlib.pyplot as plt
import ValidateRealModel as rm
import ValidateBuildMetaModel as  build_meta
import ValidateUi as cp
from CustomedScrolledWindow import CustomedScrolledWindow as csw
import wx.grid
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
class ShowNotebook(aui.AuiNotebook):
    signal = False
    def __init__(self, parent=None):

        aui.AuiNotebook.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                                 wx.DefaultSize, aui.AUI_NB_DEFAULT_STYLE)




        # db_config = {
        #     'user': 'test_user1',
        #     'password': '1234',


    def NewProj2(self, pProj=0):
        box_sizer = wx.BoxSizer(wx.VERTICAL)


        self.show_panel = scrolled.ScrolledPanel(self, -1,
                                                 style=wx.TAB_TRAVERSAL | wx.SUNKEN_BORDER, name="panel1")
        self.show_panel.SetAutoLayout(1)
        self.show_panel.SetupScrolling()

        self.AddPage(self.show_panel, u"选择仿真验证模型", True, wx.NullBitmap)
        show_panel = self.show_panel

        self.static_text_1 = wx.StaticText(show_panel, -1, label="一维静态数据验证:")
        #self.button_t1a = wx.Button(show_panel, -1, label='一维静态数据验证')
        box_sizer.Add(self.static_text_1)

       # box_sizer.Add(self.button_t1a)

        self.button_t11a = wx.Button(show_panel, -1,label='欧式距离验证',pos=(100,0))
        self.button_t11a.Bind(wx.EVT_BUTTON, self.onClick_button_t1a)
        box_sizer.Add(self.button_t11a)

        self.static_text_2 = wx.StaticText(show_panel, -1, label="多维静态数据验证:",pos=(0,25))
        box_sizer.Add(self.static_text_2)


        self.button_t2a = wx.Button(show_panel, -1,label='曼哈顿距离验证',pos=(100,25))
        self.button_t2a.Bind(wx.EVT_BUTTON, self.onClick_button_t2a)
        box_sizer.Add(self.button_t2a)

        self.button_t3a = wx.Button(show_panel, -1,label='马氏距离验证')
        self.button_t3a.Bind(wx.EVT_BUTTON, self.onClick_button_t3a)
        box_sizer.Add(self.button_t3a)

        self.button_t4a = wx.Button(show_panel,-1, label='切比雪夫距离验证')
        self.button_t4a.Bind(wx.EVT_BUTTON, self.onClick_button_t4a)
        box_sizer.Add(self.button_t4a)

        self.static_text_3 = wx.StaticText(show_panel, -1, label="动态仿真数据验证:",pos=(0,50))
        box_sizer.Add(self.static_text_3)

        self.button_t5a = wx.Button(show_panel, -1,label='KL散度验证',pos=(100,50))
        self.button_t5a.Bind(wx.EVT_BUTTON, self.onClick_button_t5a)
        box_sizer.Add(self.button_t5a)
        show_panel.SetSizer(box_sizer)
        self.Show(True)
        show_panel.Layout()


    def ImportDataPanel(self, pProj = 0):  #数据导入
        self.show_panel = scrolled.ScrolledPanel(self, -1,
                                                 style=wx.TAB_TRAVERSAL | wx.SUNKEN_BORDER, name="panel1")
        self.show_panel.SetAutoLayout(1)
        self.show_panel.SetupScrolling()

        self.AddPage(self.show_panel, u"数据导入", True, wx.NullBitmap)
        show_panel = self.show_panel

        self.button_import = wx.Button(show_panel, label="ImportData")
        self.button_import.Bind(wx.EVT_BUTTON, self.Auto_Click)
        self.button_import.Show(False)

        box_sizer = wx.BoxSizer(orient=wx.VERTICAL)
        box_sizer.Add(self.button_import)
        # box_sizer.Add(self.grid)
        show_panel.SetSizer(box_sizer)

        self.Show(True)
        show_panel.Layout()
        self.signal = True


    def onClick_button_t1a(self, event):
       self.button_t11a.Disable()
       show_panel = self.show_panel
       sizer1 = show_panel.GetSizer()

       sizer_a = wx.BoxSizer(orient=wx.VERTICAL)
       static_text = wx.StaticText(show_panel, label='欧式距离度量因子')
       static_text1 = wx.StaticText(show_panel, label='   ')
       self.grid_out = wx.grid.Grid(show_panel)
       #self.sw = csw(show_panel)

       sizer_a.Add(static_text)
       sizer_a.Add(self.grid_out)
       sizer_a.Add(static_text1)



       sizer_b = wx.BoxSizer(orient=wx.VERTICAL)
       self.figure = Figure()
       self.axes = self.figure.add_subplot(111)
       # self.axes.set(xlabel='Number of iterations', ylabel='Consistency measure', title='Iterative metric trends')
       self.canvas = FigureCanvas(show_panel, -1, self.figure)

       self.figure2 = Figure()
       self.axes2 = self.figure2.add_subplot(111)
       # self.axes2.set(xlabel='Number of iterations', ylabel='Consistency measure', title='Compare verification trends')
       self.canvas2 = FigureCanvas(show_panel, -1, self.figure2)

       sizer_b.Add(self.canvas)
       sizer_b.Add(self.canvas2)


       sizer_c = wx.BoxSizer(orient=wx.VERTICAL)
       sizer_c.Add(sizer_a)
       sizer_c.Add(sizer_b)

       sizer1.Add(sizer_c)
       show_panel.Layout()
       build_meta.buildoushidistance(self,build_meta.cog_p, build_meta.inh_p, build_meta.output1,
                                      build_meta.input_v1)  # , cus_C, cus_epsilon, cus_kernel)






    def onClick_button_t2a(self, event):
        self.button_t2a.Disable()
        show_panel = self.show_panel
        sizer1 = show_panel.GetSizer()

        sizer_a = wx.BoxSizer(orient=wx.VERTICAL)
        static_text = wx.StaticText(show_panel, label='曼哈顿距离度量因子')
        static_text1 = wx.StaticText(show_panel, label='   ')
        self.grid_out = wx.grid.Grid(show_panel)
        # self.sw = csw(show_panel)

        sizer_a.Add(static_text)
        sizer_a.Add(self.grid_out)
        sizer_a.Add(static_text1)

        sizer_b = wx.BoxSizer(orient=wx.VERTICAL)
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        # self.axes.set(xlabel='Number of iterations', ylabel='Consistency measure', title='Iterative metric trends')
        self.canvas = FigureCanvas(show_panel, -1, self.figure)

        self.figure2 = Figure()
        self.axes2 = self.figure2.add_subplot(111)
        # self.axes2.set(xlabel='Number of iterations', ylabel='Consistency measure', title='Compare verification trends')
        self.canvas2 = FigureCanvas(show_panel, -1, self.figure2)

        sizer_b.Add(self.canvas)
        sizer_b.Add(self.canvas2)

        sizer_c = wx.BoxSizer(orient=wx.VERTICAL)
        sizer_c.Add(sizer_a)
        sizer_c.Add(sizer_b)

        sizer1.Add(sizer_c)
        show_panel.Layout()
        build_meta.buildmanhadundistance(self,build_meta.cog_p, build_meta.inh_p, build_meta.output1,
                                      build_meta.input_v1)

    def onClick_button_t3a(self, event):
        self.button_t3a.Disable()
        show_panel = self.show_panel
        sizer1 = show_panel.GetSizer()

        sizer_a = wx.BoxSizer(orient=wx.VERTICAL)
        static_text = wx.StaticText(show_panel, label='马氏距离度量因子')
        static_text1 = wx.StaticText(show_panel, label='   ')
        self.grid_out = wx.grid.Grid(show_panel)
        # self.sw = csw(show_panel)

        sizer_a.Add(static_text)
        sizer_a.Add(self.grid_out)
        sizer_a.Add(static_text1)

        sizer_b = wx.BoxSizer(orient=wx.VERTICAL)
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        # self.axes.set(xlabel='Number of iterations', ylabel='Consistency measure', title='Iterative metric trends')
        self.canvas = FigureCanvas(show_panel, -1, self.figure)

        self.figure2 = Figure()
        self.axes2 = self.figure2.add_subplot(111)
        # self.axes2.set(xlabel='Number of iterations', ylabel='Consistency measure', title='Compare verification trends')
        self.canvas2 = FigureCanvas(show_panel, -1, self.figure2)

        sizer_b.Add(self.canvas)
        sizer_b.Add(self.canvas2)

        sizer_c = wx.BoxSizer(orient=wx.VERTICAL)
        sizer_c.Add(sizer_a)
        sizer_c.Add(sizer_b)

        sizer1.Add(sizer_c)
        show_panel.Layout()
        build_meta.buildmshidistance(self,build_meta.cog_p, build_meta.inh_p, build_meta.output1,
                                      build_meta.input_v1)

    def onClick_button_t4a(self, event):
        self.button_t4a.Disable()
        show_panel = self.show_panel
        sizer1 = show_panel.GetSizer()

        sizer_a = wx.BoxSizer(orient=wx.VERTICAL)
        static_text = wx.StaticText(show_panel, label='切比雪夫距离度量因子')
        static_text1 = wx.StaticText(show_panel, label='   ')
        self.grid_out = wx.grid.Grid(show_panel)
        # self.sw = csw(show_panel)

        sizer_a.Add(static_text)
        sizer_a.Add(self.grid_out)
        sizer_a.Add(static_text1)

        sizer_b = wx.BoxSizer(orient=wx.VERTICAL)
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        # self.axes.set(xlabel='Number of iterations', ylabel='Consistency measure', title='Iterative metric trends')
        self.canvas = FigureCanvas(show_panel, -1, self.figure)

        self.figure2 = Figure()
        self.axes2 = self.figure2.add_subplot(111)
        # self.axes2.set(xlabel='Number of iterations', ylabel='Consistency measure', title='Compare verification trends')
        self.canvas2 = FigureCanvas(show_panel, -1, self.figure2)

        sizer_b.Add(self.canvas)
        sizer_b.Add(self.canvas2)

        sizer_c = wx.BoxSizer(orient=wx.VERTICAL)
        sizer_c.Add(sizer_a)
        sizer_c.Add(sizer_b)

        sizer1.Add(sizer_c)
        #show_panel.Layout()
        build_meta.buildqiebixuefudistance(self,build_meta.cog_p, build_meta.inh_p, build_meta.output1,
                                      build_meta.input_v1)

    def onClick_button_t5a(self, event):
        self.button_t5a.Disable()
        show_panel = self.show_panel
        sizer1 = show_panel.GetSizer()

        sizer_a = wx.BoxSizer(orient=wx.VERTICAL)
        static_text = wx.StaticText(show_panel, label='相对熵度量因子')
        static_text1 = wx.StaticText(show_panel, label='   ')
        self.grid_out = wx.grid.Grid(show_panel)
        # self.sw = csw(show_panel)

        sizer_a.Add(static_text)
        sizer_a.Add(self.grid_out)
        sizer_a.Add(static_text1)

        #sizer_b = wx.BoxSizer(orient=wx.VERTICAL)
        #self.figure = Figure()
       # self.axes = self.figure.add_subplot(111)
        # self.axes.set(xlabel='Number of iterations', ylabel='Consistency measure', title='Iterative metric trends')
        #self.canvas = FigureCanvas(show_panel, -1, self.figure)

        #self.figure2 = Figure()
       # self.axes2 = self.figure2.add_subplot(111)
        # self.axes2.set(xlabel='Number of iterations', ylabel='Consistency measure', title='Compare verification trends')
        #self.canvas2 = FigureCanvas(show_panel, -1, self.figure2)

        #sizer_b.Add(self.canvas)
        #sizer_b.Add(self.canvas2)

        sizer_c = wx.BoxSizer(orient=wx.VERTICAL)
        sizer_c.Add(sizer_a)
       # sizer_c.Add(sizer_b)

        sizer1.Add(sizer_c)
        show_panel.Layout()

        build_meta.buildKLdistance(self,build_meta.cog_p, build_meta.inh_p, build_meta.output1,
                                           build_meta.input_v1)












    def onClick_button_import(self, event):
        print("INTO click!")
        show_panel = self.show_panel
        sizer = show_panel.GetSizer()

        sizer_A = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.grid1 = wx.grid.Grid(show_panel)
        sizer_v1 = wx.BoxSizer(orient=wx.VERTICAL)
        static_text_v1 = wx.StaticText(show_panel, label='认知不确定参数抽样取值结果')
        sizer_v1.Add(static_text_v1)
        sizer_v1.Add(self.grid1)
        sizer_A.Add(sizer_v1)

        sizer_B = wx.BoxSizer(orient=wx.VERTICAL)
        self.grid2 = wx.grid.Grid(show_panel)
        sizer_v2 = wx.BoxSizer(orient=wx.VERTICAL)
        static_text_v2 = wx.StaticText(show_panel, label='固有不确定参数抽样取值结果')
        sizer_v2.Add(static_text_v2)
        sizer_v2.Add(self.grid2)
        sizer_B.Add(sizer_v2)

        sizer_a = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.grid3 = wx.grid.Grid(show_panel)
        sizer_v3 = wx.BoxSizer(orient=wx.VERTICAL)
        static_text_v3 = wx.StaticText(show_panel, label='计算一致性输入抽样取值结果')
        sizer_v3.Add(static_text_v3)
        sizer_v3.Add(self.grid3)
        sizer_a.Add(sizer_v3)

        self.grid5 = wx.grid.Grid(show_panel)
        sizer_v5 = wx.BoxSizer(orient=wx.VERTICAL)
        static_text_v5 = wx.StaticText(show_panel, label='计算一致性输出结果')
        sizer_v5.Add(static_text_v5)
        sizer_v5.Add(self.grid5)
        sizer_a.Add(sizer_v5)

        sizer_B.Add(sizer_a)

        sizer_b = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.grid4 = wx.grid.Grid(show_panel)
        sizer_v4 = wx.BoxSizer(orient=wx.VERTICAL)
        static_text_v4 = wx.StaticText(show_panel, label='对比验证输入抽样取值结果')
        sizer_v4.Add(static_text_v4)
        sizer_v4.Add(self.grid4)
        sizer_b.Add(sizer_v4)

        self.grid6 = wx.grid.Grid(show_panel)
        sizer_v6 = wx.BoxSizer(orient=wx.VERTICAL)
        static_text_v6 = wx.StaticText(show_panel, label='对比验证输出结果')
        sizer_v6.Add(static_text_v6)
        sizer_v6.Add(self.grid6)
        sizer_b.Add(sizer_v6)

        sizer_B.Add(sizer_b)

        sizer_A.Add(sizer_B)

        sizer.Add(sizer_A)
        # self.grid = wx.grid.Grid(show_panel)
        # self.grid.CreateGrid(100, 100)
        # sizer.Add(self.grid)

        show_panel.Layout()

        build_meta.importData(self, cp.n_id)

    def Thread_to_run_click(self):
        # 创建用于导入数据的 事件 用来代替展示结果按键绑定的事件 使之能自动发起该事件 而不用 点击按键
        while (self.signal == False):
            time.sleep(0.7)
            print("waiting!")
        ImportDataEvent, EVT_IMPORT_DATA = wx.lib.newevent.NewEvent()
        m_import = wx.Control()
        wx.PostEvent(m_import, ImportDataEvent())
        m_import.Bind(EVT_IMPORT_DATA, self.onClick_button_import)
        print("here>")

    def Auto_Click(self):
        try:
            thread.start_new_thread(self.Thread_to_run_click, ())
        except:
            print("Error: unable to start thread")


