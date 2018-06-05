# -*- coding: utf-8 -*-
from functools import wraps
import SamplingMethod as SM
import wx
from wx import aui, grid
import UPShowPanel
import UPSelectMethodPanel

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

""""装饰器实现单例模式 方便传参"""
def singleton(cls):
    instances = {}

    @wraps(cls)
    def getinstance(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return getinstance

@singleton
class UTNotebook(aui.AuiNotebook):

    def __init__(self, parent=None):

        aui.AuiNotebook.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                                 wx.DefaultSize, aui.AUI_NB_DEFAULT_STYLE)

    # 以表格的形式显示参数信息
    # 参数的抽样方法为可选下拉框
    def ShowArg(self, record):
        """ 显示参数信息 Notebook """

        self.show_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
                                   wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.AddPage(self.show_panel, u"设置抽样方法", True, wx.NullBitmap)

        show_panel = self.show_panel
        # show_panel 的布局，只有 scrollPanel 一个元素
        show_panel.bSizer = wx.BoxSizer(wx.VERTICAL)
        # 为实现滚动条加入 scrollPanel
        show_panel.scrolledWindow = wx.ScrolledWindow(show_panel, wx.ID_ANY,
                                                      wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL | wx.VSCROLL)
        show_panel.scrolledWindow.SetScrollRate(5, 5)
        scrollPanel = show_panel.scrolledWindow
        # scrollPanel 的布局，元素为显示的控件
        show_panel.gbSizer = wx.GridBagSizer(5, 5)
        show_panel.gbSizer.SetFlexibleDirection(wx.BOTH)
        show_panel.gbSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        show_panel.m_grid4 = grid.Grid(show_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)

        # Grid
        # 利用record的大小动态建立表长度
        self.tablelen = len(record)
        show_panel.m_grid4.CreateGrid(self.tablelen, 5)
        show_panel.m_grid4.EnableEditing(True)
        show_panel.m_grid4.EnableGridLines(True)
        show_panel.m_grid4.EnableDragGridSize(False)
        show_panel.m_grid4.SetMargins(0, 0)

        # Columns
        show_panel.m_grid4.EnableDragColMove(False)
        show_panel.m_grid4.EnableDragColSize(True)
        show_panel.m_grid4.SetColLabelSize(30)
        show_panel.m_grid4.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        show_panel.m_grid4.SetColLabelValue(0, "模型名称")
        show_panel.m_grid4.SetColLabelValue(1, "参数名称")
        show_panel.m_grid4.SetColLabelValue(2, "分布类型")
        show_panel.m_grid4.SetColLabelValue(3, "分布参数")
        show_panel.m_grid4.SetColLabelValue(4, "抽样方法")

        # Rows
        show_panel.m_grid4.EnableDragRowSize(True)
        show_panel.m_grid4.SetRowLabelSize(80)
        show_panel.m_grid4.SetRowLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Label Appearance

        # Cell Defaults
        show_panel.m_grid4.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_TOP)

        """"设置内容"""
        i = 0
        for row in record:
            show_panel.m_grid4.SetCellValue(i, 0, str(row[0]))
            show_panel.m_grid4.SetCellValue(i, 1, str(row[1]))
            show_panel.m_grid4.SetCellValue(i, 2, str(row[2]))
            show_panel.m_grid4.SetCellValue(i, 3, str(row[3]))
            # 按照分布方式对应的可选抽样方法设置下拉框
            show_panel.m_grid4.SetCellEditor(i, 4, grid.GridCellChoiceEditor(SM.available_method[str(row[2])]))
            i = i + 1

        show_panel.gbSizer.Add(show_panel.m_grid4, wx.GBPosition(3, 4),
                         wx.GBSpan(1, 3), wx.ALL, 5)

        show_panel.m_button = wx.Button(show_panel, wx.ID_ANY, u"确定", wx.DefaultPosition, wx.DefaultSize, 0)

        # Connect Events
        show_panel.m_button.Bind(wx.EVT_BUTTON, self.select_method_test)

        show_panel.gbSizer.Add(show_panel.m_button, wx.GBPosition(5, 6),
                               wx.GBSpan(1, 3), wx.ALL, 5)

        scrollPanel.SetSizer(show_panel.gbSizer)
        scrollPanel.Layout()
        show_panel.Layout()


    # 逐一输出选择的抽样方法
    def select_method_test(self, event):
        self.method = []
        for i in range(0,self.tablelen):
            x = self.show_panel.m_grid4.GetCellEditor(i, 4)
            print(x.GetValue())
            self.method.append(x.GetValue())
        dlg = wx.MessageDialog(None, message='请进行抽样数量设置')
        dlg.ShowModal()

    def up_select_method(self):
        """ 选择抽样方法 """
        self.select_method_panel = UPSelectMethodPanel.SelectSamplingMethodPanel(self)
        self.select_method_panel.set_up(self.Para, self.method)  # 在这里传入参数
        self.AddPage(self.select_method_panel, u"设置抽样数量", True, wx.NullBitmap)

    def up_test(self):
        """ 传播实验展示 """
        self.test_panel = UPShowPanel.TestPanel(self, para=self.Para ,id = self.Para.model_id)
        self.AddPage(self.test_panel, u"传播分析", True, wx.NullBitmap)