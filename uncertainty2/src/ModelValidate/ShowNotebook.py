# -*- coding: utf-8 -*-

import wx
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
import pandas as pd
import ValidateBuildMetaModel as  build_meta
import ValidateUi as cp
from CustomedScrolledWindow import CustomedScrolledWindow as csw
class ShowNotebook(aui.AuiNotebook):

    def __init__(self, parent=None):

        aui.AuiNotebook.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                                 wx.DefaultSize, aui.AUI_NB_DEFAULT_STYLE)

    def NewProj0(self, pProj=0):
        self.show_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
                                   wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.AddPage(self.show_panel, u"数据库连接", True, wx.NullBitmap)
        show_panel = self.show_panel
        self.button_db = wx.Button(show_panel, label="导入数据")
        self.button_db.Bind(wx.EVT_BUTTON, self.onClick_button_db)
        self.text_static_db = wx.StaticText(show_panel, -1, label="")

        box_sizer = wx.BoxSizer(orient=wx.VERTICAL)
        box_sizer_db = wx.BoxSizer(orient=wx.HORIZONTAL)
        box_sizer_db.Add(self.button_db)
        box_sizer_db.Add(self.text_static_db)
        box_sizer.Add(box_sizer_db, flag=wx.EXPAND, proportion=wx.EXPAND)

        show_panel.SetSizer(box_sizer)
        self.Show(True)

        show_panel.Layout()

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
            self.text_static_db.SetLabel(str(self.conn.connection_id))
        except Error as e:
            print(e)
        finally:
            print '导入数据'

    def NewProj1(self, pProj=0):
        return


    def NewProj2(self, pProj=0):


        tabSizer = wx.BoxSizer(wx.HORIZONTAL)


        self.show_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
                                   wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.AddPage(self.show_panel, u"选择仿真验证模型", True, wx.NullBitmap)
        show_panel = self.show_panel

        self.button_t1a = wx.Button(show_panel, -1, label='一维静态数据验证', pos=(0, 0))
        tabSizer.Add(self.button_t1a, 0, wx.ALL, 5)
        box_sizer = wx.BoxSizer(orient=wx.VERTICAL)
        box_sizer.Add(self.button_t1a)

        self.button_t1a = wx.Button(show_panel, -1,label='欧式距离验证',pos=(30, 30))
        self.button_t1a.Bind(wx.EVT_BUTTON, self.onClick_button_t1a)
        tabSizer.Add(self.button_t1a, 0, wx.ALL, 5)
        box_sizer = wx.BoxSizer(orient=wx.VERTICAL)
        box_sizer.Add(self.button_t1a)

        self.button_t1a = wx.Button(show_panel, -1, label='多维静态数据验证', pos=(0, 100))
        tabSizer.Add(self.button_t1a, 0, wx.ALL, 5)
        box_sizer = wx.BoxSizer(orient=wx.VERTICAL)
        box_sizer.Add(self.button_t1a)

        self.button_t2a = wx.Button(show_panel, -1,label='曼哈顿距离验证',pos=(30, 130))
        self.button_t2a.Bind(wx.EVT_BUTTON, self.onClick_button_t2a)
        tabSizer.Add(self.button_t2a, 0, wx.ALL, 5)
        box_sizer = wx.BoxSizer(orient=wx.VERTICAL)
        box_sizer.Add(self.button_t2a)

        self.button_t3a = wx.Button(show_panel, -1,label='马氏距离验证',pos=(30, 170))
        self.button_t3a.Bind(wx.EVT_BUTTON, self.onClick_button_t3a)
        tabSizer.Add(self.button_t3a, 0, wx.ALL, 5)
        box_sizer = wx.BoxSizer(orient=wx.VERTICAL)
        box_sizer.Add(self.button_t3a)

        self.button_t4a = wx.Button(show_panel,-1, label='切比雪夫距离验证',pos=(30, 210))
        self.button_t4a.Bind(wx.EVT_BUTTON, self.onClick_button_t4a)
        tabSizer.Add(self.button_t4a, 0, wx.ALL, 5)
        box_sizer = wx.BoxSizer(orient=wx.VERTICAL)
        box_sizer.Add(self.button_t4a)

        self.button_t1a = wx.Button(show_panel, -1, label='多维动态数据验证', pos=(0, 280))
        tabSizer.Add(self.button_t1a, 0, wx.ALL, 5)
        box_sizer = wx.BoxSizer(orient=wx.VERTICAL)
        box_sizer.Add(self.button_t1a)

        self.button_t5a = wx.Button(show_panel, -1,label='KL散度验证',pos=(30, 310))
        self.button_t5a.Bind(wx.EVT_BUTTON, self.onClick_button_t5a)
        tabSizer.Add(self.button_t5a, 0, wx.ALL, 5)
        box_sizer = wx.BoxSizer(orient=wx.VERTICAL)
        box_sizer.Add(self.button_t5a)


        self.Show(True)

        show_panel.Layout()


    def ImportDataPanel(self, pProj = 0):
        self.panel_import = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
                                   wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.AddPage(self.panel_import, u"数据导入", True, wx.NullBitmap)
        show_panel = self.panel_import

        self.button_import = wx.Button(show_panel, label="ImportData")
        self.button_import.Bind(wx.EVT_BUTTON, self.onClick_button_import)
        box_sizer = wx.BoxSizer(orient=wx.VERTICAL)
        box_sizer.Add(self.button_import)
        show_panel.SetSizer(box_sizer)
        self.Show(True)

        show_panel.Layout()


    def onClick_button_t1a(self, event):
        build_meta.buildoushidistance(build_meta.cog_p, build_meta.inh_p, build_meta.output1,
                                      build_meta.input_v1)  # , cus_C, cus_epsilon, cus_kernel)



    def onClick_button_t2a(self, event):
        build_meta.buildmanhadundistance(build_meta.cog_p, build_meta.inh_p, build_meta.output1,
                                      build_meta.input_v1)

    def onClick_button_t3a(self, event):
        build_meta.buildmshidistance(build_meta.cog_p, build_meta.inh_p, build_meta.output1,
                                      build_meta.input_v1)

    def onClick_button_t4a(self, event):
        build_meta.buildqiebixuefudistance(build_meta.cog_p, build_meta.inh_p, build_meta.output1,
                                      build_meta.input_v1)

    def onClick_button_t5a(self, event):
        build_meta.buildKLdistance(build_meta.cog_p, build_meta.inh_p, build_meta.output1,
                                           build_meta.input_v1)


    def onClick_button_import(self, event):
        show_panel = self.panel_import
        sizer = show_panel.GetSizer()

        self.sw = csw(show_panel)

        sizer.Add(self.sw, flag=wx.EXPAND, proportion=wx.EXPAND)

        show_panel.Layout()

        build_meta.importData(self, cp.n_id)
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
