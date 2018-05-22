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
    def __init__(self, parent, name ,kind=['normal'], *para):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition,
                          wx.DefaultSize, wx.TAB_TRAVERSAL)

        self.kind = kind  # 分布类型
        self.para = para  # 参数

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENU))

        self.bSizer_main = wx.BoxSizer(wx.VERTICAL)

        ''' 样本大小的panel begins '''
        self.m_panel_size = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.m_panel_size.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_SCROLLBAR))

        self.bSizer_size = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText_size = wx.StaticText(self.m_panel_size, wx.ID_ANY, u"数    量", wx.DefaultPosition,
                                               wx.DefaultSize, 0)
        self.m_staticText_size.Wrap(-1)
        self.bSizer_size.Add(self.m_staticText_size, 0, wx.ALL, 5)

        self.m_textCtrl_size = wx.TextCtrl(self.m_panel_size, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.bSizer_size.Add(self.m_textCtrl_size, 0, wx.ALL, 5)

        self.m_panel_size.SetSizer(self.bSizer_size)
        self.m_panel_size.Layout()
        self.bSizer_size.Fit(self.m_panel_size)
        ''' 样本大小的panel ends '''

        self.bSizer_main.Add(self.m_panel_size, 1, wx.EXPAND | wx.ALL, 5)

        ''' 确认和重置按钮的panel begins '''
        self.m_panel_ok = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.m_panel_ok.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_SCROLLBAR))

        bSizer_ok = wx.BoxSizer(wx.HORIZONTAL)

        self.m_button_ok = wx.Button(self.m_panel_ok, wx.ID_ANY, u"确定", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer_ok.Add(self.m_button_ok, 0, wx.ALL, 5)
        self.m_button_ok.Bind(wx.EVT_BUTTON, self.create_sample)

        bSizer_ok.AddSpacer(70)

        self.m_button_reset = wx.Button(self.m_panel_ok, wx.ID_ANY, u"重置", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer_ok.Add(self.m_button_reset, 0, wx.ALL, 5)
        self.m_button_reset.Bind(wx.EVT_BUTTON, self.reset_settings)

        self.m_button_show = wx.Button(self.m_panel_ok, wx.ID_ANY, u"展示结果", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer_ok.Add(self.m_button_show, 0, wx.ALL, 5)
        self.m_button_show.Bind(wx.EVT_BUTTON, self.show_result)

        self.m_panel_ok.SetSizer(bSizer_ok)
        self.m_panel_ok.Layout()
        bSizer_ok.Fit(self.m_panel_ok)
        ''' 确认和重置按钮的panel ends '''
        self.bSizer_main.Add(self.m_panel_ok, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(self.bSizer_main)
        self.Layout()
        self.Centre(wx.BOTH)

    def __del__(self):
        pass

    def set_kind_and_para_and_name(self, kind,name,method ,*para):
        """ 外部设置分布类型、抽样方法和参数以及参数名称 """
        self.kind = kind
        self.para = para
        self.name = name
        self.method_name = method

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
        for p in self.para:
            print("===========WRITING==============")
            self.getResultOfParas(tuple(p), self.kind[self.count], self.method_name[self.count], self.ssize, self.name[self.count])
            self.count += 1
        print 'Finished creating samples.'
        self.end = 1

    # 展示结果的方法
    # FIXME: 布局有点混乱 会覆盖前面的输入框
    def show_result(self, event):
        '''Table'''
        self.m_panel_table = wx.Panel(self, wx.ID_ANY, (1000,200), wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.m_panel_table.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_SCROLLBAR))
        bSizer_table = wx.BoxSizer(wx.HORIZONTAL)
        self.m_grid4 = wx.grid.Grid(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        result = Sql.show_sampling_result(self.name[0])
        # 先通过一个名字获得结果长度建表 再在后面获取每行每列值
        # Grid
        self.m_grid4.CreateGrid(len(result), len(self.name))
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
        for namei in self.name:
            self.m_grid4.SetColLabelValue(i, namei)
            i += 1

        # 根据参数名获取相应的抽样数据
        results = []
        for n in self.name: # 查询每个name 得到的列表result 追加在二维列表results中 生成实验方案
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
        """"""
        bSizer_table.Add(self.m_grid4, 0, wx.ALL, 5)

        self.m_panel_table.SetSizer(bSizer_table)
        self.m_panel_table.Layout()
        bSizer_table.Fit(self.m_panel_table)
        ''' table的panel ends '''
        self.bSizer_main.Add(self.m_panel_table, 1, wx.EXPAND | wx.ALL, 5)
        self.Centre(wx.BOTH)
        self.Refresh()

    def create_sample(self, event):
        """ 用户点击确定按钮后开始抽样并写入数据库 """
        self.ssize = int(self.m_textCtrl_size.GetValue())
        print self.para[0]
        self.stra = 0  # 具体策略编号

        # FIXME: 这里由于元组的问题，必须传入足够多的参数，传入para的数量是现有分布所需参数个数的最大值
        # 此处的para是只有一个元素且元素为一个元祖的元祖 而我们需要的是这个元素作为para 则 作以下处理
        self.para = self.para[0]


        Sql.clear_sampling_result() # 先清空历史数据
        # 进度条UI放入子线程：
        try:
            thread.start_new_thread(self.wait_writing, (len(self.para),))
        except:
            print "Error: unable to start thread"




    def reset_settings(self, event):
        """ 重置窗口中以输入的数据 """
        self.m_textCtrl_size.Clear()

    def getResultOfParas(self,para,kind,m_name,size,name):
        # 判断长度防止元祖越界
        result = 0
        #FIXME:情况不全
        if len(para) is 3:
            result = strategy[m_name].GetResult(size, kind_dict[kind],
                                              para[0], para[1], para[2])
        if len(para) is 2:
            result = strategy[m_name].GetResult(size, kind_dict[kind],
                                              para[0], para[1])

        # 进度条显示不应该放入子线程
        self.SQLrun(name, result)
        # 网络操作放入子线程：
        # try:
        #     thread.start_new_thread(self.SQLrun, (name, result,))
        # except:
        #     print "Error: unable to start thread"

    def SQLrun(self,arg_name, result):
        Sql.insert_sampling_result(arg_name, result)
