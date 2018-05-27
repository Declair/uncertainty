# -*- coding: utf-8 -*-
from functools import wraps

import wx
from wx import aui
from wx import grid
import Sql
from ModelManage import Run, Import_file

""""装饰器实现单例模式 方便在NAV界面更新SHOW界面"""
def singleton(cls):
    instances = {}

    @wraps(cls)
    def getinstance(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return getinstance

@singleton
class ShowNotebook(aui.AuiNotebook):

    def __init__(self, parent=None):

        aui.AuiNotebook.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                                 wx.DefaultSize, aui.AUI_NB_DEFAULT_STYLE)

    def ShowArg(self, record):

        self.show_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
                                   wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.AddPage(self.show_panel, u"显示参数信息", True, wx.NullBitmap)
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



        """"""

        show_panel.m_grid4 = grid.Grid(show_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)

        # Grid
        show_panel.m_grid4.CreateGrid(5, 4)
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
            i = i + 1

        """"""

        show_panel.bSizer.Add(show_panel.m_grid4, 1, wx.ALL | wx.EXPAND, 5)

        scrollPanel.SetSizer(show_panel.gbSizer)
        scrollPanel.Layout()
        show_panel.bSizer.Add(scrollPanel, 1, wx.EXPAND | wx.ALL, 5)
        show_panel.SetSizer(show_panel.bSizer)
        show_panel.Layout()

    # 点击导入模型事件
    def ClickImport(self, event):
        show_panel = self.GetCurrentPage()
        proj_name = show_panel.textCtrl1.GetValue()
        if proj_name == '':
            return
        proj_descr = show_panel.textCtrl2.GetValue()
        record = Sql.selectSql((proj_name, show_panel.pid), Sql.selectProj)
        if record != []:
            show_panel.staticText3.Show(show=True)
            show_panel.Layout()
            return
        show_panel.staticText3.Show(show=False)
        dlg = wx.DirDialog(self, u"选择文件夹", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            proj = Import_file.insert_blob(proj_name, show_panel.pid,
                                           proj_descr, dlg.GetPath())
            show_panel.textCtrl1.Disable()  # 导入成功后控件变为不可编辑
            show_panel.textCtrl2.Disable()
            show_panel.button1.Disable()
            self.GetParent().GetParent().navTree.updateTree()
            self.genInParams(proj, show_panel)
        dlg.Destroy()

    # 导入成功后生成输入参数控件
    def genInParams(self, proj, show_panel):
        Run.read_blob(proj)
        params = Run.read_param(proj)
        scrollPanel = show_panel.scrolledWindow
        show_panel.staticText4 = wx.StaticText(scrollPanel, wx.ID_ANY,
                                               u"模型输入参数共" + str(len(params)) + u"个：",
                                               wx.DefaultPosition, wx.DefaultSize, 0)
        show_panel.gbSizer.Add(show_panel.staticText4, wx.GBPosition(7, 4),
                               wx.GBSpan(1, 2), wx.ALL, 5)
        show_panel.staticText5 = wx.StaticText(scrollPanel, wx.ID_ANY,
                                               u"参数描述", wx.DefaultPosition, wx.DefaultSize, 0)
        show_panel.gbSizer.Add(show_panel.staticText5, wx.GBPosition(7, 4),
                               wx.GBSpan(1, 2), wx.ALL, 5)
        show_panel.Layout()