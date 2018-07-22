# -*- coding: utf-8 -*-

from __future__ import division
from wx import aui
import wx
import GenericAlgorithm
import BuildMetaModel
import CalibrationPanel as cp
import wx.grid
import wx.lib.scrolledpanel as scrolled
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

sym1=1
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

    def ImportDataPanel_NEW(self, pProj = 0):
        #self.panel_import = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
                                   # wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.show_panel = scrolled.ScrolledPanel(self, -1,
                                                     style=wx.TAB_TRAVERSAL | wx.SUNKEN_BORDER, name="panel1")
        self.show_panel.SetAutoLayout(1)
        self.show_panel.SetupScrolling()

        self.AddPage(self.show_panel, u"数据导入", True, wx.NullBitmap)
        show_panel = self.show_panel

        self.static_text_real = wx.StaticText(show_panel, label='请输入真实认知不确定参数:')
        self.text_ctrl_real = wx.TextCtrl(show_panel, value='4,1,8')
        box_sizer_a = wx.BoxSizer(orient=wx.HORIZONTAL)
        box_sizer_a.Add(self.static_text_real)
        box_sizer_a.Add(self.text_ctrl_real)

        self.button_import = wx.Button(show_panel, label="点击导入数据")
        self.button_import.Bind(wx.EVT_BUTTON, self.onClick_button_import)

        box_sizer = wx.BoxSizer(orient=wx.VERTICAL)
        box_sizer.Add(box_sizer_a)
        box_sizer.Add(self.button_import)
        #box_sizer.Add(self.grid)
        show_panel.SetSizer(box_sizer)

        self.Show(True)

        show_panel.Layout()

    def onClick_button_import(self, event):
        self.button_import.Disable()
        show_panel = self.show_panel
        sizer = show_panel.GetSizer()

        self.real_cog_p_r = self.text_ctrl_real.GetLineText(0)
        self.text_ctrl_real.Disable()

        # sizer_A = wx.BoxSizer(orient=wx.HORIZONTAL)
        # self.grid1 = wx.grid.Grid(show_panel)
        # sizer_v1 = wx.BoxSizer(orient=wx.VERTICAL)
        # static_text_v1 = wx.StaticText(show_panel, label='认知不确定参数抽样取值结果')
        # sizer_v1.Add(static_text_v1)
        # sizer_v1.Add(self.grid1)
        # sizer_A.Add(sizer_v1)

        sizer_B = wx.BoxSizer(orient=wx.VERTICAL)
        self.grid2 = wx.grid.Grid(show_panel)
        sizer_v2 = wx.BoxSizer(orient=wx.VERTICAL)
        static_text_v2 = wx.StaticText(show_panel, label='固有不确定参数抽样取值结果')
        sizer_v2.Add(static_text_v2)
        sizer_v2.Add(self.grid2)
        sizer_B.Add(sizer_v2)

        sizer_a = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.grid3 = wx.grid.Grid(show_panel)
        sizer_v3 = wx.BoxSizer(orient=wx.VERTICAL)
        static_text_v3 = wx.StaticText(show_panel, label='计算一致性输入抽样取值结果')
        sizer_v3.Add(static_text_v3)
        sizer_v3.Add(self.grid3)
        sizer_a.Add(sizer_v3)

        self.grid5 = wx.grid.Grid(show_panel)
        sizer_v5 = wx.BoxSizer(orient=wx.VERTICAL)
        static_text_v5 = wx.StaticText(show_panel, label='计算一致性输出结果')
        sizer_v5.Add(static_text_v5)
        sizer_v5.Add(self.grid5)
        sizer_a.Add(sizer_v5)

        sizer_B.Add(sizer_a)

        sizer_b = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.grid4 = wx.grid.Grid(show_panel)
        sizer_v4 = wx.BoxSizer(orient=wx.VERTICAL)
        static_text_v4 = wx.StaticText(show_panel, label='对比验证输入抽样取值结果')
        sizer_v4.Add(static_text_v4)
        sizer_v4.Add(self.grid4)
        sizer_b.Add(sizer_v4)

        self.grid6 = wx.grid.Grid(show_panel)
        sizer_v6 = wx.BoxSizer(orient=wx.VERTICAL)
        static_text_v6 = wx.StaticText(show_panel, label='对比验证输出结果')
        sizer_v6.Add(static_text_v6)
        sizer_v6.Add(self.grid6)
        sizer_b.Add(sizer_v6)

        sizer_B.Add(sizer_b)

        # sizer_A.Add(sizer_B)

        sizer.Add(sizer_B)
        # self.grid = wx.grid.Grid(show_panel)
        # self.grid.CreateGrid(100, 100)
        # sizer.Add(self.grid)

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
        self.combobox.SetSelection(0)

        box_sizer_a = wx.BoxSizer(orient=wx.HORIZONTAL)
        box_sizer_a.Add(self.static_text_a)
        box_sizer_a.Add(self.combobox)

        self.combobox.Bind(wx.EVT_COMBOBOX, self.onSelect_combobox)

        box_sizer = wx.BoxSizer(orient=wx.VERTICAL)
        box_sizer.Add(box_sizer_a)

        show_panel.SetSizer(box_sizer)
        self.Show(True)
        show_panel.Layout()

    def BuildMetaPanel_NEW(self, pProj = 0):
        self.show_panel = scrolled.ScrolledPanel(self, -1,
                                                   style=wx.TAB_TRAVERSAL | wx.SUNKEN_BORDER, name="panel1")
        self.show_panel.SetAutoLayout(1)
        self.show_panel.SetupScrolling()
        self.AddPage(self.show_panel, u"元模型建模", True, wx.NullBitmap)
        show_panel = self.show_panel

        self.static_text_a = wx.StaticText(show_panel, -1, label="请选择一致性度量方法:")
        self.measure = ['欧式距离', '马氏距离']
        self.combobox_a = wx.ComboBox(self.show_panel, -1, choices=self.measure)
        self.combobox_a.SetSelection(0)
        self.combobox_a.Bind(wx.EVT_COMBOBOX, self.onSelect_combobox_a)
        box_sizer_a = wx.BoxSizer(orient=wx.HORIZONTAL)
        box_sizer_a.Add(self.static_text_a)
        box_sizer_a.Add(self.combobox_a)



        self.static_text_b = wx.StaticText(show_panel, -1, label="请选择一种建模方法:")
        self.methods = ['SVR', 'GPR', 'KRR']
        self.combobox_b = wx.ComboBox(self.show_panel, -1, choices=self.methods)
        self.combobox_b.SetSelection(0)
        self.combobox_b.Bind(wx.EVT_COMBOBOX, self.onSelect_combobox_b)

        box_sizer_b = wx.BoxSizer(orient=wx.HORIZONTAL)
        box_sizer_b.Add(self.static_text_b)
        box_sizer_b.Add(self.combobox_b)

        box_sizer = wx.BoxSizer(orient=wx.VERTICAL)
        box_sizer.Add(box_sizer_a)
        box_sizer.Add(box_sizer_b)

        self.button_1a = wx.Button(show_panel, label="元模型建模")
        self.button_1a.Bind(wx.EVT_BUTTON, self.onClick_button_1a)
        box_sizer.Add(self.button_1a)

        show_panel.SetSizer(box_sizer)
        self.sym=1
        self.Show(True)
        show_panel.Layout()

    def onSelect_combobox_a(self, event):
        pos = self.combobox_a.GetSelection()
        measure_name = self.measure[pos]
        global sym1
        if measure_name == "欧式距离":
            print ("欧式距离")
            sym1 = 1
        else:
            print ("马氏距离")
            sym1 = 2

    def onSelect_combobox_b(self, event):
        pos = self.combobox_b.GetSelection()
        method_name = self.methods[pos]
        if method_name == "SVR":
            print ("SVR")
            self.sym = 1
        elif method_name == "GPR":
            print ("GPR")
            self.sym = 2
        else:
            print ("KRR")
            self.sym = 3

    def onClick_button_1a(self, event):
        self.combobox_a.Disable()
        self.combobox_b.Disable()
        self.button_1a.Disable()
        global sym1
        print 'self.sym: %d'%(self.sym)
        print 'sym1: %d'%(sym1)
        show_panel = self.show_panel
        sizer = show_panel.GetSizer()

        #sizer_1 = wx.BoxSizer(orient=wx.HORIZONTAL)
        static_text = wx.StaticText(show_panel, label='一致性度量输出')
        static_text1 = wx.StaticText(show_panel, label='   ')
        self.grid_out = wx.grid.Grid(show_panel)
        #self.sw = csw(show_panel)

        sizer.Add(static_text)
        sizer.Add(self.grid_out)
        sizer.Add(static_text1)

        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.axes.set(xlabel='Sample Numbers', ylabel='Consistency measure', title='Forecast accuracy map')
        self.canvas = FigureCanvas(show_panel, -1, self.figure)

        sizer.Add(self.canvas)
        #sizer.Add(self.sw, flag=wx.EXPAND, proportion=wx.EXPAND)

        show_panel.Layout()
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

    def OptPanel_NEW(self, pProj = 0):
        self.show_panel = scrolled.ScrolledPanel(self, -1,
                                                 style=wx.TAB_TRAVERSAL | wx.SUNKEN_BORDER, name="panel1")
        self.show_panel.SetAutoLayout(1)
        self.show_panel.SetupScrolling()
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
        self.button_1.Disable()
        show_panel = self.show_panel
        sizer = show_panel.GetSizer()

        sizer_a = wx.BoxSizer(orient=wx.VERTICAL)
        self.grid1 = wx.grid.Grid(show_panel)
        sizer_v1 = wx.BoxSizer(orient=wx.VERTICAL)
        static_text_v1 = wx.StaticText(show_panel, label='每次迭代的度量取值结果')
        sizer_v1.Add(static_text_v1)
        sizer_v1.Add(self.grid1)

        self.grid2 = wx.grid.Grid(show_panel)
        sizer_v2 = wx.BoxSizer(orient=wx.VERTICAL)
        static_text_v2 = wx.StaticText(show_panel, label='每次迭代的最佳认知参数取值结果')
        sizer_v2.Add(static_text_v2)
        sizer_v2.Add(self.grid2)

        sizer_a.Add(sizer_v1)
        sizer_a.Add(sizer_v2)

        sizer_b = wx.BoxSizer(orient=wx.VERTICAL)
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        #self.axes.set(xlabel='Number of iterations', ylabel='Consistency measure', title='Iterative metric trends')
        self.canvas = FigureCanvas(show_panel, -1, self.figure)

        self.figure2 = Figure()
        self.axes2 = self.figure2.add_subplot(111)
        #self.axes2.set(xlabel='Number of iterations', ylabel='Consistency measure', title='Compare verification trends')
        self.canvas2 = FigureCanvas(show_panel, -1, self.figure2)

        sizer_b.Add(self.canvas)
        sizer_b.Add(self.canvas2)

        sizer_c = wx.BoxSizer(orient=wx.HORIZONTAL)
        sizer_c.Add(sizer_a)
        sizer_c.Add(sizer_b)

        sizer.Add(sizer_c)

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