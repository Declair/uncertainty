# -*- coding: utf-8 -*-

import wx
import Sql


class NavTree(wx.TreeCtrl):
    
    def __init__(self, parent = None):
        
        wx.TreeCtrl.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, 
                          wx.DefaultSize, wx.TR_DEFAULT_STYLE | wx.TR_EDIT_LABELS)
        
        self.updateTree()
        
#更新导航栏树
    def updateTree(self):
        # Create an image list
        il = wx.ImageList(16,16)

        # Get some standard images from the art provider and add them
        # to the image list
        self.fldridx = il.Add(
            wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, (16,16)))
        self.fldropenidx = il.Add(
            wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN,   wx.ART_OTHER, (16,16)))
        self.fileidx = il.Add(
            wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, (16,16)))

        self.DeleteAllItems()
        
        record = Sql.selectSql(sql=Sql.modelSql)
            
        """左侧树状图"""
        root = self.AddRoot('模型', data=0)
        self.SetItemImage(root, self.fldridx,
                               wx.TreeItemIcon_Normal)
        self.SetItemImage(root, self.fldropenidx,
                               wx.TreeItemIcon_Expanded)
        tree = [0]*100
        treeMap = {}
        i = 0
        for model in record:
            if(model[2] == 0):    #最上层节点
                tree[i] = self.AppendItem(root, model[1], data=model[0])
            else:    #子节点
                tree[i] = self.AppendItem(treeMap[model[2]], model[1], data=model[0])
            self.SetItemImage(tree[i], self.fldridx,
                                       wx.TreeItemIcon_Normal)
            self.SetItemImage(tree[i], self.fldropenidx,
                                       wx.TreeItemIcon_Expanded)
            treeMap[model[0]] = tree[i]
            i += 1
#         self.m_treeCtrl4.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, id=1)