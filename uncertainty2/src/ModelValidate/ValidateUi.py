# -*- coding: utf-8 -*-

import wx
import NavTree
import ShowNotebook

#模型管理功能模块界面
class ParamPanel(wx.Panel):
    
    def __init__(self, parent = None):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, 
                          wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.InitUI()
        
    def InitUI(self):
        #上方按钮区域panel
        self.btnPanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, 
                                 wx.Size(-1, 40), wx.TAB_TRAVERSAL)
        tabSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btnPanel.SetSizer(tabSizer)
        
        self.button = wx.Button(self.btnPanel, wx.ID_ANY, u"新建", 
                                 wx.DefaultPosition, wx.DefaultSize, 0)
        self.Bind(wx.EVT_BUTTON, self.ClickNewProj, self.button)
#         self.button.Bind(wx.EVT_LEFT_DOWN, self.ClickNewProj)
        self.button.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, (16,16)))
        tabSizer.Add(self.button, 0, wx.ALL, 5)
        
        self.button1 = wx.Button(self.btnPanel, wx.ID_ANY, u"模型导入", 
                                 wx.DefaultPosition, wx.DefaultSize, 0)
#         self.button1.SetBitmap(wx.Bitmap('icon/btn_show1.tga'))
        self.button1.Bind(wx.EVT_LEFT_DOWN, self.ClickImport)
        tabSizer.Add(self.button1, 0, wx.ALL, 5)

        self.button2 = wx.Button(self.btnPanel, wx.ID_ANY, u"参数设置", 
                                 wx.DefaultPosition, wx.DefaultSize, 0)
        tabSizer.Add(self.button2, 0, wx.ALL, 5)

        self.button3 = wx.Button(self.btnPanel, wx.ID_ANY, u"数据导入",
                                 wx.DefaultPosition, wx.DefaultSize, 0)
        tabSizer.Add(self.button3, 0, wx.ALL, 5)
        
        
        #下方导航树及展示界面panel 
        self.displayPanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, 
                                     wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.navTree = NavTree.NavTree(self.displayPanel)
        self.showNotebook = ShowNotebook.ShowNotebook(self.displayPanel)
        #displayPanel布局
        hBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        hBoxSizer.Add(self.navTree, 1, wx.ALL | wx.EXPAND, 5)
        hBoxSizer.Add(self.showNotebook, 4, wx.EXPAND | wx.ALL, 5)
        self.displayPanel.SetSizer(hBoxSizer)
        
        #整个模块布局
        vBoxSizer = wx.BoxSizer(wx.VERTICAL)
        vBoxSizer.Add(self.btnPanel, 0, wx.EXPAND | wx.ALL, 5)
        vBoxSizer.Add(self.displayPanel, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(vBoxSizer)
#         self.Layout()
#         vBoxSizer.Fit(self)
        
        
    def ClickImport(self, event):
        return 
#         dlg = wx.DirDialog(self,u"选择文件夹",style=wx.DD_DEFAULT_STYLE)  
#         if dlg.ShowModal() == wx.ID_OK:
#             Import_file.insert_blob(project='一元非线性回归', _dir=dlg.GetPath()) #文件夹路径  
#         dlg.Destroy()
        
    def ClickNewProj(self, event):
        return 
#         self.showNotebook.NewProj()
#         dlg = wx.TextEntryDialog(self, '输入项目名称','项目创建') 
#         if dlg.ShowModal() == wx.ID_OK:
#             Sql.insertSql((dlg.GetValue(), 0), Sql.insertProj)
#             self.navTree.updateTree()
#         dlg.Destroy()
         