# -*- coding: utf-8 -*-

import wx
from wx import aui
from wx import grid
import Import_file
import Run
import Sql
import sys
from wx.lib.mixins.listctrl import TextEditMixin

class ShowNotebook(aui.AuiNotebook):
    
    def __init__(self, parent = None):
        
        aui.AuiNotebook.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, 
                                 wx.DefaultSize, aui.AUI_NB_DEFAULT_STYLE)

    def UpdateModel(self,id):
        flag = 0
        for x in range(self.GetPageCount()):
            if 2 == self.GetPage(x).GetId():
                self.GetPage(x).SetFocus()
                self.Refresh()
                flag = 1
                break
        if flag == 0:
            #生成panel
            """从数据库读取数据"""
            modelinfo = Sql.selectSql(args=(id,),sql=Sql.selectModel)
            params = Sql.selectSql(args=(id,),sql=Sql.selectModelArgs)

            self.show_panel2 = wx.Panel(self, 2, wx.DefaultPosition,
                                       wx.DefaultSize, wx.TAB_TRAVERSAL)
            self.AddPage(self.show_panel2, u"模型修改", True, wx.NullBitmap)
            show_panel = self.show_panel2
            show_panel.pid = modelinfo[0][2]
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

            show_panel.staticText1 = wx.StaticText(scrollPanel, wx.ID_ANY, u"模型名称：",
                                                   wx.DefaultPosition, wx.DefaultSize, 0)
            show_panel.gbSizer.Add(show_panel.staticText1, wx.GBPosition(2, 4),
                                   wx.GBSpan(1, 1), wx.ALL, 5)

            show_panel.textCtrl1 = wx.TextCtrl(scrollPanel, wx.ID_ANY, wx.EmptyString,
                                               wx.DefaultPosition, wx.Size(480, -1), 0)
            show_panel.gbSizer.Add(show_panel.textCtrl1, wx.GBPosition(2, 5),
                                   wx.GBSpan(1, 3), wx.ALL, 5)
            show_panel.textCtrl1.WriteText(modelinfo[0][0])

            show_panel.staticText3 = wx.StaticText(scrollPanel, wx.ID_ANY, u"*此模型名称已存在",
                                                   wx.DefaultPosition, wx.DefaultSize, 0)
            show_panel.staticText3.SetForegroundColour('red')
            show_panel.gbSizer.Add(show_panel.staticText3, wx.GBPosition(2, 8),
                                   wx.GBSpan(1, 1), wx.ALL, 5)
            show_panel.staticText3.Show(show=False)

            show_panel.staticText2 = wx.StaticText(scrollPanel, wx.ID_ANY, u"模型描述：",
                                                   wx.DefaultPosition, wx.DefaultSize, 0)
            show_panel.gbSizer.Add(show_panel.staticText2, wx.GBPosition(3, 4),
                                   wx.GBSpan(1, 1), wx.ALL, 5)

            show_panel.textCtrl2 = wx.TextCtrl(scrollPanel, wx.ID_ANY, wx.EmptyString,
                                               wx.DefaultPosition, wx.Size(480, 100), wx.TE_MULTILINE | wx.TE_RICH)
            show_panel.gbSizer.Add(show_panel.textCtrl2, wx.GBPosition(3, 5),
                                   wx.GBSpan(3, 5), wx.ALL, 5)
            show_panel.textCtrl2.WriteText(modelinfo[0][1])

            show_panel.model_select = wx.StaticText(scrollPanel, wx.ID_ANY, u"选择模型：",
                                                    wx.DefaultPosition, wx.DefaultSize, 0)
            show_panel.gbSizer.Add(show_panel.model_select, wx.GBPosition(6, 4),
                                   wx.GBSpan(1, 1), wx.ALL, 5)

            show_panel.dir_text = wx.TextCtrl(scrollPanel, wx.ID_ANY, wx.EmptyString,
                                              wx.DefaultPosition, wx.Size(380, -1), 0)
            show_panel.gbSizer.Add(show_panel.dir_text, wx.GBPosition(6, 5),
                                   wx.GBSpan(1, 1), wx.ALL, 5)
            show_panel.dir_text.WriteText('model_'+str(id))

            show_panel.button1 = wx.Button(scrollPanel, wx.ID_ANY, u"导入模型",
                                           wx.DefaultPosition, wx.DefaultSize, 0)
           # self.Bind(wx.EVT_BUTTON, self.ClickImport, show_panel.button1)
            show_panel.gbSizer.Add(show_panel.button1, wx.GBPosition(6, 6),
                                   wx.GBSpan(1, 1), wx.ALL, 5)

            # Run.read_blob(id)
            # params = Run.read_param(id)

            scrollPanel = show_panel.scrolledWindow
            show_panel.staticText4 = wx.StaticText(scrollPanel, wx.ID_ANY,
                                                   u"参数个数：", wx.DefaultPosition, wx.DefaultSize, 0)
            show_panel.gbSizer.Add(show_panel.staticText4, wx.GBPosition(7, 4),
                                   wx.GBSpan(1, 1), wx.ALL, 5)
            show_panel.var_num = wx.StaticText(scrollPanel, wx.ID_ANY, str(len(params)),
                                               wx.DefaultPosition, wx.DefaultSize, 0)
            show_panel.gbSizer.Add(show_panel.var_num, wx.GBPosition(7, 5),
                                   wx.GBSpan(1, 1), wx.ALL, 5)

            show_panel.staticText5 = wx.StaticText(scrollPanel, wx.ID_ANY,
                                                   u"参数设置：", wx.DefaultPosition, wx.DefaultSize, 0)
            show_panel.gbSizer.Add(show_panel.staticText5, wx.GBPosition(8, 4),
                                   wx.GBSpan(1, 1), wx.ALL, 5)

            show_panel.inputform = EditMixin(scrollPanel)
            show_panel.inputform.InsertColumn(0, '参数名', width=160)
            show_panel.inputform.InsertColumn(1, '变量名', width=160)
            show_panel.inputform.InsertColumn(2, '初始值', width=160)
            for i in params:
                index = show_panel.inputform.InsertItem(sys.maxint, '变量' + str(i[1]))
                show_panel.inputform.SetItem(index, 1, i[0])
                show_panel.inputform.SetItem(index, 2, str(i[2]))
            show_panel.inputform.make_editor()

            show_panel.gbSizer.Add(show_panel.inputform, wx.GBPosition(8, 5), wx.GBSpan(7, 2 * len(params)+1), wx.ALL, 5)

            show_panel.staticText7 = wx.StaticText(scrollPanel, wx.ID_ANY,
                                                   u"输出参数：", wx.DefaultPosition, wx.DefaultSize, 0)
            show_panel.gbSizer.Add(show_panel.staticText7, wx.GBPosition(8 + 7 , 4),
                                   wx.GBSpan(1, 1), wx.ALL, 5)

            show_panel.outputform = EditMixin(scrollPanel)
            show_panel.outputform.InsertColumn(0, '参数名', width=160)
            show_panel.outputform.InsertColumn(1, '变量名', width=160)
            show_panel.outputform.InsertColumn(2, '初始值', width=160)
            for i in params:
                index = show_panel.outputform.InsertItem(sys.maxint, '变量'+str(i[1]))
                show_panel.outputform.SetItem(index, 1, i[0])
                show_panel.outputform.SetItem(index, 2, str(i[2]))
            show_panel.outputform.make_editor()

            show_panel.gbSizer.Add(show_panel.outputform, wx.GBPosition(8 + 7, 5), wx.GBSpan(7, 2 * len(params)+1),
                                   wx.ALL, 5)

            # 右下角savepanel
            self.savePanel2 = wx.Panel(scrollPanel, wx.ID_ANY, wx.DefaultPosition,
                                      (240, 28), wx.TAB_TRAVERSAL)
            x, y = self.show_panel2.GetSize()
            w, h = self.savePanel2.GetSize()
            self.savePanel2.SetPosition((x - w - 25, y - h - 10))
            show_panel.save = wx.Button(self.savePanel2, wx.ID_ANY, u"保存",
                                        (0, 0), (100, 28), 0)
            show_panel.save.Bind(wx.EVT_LEFT_DOWN,self.SaveUpdate)
            show_panel.cancel = wx.Button(self.savePanel2, wx.ID_ANY, u"取消",
                                          (140, 0), (100, 28), 0)
            show_panel.cancel.Bind(wx.EVT_LEFT_DOWN,self.CancelUpdate)

            #show_panel.gbSizer.Add(self.savePanel2, wx.GBPosition(22, 5), wx.GBSpan(1, 1),
             #                      wx.ALL, 5)

            scrollPanel.SetSizer(show_panel.gbSizer)
            scrollPanel.Layout()
            show_panel.bSizer.Add(scrollPanel, 1, wx.EXPAND | wx.ALL, 5)
            show_panel.SetSizer(show_panel.bSizer)
            show_panel.Layout()

            show_panel.Bind(wx.EVT_SIZE, self.OnReSize2)

    def OnReSize2(self, event):
        #       在绑定的size事件中使右上角用户panel右对齐
        x, y = self.show_panel2.scrolledWindow.GetSize()
        w, h = self.savePanel2.GetSize()
        self.savePanel2.SetPosition((x - w - 25, y - h - 10))
        self.Refresh()
        self.show_panel2.Layout()
        
    def NewProj(self, pProj = 0):
        flag = 0
        for x in range(self.GetPageCount()):
            if 1 == self.GetPage(x).GetId():
                self.GetPage(x).SetFocus()
                self.Refresh()
                flag = 1
                break
        if flag == 0:
            self.show_panel = wx.Panel(self, 1, wx.DefaultPosition,
                                       wx.DefaultSize, wx.TAB_TRAVERSAL)
            self.AddPage(self.show_panel, u"新建模型", True, wx.NullBitmap)
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

            show_panel.staticText1 = wx.StaticText(scrollPanel, wx.ID_ANY, u"模型名称：",
                                                   wx.DefaultPosition, wx.DefaultSize, 0)
            show_panel.gbSizer.Add(show_panel.staticText1, wx.GBPosition(2, 4),
                                   wx.GBSpan(1, 1), wx.ALL, 5)

            show_panel.textCtrl1 = wx.TextCtrl(scrollPanel, wx.ID_ANY, wx.EmptyString,
                                               wx.DefaultPosition, wx.Size(480,-1), 0)
            show_panel.gbSizer.Add(show_panel.textCtrl1, wx.GBPosition(2, 5),
                                   wx.GBSpan(1, 3), wx.ALL, 5)

            show_panel.staticText3 = wx.StaticText(scrollPanel, wx.ID_ANY, u"*此模型名称已存在",
                                                   wx.DefaultPosition, wx.DefaultSize, 0)
            show_panel.staticText3.SetForegroundColour('red')
            show_panel.gbSizer.Add(show_panel.staticText3, wx.GBPosition(2, 8),
                                 wx.GBSpan(1, 1), wx.ALL, 5)
            show_panel.staticText3.Show(show=False)

            show_panel.staticText2 = wx.StaticText(scrollPanel, wx.ID_ANY, u"模型描述：",
                                                   wx.DefaultPosition, wx.DefaultSize, 0)
            show_panel.gbSizer.Add(show_panel.staticText2, wx.GBPosition(3, 4),
                                   wx.GBSpan(1, 1), wx.ALL, 5)

            show_panel.textCtrl2 = wx.TextCtrl(scrollPanel, wx.ID_ANY, wx.EmptyString,
                        wx.DefaultPosition, wx.Size(480,100), wx.TE_MULTILINE | wx.TE_RICH)
            show_panel.gbSizer.Add(show_panel.textCtrl2, wx.GBPosition(3, 5),
                                   wx.GBSpan(3, 5), wx.ALL, 5)

            show_panel.model_select = wx.StaticText(scrollPanel, wx.ID_ANY, u"选择模型：",
                                                    wx.DefaultPosition, wx.DefaultSize, 0)
            show_panel.gbSizer.Add(show_panel.model_select, wx.GBPosition(6, 4),
                                    wx.GBSpan(1, 1), wx.ALL, 5)

            show_panel.dir_text = wx.TextCtrl(scrollPanel, wx.ID_ANY,wx.EmptyString,
                                               wx.DefaultPosition, wx.Size(380,-1), 0)
            show_panel.gbSizer.Add(show_panel.dir_text, wx.GBPosition(6,5),
                                    wx.GBSpan(1, 1), wx.ALL, 5)

            show_panel.button1 = wx.Button(scrollPanel, wx.ID_ANY, u"导入模型",
                                           wx.DefaultPosition, wx.DefaultSize, 0)
            self.Bind(wx.EVT_BUTTON, self.ClickImport, show_panel.button1)
            show_panel.gbSizer.Add(show_panel.button1, wx.GBPosition(6, 6),
                                   wx.GBSpan(1, 1), wx.ALL, 5)

            # 右下角savepanel
            self.savePanel = wx.Panel(show_panel, wx.ID_ANY, wx.DefaultPosition,
                                      (240, 28), wx.TAB_TRAVERSAL)
            x, y = self.show_panel.GetSize()
            w, h = self.savePanel.GetSize()
            self.savePanel.SetPosition((x - w - 25, y - h - 10))
            show_panel.save = wx.Button(self.savePanel, wx.ID_ANY, u"保存",
                                        (0, 0), (100, 28), 0)
            show_panel.Bind(wx.EVT_LEFT_DOWN, self.SaveNew,show_panel.save)
            show_panel.cancel = wx.Button(self.savePanel, wx.ID_ANY, u"取消",
                                          (140, 0), (100, 28), 0)
            show_panel.Bind(wx.EVT_LEFT_DOWN, self.CancelNew,show_panel.cancel)

            scrollPanel.SetSizer(show_panel.gbSizer)
            scrollPanel.Layout()
            show_panel.bSizer.Add(scrollPanel, 1, wx.EXPAND |wx.ALL, 5 )
            show_panel.SetSizer(show_panel.bSizer)
            show_panel.Layout()

            show_panel.Bind(wx.EVT_SIZE, self.OnReSize)

    def OnReSize(self, event):
        #       在绑定的size事件中使右上角用户panel右对齐
        x, y = self.show_panel.GetSize()
        w, h = self.savePanel.GetSize()
        self.savePanel.SetPosition((x - w - 25, y - h - 10))
        self.Refresh()
        self.show_panel.Layout()

    #点击导入模型事件
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
        dlg = wx.DirDialog(self,u"选择文件夹",style=wx.DD_DEFAULT_STYLE)  
        if dlg.ShowModal() == wx.ID_OK:
            proj = Import_file.insert_blob(proj_name, show_panel.pid, 
                                           proj_descr, dlg.GetPath())
            show_panel.dir_text.SetValue(dlg.GetPath())
            show_panel.dir_text.Disable()
            show_panel.textCtrl1.Disable() #导入成功后控件变为不可编辑
            show_panel.textCtrl2.Disable()
            show_panel.button1.Disable()
            self.GetParent().GetParent().navTree.updateTree()
            self.genInParams(proj, show_panel)
        dlg.Destroy()
    
    #导入成功后生成输入参数控件
    def genInParams(self, proj, show_panel):
        Run.read_blob(proj)
        params = Run.read_param(proj)
        scrollPanel = show_panel.scrolledWindow
        show_panel.staticText4 = wx.StaticText(scrollPanel, wx.ID_ANY, 
                                u"参数个数：",wx.DefaultPosition, wx.DefaultSize, 0)
        show_panel.gbSizer.Add(show_panel.staticText4, wx.GBPosition(7, 4), 
                               wx.GBSpan(1, 1), wx.ALL, 5)
        show_panel.var_num = wx.StaticText(scrollPanel, wx.ID_ANY,str(len(params)),
                                               wx.DefaultPosition, wx.DefaultSize, 0)
        show_panel.gbSizer.Add(show_panel.var_num, wx.GBPosition(7, 5),
                               wx.GBSpan(1, 1), wx.ALL, 5)

        show_panel.staticText5 = wx.StaticText(scrollPanel, wx.ID_ANY, 
                                u"参数设置：", wx.DefaultPosition, wx.DefaultSize, 0)
        show_panel.gbSizer.Add(show_panel.staticText5, wx.GBPosition(8, 4),
                               wx.GBSpan(1, 1), wx.ALL, 5)

        show_panel.inputform = EditMixin(scrollPanel)
        show_panel.inputform.InsertColumn(0, '参数名', width=160)
        show_panel.inputform.InsertColumn(1, '变量名', width=160)
        show_panel.inputform.InsertColumn(2, '初始值', width=160)
        for i in params:
            index = show_panel.inputform.InsertItem(sys.maxint, i[0])
            show_panel.inputform.SetItem(index, 1, i[1])
            show_panel.inputform.SetItem(index, 2, '0')
        show_panel.inputform.make_editor()

        show_panel.gbSizer.Add(show_panel.inputform, wx.GBPosition(8, 5), wx.GBSpan(5, 2*len(params)),wx.ALL, 5)

        show_panel.staticText6 = wx.StaticText(scrollPanel, wx.ID_ANY,
                                               u"输出个数：", wx.DefaultPosition, wx.DefaultSize, 0)
        show_panel.gbSizer.Add(show_panel.staticText6, wx.GBPosition(13, 4),
                               wx.GBSpan(1, 1), wx.ALL, 5)
        show_panel.output_var = wx.TextCtrl(scrollPanel, wx.ID_ANY, str(len(params)),
                                              wx.DefaultPosition, wx.DefaultSize, 0)
        show_panel.output_var.Bind(wx.EVT_TEXT, self.OutputManage)
        show_panel.gbSizer.Add(show_panel.output_var, wx.GBPosition(13, 5),
                               wx.GBSpan(1, 1), wx.ALL, 5)

        show_panel.staticText7 = wx.StaticText(scrollPanel, wx.ID_ANY,
                                               u"输出参数：", wx.DefaultPosition, wx.DefaultSize, 0)
        show_panel.gbSizer.Add(show_panel.staticText7, wx.GBPosition(8+5+1, 4),
                               wx.GBSpan(1, 1), wx.ALL, 5)

        show_panel.output_form = EditMixin(scrollPanel)
        show_panel.output_form.InsertColumn(0, '参数名', width=160)
        show_panel.output_form.InsertColumn(1, '变量名', width=160)
        show_panel.output_form.InsertColumn(2, '初始值', width=160)
        # for i in params:
        #     index = show_panel.output_form.InsertItem(sys.maxint, i[0])
        #     show_panel.output_form.SetItem(index, 1, i[1])
        # show_panel.output_form.make_editor()

        show_panel.gbSizer.Add(show_panel.output_form, wx.GBPosition(8+5+1, 5), wx.GBSpan(5, 2 * len(params)-1), wx.ALL, 5)

        show_panel.Layout()

    # 生成输出参数表
    def OutputManage(self, event):
        show_panel = self.GetCurrentPage()
        num = show_panel.output_var.GetValue()
        if num.isdigit() == True:
            show_panel.output_form.ClearAll()
            show_panel.output_form.InsertColumn(0, '参数名', width=160)
            show_panel.output_form.InsertColumn(1, '变量名', width=160)
            show_panel.output_form.InsertColumn(2, '初始值', width=160)
            for i in range(int(num)):
                index = show_panel.output_form.InsertItem(sys.maxint, '输出'+str(i))
            show_panel.output_form.make_editor()

    # 保存更新设置
    def SaveUpdate(self, event):
        return

    # 保存新建设置
    def SaveNew(self, event):
        return

    # 关闭
    def CancelUpdate(self, event):
        show_panel = self.GetCurrentPage()
        self.DeletePage(self.GetPageIndex(show_panel))
        self.Refresh()

    # 关闭
    def CancelNew(self, event):
        show_panel = self.GetCurrentPage()
        self.DeletePage(self.GetPageIndex(show_panel))
        self.Refresh()

class EditMixin(wx.ListCtrl, TextEditMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
        TextEditMixin.__init__(self)