# -*- coding: utf-8 -*-

import wx
import UTNotebook
import NavTree
import config
import Sql
import mysql.connector


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

        self.button_ModelSelect = wx.Button(self.btnPanel, wx.ID_ANY, u"模型选择",
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        self.button_ModelSelect.SetBitmap(wx.Bitmap('icon/select.ico'))
        self.Bind(wx.EVT_BUTTON, self.ClickModelSelect, self.button_ModelSelect)
        tabSizer.Add(self.button_ModelSelect, 0, wx.ALL, 5)

        self.button_sample = wx.Button(self.btnPanel, wx.ID_ANY, u"抽样设置", wx.DefaultPosition,
                                 wx.DefaultSize, 0)
        self.button_sample.Bind(wx.EVT_BUTTON, self.sampling_settings)
        self.button_sample.SetBitmap(wx.Bitmap('icon/samp.ico'))
        tabSizer.Add(self.button_sample, 0, wx.ALL, 5)

        self.button_plan = wx.Button(self.btnPanel, wx.ID_ANY, u"传播分析", wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        self.button_plan.Bind(wx.EVT_BUTTON, self.Test)
        self.button_plan.SetBitmap(wx.Bitmap('icon/prop.ico'))
        tabSizer.Add(self.button_plan, 0, wx.ALL, 5)
        """ 添加菜单按钮 ends """

        # 下方导航树及展示界面panel
        self.displayPanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition,
                                     wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.navTree = NavTree.NavTree(self.displayPanel)
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
            return

        # """不是根节点再进行数据库操作"""
        # if self.m_treeCtrl4.RootItem != item:
        db_config = config.datasourse
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            # FIXME:此处用模型名称查询 目前没有找到获取到树编号的方法 后期需要修改 以应对名称重复的情况
            cursor.execute((Sql.get_arg_Sql + str(n_id) + ";"))
            record = cursor.fetchall()
        except mysql.connector.Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

        """"模型ID"""""
        model_id = record[0][6]

        """"得到分布类型"""""
        dtype = []
        for t in record:
            dtype.append(t[2])
        """"得到分布参数"""
        paras = []
        for par in record:
            args = par[3].split(" ")
            a = []
            for p in args:
                a.append(float(p))  # 每个a是每一个参数的分布参数
            paras.append(a)  # paras 包含所有参数的分布参数
        """"参数名称"""""
        parname = []
        """"参数ID"""""
        parid = []
        """"参数类型"""""
        partype = []
        for par in record:
            parname.append(par[1])
            parid.append(par[4])
            partype.append(par[5])
        """"传参到抽样方法选择模块"""
        UTN = UTNotebook.UTNotebook()
        UTN.Para = self.Para(dtype, paras, parname, parid, partype, model_id)
        UTN.ShowArg(record)

    # 将传参集中在一个类中
    # 对于同一个模型的参数 参数名字是不会重复的 每次抽出来的都是同一个模型的参数 则参数名可以唯一确定一行记录
    class Para:
        def __init__(self, dtype=None, paras=None, parname=None, parid=None, partype=None, modelid=None):
            self.dtype = dtype
            self.para = tuple(paras)
            self.name = parname
            self.parid = parid
            self.partype = partype
            self.model_id = modelid

    def sampling_settings(self, event):
        """ 按下 抽样方法 按钮 """
        self.showNotebook.up_select_method()

    def Test(self, event):
        """ 按下 实验方案 按钮 """
        self.showNotebook.up_test()