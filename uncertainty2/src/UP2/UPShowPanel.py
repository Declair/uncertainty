# -*- coding: utf-8 -*-

import wx
import numpy
from wx import grid
import Sql
from ModelCalibration import CalibrationPanel as CP
import matplotlib

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
from matplotlib.ticker import MultipleLocator, FuncFormatter

import pylab
import matplotlib.pyplot as plt

'''将绘图操作嵌入到wxpython'''
######################################################################################
class MPL_Panel_base(wx.Panel):
    ''''' #MPL_Panel_base面板,可以继承或者创建实例'''

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=-1)

        self.Figure = matplotlib.figure.Figure(figsize=(4, 3))
        self.axes = self.Figure.add_axes([0.1, 0.1, 0.8, 0.8])
        self.FigureCanvas = FigureCanvas(self, -1, self.Figure)

        self.NavigationToolbar = NavigationToolbar(self.FigureCanvas)

        self.StaticText = wx.StaticText(self, -1, label='Show Help String')

        self.SubBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SubBoxSizer.Add(self.NavigationToolbar, proportion=0, border=2, flag=wx.ALL | wx.EXPAND)
        self.SubBoxSizer.Add(self.StaticText, proportion=-1, border=2, flag=wx.ALL | wx.EXPAND)

        self.TopBoxSizer = wx.BoxSizer(wx.VERTICAL)
        self.TopBoxSizer.Add(self.SubBoxSizer, proportion=-1, border=2, flag=wx.ALL | wx.EXPAND)
        self.TopBoxSizer.Add(self.FigureCanvas, proportion=-10, border=2, flag=wx.ALL | wx.EXPAND)

        self.SetSizer(self.TopBoxSizer)

        ###方便调用
        self.pylab = pylab
        self.pl = pylab
        self.pyplot = plt
        self.numpy = numpy
        self.numpy = numpy
        self.plt = plt

    def UpdatePlot(self):
        '''''#修改图形的任何属性后都必须使用self.UpdatePlot()更新GUI界面 '''
        self.FigureCanvas.draw()

    def plot(self, *args, **kwargs):
        '''''#最常用的绘图命令plot '''
        self.axes.plot(*args, **kwargs)
        self.UpdatePlot()

    def semilogx(self, *args, **kwargs):
        ''''' #对数坐标绘图命令 '''
        self.axes.semilogx(*args, **kwargs)
        self.UpdatePlot()

    def semilogy(self, *args, **kwargs):
        ''''' #对数坐标绘图命令 '''
        self.axes.semilogy(*args, **kwargs)
        self.UpdatePlot()

    def loglog(self, *args, **kwargs):
        ''''' #对数坐标绘图命令 '''
        self.axes.loglog(*args, **kwargs)
        self.UpdatePlot()

    def grid(self, flag=True):
        ''''' ##显示网格  '''
        if flag:
            self.axes.grid()
        else:
            self.axes.grid(False)

    def title_MPL(self, TitleString="wxMatPlotLib Example In wxPython"):
        ''''' # 给图像添加一个标题   '''
        self.axes.set_title(TitleString)

    def xlabel(self, XabelString="X"):
        ''''' # Add xlabel to the plotting    '''
        self.axes.set_xlabel(XabelString)

    def ylabel(self, YabelString="Y"):
        ''''' # Add ylabel to the plotting '''
        self.axes.set_ylabel(YabelString)

    def xticker(self, major_ticker=1.0, minor_ticker=0.1):
        ''''' # 设置X轴的刻度大小 '''
        self.axes.xaxis.set_major_locator(MultipleLocator(major_ticker))
        self.axes.xaxis.set_minor_locator(MultipleLocator(minor_ticker))

    def yticker(self, major_ticker=1.0, minor_ticker=0.1):
        ''''' # 设置Y轴的刻度大小 '''
        self.axes.yaxis.set_major_locator(MultipleLocator(major_ticker))
        self.axes.yaxis.set_minor_locator(MultipleLocator(minor_ticker))

    def legend(self, *args, **kwargs):
        ''''' #图例legend for the plotting  '''
        self.axes.legend(*args, **kwargs)

    def xlim(self, x_min, x_max):
        ''' # 设置x轴的显示范围  '''
        self.axes.set_xlim(x_min, x_max)

    def ylim(self, y_min, y_max):
        ''' # 设置y轴的显示范围   '''
        self.axes.set_ylim(y_min, y_max)

    def savefig(self, *args, **kwargs):
        ''' #保存图形到文件 '''
        self.Figure.savefig(*args, **kwargs)

    def cla(self):
        ''' # 再次画图前,必须调用该命令清空原来的图形  '''
        self.axes.clear()
        self.Figure.set_canvas(self.FigureCanvas)
        self.UpdatePlot()

    def ShowHelpString(self, HelpString="Show Help String"):
        ''''' #可以用它来显示一些帮助信息,如鼠标位置等 '''
        self.StaticText.SetLabel(HelpString)

        ################################################################


class MPL_Panel(MPL_Panel_base):
    ''''' #MPL_Panel重要面板,可以继承或者创建实例 '''

    def __init__(self, parent):
        MPL_Panel_base.__init__(self, parent=parent)

        # 测试一下
        self.FirstPlot()


        # 仅仅用于测试和初始化,意义不大

    def FirstPlot(self):
        # self.rc('lines',lw=5,c='r')
        self.cla()
        x = numpy.arange(-5, 5, 0.25)
        y = numpy.sin(x)
        self.yticker(0.5, 0.1)
        self.xticker(1.0, 0.2)
        self.xlabel('X')
        self.ylabel('Y')
        self.title_MPL("图像")
        self.grid()
        self.plot(x, y, '--^g')


        ###############################################################################


class ShowPanel(wx.Panel):

    def __init__(self, parent = None):

        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                          wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DLIGHT))

        bSizer8 = wx.BoxSizer(wx.VERTICAL)
        """"""

        self.m_grid4 = wx.grid.Grid(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)

        # Grid
        self.m_grid4.CreateGrid(5, 4)
        self.m_grid4.EnableEditing(True)
        self.m_grid4.EnableGridLines(True)
        self.m_grid4.EnableDragGridSize(False)
        self.m_grid4.SetMargins(0, 0)

        # Columns
        self.m_grid4.EnableDragColMove(False)
        self.m_grid4.EnableDragColSize(True)
        self.m_grid4.SetColLabelSize(30)
        self.m_grid4.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        self.m_grid4.SetColLabelValue(0, "模型名称")
        self.m_grid4.SetColLabelValue(1, "参数名称")
        self.m_grid4.SetColLabelValue(2, "分布类型")
        self.m_grid4.SetColLabelValue(3, "分布参数")

        # Rows
        self.m_grid4.EnableDragRowSize(True)
        self.m_grid4.SetRowLabelSize(80)
        self.m_grid4.SetRowLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Label Appearance

        # Cell Defaults
        self.m_grid4.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_TOP)


        """"""
        bSizer8.Add(self.m_grid4, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(bSizer8)
        self.Layout()
        bSizer8.Fit(self)

    def set_name(self,name):
        self.name = name

class TestPanel(wx.Panel):

    def __init__(self,  parent = None, name=[]):

        global a_mat
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                          wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DLIGHT))

        self.BoxSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.MPL1 = MPL_Panel_base(self)
        self.BoxSizer.Add(self.MPL1, proportion=-1, border=2, flag=wx.ALL | wx.EXPAND)

        self.MPL2 = MPL_Panel_base(self)
        self.BoxSizer.Add(self.MPL2, proportion=-1, border=2, flag=wx.ALL | wx.EXPAND)

        self.RightPanel = wx.Panel(self, -1)
        self.BoxSizer.Add(self.RightPanel, proportion=0, border=2, flag=wx.ALL | wx.EXPAND)

        self.SetSizer(self.BoxSizer)

        # 创建FlexGridSizer
        self.FlexGridSizer = wx.FlexGridSizer(rows=9, cols=1, vgap=5, hgap=5)
        self.FlexGridSizer.SetFlexibleDirection(wx.BOTH)


        self.RightPanel.SetSizer(self.FlexGridSizer)


        # MPL2_Frame界面居中显示
        self.Centre(wx.BOTH)
        """"""

        # self.m_grid4 = wx.grid.Grid(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        #
        # # Grid
        # self.m_grid4.CreateGrid(5, 4)
        # self.m_grid4.EnableEditing(True)
        # self.m_grid4.EnableGridLines(True)
        # self.m_grid4.EnableDragGridSize(False)
        # self.m_grid4.SetMargins(0, 0)
        #
        # # Columns
        # self.m_grid4.EnableDragColMove(False)
        # self.m_grid4.EnableDragColSize(True)
        # self.m_grid4.SetColLabelSize(30)
        # self.m_grid4.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        # self.m_grid4.SetColLabelValue(0, "模型名称")
        # self.m_grid4.SetColLabelValue(1, "参数名称")
        # self.m_grid4.SetColLabelValue(2, "分布类型")
        # self.m_grid4.SetColLabelValue(3, "分布参数")
        #
        # # Rows
        # self.m_grid4.EnableDragRowSize(True)
        # self.m_grid4.SetRowLabelSize(80)
        # self.m_grid4.SetRowLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        #
        # # Label Appearance
        #
        # # Cell Defaults
        # self.m_grid4.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_TOP)


        """"""
        # bSizer8.Add(self.m_grid4, 1, wx.ALL | wx.EXPAND, 5)

        """实验 Start"""
        # FIXME: 字典临时代替表连接查询 规范统一数据库后更换为以查询表确定参数是 认知2、固有1还是输入0
        dict = {'x1': 0, 'x2': 0, 'x3': 0, 'a1': 2, 'a2': 2, 'a3': 1, 'a4': 1}
        # 根据参数名获取相应的抽样数据

        input_X = []
        Er_p = []
        Es_p = []

        results = input_X, Er_p, Es_p

        for n in name:  # 查询每个name 得到的列表result 追加在二维列表results中 生成实验方案
            result = list(Sql.show_sampling_result_with_type(n))
            results[dict[n]].append(result)


        # Er_p_m = numpy.zeros((len(Er_p),len(Er_p[0]) ))
        #
        # i = 0
        # j = 0
        # for erp in Er_p:
        #     for er in erp:
        #         Er_p_m[i][j] = er
        #         j += 1
        #     i += 1
        #
        # i_X_m = numpy.zeros((len(input_X), len(input_X[0])))
        #
        # i = 0
        # j = 0
        # for i_x_m in input_X:
        #     for i_x in i_x_m:
        #         i_X_m[i][j] = i_x
        #         j += 1
        #     i += 1

        fig = self.MPL1, self.MPL2

        mark = 0
        for i in Es_p:  # 每一组认知不确定参数
            a_mat = CP.inner_level_loop(numpy.matrix(numpy.array(i)), numpy.matrix(numpy.array(Er_p)), numpy.matrix(numpy.array(input_X)))
            print('获得的仿真输出:')
            print(a_mat)
            fig[mark].cla()  # 必须清理图形,才能显示下一幅图
            x = []
            y = []
            for xi in numpy.array(a_mat):
                x.append(xi[0])
                y.append(xi[1])
            fig[mark].plot(x,y)
            fig[mark].xticker(10e+03, 1e+03)
            fig[mark].yticker(10e+16, 1e+16)
            fig[mark].title_MPL(u"每一组认知不确定参数获得的仿真输出:")
            fig[mark].ShowHelpString(" ")
            fig[mark].grid()
            fig[mark].UpdatePlot()  # 必须刷新才能显示
            mark += 1

        
        """实验 End"""

    def set_name(self,name):
        self.name = name