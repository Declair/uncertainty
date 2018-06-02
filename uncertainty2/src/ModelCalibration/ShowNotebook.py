# -*- coding: utf-8 -*-

from __future__ import division
from wx import aui
import wx
import GenericAlgorithm
import BuildMetaModel
from CustomedScrolledWindow import CustomedScrolledWindow as csw
import CalibrationPanel as cp

class ShowNotebook(aui.AuiNotebook):
    
    def __init__(self, parent = None):
        
        aui.AuiNotebook.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, 
                                 wx.DefaultSize, aui.AUI_NB_DEFAULT_STYLE)

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

    def onClick_button_import(self, event):
        show_panel = self.panel_import
        sizer = show_panel.GetSizer()

        self.sw = csw(show_panel)

        sizer.Add(self.sw, flag=wx.EXPAND, proportion=wx.EXPAND)

        show_panel.Layout()

        BuildMetaModel.importData(self, cp.n_id)

    def BuildMetaPanel(self, pProj = 0):
        self.show_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, 
                                   wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.AddPage(self.show_panel, u"元模型建模", True, wx.NullBitmap)
        show_panel = self.show_panel

        self.static_text_a = wx.StaticText(show_panel, -1, label="建模方法:")

        self.methods = ['SVR', 'GPR', 'KRR']
        self.combobox = wx.ComboBox(self.show_panel, -1, choices=self.methods)

        box_sizer_a = wx.BoxSizer(orient=wx.HORIZONTAL)
        box_sizer_a.Add(self.static_text_a)
        box_sizer_a.Add(self.combobox)

        self.combobox.Bind(wx.EVT_COMBOBOX, self.onSelect_combobox)

        box_sizer = wx.BoxSizer(orient=wx.VERTICAL)
        box_sizer.Add(box_sizer_a)

        show_panel.SetSizer(box_sizer)
        self.Show(True)
        show_panel.Layout()

    def onSelect_combobox(self, event):
        pos = self.combobox.GetSelection()
        method_name = self.methods[pos]
        if method_name == "SVR":
            print ("SVR")
            self.sym = 1
            show_panel = self.show_panel
            sizer = show_panel.GetSizer()

            self.button_1a = wx.Button(show_panel, label="元模型建模")
            self.button_1a.Bind(wx.EVT_BUTTON, self.onClick_button_1a)

            self.sw = csw(show_panel)

            sizer.Add(self.button_1a)
            sizer.Add(self.sw, flag=wx.EXPAND, proportion=wx.EXPAND)

            show_panel.Layout()
        elif method_name == "GPR":
            print ("GPR")
            self.sym = 2

            show_panel = self.show_panel
            sizer = show_panel.GetSizer()

            self.button_1a = wx.Button(show_panel, label="元模型建模")
            self.button_1a.Bind(wx.EVT_BUTTON, self.onClick_button_1a)

            self.sw = csw(show_panel)

            sizer.Add(self.button_1a)
            sizer.Add(self.sw, flag=wx.EXPAND, proportion=wx.EXPAND)

            show_panel.Layout()
        else:
            print ("KRR")
            self.sym = 3

            show_panel = self.show_panel
            sizer = show_panel.GetSizer()

            self.button_1a = wx.Button(show_panel, label="元模型建模")
            self.button_1a.Bind(wx.EVT_BUTTON, self.onClick_button_1a)

            self.sw = csw(show_panel)

            sizer.Add(self.button_1a)
            sizer.Add(self.sw, flag=wx.EXPAND, proportion=wx.EXPAND)
            show_panel.Layout()

    def onClick_button_1a(self, event):
        if self.sym == 1:
            self.svr = BuildMetaModel.buildSVR(self, BuildMetaModel.cog_p, BuildMetaModel.inh_p, BuildMetaModel.output1, BuildMetaModel.input_v1)#, cus_C, cus_epsilon, cus_kernel)
        elif self.sym == 2:
            self.gpr = BuildMetaModel.buildGPR(self, BuildMetaModel.cog_p, BuildMetaModel.inh_p, BuildMetaModel.output1, BuildMetaModel.input_v1)#, cus_alpha)
        else:
            self.bayes = BuildMetaModel.buildKRR(self, BuildMetaModel.cog_p, BuildMetaModel.inh_p, BuildMetaModel.output1, BuildMetaModel.input_v1)#, cus_n_iter, cus_tol)


    def OptPanel(self, pProj = 0):
        self.show_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
                                   wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.AddPage(self.show_panel, u"优化设置", True, wx.NullBitmap)
        show_panel = self.show_panel

        self.static_text_1 = wx.StaticText(show_panel, -1, label="群体总数:")
        self.text_ctrl_1 = wx.TextCtrl(show_panel, -1, value='2000')
        self.static_text_2 = wx.StaticText(show_panel, -1, label="交叉概率:")
        self.text_ctrl_2 = wx.TextCtrl(show_panel, -1, value='0.5')
        self.static_text_3 = wx.StaticText(show_panel, -1, label="变异概率:")
        self.text_ctrl_3 = wx.TextCtrl(show_panel, -1, value='0.05')
        self.static_text_4 = wx.StaticText(show_panel, -1, label="迭代次数:")
        self.text_ctrl_4 = wx.TextCtrl(show_panel, -1, value='15')

        self.button_1 = wx.Button(show_panel, label="点击开始校准")
        self.button_1.Bind(wx.EVT_BUTTON, self.onClick_button_1)

        box_sizer = wx.BoxSizer(orient=wx.VERTICAL)

        box_sizer_1 = wx.BoxSizer(orient=wx.HORIZONTAL)
        box_sizer_1.Add(self.static_text_1)
        box_sizer_1.Add(self.text_ctrl_1)

        box_sizer_2 = wx.BoxSizer(orient=wx.HORIZONTAL)
        box_sizer_2.Add(self.static_text_2)
        box_sizer_2.Add(self.text_ctrl_2)

        box_sizer_3 = wx.BoxSizer(orient=wx.HORIZONTAL)
        box_sizer_3.Add(self.static_text_3)
        box_sizer_3.Add(self.text_ctrl_3)

        box_sizer_4 = wx.BoxSizer(orient=wx.HORIZONTAL)
        box_sizer_4.Add(self.static_text_4)
        box_sizer_4.Add(self.text_ctrl_4)

        box_sizer.Add(box_sizer_1)
        box_sizer.Add(box_sizer_2)
        box_sizer.Add(box_sizer_3)
        box_sizer.Add(box_sizer_4)

        box_sizer.Add(self.button_1)

        show_panel.SetSizer(box_sizer)
        self.Show(True)

        show_panel.Layout()

    def onClick_button_1(self, event):
        show_panel = self.show_panel
        sizer = show_panel.GetSizer()

        self.sw = csw(show_panel)
        sizer.Add(self.sw, flag=wx.EXPAND, proportion=wx.EXPAND)
        show_panel.Layout()
        # print(self.text_ctrl_1.GetLineText(0))
        pn = int(self.text_ctrl_1.GetLineText(0))
        itn = int(self.text_ctrl_4.GetLineText(0))
        cp = float(self.text_ctrl_2.GetLineText(0))
        mp = float(self.text_ctrl_3.GetLineText(0))
        if self.sym == 1:
            GenericAlgorithm.GA(self, self.svr, pn, itn, cp, mp)
        elif self.sym == 2:
            GenericAlgorithm.GA(self, self.gpr, pn, itn, cp, mp)
        else:
            GenericAlgorithm.GA(self, self.bayes, pn, itn, cp, mp)