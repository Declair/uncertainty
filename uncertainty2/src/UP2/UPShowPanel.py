# -*- coding: utf-8 -*-

import wx
import numpy
from wx import grid
import Sql
from ModelCalibration import CalibrationPanel as CP

class ShowPanel(wx.Panel):

    def __init__(self, parent = None):

        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                          wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DLIGHT))

        bSizer8 = wx.BoxSizer(wx.VERTICAL)
        """"""

        self.m_grid4 = wx.grid.Grid(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)

        # Grid
        self.m_grid4.CreateGrid(5, 4)
        self.m_grid4.EnableEditing(True)
        self.m_grid4.EnableGridLines(True)
        self.m_grid4.EnableDragGridSize(False)
        self.m_grid4.SetMargins(0, 0)

        # Columns
        self.m_grid4.EnableDragColMove(False)
        self.m_grid4.EnableDragColSize(True)
        self.m_grid4.SetColLabelSize(30)
        self.m_grid4.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        self.m_grid4.SetColLabelValue(0, "模型名称")
        self.m_grid4.SetColLabelValue(1, "参数名称")
        self.m_grid4.SetColLabelValue(2, "分布类型")
        self.m_grid4.SetColLabelValue(3, "分布参数")

        # Rows
        self.m_grid4.EnableDragRowSize(True)
        self.m_grid4.SetRowLabelSize(80)
        self.m_grid4.SetRowLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Label Appearance

        # Cell Defaults
        self.m_grid4.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_TOP)


        """"""
        bSizer8.Add(self.m_grid4, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(bSizer8)
        self.Layout()
        bSizer8.Fit(self)

    def set_name(self,name):
        self.name = name

class TestPanel(wx.Panel):

    def __init__(self,  parent = None, name=[]):

        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                          wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DLIGHT))

        bSizer8 = wx.BoxSizer(wx.VERTICAL)
        """"""

        # self.m_grid4 = wx.grid.Grid(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        #
        # # Grid
        # self.m_grid4.CreateGrid(5, 4)
        # self.m_grid4.EnableEditing(True)
        # self.m_grid4.EnableGridLines(True)
        # self.m_grid4.EnableDragGridSize(False)
        # self.m_grid4.SetMargins(0, 0)
        #
        # # Columns
        # self.m_grid4.EnableDragColMove(False)
        # self.m_grid4.EnableDragColSize(True)
        # self.m_grid4.SetColLabelSize(30)
        # self.m_grid4.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        # self.m_grid4.SetColLabelValue(0, "模型名称")
        # self.m_grid4.SetColLabelValue(1, "参数名称")
        # self.m_grid4.SetColLabelValue(2, "分布类型")
        # self.m_grid4.SetColLabelValue(3, "分布参数")
        #
        # # Rows
        # self.m_grid4.EnableDragRowSize(True)
        # self.m_grid4.SetRowLabelSize(80)
        # self.m_grid4.SetRowLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        #
        # # Label Appearance
        #
        # # Cell Defaults
        # self.m_grid4.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_TOP)


        """"""
        # bSizer8.Add(self.m_grid4, 1, wx.ALL | wx.EXPAND, 5)

        """实验 Start"""
        # FIXME: 字典临时代替表连接查询 规范统一数据库后更换为以查询表确定参数是 认知2、固有1还是输入0
        dict = {'x1': 0, 'x2': 0, 'x3': 0, 'a1': 2, 'a2': 2, 'a3': 1, 'a4': 1}
        # 根据参数名获取相应的抽样数据

        input_X = []
        Er_p = []
        Es_p = []

        results = input_X, Er_p, Es_p

        for n in name:  # 查询每个name 得到的列表result 追加在二维列表results中 生成实验方案
            result = list(Sql.show_sampling_result_with_type(n))
            results[dict[n]].append(result)

        # Er_p_m = numpy.zeros((len(Er_p),len(Er_p[0]) ))
        #
        # i = 0
        # j = 0
        # for erp in Er_p:
        #     for er in erp:
        #         Er_p_m[i][j] = er
        #         j += 1
        #     i += 1
        #
        # i_X_m = numpy.zeros((len(input_X), len(input_X[0])))
        #
        # i = 0
        # j = 0
        # for i_x_m in input_X:
        #     for i_x in i_x_m:
        #         i_X_m[i][j] = i_x
        #         j += 1
        #     i += 1

        for i in Es_p:  # 每一组认知不确定参数
            a_mat = CP.inner_level_loop(numpy.matrix(numpy.array(i)), numpy.matrix(numpy.array(Er_p)), numpy.matrix(numpy.array(input_X)))
            print('获得的仿真输出:')
            print(a_mat)

        """实验 End"""
        self.SetSizer(bSizer8)
        self.Layout()
        bSizer8.Fit(self)

    def set_name(self,name):
        self.name = name