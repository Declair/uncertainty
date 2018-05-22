# -*- coding: utf-8 -*-
from functools import wraps
import SamplingMethod as SM
import wx
from wx import aui, grid
import UPShowPanel
import UPSelectMethodPanel

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

    def up_show(self):
        """ 在NoteBook里添加页面“试验设计” """
        self.show_panel = UPShowPanel.ShowPanel(self)
        self.AddPage(self.self.show_panel, u"试验设计", True, wx.NullBitmap)

    def ShowArg(self, record):

        self.show_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
                                   wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.AddPage(self.show_panel, u"显示参数信息", True, wx.NullBitmap)
        # self.show_panel 的布局，只有 scrollPanel 一个元素
        self.show_panel.bSizer = wx.BoxSizer(wx.VERTICAL)
        # 为实现滚动条加入 scrollPanel
        self.show_panel.scrolledWindow = wx.ScrolledWindow(self.show_panel, wx.ID_ANY,
                                                      wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL | wx.VSCROLL)
        self.show_panel.scrolledWindow.SetScrollRate(5, 5)
        scrollPanel = self.show_panel.scrolledWindow
        # scrollPanel 的布局，元素为显示的控件
        self.show_panel.gbSizer = wx.GridBagSizer(5, 5)
        self.show_panel.gbSizer.SetFlexibleDirection(wx.BOTH)
        self.show_panel.gbSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)



        """"""

        self.show_panel.m_grid4 = wx.grid.Grid(self.show_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)

        # Grid
        # 利用record的大小动态建立表长度
        self.tablelen = len(record)
        self.show_panel.m_grid4.CreateGrid(self.tablelen, 5)
        self.show_panel.m_grid4.EnableEditing(True)
        self.show_panel.m_grid4.EnableGridLines(True)
        self.show_panel.m_grid4.EnableDragGridSize(False)
        self.show_panel.m_grid4.SetMargins(0, 0)

        # Columns
        self.show_panel.m_grid4.EnableDragColMove(False)
        self.show_panel.m_grid4.EnableDragColSize(True)
        self.show_panel.m_grid4.SetColLabelSize(30)
        self.show_panel.m_grid4.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        self.show_panel.m_grid4.SetColLabelValue(0, "模型名称")
        self.show_panel.m_grid4.SetColLabelValue(1, "参数名称")
        self.show_panel.m_grid4.SetColLabelValue(2, "分布类型")
        self.show_panel.m_grid4.SetColLabelValue(3, "分布参数")
        self.show_panel.m_grid4.SetColLabelValue(4, "抽样方法")

        # Rows
        self.show_panel.m_grid4.EnableDragRowSize(True)
        self.show_panel.m_grid4.SetRowLabelSize(80)
        self.show_panel.m_grid4.SetRowLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Label Appearance

        # Cell Defaults
        self.show_panel.m_grid4.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_TOP)

        """"设置内容"""
        i = 0
        for row in record:
            self.show_panel.m_grid4.SetCellValue(i, 0, str(row[0]))
            self.show_panel.m_grid4.SetCellValue(i, 1, str(row[1]))
            self.show_panel.m_grid4.SetCellValue(i, 2, str(row[2]))
            self.show_panel.m_grid4.SetCellValue(i, 3, str(row[3]))
            self.show_panel.m_grid4.SetCellEditor(i, 4, grid.GridCellChoiceEditor(SM.available_method[str(row[2])]))
            i = i + 1

        """"""


        self.show_panel.bSizer.Add(self.show_panel.m_grid4, 1, wx.ALL | wx.EXPAND, 5)

        self.show_panel.m_button = wx.Button(self.show_panel, wx.ID_ANY, u"确定", wx.DefaultPosition, wx.DefaultSize, 0)
        self.show_panel.bSizer.Add(self.show_panel.m_button, 0, wx.ALL, 5)

        # Connect Events
        self.show_panel.m_button.Bind(wx.EVT_BUTTON, self.select_method_test)

        scrollPanel.SetSizer(self.show_panel.gbSizer)
        scrollPanel.Layout()
        self.show_panel.bSizer.Add(scrollPanel, 1, wx.EXPAND | wx.ALL, 5)
        self.show_panel.SetSizer(self.show_panel.bSizer)
        self.show_panel.Layout()

    # 逐一输出选择的抽样方法
    def select_method_test(self, event):
        self.method = []
        for i in range(0,self.tablelen):
            x = self.show_panel.m_grid4.GetCellEditor(i, 4)
            print(x.GetValue())
            self.method.append(x.GetValue())

    def up_select_method(self):
        """ 选择抽样方法 """
        print(self.kind)
        print(self.para)
        self.select_method_panel = UPSelectMethodPanel.SelectSamplingMethodPanel(self,self.name)  # 在这里传入参数
        self.select_method_panel.set_kind_and_para_and_name(self.kind,self.name,self.method,self.para)
        self.AddPage(self.select_method_panel, u"抽样方法", True, wx.NullBitmap)

    def up_test(self):
        """ 传播实验展示 """
        self.test_panel = UPShowPanel.TestPanel(self, name=self.name)
        # self.plan_panel.set_name(self.name)
        self.AddPage(self.test_panel, u"传播分析", True, wx.NullBitmap)