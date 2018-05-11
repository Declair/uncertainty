# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
from ModelManage import ModelUi
from UncertaintyPropagation import UncertaintyPropagationUi
#主界面
class PlatformForUncertainly(wx.Frame):
    
    def __init__(self, parent = None, id = -1, UpdateUI = None, params = {}):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title= u"不确定性智能仿真模型校准平台", 
                          pos=wx.DefaultPosition, size=wx.Size(1280, 720), 
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.SetIcon(wx.Icon('icon/lihf.ico', wx.BITMAP_TYPE_ICO))
        self.SetSizeHints((1280, 720), wx.DefaultSize)
        self.Maximize(True)
        self.UpdateUI = UpdateUI
        self.InitUI(params)
        
    def InitUI(self, params):
        
#         px = wx.DisplaySize()
        #最底层panel
        self.main_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, 
                                    wx.DefaultSize, wx.TAB_TRAVERSAL)
        #最底层panel垂直布局
        bSizerforwholepanel = wx.BoxSizer(wx.VERTICAL)
        self.main_panel.SetSizer(bSizerforwholepanel)
        
        
        #右上角用户panel
        self.userPanel = wx.Panel(self.main_panel,wx.ID_ANY, wx.DefaultPosition, 
                                    (200,28), wx.TAB_TRAVERSAL)
#         self.userPanel.SetBackgroundColour('yellow')
        #用户显示栏
        self.userText = wx.StaticText(self.userPanel, wx.ID_ANY, params['account'],
                                            (0,4), (100,28), 0)
        self.userText.SetFont(wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.NORMAL, True))
        #注销按钮
        self.logoffBtn = wx.Button(self.userPanel, wx.ID_ANY, u"注销", 
                                 (100,0), (100,28), 0)
        self.logoffBtn.Bind(wx.EVT_LEFT_DOWN, self.Logoff)
        
    
        #上方导航页签
        self.statusBar = wx.Notebook(self.main_panel, wx.ID_ANY, 
                                     wx.DefaultPosition, wx.DefaultSize, 0)
        self.statusBar.SetPadding(wx.Size(20,5))
        bSizerforwholepanel.Add(self.statusBar, 1, wx.EXPAND | wx.ALL, 5)
        
        #每个页签下加入各功能模块panel
        self.model_panel = ModelUi.ModelPanel(self.statusBar)
        self.model_panel2 = ModelUi.ModelPanel(self.statusBar)
        self.model_panel3 = UncertaintyPropagationUi.ModelPanel(self.statusBar)
        self.model_panel4 = ModelUi.ModelPanel(self.statusBar)
        self.statusBar.AddPage(self.model_panel, u"仿真模型管理", True)
        self.statusBar.AddPage(self.model_panel2, u"不确定性建模", False)
        self.statusBar.AddPage(self.model_panel3, u"不确定性传播分析", False)
        self.statusBar.AddPage(self.model_panel4, u"仿真验证分析", True)
        
        self.main_panel.Layout()
        self.main_panel.Bind(wx.EVT_SIZE, self.OnReSize)
         
#         bSizerforwholepanel.Fit(self.main_panel)

    def OnReSize(self, event):
#       在绑定的size事件中使右上角用户panel右对齐  
        x, y = self.GetSize() 
        w, h = self.userPanel.GetSize()
        self.userPanel.SetPosition((x - w - 25, 0))  
        self.Refresh()
        self.main_panel.Layout()
    
        
    def Logoff(self, event):
        #注销操作
        self.Destroy()
        self.UpdateUI(0)
        
class MainApp(wx.App):
    def OnInit(self):
        self.frame = PlatformForUncertainly(params = {"account": 'admin'})
        self.frame.Show()
        return True

def main():
    app = MainApp()
    app.MainLoop()

if __name__ == "__main__":
    main()