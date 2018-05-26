# -*- coding: utf-8 -*-

import wx
from wx import aui
from wx import grid
import Sql
import config
import mysql.connector
from mysql.connector import Error

class ShowNotebook(aui.AuiNotebook):
    
    def __init__(self, parent = None):
        
        aui.AuiNotebook.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, 
                                 wx.DefaultSize, aui.AUI_NB_DEFAULT_STYLE)
        
    def NewProj(self, pProj = 0):
        self.show_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, 
                                   wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.AddPage(self.show_panel, u"新建项目", True, wx.NullBitmap)
        show_panel = self.show_panel
        show_panel.pid = pProj
        # show_panel 的布局，只有 scrollPanel 一个元素
        show_panel.bSizer = wx.BoxSizer(wx.VERTICAL)
        #为实现滚动条加入 scrollPanel
        show_panel.scrolledWindow = wx.ScrolledWindow(show_panel, wx.ID_ANY, 
                    wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL)
        show_panel.scrolledWindow.SetScrollRate(5, 5)
        scrollPanel = show_panel.scrolledWindow
        # scrollPanel 的布局，元素为显示的控件
        show_panel.gbSizer = wx.GridBagSizer(5, 5)
        show_panel.gbSizer.SetFlexibleDirection(wx.BOTH)
        show_panel.gbSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        
        show_panel.staticText1 = wx.StaticText(scrollPanel, wx.ID_ANY, u"项目名称：", 
                                               wx.DefaultPosition, wx.DefaultSize, 0)
        show_panel.gbSizer.Add(show_panel.staticText1, wx.GBPosition(2, 4), 
                               wx.GBSpan(1, 1), wx.ALL, 5)
        
        show_panel.textCtrl1 = wx.TextCtrl(scrollPanel, wx.ID_ANY, wx.EmptyString, 
                                           wx.DefaultPosition, wx.Size(300,-1), 0)
        show_panel.gbSizer.Add(show_panel.textCtrl1, wx.GBPosition(2, 5), 
                               wx.GBSpan(1, 3), wx.ALL, 5)
        
        show_panel.staticText3 = wx.StaticText(scrollPanel, wx.ID_ANY, u"*此项目已存在", 
                                               wx.DefaultPosition, wx.DefaultSize, 0)
        show_panel.staticText3.SetForegroundColour('red')
        show_panel.gbSizer.Add(show_panel.staticText3, wx.GBPosition(2, 8), 
                             wx.GBSpan(1, 1), wx.ALL, 5)
        show_panel.staticText3.Show(show=False)
        
        show_panel.staticText2 = wx.StaticText(scrollPanel, wx.ID_ANY, u"项目描述：", 
                                               wx.DefaultPosition, wx.DefaultSize, 0)
        show_panel.gbSizer.Add(show_panel.staticText2, wx.GBPosition(3, 4), 
                               wx.GBSpan(1, 1), wx.ALL, 5)
        
        show_panel.textCtrl2 = wx.TextCtrl(scrollPanel, wx.ID_ANY, wx.EmptyString, 
                    wx.DefaultPosition, wx.Size(500,100), wx.TE_MULTILINE | wx.TE_RICH)
        show_panel.gbSizer.Add(show_panel.textCtrl2, wx.GBPosition(3, 5), 
                               wx.GBSpan(3, 5), wx.ALL, 5)
        
        show_panel.button1 = wx.Button(scrollPanel, wx.ID_ANY, u"导入模型", 
                                       wx.DefaultPosition, wx.DefaultSize, 0)
        self.Bind(wx.EVT_BUTTON, self.ClickImport, show_panel.button1)
        show_panel.gbSizer.Add(show_panel.button1, wx.GBPosition(5, 12), 
                               wx.GBSpan(1, 1), wx.ALL, 5)
        
        scrollPanel.SetSizer(show_panel.gbSizer)
        scrollPanel.Layout()
        show_panel.bSizer.Add(scrollPanel, 1, wx.EXPAND |wx.ALL, 5 )
        show_panel.SetSizer(show_panel.bSizer)
        show_panel.Layout()
    
    #点击导入模型事件
    def ClickImport(self, event):
        return
#         show_panel = self.GetCurrentPage()
#         proj_name = show_panel.textCtrl1.GetValue()
#         if proj_name == '':
#             return
#         proj_descr = show_panel.textCtrl2.GetValue()
#         record = Sql.selectSql((proj_name, show_panel.pid), Sql.selectProj)
#         if record != []:
#             show_panel.staticText3.Show(show=True)
#             show_panel.Layout()
#             return
#         show_panel.staticText3.Show(show=False)
#         dlg = wx.DirDialog(self,u"选择文件夹",style=wx.DD_DEFAULT_STYLE)  
#         if dlg.ShowModal() == wx.ID_OK:
#             show_panel.proj = Import_file.insert_blob(proj_name, show_panel.pid, 
#                                            proj_descr, dlg.GetPath())
#             show_panel.textCtrl1.Disable() #导入成功后控件变为不可编辑
#             show_panel.textCtrl2.Disable()
#             show_panel.button1.Disable()
#             self.GetParent().GetParent().navTree.updateTree()
#             self.genInParams(show_panel.proj, show_panel)
#         dlg.Destroy()
#         show_panel.proj = 1
#         self.genInParams(1, show_panel)
    
    #导入成功后生成输入参数控件
    def genInParams(self, proj, show_panel):
        return 
#         Run.read_blob(proj)
#         #输入参数
#         show_panel.params = Run.read_param(proj, config.param_func)
#         scrollPanel = show_panel.scrolledWindow
#         show_panel.staticText4 = wx.StaticText(scrollPanel, wx.ID_ANY, 
#                                 u"模型输入参数共" + str(len(show_panel.params)) + u"个：", 
#                                 wx.DefaultPosition, wx.DefaultSize, 0)
#         show_panel.gbSizer.Add(show_panel.staticText4, wx.GBPosition(7, 4), 
#                                wx.GBSpan(1, 2), wx.ALL, 5)
#         show_panel.grid = grid.Grid(scrollPanel, wx.ID_ANY, 
#                                        wx.DefaultPosition, wx.DefaultSize, 0)
#         # 参数表格
#         show_panel.grid.CreateGrid(len(show_panel.params), 4)
#         show_panel.grid.SetColSize(0, 200)
#         show_panel.grid.SetColLabelValue(0, "参数描述")
#         show_panel.grid.SetColLabelValue(1, "参数名")
#         show_panel.grid.SetColLabelValue(2, "单位")
#         show_panel.grid.SetColLabelValue(3, "初始值")
#         show_panel.grid.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
#         for index in range(len(show_panel.params)):
#             for i in range(3):
#                 show_panel.grid.SetCellValue(index, i, show_panel.params[index][i])
#                 show_panel.grid.SetReadOnly(index, i)
#             show_panel.grid.SetCellEditor(index, 3, grid.GridCellFloatEditor())
#         show_panel.gbSizer.Add(show_panel.grid, wx.GBPosition(8, 5), 
#                                wx.GBSpan(1, 6), wx.ALL, 5)
#         #输入变量
#         show_panel.vars = Run.read_param(proj, config.var_func)
#         show_panel.staticText5 = wx.StaticText(scrollPanel, wx.ID_ANY, 
#                                 u"模型输入变量共" + str(len(show_panel.vars)) + u"个：", 
#                                 wx.DefaultPosition, wx.DefaultSize, 0)
#         show_panel.gbSizer.Add(show_panel.staticText5, wx.GBPosition(10, 4), 
#                                wx.GBSpan(1, 2), wx.ALL, 5)
#         show_panel.grid2 = grid.Grid(scrollPanel, wx.ID_ANY, 
#                                        wx.DefaultPosition, wx.DefaultSize, 0)
#         # 变量表格
#         show_panel.grid2.CreateGrid(len(show_panel.vars), 4)
#         show_panel.grid2.SetColSize(0, 200)
#         show_panel.grid2.SetColLabelValue(0, "变量描述")
#         show_panel.grid2.SetColLabelValue(1, "变量名")
#         show_panel.grid2.SetColLabelValue(2, "单位")
#         show_panel.grid2.SetColLabelValue(3, "初始值")
#         show_panel.grid2.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
#         for index in range(len(show_panel.vars)):
#             for i in range(3):
#                 show_panel.grid2.SetCellValue(index, i, show_panel.vars[index][i])
#                 show_panel.grid2.SetReadOnly(index, i)
#             show_panel.grid2.SetCellEditor(index, 3, grid.GridCellFloatEditor())
#         show_panel.gbSizer.Add(show_panel.grid2, wx.GBPosition(11, 5), 
#                                wx.GBSpan(1, 6), wx.ALL, 5)
#         show_panel.button2 = wx.Button(scrollPanel, wx.ID_ANY, u"保存", 
#                                        wx.DefaultPosition, wx.DefaultSize, 0)
#         self.Bind(wx.EVT_BUTTON, self.ClickSave, show_panel.button2)
#         show_panel.gbSizer.Add(show_panel.button2, wx.GBPosition(12, 12), 
#                                wx.GBSpan(1, 1), wx.ALL, 5)
#         show_panel.Layout()
#         
#     def ClickSave(self, event):
#         show_panel = self.GetCurrentPage()
#         db_config = config.datasourse
#         try:
#             conn = mysql.connector.connect(**db_config)
#             cursor = conn.cursor()
#             i = 0
#             for param in show_panel.params:
#                 init = show_panel.grid.GetCellValue(i, 3)
#                 cursor.execute(Sql.insertParam, (param[1], show_panel.proj, 
#                                 param[0], param[2], init))
#                 i += 1
#             i = 0
#             for var in show_panel.vars:
#                 init = show_panel.grid2.GetCellValue(i, 3)
#                 cursor.execute(Sql.insertVar, (var[1], show_panel.proj, 
#                                 var[0], var[2], init))
#                 i += 1
#             conn.commit()
#         except Error as e:
#             print(e)
#             wx.MessageBox("保存失败", "消息提示" ,wx.OK | wx.ICON_ERROR)
#         finally:
#             cursor.close()
#             conn.close()
#         wx.MessageBox("保存成功", "消息提示" ,wx.OK | wx.ICON_INFORMATION)
#         show_panel.button2.Disable()
