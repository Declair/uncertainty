# -*- coding: utf-8 -*-

import wx
import wx.xrc

###########################################################################
## Class login_frame
###########################################################################


class login_frame(wx.Frame):

    def __init__(self, parent):
        px = wx.DisplaySize()
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"登录", pos=(px[0]/3, px[1]/3), size=wx.Size(400, 250),
                          style=wx.CAPTION | wx.CLOSE_BOX | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer_main = wx.BoxSizer(wx.VERTICAL)

        self.m_panel_up = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer_pic = wx.BoxSizer(wx.VERTICAL)

        uncertainty_image = wx.Image('img/uncertainty.jpg', wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
        self.bmp = wx.StaticBitmap(parent=self.m_panel_up, bitmap=uncertainty_image)

        self.m_panel_up.SetSizer(bSizer_pic)
        self.m_panel_up.Layout()
        bSizer_pic.Fit(self.m_panel_up)
        bSizer_main.Add(self.m_panel_up, 2, wx.EXPAND | wx.ALL, 5)

        self.m_panel_down = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)

        label_wrong_info = wx.StaticText(self.m_panel_down, wx.ID_ANY, '账号或密码错误', pos=(110, 6))
        label_wrong_info.SetForegroundColour('#ff0000')

        label_username = wx.StaticText(self.m_panel_down, wx.ID_ANY, '账号', pos=(70, 30))
        self.textCtrl_username = wx.TextCtrl(self.m_panel_down, wx.ID_ANY, u'', pos=(110, 27), size=(180, -1))
        # textCtrl的纵坐标要比StaticText的小3

        label_password = wx.StaticText(self.m_panel_down, wx.ID_ANY, '密码', pos=(70, 60))
        self.textCtrl_password = wx.TextCtrl(self.m_panel_down, wx.ID_ANY, u'', pos=(110, 57), size=(180, -1), style=wx.TE_PASSWORD)

        self.buttom_login = wx.Button(self.m_panel_down, wx.ID_ANY, u'登录', pos=(70, 87),  size=wx.DefaultSize)
        self.buttom_login.SetBitmap(wx.Bitmap('../uncertainty2/src/MainUI/icon/login.ico'))

        self.buttom_signin = wx.Button(self.m_panel_down, wx.ID_ANY, u'注册', pos=(200, 87), size=wx.DefaultSize)
        self.buttom_signin.SetBitmap(wx.Bitmap('../uncertainty2/src/MainUI/icon/signin.ico'))
        # self.logoffBtn = wx.Button(self.userPanel, wx.ID_ANY, u"注 销",
        #                            (100, 3), (-1, 26), 0)
        # self.logoffBtn.SetBitmap(wx.Bitmap('icon/logoff.ico'))
        # self.logoffBtn.Bind(wx.EVT_BUTTON, self.Logoff)

        bSizer_main.Add(self.m_panel_down, 3, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(bSizer_main)
        self.Layout()

        self.Centre(wx.BOTH)

    def __del__(self):
        pass


app = wx.App(False)
frame = login_frame(None)
frame.Show()
app.MainLoop()