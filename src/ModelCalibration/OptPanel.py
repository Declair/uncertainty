# -*- coding: utf-8 -*-
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
class OptPanel(wx.Panel):
    count = 0
    def __init__(self, parent,sym = None):
        """ 初始化 """
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                          wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.show_panel2 = sym
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
                                       (-1, 120), wx.TAB_TRAVERSAL)
        self.input_panel.SetMaxSize(wx.Size(-1,120))

        first_positon = 0
        next_positon = 1 + first_positon

        self.static_text_1 = wx.StaticText(self.input_panel, -1, label="群体总数:")
        self.text_ctrl_1 = wx.TextCtrl(self.input_panel, -1,size=(280,-1), value='2000')
        self.static_text_2 = wx.StaticText(self.input_panel, -1, label="交叉概率:")
        self.text_ctrl_2 = wx.TextCtrl(self.input_panel, -1,size=(280,-1), value='0.5')
        self.static_text_3 = wx.StaticText(self.input_panel, -1, label="变异概率:")
        self.text_ctrl_3 = wx.TextCtrl(self.input_panel, -1,size=(280,-1), value='0.05')
        self.static_text_4 = wx.StaticText(self.input_panel, -1, label="迭代次数:")
        self.text_ctrl_4 = wx.TextCtrl(self.input_panel, -1, size=(280,-1), value='15')

        self.gbSizer.Add(self.static_text_1, wx.GBPosition(first_positon, 4),
                               wx.GBSpan(1, 1), wx.ALL, 5)
        self.gbSizer.Add(self.text_ctrl_1, wx.GBPosition(first_positon, 5),
                               wx.GBSpan(1, 3), wx.ALL, 5)
        self.gbSizer.Add(self.static_text_2, wx.GBPosition(first_positon, 11),
                         wx.GBSpan(1, 1), wx.ALL, 5)
        self.gbSizer.Add(self.text_ctrl_2, wx.GBPosition(first_positon, 12),
                         wx.GBSpan(1, 3), wx.ALL, 5)
        self.gbSizer.Add(self.static_text_3, wx.GBPosition(next_positon, 4),
                         wx.GBSpan(1, 1), wx.ALL, 5)
        self.gbSizer.Add(self.text_ctrl_3, wx.GBPosition(next_positon, 5),
                         wx.GBSpan(1, 3), wx.ALL, 5)
        self.gbSizer.Add(self.static_text_4, wx.GBPosition(next_positon, 11),
                         wx.GBSpan(1, 1), wx.ALL, 5)
        self.gbSizer.Add(self.text_ctrl_4, wx.GBPosition(next_positon, 12),
                         wx.GBSpan(1, 3), wx.ALL, 5)

        ''' 元模型建模按钮的panel begins '''
        self.m_button_ok = wx.Button(self.input_panel, wx.ID_ANY, u"开始校准", wx.DefaultPosition, wx.Size(80, -1), 0)
        self.m_button_ok.Bind(wx.EVT_BUTTON, self.onClick_button_1)
        self.gbSizer.Add(self.m_button_ok, wx.GBPosition(next_positon + 1, 14),
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
        self.m_staticText_set = wx.StaticText(self, wx.ID_ANY, u"参数设置：",
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

    def onClick_button_1(self, event):
        self.m_button_ok.Disable()
        show_panel = self.scrolledWindow
        sizer = self.gbSizer_show

        sizer_a = wx.BoxSizer(orient=wx.VERTICAL)
        self.grid1 = wx.grid.Grid(show_panel)
        self.grid1.SetLabelBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        self.grid1.SetMinSize((400, 480))
        self.grid1.SetMaxSize((400, 480))
        sizer_v1 = wx.BoxSizer(orient=wx.VERTICAL)
        static_text_v1 = wx.StaticText(show_panel, label='每次迭代的度量取值结果')
        sizer_v1.Add(static_text_v1)
        sizer_v1.Add(self.grid1)

        self.grid2 = wx.grid.Grid(show_panel)
        self.grid2.SetMinSize((400, 480))
        self.grid2.SetMaxSize((400, 480))
        self.grid2.SetLabelBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHTTEXT ) )
        sizer_v2 = wx.BoxSizer(orient=wx.VERTICAL)
        static_text_v2 = wx.StaticText(show_panel, label='每次迭代的最佳认知参数取值结果')
        sizer_v2.Add(static_text_v2)
        sizer_v2.Add(self.grid2)

        sizer.Add(sizer_v1,wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL, 5)
        sizer.Add(sizer_v2,wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        sizer_b = wx.BoxSizer(orient=wx.VERTICAL)
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        # self.axes.set(xlabel='Number of iterations', ylabel='Consistency measure', title='Iterative metric trends')
        self.canvas = FigureCanvas(show_panel, -1, self.figure)
        sizer_v3 = wx.BoxSizer(orient=wx.VERTICAL)
        static_text_v3 = wx.StaticText(show_panel, label='度量值比较图')
        sizer_v3.Add(static_text_v3)
        sizer_v3.Add(self.canvas)

        self.figure2 = Figure()
        self.axes2 = self.figure2.add_subplot(111)
        # self.axes2.set(xlabel='Number of iterations', ylabel='Consistency measure', title='Compare verification trends')
        self.canvas2 = FigureCanvas(show_panel, -1, self.figure2)
        sizer_v4 = wx.BoxSizer(orient=wx.VERTICAL)
        static_text_v4 = wx.StaticText(show_panel, label='度量值差异图')
        sizer_v4.Add(static_text_v4)
        sizer_v4.Add(self.canvas2)

        sizer.Add(sizer_v3,wx.GBPosition(0, 2), wx.GBSpan(1, 1), wx.ALL, 5)
        sizer.Add(sizer_v4,wx.GBPosition(1, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        # sizer_c = wx.BoxSizer(orient=wx.HORIZONTAL)
        # sizer_c.Add(sizer_a)
        # sizer_c.Add(sizer_b)
        #
        # sizer.Add(sizer_c,wx.GBPosition(0, 0),
        #                  wx.GBSpan(1, 3), wx.ALL, 5)

        show_panel.Layout()
        # print(self.text_ctrl_1.GetLineText(0))
        pn = int(self.text_ctrl_1.GetLineText(0))
        itn = int(self.text_ctrl_4.GetLineText(0))
        cp = float(self.text_ctrl_2.GetLineText(0))
        mp = float(self.text_ctrl_3.GetLineText(0))
        if self.show_panel2.sym == 1:
            GenericAlgorithm.GA(self, self.show_panel2.svr, pn, itn, cp, mp)
        elif self.show_panel2.sym == 2:
            GenericAlgorithm.GA(self, self.show_panel2.gpr, pn, itn, cp, mp)
        else:
            GenericAlgorithm.GA(self, self.show_panel2.bayes, pn, itn, cp, mp)


class EditMixin(wx.ListCtrl, TextEditMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
        TextEditMixin.__init__(self)