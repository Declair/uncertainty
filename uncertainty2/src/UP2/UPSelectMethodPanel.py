# -*- coding: utf-8 -*-

###########################################################################
# Created on 2018.5.10
###########################################################################
import thread
import wx
import wx.xrc
from wx import grid
import ProcessBar as pb

from SamplingMethod import *
import Sql

class SelectSamplingMethodPanel(wx.Panel):
    count = 0
    strategystr = {'random':1,'LHS':2}
    def __init__(self, parent):
        """ 初始化 """
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                          wx.DefaultSize, wx.TAB_TRAVERSAL)
        # self 的布局，只有 scrollPanel 一个元素
        self.bSizer = wx.BoxSizer(wx.VERTICAL)
        # 为实现滚动条加入 scrollPanel
        self.scrolledWindow = wx.ScrolledWindow(self, wx.ID_ANY,
                                                      wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL | wx.VSCROLL)
        self.scrolledWindow.SetScrollRate(5, 5)
        scrollPanel = self.scrolledWindow
        # scrollPanel 的布局，元素为显示的控件
        self.gbSizer = wx.GridBagSizer(5, 5)
        self.gbSizer.SetFlexibleDirection(wx.BOTH)
        self.gbSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText_size = wx.StaticText(scrollPanel, wx.ID_ANY, u"数    量：",
                                               wx.DefaultPosition, wx.DefaultSize, 0)
        self.gbSizer.Add(self.m_staticText_size, wx.GBPosition(2, 4),
                               wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_textCtrl_size = wx.TextCtrl(scrollPanel, wx.ID_ANY, wx.EmptyString,
                                           wx.DefaultPosition, wx.Size(180, -1), 0)
        self.gbSizer.Add(self.m_textCtrl_size, wx.GBPosition(2, 5),
                               wx.GBSpan(1, 3), wx.ALL, 5)

        ''' 确认和重置按钮的panel begins '''
        self.m_button_ok = wx.Button(scrollPanel, wx.ID_ANY, u"确定", wx.DefaultPosition, wx.Size(80, -1), 0)
        self.m_button_ok.Bind(wx.EVT_BUTTON, self.create_sample)
        self.gbSizer.Add(self.m_button_ok, wx.GBPosition(3, 4),
                         wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_button_reset = wx.Button(scrollPanel, wx.ID_ANY, u"重置", wx.DefaultPosition, wx.Size(80, -1), 0)
        self.m_button_reset.Bind(wx.EVT_BUTTON, self.reset_settings)
        self.gbSizer.Add(self.m_button_reset, wx.GBPosition(3, 5),
                         wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_button_show = wx.Button(scrollPanel, wx.ID_ANY, u"展示结果", wx.DefaultPosition, wx.Size(80, -1), 0)
        self.m_button_show.Bind(wx.EVT_BUTTON, self.show_result)
        self.gbSizer.Add(self.m_button_show, wx.GBPosition(4, 4),
                         wx.GBSpan(1, 1), wx.ALL, 5)
        ''' 确认和重置按钮的panel ends '''

        scrollPanel.SetSizer(self.gbSizer)
        scrollPanel.Layout()
        self.bSizer.Add(scrollPanel, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(self.bSizer)
        self.Layout()
        self.Centre(wx.BOTH)

    def __del__(self):
        pass

    def set_up(self, p, method):
        """ 外部设置分布类型、抽样方法和参数以及参数名称等 """
        '''用类传递'''
        self.method_name = method
        self.param = p
        pass

    # 等待写操作完成的方法
    # FIXME: 进度条控制没有添加完成
    def wait_writing(self,range):
        self.end = 0
        try:
            thread.start_new_thread(self.writing, ())
        except:
            print "Error: unable to start thread"


    # FIXME: 进度条由此处发消息进行控制
    def writing(self):
        # 循环抽样并写入所有的参数的抽样结果 生成抽样实验方案
        self.count = 0
        for p in self.param.para:
            print("===========WRITING==============")
            self.get_Result_Of_Paras(self.count)
            self.count += 1
        print 'Finished creating samples.'
        self.end = 1

    # 展示结果的方法
    def show_result(self, event):
        scrollPanel = self.scrolledWindow
        '''Table'''
        self.m_grid4 = wx.grid.Grid(scrollPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)

        result = Sql.show_sampling_result(self.param.name[0])
        # 先通过一个名字获得结果长度建表 再在后面获取每行每列值
        # Grid
        self.m_grid4.CreateGrid(len(result), len(self.param.name))
        self.m_grid4.EnableEditing(True)
        self.m_grid4.EnableGridLines(True)
        self.m_grid4.EnableDragGridSize(False)
        self.m_grid4.SetMargins(0, 0)

        # Columns
        self.m_grid4.EnableDragColMove(False)
        self.m_grid4.EnableDragColSize(True)
        self.m_grid4.SetColLabelSize(30)
        self.m_grid4.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        i = 0
        for namei in self.param.name:
            self.m_grid4.SetColLabelValue(i, namei)
            i += 1

        # 根据参数名获取相应的抽样数据
        results = []
        for n in self.param.name: # 查询每个name 得到的列表result 追加在二维列表results中 生成实验方案
            result = Sql.show_sampling_result(n)
            results.append(result)

        # 设置内容
        j = 0
        for result in results:
            i = 0
            for row in result:
                self.m_grid4.SetCellValue(i, j, str(row[0]))
                i = i + 1
            j += 1
        '''Table ends'''

        self.gbSizer.Add(self.m_grid4, wx.GBPosition(5, 4),
                         wx.GBSpan(1, 3), wx.ALL, 5)
        ''' table的panel ends '''
        # self.bSizer_main.Add(self.m_panel_table, 1, wx.EXPAND | wx.ALL, 5)
        # self.Centre(wx.BOTH)
        self.Refresh()

    def create_sample(self, event):
        """ 用户点击确定按钮后开始抽样并写入数据库 """
        self.ssize = int(self.m_textCtrl_size.GetValue())
        print self.param.para[0]
        self.stra = 0  # 具体策略编号

        # FIXME: 这里由于元组的问题，必须传入足够多的参数，传入para的数量是现有分布所需参数个数的最大值

        Sql.clear_sampling_result() # 先清空历史数据
        # 进度条UI放入子线程：
        try:
            thread.start_new_thread(self.wait_writing, (len(self.param.para[0]),))
        except:
            print "Error: unable to start thread"

    def reset_settings(self, event):
        """ 重置窗口中以输入的数据 """
        self.m_textCtrl_size.Clear()

    def get_Result_Of_Paras(self,i):
        # 判断长度防止元祖越界
        result = 0
        #FIXME:情况不全
        if len(self.param.para[i]) is 3:
            result = strategy[self.method_name[i]].GetResult(self.ssize, kind_dict[self.param.dtype[i]],
                                                         self.param.para[i][0], self.param.para[i][1], self.param.para[i][2])
        if len(self.param.para[i]) is 2:
            result = strategy[self.method_name[i]].GetResult(self.ssize, kind_dict[self.param.dtype[i]],
                                                self.param.para[i][0], self.param.para[i][1])

        # 进度条显示不应该放入子线程
        self.SQLrun(self.param.name[i], result)
        # 网络操作放入子线程：
        # try:
        #     thread.start_new_thread(self.SQLrun, (name, result,))
        # except:
        #     print "Error: unable to start thread"

    def SQLrun(self,arg_name, result):
        Sql.insert_sampling_result(arg_name, result)


