# -*- coding: utf-8 -*-

###########################################################################
# Created on 2018.5.10
###########################################################################
from __future__ import print_function
from __future__ import print_function
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

        self.m_staticText_erp_size = wx.StaticText(scrollPanel, wx.ID_ANY, u"固有不确定性参数抽样数量：",
                                               wx.DefaultPosition, wx.DefaultSize, 0)
        self.gbSizer.Add(self.m_staticText_erp_size, wx.GBPosition(2, 4),
                               wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_textCtrl_erp_size = wx.TextCtrl(scrollPanel, wx.ID_ANY, wx.EmptyString,
                                           wx.DefaultPosition, wx.Size(180, -1), 0)
        self.gbSizer.Add(self.m_textCtrl_erp_size, wx.GBPosition(2, 5),
                               wx.GBSpan(1, 3), wx.ALL, 5)

        self.m_staticText_esp_size = wx.StaticText(scrollPanel, wx.ID_ANY, u"认知不确定性参数抽样数量：",
                                               wx.DefaultPosition, wx.DefaultSize, 0)
        self.gbSizer.Add(self.m_staticText_esp_size, wx.GBPosition(3, 4),
                         wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_textCtrl_esp_size = wx.TextCtrl(scrollPanel, wx.ID_ANY, wx.EmptyString,
                                           wx.DefaultPosition, wx.Size(180, -1), 0)
        self.gbSizer.Add(self.m_textCtrl_esp_size, wx.GBPosition(3, 5),
                         wx.GBSpan(1, 3), wx.ALL, 5)

        self.m_staticText_input_size = wx.StaticText(scrollPanel, wx.ID_ANY, u"仿真系统输入参数抽样数量：",
                                               wx.DefaultPosition, wx.DefaultSize, 0)
        self.gbSizer.Add(self.m_staticText_input_size, wx.GBPosition(4, 4),
                         wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_textCtrl_input_size = wx.TextCtrl(scrollPanel, wx.ID_ANY, wx.EmptyString,
                                           wx.DefaultPosition, wx.Size(180, -1), 0)
        self.gbSizer.Add(self.m_textCtrl_input_size, wx.GBPosition(4, 5),
                         wx.GBSpan(1, 3), wx.ALL, 5)

        ''' 确认和重置按钮的panel begins '''
        self.m_button_ok = wx.Button(scrollPanel, wx.ID_ANY, u"确定", wx.DefaultPosition, wx.Size(80, -1), 0)
        self.m_button_ok.Bind(wx.EVT_BUTTON, self.create_sample)
        self.gbSizer.Add(self.m_button_ok, wx.GBPosition(5, 4),
                         wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_button_reset = wx.Button(scrollPanel, wx.ID_ANY, u"重置", wx.DefaultPosition, wx.Size(80, -1), 0)
        self.m_button_reset.Bind(wx.EVT_BUTTON, self.reset_settings)
        self.gbSizer.Add(self.m_button_reset, wx.GBPosition(5, 5),
                         wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_button_show = wx.Button(scrollPanel, wx.ID_ANY, u"展示结果", wx.DefaultPosition, wx.Size(80, -1), 0)
        self.m_button_show.Bind(wx.EVT_BUTTON, self.show_result)
        self.gbSizer.Add(self.m_button_show, wx.GBPosition(6, 4),
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
        self.Er_p_size_of_par = 0
        self.Es_p_size_of_par = 0
        self.input_size_of_par = 0

        self.Er_p_name = []
        self.Es_p_name = []
        self.input_name = []
        i = 0
        for pt in self.param.partype:
            if (pt == 1):
                self.Er_p_size_of_par += 1
                self.Er_p_name.append(self.param.name[i])
            else:
                if(pt == 2):
                    self.Es_p_size_of_par += 1
                    self.Es_p_name.append(self.param.name[i])
                else:
                    self.input_size_of_par += 1
                    self.input_name.append(self.param.name[i])
            i += 1
        pass

    # 等待写操作完成的方法
    # FIXME: 进度条控制没有添加完成
    def wait_writing(self,range):
        self.end = 0
        try:
            thread.start_new_thread(self.writing, ())
        except:
            print("Error: unable to start thread")


    # FIXME: 进度条由此处发消息进行控制
    def writing(self):
        # 循环抽样并写入所有的参数的抽样结果 生成抽样实验方案
        self.count = 0
        self.results = []
        for p in self.param.para:
            self.get_Result_Of_Paras(self.count)

            self.count += 1
        self.SQLrun()
        print('Finished creating samples.')

        self.end = 1

    def draw_table(self, i, x):
        results = self.type_result[i]
        size = self.ssize[i]
        size_of_par = self.size_of_par[i]
        names = self.names[i]
        scrollPanel = self.scrolledWindow
        '''Table'''
        self.m_grid4 = wx.grid.Grid(scrollPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)

        # result = Sql.show_sampling_result(self.param.name[0])

        # 先通过一个名字获得结果长度建表 再在后面获取每行每列值
        # Grid
        self.m_grid4.CreateGrid(size, size_of_par)
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
        for namei in names:
            self.m_grid4.SetColLabelValue(i, namei)
            i += 1

        # 设置内容
        j = 0
        for result in results:
            i = 0
            for row in result:
                # 截段输出 numpy 抽样结果过长
                self.m_grid4.SetCellValue(i, j, str(("%.3f" % row)))
                i = i + 1
            j += 1
        '''Table ends'''
        self.gbSizer.Add(self.m_grid4, wx.GBPosition(x, 4),
                         wx.GBSpan(1, 3), wx.ALL, 5)
        ''' table的panel ends '''
        # self.bSizer_main.Add(self.m_panel_table, 1, wx.EXPAND | wx.ALL, 5)
        # self.Centre(wx.BOTH)
        self.Refresh()

    # 展示结果的方法
    # 抽样和显示抽样结果在一个类里面 反复读写数据库 没有必要 直接读取类的成员变量即可
    def show_result(self, event):
        self.m_staticText_input_size = wx.StaticText(self.scrolledWindow, wx.ID_ANY, u"固有不确定性参数：",
                                                     wx.DefaultPosition, wx.DefaultSize, 0)
        self.gbSizer.Add(self.m_staticText_input_size, wx.GBPosition(7, 4),
                         wx.GBSpan(1, 1), wx.ALL, 5)
        self.draw_table(1,8)

        self.m_staticText_input_size = wx.StaticText(self.scrolledWindow, wx.ID_ANY, u"认知不确定性参数：",
                                                     wx.DefaultPosition, wx.DefaultSize, 0)
        self.gbSizer.Add(self.m_staticText_input_size, wx.GBPosition(9, 4),
                         wx.GBSpan(1, 1), wx.ALL, 5)
        self.draw_table(2,10)

        self.m_staticText_input_size = wx.StaticText(self.scrolledWindow, wx.ID_ANY, u"输入参数：",
                                                     wx.DefaultPosition, wx.DefaultSize, 0)
        self.gbSizer.Add(self.m_staticText_input_size, wx.GBPosition(11, 4),
                         wx.GBSpan(1, 1), wx.ALL, 5)
        self.draw_table(0,12)

    def create_sample(self, event):
        """ 用户点击确定按钮后开始抽样并写入数据库 """
        self.Er_p_size = int(self.m_textCtrl_erp_size.GetValue())
        self.Es_p_size = int(self.m_textCtrl_esp_size.GetValue())
        self.input_size = int(self.m_textCtrl_input_size.GetValue())
        self.ssize = self.input_size, self.Er_p_size, self.Es_p_size
        self.size_of_par = self.input_size_of_par, self.Er_p_size_of_par, self.Es_p_size_of_par
        self.names = self.input_name, self.Er_p_name, self.Es_p_name
        self.type_result = [],[],[]
        print (self.param.para[0])
        self.stra = 0  # 具体策略编号

        # FIXME: 这里由于元组的问题，必须传入足够多的参数，传入para的数量是现有分布所需参数个数的最大值

        Sql.clear_sampling_result() # 先清空历史数据
        Sql.clear_sampling_result_of_model(self.param.model_id)
        # 进度条UI放入子线程：
        try:
            thread.start_new_thread(self.wait_writing, (len(self.param.para[0]),))
        except:
            print("Error: unable to start thread")

    def reset_settings(self, event):
        """ 重置窗口中以输入的数据 """
        self.m_textCtrl_erp_size.Clear()
        self.m_textCtrl_esp_size.Clear()
        self.m_textCtrl_input_size.Clear()

    def get_Result_Of_Paras(self, i):
        # 判断长度防止元祖越界
        result = 0
        #FIXME:情况不全
        if len(self.param.para[i]) is 3:
            result = strategy[self.method_name[i]].GetResult(self.ssize[self.param.partype[i]], kind_dict[self.param.dtype[i]],
                                                         self.param.para[i][0], self.param.para[i][1], self.param.para[i][2])
        if len(self.param.para[i]) is 2:
            result = strategy[self.method_name[i]].GetResult(self.ssize[self.param.partype[i]], kind_dict[self.param.dtype[i]],
                                                self.param.para[i][0], self.param.para[i][1])
        self.type_result[self.param.partype[i]].append(result)
        self.results.append(result)

    def SQLrun(self):
        Sql.insert_sampling_result(self.param.name, self.results)
        Sql.insert_sampling_results(self.param.name, self.results,self.method_name)


