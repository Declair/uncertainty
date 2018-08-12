# -*- coding: utf-8 -*-
from __future__ import division

import wx
import wx.grid
import wx.lib.scrolledpanel as scrolled
import wx.lib.newevent
from matplotlib.figure import Figure
#from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import zhi as zi
import pandas as pdS
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
import MetaPanel
# from UncertaintyPropagation.UPSelectMethodPanel import EditMixin


class ShowNotebook(aui.AuiNotebook):
    def __init__(self, parent=None):

        aui.AuiNotebook.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                                 wx.DefaultSize, aui.AUI_NB_DEFAULT_STYLE)

    def BuildMetaPanel(self, pProj = 0):
        self.show_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
                                   wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.AddPage(self.show_panel, u"元模型建模", True, wx.NullBitmap)
        show_panel = self.show_panel

        self.static_text_a = wx.StaticText(show_panel, -1, label="建模方法:")

        self.methods = ['SVR', 'GPR', 'KRR']
        self.combobox = wx.ComboBox(self.show_panel, -1, choices=self.methods)
        self.combobox.SetSelection(0)

        box_sizer_a = wx.BoxSizer(orient=wx.HORIZONTAL)
        box_sizer_a.Add(self.static_text_a)
        box_sizer_a.Add(self.combobox)

        self.combobox.Bind(wx.EVT_COMBOBOX, self.onSelect_combobox)

        box_sizer = wx.BoxSizer(orient=wx.VERTICAL)
        box_sizer.Add(box_sizer_a)

        show_panel.SetSizer(box_sizer)
        self.Show(True)
        show_panel.Layout()

    def NewProj2(self, pProj=0):
        box_sizer = wx.BoxSizer(wx.VERTICAL)


        self.show_panel = scrolled.ScrolledPanel(self, -1,
                                                 style=wx.TAB_TRAVERSAL | wx.SUNKEN_BORDER, name="panel1")
        self.show_panel.SetAutoLayout(1)
        self.show_panel.SetupScrolling()

        self.show_panel2 = MetaPanel.MetaPanel(self,1)
        self.AddPage(self.show_panel2, u"选择仿真验证模型", True, wx.NullBitmap)

        # self.AddPage(self.show_panel, u"选择仿真验证模型", True, wx.NullBitmap)
        # show_panel = self.show_panel
        #
        # bSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        #
        # self.m_radioBtn1 = wx.RadioButton(show_panel, wx.ID_ANY, u"欧式距离验证", wx.DefaultPosition, wx.DefaultSize, 0)
        # # self.m_radioBtn1.Bind(wx.EVT_BUTTON, self.onClick_button_t1a)
        # self.m_radioBtn1.Bind(wx.EVT_RADIOBUTTON, self.onClick_button_t1a)
        # bSizer1.Add(self.m_radioBtn1, 0, wx.ALL, 5)
        #
        # self.m_radioBtn2 = wx.RadioButton(show_panel, wx.ID_ANY, u"曼哈顿距离验证", wx.DefaultPosition, wx.DefaultSize, 0)
        # self.m_radioBtn2.Bind(wx.EVT_BUTTON, self.onClick_button_t2a)
        # bSizer1.Add(self.m_radioBtn2, 0, wx.ALL, 5)
        #
        # self.m_radioBtn3 = wx.RadioButton(show_panel, wx.ID_ANY, u"马氏距离验证", wx.DefaultPosition, wx.DefaultSize, 0)
        # self.m_radioBtn3.Bind(wx.EVT_BUTTON, self.onClick_button_t3a)
        # bSizer1.Add(self.m_radioBtn3, 0, wx.ALL, 5)
        #
        # self.m_radioBtn4 = wx.RadioButton(show_panel, wx.ID_ANY, u"切比雪夫距离验证", wx.DefaultPosition, wx.DefaultSize, 0)
        # self.m_radioBtn4.Bind(wx.EVT_BUTTON, self.onClick_button_t4a)
        # bSizer1.Add(self.m_radioBtn4, 0, wx.ALL, 5)
        #
        # self.m_radioBtn5 = wx.RadioButton(show_panel, wx.ID_ANY, u"KL散度验证", wx.DefaultPosition, wx.DefaultSize, 0)
        # self.m_radioBtn5.Bind(wx.EVT_BUTTON, self.onClick_button_t5a)
        # bSizer1.Add(self.m_radioBtn5, 0, wx.ALL, 5)
        #
        # box_sizer.Add(bSizer1)


        # self.static_text_1 = wx.StaticText(show_panel, -1, label="一维静态数据验证:")
        # #self.button_t1a = wx.Button(show_panel, -1, label='一维静态数据验证')
        # box_sizer.Add(self.static_text_1)

       # box_sizer.Add(self.button_t1a)

        # self.button_t11a = wx.Button(show_panel, -1,label='欧式距离验证',pos=(100,0))
        # self.button_t11a.Bind(wx.EVT_BUTTON, self.onClick_button_t1a)
        # box_sizer.Add(self.button_t11a)
        #
        # self.static_text_2 = wx.StaticText(show_panel, -1, label="多维静态数据验证:",pos=(0,25))
        # box_sizer.Add(self.static_text_2)
        #
        #
        # self.button_t2a = wx.Button(show_panel, -1,label='曼哈顿距离验证',pos=(100,25))
        # self.button_t2a.Bind(wx.EVT_BUTTON, self.onClick_button_t2a)
        # box_sizer.Add(self.button_t2a)
        #
        # self.button_t3a = wx.Button(show_panel, -1,label='马氏距离验证')
        # self.button_t3a.Bind(wx.EVT_BUTTON, self.onClick_button_t3a)
        # box_sizer.Add(self.button_t3a)
        #
        # self.button_t4a = wx.Button(show_panel,-1, label='切比雪夫距离验证')
        # self.button_t4a.Bind(wx.EVT_BUTTON, self.onClick_button_t4a)
        # box_sizer.Add(self.button_t4a)
        #
        # self.static_text_3 = wx.StaticText(show_panel, -1, label="动态仿真数据验证:",pos=(0,50))
        # box_sizer.Add(self.static_text_3)
        #
        # self.button_t5a = wx.Button(show_panel, -1,label='KL散度验证',pos=(100,50))
        # self.button_t5a.Bind(wx.EVT_BUTTON, self.onClick_button_t5a)
#        box_sizer.Add(self.button_t5a)
#         show_panel.SetSizer(box_sizer)
#         self.Show(True)
#         show_panel.Layout()


    def ImportDataPanel(self, pProj = 0):  #数据导入
        self.show_panel = scrolled.ScrolledPanel(self, -1,
                                                 style=wx.TAB_TRAVERSAL | wx.SUNKEN_BORDER, name="panel1")
        self.show_panel.SetAutoLayout(1)
        self.show_panel.SetupScrolling()

        self.AddPage(self.show_panel, u"数据导入", True, wx.NullBitmap)
        show_panel = self.show_panel

        box_sizer = wx.BoxSizer(orient=wx.VERTICAL)
        show_panel.SetSizer(box_sizer)

        self.Show(True)
        show_panel.Layout()

    def onClick_button_import(self):
        show_panel = self.show_panel
        sizer = show_panel.GetSizer()
        self.gbSizer_show = wx.GridBagSizer( 0, 0 )
        sizer.Add(self.gbSizer_show,0, wx.EXPAND, 5)

        """计算结果表"""
        self.Cal_Grid = grid.Grid(show_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        # self.Cal_form = EditMixin(show_panel)
        # self.Cal_form.Set
        table_position = 0
        self.gbSizer_show.Add(self.Cal_Grid, wx.GBPosition(table_position, 0),
                         wx.GBSpan(28, 13), wx.ALL|wx.EXPAND, 5)
        show_panel.Layout()


        build_meta.importData(self, cp.n_id)


