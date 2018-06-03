# -*- coding: utf-8 -*-

from __future__ import division
import wx
import NavTree
import ShowNotebook


n_id = 0
sym0 = 0
sym1 = 0
sym2 = 0
class CalibrationPanel(wx.Panel):

    def __init__(self, parent=None):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.InitUI()

    def InitUI(self):
        # 上方按钮区域panel
        self.btnPanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
                                 wx.Size(-1, 40), wx.TAB_TRAVERSAL)
        tabSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btnPanel.SetSizer(tabSizer)


        self.button_ModelSelect = wx.Button(self.btnPanel, wx.ID_ANY, u"模型选择",
                                           wx.DefaultPosition, wx.DefaultSize, 0)
        self.button_ModelSelect.SetBitmap(wx.Bitmap('icon/select.ico'))
        self.Bind(wx.EVT_BUTTON, self.ClickModelSelect, self.button_ModelSelect)


        self.button_ImportData = wx.Button(self.btnPanel, wx.ID_ANY, u"数据导入",
                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.button_ImportData.SetBitmap(wx.Bitmap('icon/data.ico'))
        self.Bind(wx.EVT_BUTTON, self.ClickImportData, self.button_ImportData)


        self.button2 = wx.Button(self.btnPanel, wx.ID_ANY, u"元模型建模",
                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.button2.SetBitmap(wx.Bitmap('icon/metamodel.ico'))
        self.Bind(wx.EVT_BUTTON, self.ClickSetup, self.button2)

        self.button3 = wx.Button(self.btnPanel, wx.ID_ANY, u"优化模型",
                                 wx.DefaultPosition, wx.DefaultSize, 0)
        self.button3.SetBitmap(wx.Bitmap('icon/optimize.ico'))
        self.Bind(wx.EVT_BUTTON, self.ClickOptSetup, self.button3)


        # tabSizer.Add(self.button1, 0, wx.ALL, 5)
        tabSizer.Add(self.button_ModelSelect, 0, wx.ALL, 5)
        tabSizer.Add(self.button_ImportData, 0, wx.ALL, 5)
        tabSizer.Add(self.button2, 0, wx.ALL, 5)
        tabSizer.Add(self.button3, 0, wx.ALL, 5)

        # self.button1 = wx.Button(self.btnPanel, wx.ID_ANY, u"模型导入",
        #                          wx.DefaultPosition, wx.DefaultSize, 0)
        # #         self.button1.SetBitmap(wx.Bitmap('icon/btn_show1.tga'))
        # self.button1.Bind(wx.EVT_LEFT_DOWN, self.ClickImport)
        # tabSizer.Add(self.button1, 0, wx.ALL, 5)
        #
        # self.button2 = wx.Button(self.btnPanel, wx.ID_ANY, u"参数设置",
        #                          wx.DefaultPosition, wx.DefaultSize, 0)
        # tabSizer.Add(self.button2, 0, wx.ALL, 5)
        #
        # self.button3 = wx.Button(self.btnPanel, wx.ID_ANY, u"数据导入",
        #                          wx.DefaultPosition, wx.DefaultSize, 0)
        # tabSizer.Add(self.button3, 0, wx.ALL, 5)

        # 下方导航树及展示界面panel
        self.displayPanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
                                     wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.navTree = NavTree.NavTree(self.displayPanel)
        self.showNotebook = ShowNotebook.ShowNotebook(self.displayPanel)
        # displayPanel布局
        hBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        hBoxSizer.Add(self.navTree, 1, wx.ALL | wx.EXPAND, 5)
        hBoxSizer.Add(self.showNotebook, 4, wx.EXPAND | wx.ALL, 5)
        self.displayPanel.SetSizer(hBoxSizer)

        # 整个模块布局
        vBoxSizer = wx.BoxSizer(wx.VERTICAL)
        vBoxSizer.Add(self.btnPanel, 0, wx.EXPAND | wx.ALL, 5)
        vBoxSizer.Add(self.displayPanel, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(vBoxSizer)

    def ClickModelSelect(self, event):
        global n_id
        try:
            n_id = self.navTree.GetItemData(self.navTree.GetSelection())  #获取校准模型的id
            if n_id==0:
                raise NameError('...')
            dlg = wx.MessageDialog(None, message='你选择了模型的id是%d'%(n_id))
            dlg.ShowModal()
            global sym0
            sym0 = 1
        except:
            dlg = wx.MessageDialog(None, message='请先选择一个仿真模型', caption='warning')
            dlg.ShowModal()


    def ClickImportData(self, event):
        try:
            if sym0 == 0:
                raise NameError('...')
            self.showNotebook.ImportDataPanel_NEW()
        except:
            dlg = wx.MessageDialog(None, message='请先完成选择模型模块', caption='warning')
            dlg.ShowModal()


    def ClickSetup(self, event):
        try:
            if sym1 == 0:
                raise NameError('...')
            self.showNotebook.BuildMetaPanel_NEW()
        except:
            dlg = wx.MessageDialog(None, message='请先完成导入数据模块', caption='warning')
            dlg.ShowModal()

    def ClickOptSetup(self, event):
        try:
            if sym2 == 0:
                raise NameError('...')
            self.showNotebook.OptPanel_NEW()
        except:
            dlg = wx.MessageDialog(None, message='请先完成元模型建模模块', caption='warning')
            dlg.ShowModal()

