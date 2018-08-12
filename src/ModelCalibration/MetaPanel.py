# -*- coding: utf-8 -*-

###########################################################################
# Created on 2018.5.10
###########################################################################
from __future__ import print_function
from __future__ import print_function
import thread

import time

import sys
import wx
import wx.xrc
import wx.lib.newevent
from wx import grid
from wx.lib.mixins.listctrl import TextEditMixin

import ProcessBar as pb

from ShowNotebook import *
import Sql

sym1=1
class MetaPanel(wx.Panel):
    count = 0
    def __init__(self, parent,sym = 1):
        """ 初始化 """
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                          wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.sym = sym
        print(sym)
        # self 的布局，有 scrollPanel 和input_panel两个元素
        self.bSizer = wx.BoxSizer(wx.VERTICAL)

        # 为实现滚动条加入 scrollPanel
        # self.scrolledWindow = wx.ScrolledWindow(self, wx.ID_ANY,
        #                                               wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL | wx.VSCROLL)
        # self.scrolledWindow.SetScrollRate(5, 5)

        self.scrolledWindow = scrolled.ScrolledPanel(self, -1,
                                                 style=wx.TAB_TRAVERSAL | wx.SUNKEN_BORDER, name="panel1")
        self.scrolledWindow.SetAutoLayout(1)
        self.scrolledWindow.SetupScrolling()

        scrollPanel = self.scrolledWindow
        # input_panel 的布局，元素为显示的控件
        self.gbSizer = wx.GridBagSizer(5, 5)
        self.gbSizer.SetFlexibleDirection(wx.BOTH)
        self.gbSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)



        # scrollPanel 的布局，元素为显示的控件
        self.gbSizer_show = wx.GridBagSizer(5, 5)
        self.gbSizer_show.SetFlexibleDirection(wx.BOTH)
        self.gbSizer_show.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        # 上部input_Panel
        self.input_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
                                       (-1, 80), wx.TAB_TRAVERSAL)
        self.input_panel.SetMaxSize(wx.Size(-1,80))

        first_positon = 0
        next_positon = 1 + first_positon

        self.m_staticText_a = wx.StaticText(self.input_panel, wx.ID_ANY, u"度量方法：",
                                               wx.DefaultPosition, wx.DefaultSize, 0)
        self.gbSizer.Add(self.m_staticText_a, wx.GBPosition(first_positon, 4),
                               wx.GBSpan(1, 1), wx.ALL, 5)
        self.measure = ['欧式距离', '马氏距离']
        self.combobox_a = wx.ComboBox(self.input_panel, -1, size = wx.Size(280, -1), choices=self.measure)
        self.combobox_a.SetSelection(0)
        self.combobox_a.Bind(wx.EVT_COMBOBOX, self.onSelect_combobox_a)
        self.gbSizer.Add(self.combobox_a, wx.GBPosition(first_positon, 5),
                               wx.GBSpan(1, 3), wx.ALL, 5)

        self.m_staticText_b = wx.StaticText(self.input_panel, wx.ID_ANY, u"建模方法：",
                                               wx.DefaultPosition, wx.DefaultSize, 0)
        self.gbSizer.Add(self.m_staticText_b, wx.GBPosition(first_positon, 11),
                         wx.GBSpan(1, 1), wx.ALL, 5)

        self.methods = ['SVR', 'GPR', 'KRR']
        self.combobox_b = wx.ComboBox(self.input_panel, -1, size=wx.Size(280, -1), choices=self.methods)
        self.combobox_b.SetSelection(0)
        self.combobox_b.Bind(wx.EVT_COMBOBOX, self.onSelect_combobox_b)
        self.gbSizer.Add(self.combobox_b, wx.GBPosition(first_positon, 12),
                         wx.GBSpan(1, 3), wx.ALL, 5)

        ''' 元模型建模按钮的panel begins '''
        self.m_button_ok = wx.Button(self.input_panel, wx.ID_ANY, u"建模", wx.DefaultPosition, wx.Size(80, -1), 0)
        self.m_button_ok.SetBitmap(wx.Bitmap('icon/run.ico'))
        self.m_button_ok.Bind(wx.EVT_BUTTON, self.onClick_button_1a)
        self.gbSizer.Add(self.m_button_ok, wx.GBPosition(next_positon, 14),
                         wx.GBSpan(1, 1), wx.ALL, 5)

        # self.m_button_reset = wx.Button(self.input_panel, wx.ID_ANY, u"重置", wx.DefaultPosition, wx.Size(80, -1), 0)
        # self.m_button_reset.Bind(wx.EVT_BUTTON, self.reset_settings)
        # self.gbSizer.Add(self.m_button_reset, wx.GBPosition(next_positon, 13),
        #                  wx.GBSpan(1, 1), wx.ALL, 5)

        # self.m_button_show = wx.Button(self.input_panel, wx.ID_ANY, u"展示结果", wx.DefaultPosition, wx.Size(80, -1), 0)
        # self.m_button_show.Bind(wx.EVT_BUTTON, self.show_result)
        # self.m_button_show.Show(False)
        # self.gbSizer.Add(self.m_button_show, wx.GBPosition(next_positon, 15),
        #                  wx.GBSpan(1, 1), wx.ALL, 5)
        ''' 元模型建模按钮的panel ends '''

        # 分割线
        self.staticline = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition,
                                              wx.DefaultSize, wx.LI_HORIZONTAL)
        # 提示信息
        self.m_staticText_set = wx.StaticText(self, wx.ID_ANY, u"方法设置：",
                                                     wx.DefaultPosition, wx.DefaultSize, 0)

        self.m_staticText_set.SetMaxSize(wx.Size(-1, 18))

        self.m_staticText_show = wx.StaticText(self, wx.ID_ANY, u"",
                                          wx.DefaultPosition, wx.DefaultSize, 0)

        self.m_staticText_show.SetMaxSize(wx.Size(-1, 20))


        # show_panel布局设置
        self.input_panel.SetSizer(self.gbSizer)
        scrollPanel.SetSizer(self.gbSizer_show)
        scrollPanel.Layout()
        # ADD
        self.bSizer.Add(self.m_staticText_set, 1, wx.EXPAND |wx.ALL, 2)
        self.bSizer.Add(self.input_panel, 1, wx.EXPAND | wx.ALL, 5)
        self.bSizer.Add(self.staticline, 0, wx.EXPAND | wx.ALL, 5)
        #self.bSizer.Add(self.m_staticText_show, 0, wx.EXPAND |wx.ALL, 2)
        self.bSizer.Add(scrollPanel, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(self.bSizer)

        self.Layout()
        self.Centre(wx.BOTH)

    def __del__(self):
        pass

    def onSelect_combobox_a(self, event):
        pos = self.combobox_a.GetSelection()
        measure_name = self.measure[pos]
        global sym1
        if measure_name == "欧式距离":
            print ("欧式距离")
            sym1 = 1
        else:
            print ("马氏距离")
            sym1 = 2

    def onSelect_combobox_b(self, event):
        pos = self.combobox_b.GetSelection()
        method_name = self.methods[pos]
        if method_name == "SVR":
            print ("SVR")
            self.sym = 1
        elif method_name == "GPR":
            print ("GPR")
            self.sym = 2
        else:
            print ("KRR")
            self.sym = 3

    def getSym(self):
        return self.sym

    def onClick_button_1a(self, event):
        self.combobox_a.Disable()
        self.combobox_b.Disable()
       # self.button_1a.Disable()
        global sym1
       # print 'self.sym: '%(self.sym)
       # print 'sym1: %d'%(sym1)
        show_panel = self.scrolledWindow
        sizer = show_panel.GetSizer()

        #sizer_1 = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.static_text = wx.StaticText(show_panel, label='一致性度量输出')
        self.static_text1 = wx.StaticText(show_panel, label='   ')
        self.grid_out = wx.grid.Grid(show_panel)
        self.grid_out.SetMinSize((1092,70))
        self.grid_out.SetMaxSize((1092,70))
        self.grid_out.SetLabelBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        #self.sw = csw(show_panel)

        sizer.Add(self.static_text, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL, 5)
        sizer.Add(self.grid_out, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.axes.set(xlabel='Sample Numbers', ylabel='Consistency measure', title='Forecast accuracy map')
        self.canvas = FigureCanvas(show_panel, -1,self.figure)
        self.canvas.SetMinSize((1092,444))
        self.canvas.SetMaxSize((1092, 444))

        sizer.Add(self.canvas, wx.GBPosition(2, 0), wx.GBSpan(1, 1), wx.ALL, 5)
        #sizer.Add(self.sw, flag=wx.EXPAND, proportion=wx.EXPAND)

        if self.sym == 1:
            self.svr = BuildMetaModel.buildSVR(self, BuildMetaModel.cog_p, BuildMetaModel.inh_p, BuildMetaModel.output1, BuildMetaModel.input_v1)#, cus_C, cus_epsilon, cus_kernel)
        elif self.sym == 2:
            self.gpr = BuildMetaModel.buildGPR(self, BuildMetaModel.cog_p, BuildMetaModel.inh_p, BuildMetaModel.output1, BuildMetaModel.input_v1)#, cus_alpha)
        else:
            self.bayes = BuildMetaModel.buildKRR(self, BuildMetaModel.cog_p, BuildMetaModel.inh_p, BuildMetaModel.output1, BuildMetaModel.input_v1)#, cus_n_iter, cus_tol)
        print("==================================")
        show_panel.Layout()


class EditMixin(wx.ListCtrl, TextEditMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
        TextEditMixin.__init__(self)