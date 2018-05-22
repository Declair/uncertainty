# -*- coding: utf-8 -*-

import wx

import config
import Sql
import UPShowPanel
import mysql.connector
import UTNotebook

class NavPanel(wx.Panel):
    
    def __init__(self, parent = None):
        
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, 
                          wx.DefaultSize, wx.TAB_TRAVERSAL)

        bSizer = wx.BoxSizer(wx.VERTICAL)

        self.m_treeCtrl4 = wx.TreeCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                       wx.TR_DEFAULT_STYLE)

        db_config = config.datasourse
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            args = ()
            cursor.execute(Sql.modelSql, args)
            record = cursor.fetchall()
        except mysql.connector.Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

        """左侧树状图"""
        root = self.m_treeCtrl4.AddRoot('选择模型实验')
        tree = [[0] * len(record)] * len(record)
        i = 0
        for par in record:
             tree[i] = self.m_treeCtrl4.AppendItem(root, par[1])
             i += 1
        bSizer.Add(self.m_treeCtrl4, 1, wx.ALL | wx.EXPAND, 5)
        """双击选择模型"""
        self.m_treeCtrl4.Bind(wx.EVT_TREE_ITEM_ACTIVATED,self.SelectModel)

        """"""""""""""""""""
        self.SetSizer(bSizer)
        self.Layout()
        bSizer.Fit(self)

    def SelectModel(self, event):
        item = self.m_treeCtrl4.GetSelection()
        select_name = self.m_treeCtrl4.GetItemText(item)
        """不是根节点再进行数据库操作"""
        if self.m_treeCtrl4.RootItem != item:
            db_config = config.datasourse
            try:
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor()
                cursor.execute((Sql.get_arg_Sql + " '" + select_name + "';"))
                record = cursor.fetchall()
            except mysql.connector.Error as e:
                print(e)
            finally:
                cursor.close()
                conn.close()

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
                    a.append(float(p))# 每个a是每一个参数的分布参数
                paras.append(a) # paras 包含所有参数的分布参数
            """"参数名称"""""
            parname = []
            for name in record:
                parname.append(name[1])
            """"传参到抽样方法选择模块"""
            UTN =UTNotebook.UTNotebook()
            UTN.kind = dtype
            UTN.para = tuple(paras)
            UTN.name = parname
            # """""更新UPSP"""
            # showPanel = UPShowPanel.ShowPanel()
            #
            # # 设置内容
            # i = 0
            # for row in record:
            #     showPanel.m_grid4.SetCellValue(i, 0, str(row[0]))
            #     showPanel.m_grid4.SetCellValue(i, 1, str(row[1]))
            #     showPanel.m_grid4.SetCellValue(i, 2, str(row[2]))
            #     showPanel.m_grid4.SetCellValue(i, 3, str(row[3]))
            #     i = i + 1
            UTN.ShowArg(record)