# -*- coding: utf-8 -*-

import wx
import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import UPNavPanel
import UTNotebook

# import import_file


"""不确定性传播分析Panel类"""
class UncertaintyPropagationPanel(wx.Panel):
    
    def __init__(self, parent=None):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, 
                          wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.InitUI()

    def InitUI(self):
        # 上方按钮区域panel
        self.btnPanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
                                 wx.Size(-1, 40), wx.TAB_TRAVERSAL)
        tabSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btnPanel.SetSizer(tabSizer)

        """ 添加菜单按钮 begins """
        self.button_design = wx.Button(self.btnPanel, wx.ID_ANY, u"试验设计", wx.DefaultPosition,
                                 wx.DefaultSize, 0)
        self.button_design.SetBitmap(wx.Bitmap('icon/btn_show1.tga'))
        self.button_design.Bind(wx.EVT_LEFT_DOWN, self.ClickModelManage)
        tabSizer.Add(self.button_design, 0, wx.ALL, 5)

        self.button_sample = wx.Button(self.btnPanel, wx.ID_ANY, u"抽样设置", wx.DefaultPosition,
                                 wx.DefaultSize, 0)
        self.button_sample.Bind(wx.EVT_BUTTON, self.sampling_settings)
        tabSizer.Add(self.button_sample, 0, wx.ALL, 5)

        self.button_plan = wx.Button(self.btnPanel, wx.ID_ANY, u"传播分析", wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        self.button_plan.Bind(wx.EVT_BUTTON, self.Test)
        tabSizer.Add(self.button_plan, 0, wx.ALL, 5)
        """ 添加菜单按钮 ends """

        # 下方导航树及展示界面panel
        self.displayPanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
                                     wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.navTree = UPNavPanel.NavPanel(self.displayPanel)
        self.showNotebook = UTNotebook.UTNotebook(self.displayPanel)
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

    def sampling_settings(self, event):
        """ 按下 抽样方法 按钮 """
        self.showNotebook.up_select_method()

    def ClickModelManage(self, event):
        """ 按下 试验设计 按钮 """
        self.showNotebook.ShowArg(None)

    def Test(self, event):
        """ 按下 实验方案 按钮 """
        self.showNotebook.up_test()