# -*- coding: utf-8 -*-

from __future__ import division
import wx
import NavTree
import ShowNotebook

n_id = 0
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

        self.test_button = wx.Button(self.btnPanel, wx.ID_ANY, u"自测试面板",
                                 wx.DefaultPosition, wx.DefaultSize, 0)
        self.Bind(wx.EVT_BUTTON, self.ClickTestPanel, self.test_button)

        # self.button1 = wx.Button(self.btnPanel, wx.ID_ANY, u"参数设置",
        #                         wx.DefaultPosition, wx.DefaultSize, 0)
        # self.Bind(wx.EVT_BUTTON, self.ClickParaSetup, self.button1)

        self.button_ModelSelect = wx.Button(self.btnPanel, wx.ID_ANY, u"模型选择",
                                           wx.DefaultPosition, wx.DefaultSize, 0)
        self.Bind(wx.EVT_BUTTON, self.ClickModelSelect, self.button_ModelSelect)


        self.button_ImportData = wx.Button(self.btnPanel, wx.ID_ANY, u"数据导入",
                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.button_ImportData.Disable()
        self.Bind(wx.EVT_BUTTON, self.ClickImportData, self.button_ImportData)


        self.button2 = wx.Button(self.btnPanel, wx.ID_ANY, u"元模型建模",
                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.button2.Disable()
        self.Bind(wx.EVT_BUTTON, self.ClickSetup, self.button2)

        self.button3 = wx.Button(self.btnPanel, wx.ID_ANY, u"优化模型",
                                 wx.DefaultPosition, wx.DefaultSize, 0)
        self.button3.Disable()
        self.Bind(wx.EVT_BUTTON, self.ClickOptSetup, self.button3)


        # tabSizer.Add(self.button1, 0, wx.ALL, 5)
        tabSizer.Add(self.button_ModelSelect, 0, wx.ALL, 5)
        tabSizer.Add(self.button_ImportData, 0, wx.ALL, 5)
        tabSizer.Add(self.button2, 0, wx.ALL, 5)
        tabSizer.Add(self.button3, 0, wx.ALL, 5)
        tabSizer.Add(self.test_button, 0, wx.ALL, 5)

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

    def ClickTestPanel(self, event):
        self.showNotebook.TestPanel()

    # def ClickParaSetup(self, event):
    #     self.showNotebook.NewProj1()

    def ClickModelSelect(self, event):
        global n_id
        n_id = self.navTree.GetItemData(self.navTree.GetSelection())
        print n_id
        self.button_ImportData.Enable()

    def ClickImportData(self, event):
        self.showNotebook.ImportDataPanel()
        self.button2.Enable()

    def ClickSetup(self, event):
        self.showNotebook.BuildMetaPanel()
        self.button3.Enable()

    def ClickOptSetup(self, event):
        self.showNotebook.OptPanel()
