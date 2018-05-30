# -*- coding: utf-8 -*-

from __future__ import division
from wx import aui
import wx
import mysql.connector
from mysql.connector import Error
import GA_f
import build_meta
from CustomedScrolledWindow import CustomedScrolledWindow as csw

class ShowNotebook(aui.AuiNotebook):
    
    def __init__(self, parent = None):
        
        aui.AuiNotebook.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, 
                                 wx.DefaultSize, aui.AUI_NB_DEFAULT_STYLE)

    def NewProj0(self, pProj = 0):
        self.show_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
                                   wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.AddPage(self.show_panel, u"数据库连接", True, wx.NullBitmap)
        show_panel = self.show_panel
        self.button_db = wx.Button(show_panel, label="导入数据")
        self.button_db.Bind(wx.EVT_BUTTON, self.onClick_button_db)
        self.text_static_db = wx.StaticText(show_panel, -1, label="")

        box_sizer = wx.BoxSizer(orient=wx.VERTICAL)
        box_sizer_db = wx.BoxSizer(orient=wx.HORIZONTAL)
        box_sizer_db.Add(self.button_db)
        box_sizer_db.Add(self.text_static_db)
        box_sizer.Add(box_sizer_db, flag=wx.EXPAND, proportion=wx.EXPAND)

        show_panel.SetSizer(box_sizer)
        self.Show(True)

        show_panel.Layout()

    def onClick_button_db(self, event):
        db_config = {
            'host': '118.89.198.205',
            'user': 'certainty',
            'password': 'Nuaa666',
            'port': 3306,
            'database': 'work',
            'charset': 'utf8'
        }

        # db_config = {
        #     'user': 'test_user1',
        #     'password': '1234',
        #     'database': 'test1',
        #     'charset': 'utf8'
        # }

        try:
            self.conn = mysql.connector.connect(**db_config)
            self.text_static_db.SetLabel(str(self.conn.connection_id))
        except Error as e:
            print(e)
        finally:
            print '导入数据'


    def NewProj1(self, pProj = 0):
        self.show_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
                                   wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.AddPage(self.show_panel, u"参数设置", True, wx.NullBitmap)
        show_panel = self.show_panel

        self.static_text_1a = wx.StaticText(show_panel,-1,label="认知不确定参数个数：")
        self.text_ctrl_1a = wx.TextCtrl(show_panel, -1, value='3')
        self.button_t1a = wx.Button(show_panel, label='确定')
        self.button_t1a.Bind(wx.EVT_BUTTON, self.onClick_button_t1a)
        self.static_text_2a = wx.StaticText(show_panel, -1, label="认知不确定参数抽样组数：")
        self.text_ctrl_2a = wx.TextCtrl(show_panel, -1,value='200')
        self.button_t2a = wx.Button(show_panel, label='导入')
        self.button_t2a.Bind(wx.EVT_BUTTON, self.onClick_button_t2a)
        self.static_text_3a = wx.StaticText(show_panel, -1, label="固有不确定参数个数：")
        self.text_ctrl_3a = wx.TextCtrl(show_panel, -1, value='3')
        self.button_t3a = wx.Button(show_panel, label='确定')
        self.button_t3a.Bind(wx.EVT_BUTTON, self.onClick_button_t3a)
        self.static_text_4a = wx.StaticText(show_panel, -1, label="固有不确定参数抽样组数：")
        self.text_ctrl_4a = wx.TextCtrl(show_panel, -1, value='20')
        self.button_t4a = wx.Button(show_panel, label='导入')
        self.button_t4a.Bind(wx.EVT_BUTTON, self.onClick_button_t4a)
        self.static_text_input = wx.StaticText(show_panel, -1, label="模型输入类型个数：")
        self.text_ctrl_input = wx.TextCtrl(show_panel, -1, value='3')
        self.button_input = wx.Button(show_panel, label="确认")
        self.button_input.Bind(wx.EVT_BUTTON, self.onClick_button_input)
        self.static_text_5a = wx.StaticText(show_panel, -1, label="参考模型输入个数：")
        self.text_ctrl_5a = wx.TextCtrl(show_panel, -1, value='20')
        self.static_text_6a = wx.StaticText(show_panel, -1, label="对比输入个数：")
        self.text_ctrl_6a = wx.TextCtrl(show_panel, -1, value='20')
        self.button_ok_input = wx.Button(show_panel, -1, "输入确认")
        self.button_ok_input.Bind(wx.EVT_BUTTON, self.onClick_button_ok_input)

        box_sizer = wx.BoxSizer(orient=wx.VERTICAL)

        box_sizer_c1 = wx.BoxSizer(orient=wx.HORIZONTAL)
        box_sizer_c1.Add(self.static_text_1a)
        box_sizer_c1.Add(self.text_ctrl_1a)

        box_sizer.Add(box_sizer_c1)
        box_sizer.Add(self.button_t1a)

        box_sizer_c2 = wx.BoxSizer(orient=wx.HORIZONTAL)
        box_sizer_c2.Add(self.static_text_2a)
        box_sizer_c2.Add(self.text_ctrl_2a)

        box_sizer.Add(box_sizer_c2)
        box_sizer.Add(self.button_t2a)

        box_sizer_c3 = wx.BoxSizer(orient=wx.HORIZONTAL)
        box_sizer_c3.Add(self.static_text_3a)
        box_sizer_c3.Add(self.text_ctrl_3a)

        box_sizer.Add(box_sizer_c3)
        box_sizer.Add(self.button_t3a)

        box_sizer_c4 = wx.BoxSizer(orient=wx.HORIZONTAL)
        box_sizer_c4.Add(self.static_text_4a)
        box_sizer_c4.Add(self.text_ctrl_4a)

        box_sizer.Add(box_sizer_c4)
        box_sizer.Add(self.button_t4a)

        box_sizer_input = wx.BoxSizer(orient=wx.HORIZONTAL)
        box_sizer_input.Add(self.static_text_input)
        box_sizer_input.Add(self.text_ctrl_input)

        box_sizer.Add(box_sizer_input)
        box_sizer.Add(self.button_input)

        box_sizer_c5 = wx.BoxSizer(orient=wx.HORIZONTAL)
        box_sizer_c5.Add(self.static_text_5a)
        box_sizer_c5.Add(self.text_ctrl_5a)
        box_sizer.Add(box_sizer_c5)

        box_sizer_c6 = wx.BoxSizer(orient=wx.HORIZONTAL)
        box_sizer_c6.Add(self.static_text_6a)
        box_sizer_c6.Add(self.text_ctrl_6a)
        box_sizer.Add(box_sizer_c6)

        box_sizer.Add(self.button_ok_input)

        show_panel.SetSizer(box_sizer)
        self.Show(True)

        show_panel.Layout()


    def onClick_button_t1a(self, event):
        p_n1 = int(self.text_ctrl_1a.GetLineText(0))
        self.p1_l = list()
        i = 1
        while i <= p_n1:
            dlg = wx.TextEntryDialog(None, "请输入第%d个认知不确定参数的分布特征" % (i))
            if dlg.ShowModal() == wx.ID_OK:
                response = dlg.GetValue()
                self.p1_l.append(response)
            i = i + 1
        print '认知不确定分布特征输入成功'

    def onClick_button_t2a(self, event):
        pg_n1 = int(self.text_ctrl_2a.GetLineText(0))
        self.pl_2 = list()
        l1 = len(self.p1_l)
        i = 0
        while i < l1:
            self.pl_2.append(pg_n1)
            i = i + 1
        self.zip_1 = zip(self.pl_2, self.p1_l)
        try:
            cursor = self.conn.cursor()
            sql_create_table = 'create table test_table1 (' \
                               'size int,' \
                               'distribution varchar(20))'
            cursor.execute(sql_create_table)
        except Error as e:
            print(e)
        finally:
            print '导入数据'
        i = 0
        sql_deleteall = 'truncate table test_table1'
        cursor.execute(sql_deleteall)
        while i < l1:
            sql_insert = 'insert into test_table1 values (%s, %s)'
            data = self.zip_1[i]
            cursor.execute(sql_insert, data)
            i = i + 1
        self.conn.commit()
        cursor.close()
        print '认知不确定个数导入成功'

    def onClick_button_t3a(self, event):
        p_n2 = int(self.text_ctrl_3a.GetLineText(0))
        self.p3_l = list()
        i = 1
        while i <= p_n2:
            dlg = wx.TextEntryDialog(None, "请输入第%d个固有不确定参数的分布特征" % (i))
            if dlg.ShowModal() == wx.ID_OK:
                response = dlg.GetValue()
                self.p3_l.append(response)
            i = i + 1
        print '固有不确定分布特征输入成功'

    def onClick_button_t4a(self, event):
        pg_n2 = int(self.text_ctrl_4a.GetLineText(0))
        self.p4_l = list()
        l3 = len(self.p3_l)
        i = 0
        while i < l3:
            self.p4_l.append(pg_n2)
            i = i + 1
        self.zip_2 = zip(self.p4_l, self.p3_l)
        try:
            cursor = self.conn.cursor()
            sql_create_table = 'create table test_table2 (' \
                               'size int,' \
                               'distribution varchar(20))'
            cursor.execute(sql_create_table)
        except Error as e:
            print(e)
        finally:
            print '导入数据'
        i = 0
        sql_deleteall = 'truncate table test_table2'
        cursor.execute(sql_deleteall)
        while i < l3:
            sql_insert = 'insert into test_table2 values (%s, %s)'
            data = self.zip_2[i]
            cursor.execute(sql_insert, data)
            i = i + 1
        print '固有不确定参数个数导入成功'
        self.conn.commit()
        cursor.close()

    def onClick_button_ok_input(self, event):
        input_n1 = int(self.text_ctrl_5a.GetLineText(0))
        input_n2 = int(self.text_ctrl_6a.GetLineText(0))
        input_l1 = list()
        i = 0
        while i < self.input_n:
            input_l1.append(input_n1+input_n2)
            i = i+1

        zip_a = zip(input_l1, self.pl_input)
        try:
            sql_create_table = 'create table test_table3 (' \
                               'size int,' \
                               'distribution varchar(20))'
            cursor = self.conn.cursor()
            cursor.execute(sql_create_table)
        except Error as e:
            print(e)
        finally:
            print '导入数据'

        i = 0
        sql_deleteall = 'truncate table test_table3'
        cursor.execute(sql_deleteall)
        while i < self.input_n:
            data = zip_a[i]
            sql_insert = 'insert into test_table3 values(%s, %s)'
            cursor.execute(sql_insert, data)
            i = i+1
        print '输入的个数导入成功'
        self.conn.commit()
        cursor.close()

    def onClick_button_input(self, event):
        self.input_n = int(self.text_ctrl_input.GetLineText(0))
        self.pl_input = list()
        i = 0
        while i < self.input_n:
            dlg = wx.TextEntryDialog(None, "请输入第%d个输入的取值范围" % (i+1))
            if dlg.ShowModal() == wx.ID_OK:
                response = dlg.GetValue()
                self.pl_input.append(response)
            i = i + 1
        print '输入范围输入成功'




    def NewProj2(self, pProj = 0):
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

    # def onClick_button_a(self, event):
    #     methoda = self.text_ctrl_a.GetLineText(0)
    #     if methoda == "SVR":
    #         print ("SVR")
    #         self.sym = 1
    #         show_panel = self.show_panel
    #         sizer = show_panel.GetSizer()
    #
    #         # sizer_p1 = wx.BoxSizer(orient=wx.HORIZONTAL)
    #         # self.static_text_p1 = wx.StaticText(show_panel, -1, label="惩罚参数:")
    #         # self.text_ctrl_p1 = wx.TextCtrl(show_panel, -1, value='1E3')
    #         # sizer_p1.Add(self.static_text_p1)
    #         # sizer_p1.Add(self.text_ctrl_p1)
    #
    #         # sizer_p2 = wx.BoxSizer(orient=wx.HORIZONTAL)
    #         # self.static_text_p2 = wx.StaticText(show_panel, -1, label="小量:")
    #         # self.text_ctrl_p2 = wx.TextCtrl(show_panel, -1, value='0.1')
    #         # sizer_p2.Add(self.static_text_p2)
    #         # sizer_p2.Add(self.text_ctrl_p2)
    #
    #         # sizer_p3 = wx.BoxSizer(orient=wx.HORIZONTAL)
    #         # self.static_text_p3 = wx.StaticText(show_panel, -1, label="内核方法(linear;poly;rbf;sigmoid):")
    #         # self.text_ctrl_p3 = wx.TextCtrl(show_panel, -1, value='rbf')
    #         # sizer_p3.Add(self.static_text_p3)
    #         # sizer_p3.Add(self.text_ctrl_p3)
    #
    #         # sizer.Add(sizer_p1)
    #         # sizer.Add(sizer_p2)
    #         # sizer.Add(sizer_p3)
    #
    #         self.button_1a = wx.Button(show_panel, label="元模型建模")
    #         self.button_1a.Bind(wx.EVT_BUTTON, self.onClick_button_1a)
    #
    #         sizer.Add(self.button_1a)
    #
    #         show_panel.Layout()
    #     elif methoda == "GPR":
    #         print ("GPR")
    #         self.sym = 2
    #
    #         show_panel = self.show_panel
    #         sizer = show_panel.GetSizer()
    #
    #         # sizer_p1 = wx.BoxSizer(orient=wx.HORIZONTAL)
    #         # self.static_text_p1 = wx.StaticText(show_panel, -1, label="alpha:")
    #         # self.text_ctrl_p1 = wx.TextCtrl(show_panel, -1, value='1e-10')
    #         # sizer_p1.Add(self.static_text_p1)
    #         # sizer_p1.Add(self.text_ctrl_p1)
    #         #
    #         # sizer.Add(sizer_p1)
    #
    #         self.button_1a = wx.Button(show_panel, label="元模型建模")
    #         self.button_1a.Bind(wx.EVT_BUTTON, self.onClick_button_1a)
    #
    #         sizer.Add(self.button_1a)
    #
    #         show_panel.Layout()
    #     else:
    #         print ("KRR")
    #         self.sym = 3
    #
    #         show_panel = self.show_panel
    #         sizer = show_panel.GetSizer()
    #
    #         # sizer_p1 = wx.BoxSizer(orient=wx.HORIZONTAL)
    #         # self.static_text_p1 = wx.StaticText(show_panel, -1, label="n_iter:")
    #         # self.text_ctrl_p1 = wx.TextCtrl(show_panel, -1, value='300')
    #         # sizer_p1.Add(self.static_text_p1)
    #         # sizer_p1.Add(self.text_ctrl_p1)
    #         #
    #         # sizer_p2 = wx.BoxSizer(orient=wx.HORIZONTAL)
    #         # self.static_text_p2 = wx.StaticText(show_panel, -1, label="tol:")
    #         # self.text_ctrl_p2 = wx.TextCtrl(show_panel, -1, value='0.001')
    #         # sizer_p2.Add(self.static_text_p2)
    #         # sizer_p2.Add(self.text_ctrl_p2)
    #         #
    #         # sizer.Add(sizer_p1)
    #         # sizer.Add(sizer_p2)
    #
    #         self.button_1a = wx.Button(show_panel, label="元模型建模")
    #         self.button_1a.Bind(wx.EVT_BUTTON, self.onClick_button_1a)
    #
    #         sizer.Add(self.button_1a)
    #         show_panel.Layout()

    def onClick_button_1a(self, event):
        self.cog_p_n = int(self.text_ctrl_1a.GetLineText(0))
        self.cog_p_gn = int(self.text_ctrl_2a.GetLineText(0))
        self.inh_p_n = int(self.text_ctrl_3a.GetLineText(0))
        self.inh_p_gn = int(self.text_ctrl_4a.GetLineText(0))
        self.c_data_n = int(self.text_ctrl_5a.GetLineText(0))
        self.cmp_data_n = int(self.text_ctrl_6a.GetLineText(0))


        build_meta.initData(self.cog_p_gn, self.cog_p_n, self.inh_p_gn, self.inh_p_n, self.c_data_n, self.cmp_data_n)
        build_meta.importData()
        if self.sym == 1:
            self.svr = build_meta.buildSVR(self, build_meta.test_cog_p, build_meta.test_inh_p, build_meta.test_output, build_meta.test_input)#, cus_C, cus_epsilon, cus_kernel)
        elif self.sym == 2:
            self.gpr = build_meta.buildGPR(self, build_meta.test_cog_p, build_meta.test_inh_p, build_meta.test_output, build_meta.test_input)#, cus_alpha)
        else:
            self.bayes = build_meta.buildKRR(self, build_meta.test_cog_p, build_meta.test_inh_p, build_meta.test_output, build_meta.test_input)#, cus_n_iter, cus_tol)

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


    def NewProj3(self, pProj = 0):
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
            GA_f.GA(self, self.svr, pn, itn, cp, mp, self.cog_p_n)
        elif self.sym == 2:
            GA_f.GA(self, self.gpr, pn, itn, cp, mp, self.cog_p_n)
        else:
            GA_f.GA(self, self.bayes, pn, itn, cp, mp, self.cog_p_n)