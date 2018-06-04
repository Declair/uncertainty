#coding=utf-8
import wx
# 导入wxPython中的通用Button
import config
import mysql.connector
import Sql


class login_frame(wx.Frame):

    def __init__(self, parent=None, id=-1, UpdateUI=None):
        px = wx.DisplaySize()
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"登录", pos=(px[0] / 3, px[1] / 3), size=wx.Size(400, 250),
                          style=wx.CAPTION | wx.CLOSE_BOX | wx.TAB_TRAVERSAL)
        self.UpdateUI = UpdateUI
        self.InitUI()  # 绘制UI界面

    def InitUI(self):
        bSizer_main = wx.BoxSizer(wx.VERTICAL)

        self.m_panel_up = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer_pic = wx.BoxSizer(wx.VERTICAL)

        uncertainty_image = wx.Image('icon/uncertainty.jpg', wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
        self.bmp = wx.StaticBitmap(parent=self.m_panel_up, bitmap=uncertainty_image)

        self.m_panel_up.SetSizer(bSizer_pic)
        self.m_panel_up.Layout()
        bSizer_pic.Fit(self.m_panel_up)
        bSizer_main.Add(self.m_panel_up, 2, wx.EXPAND | wx.ALL, 5)

        self.m_panel_down = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)

        # 错误提示信息
        self.label_wrong_info = wx.StaticText(self.m_panel_down, wx.ID_ANY, '账号或密码错误', pos=(110, 6))
        self.label_wrong_info.SetForegroundColour('#ff0000')
        self.label_wrong_info.Hide()

        label_username = wx.StaticText(self.m_panel_down, wx.ID_ANY, '账号', pos=(70, 30))
        self.textCtrl_username = wx.TextCtrl(self.m_panel_down, wx.ID_ANY, u'', pos=(110, 27), size=(180, -1))
        # textCtrl的纵坐标要比StaticText的小3

        label_password = wx.StaticText(self.m_panel_down, wx.ID_ANY, '密码', pos=(70, 60))
        self.textCtrl_password = wx.TextCtrl(self.m_panel_down, wx.ID_ANY, u'', pos=(110, 57), size=(180, -1),
                                             style=wx.TE_PASSWORD)

        self.buttom_login = wx.Button(self.m_panel_down, wx.ID_ANY, u'登录', pos=(70, 87), size=wx.DefaultSize)
        self.buttom_login.SetBitmap(wx.Bitmap('icon/login.ico'))
        self.buttom_login.Bind(wx.EVT_BUTTON, self.loginFunction)

        self.buttom_signin = wx.Button(self.m_panel_down, wx.ID_ANY, u'注册', pos=(200, 87), size=wx.DefaultSize)
        self.buttom_signin.SetBitmap(wx.Bitmap('icon/signin.ico'))

        bSizer_main.Add(self.m_panel_down, 3, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(bSizer_main)
        self.Layout()

        self.Centre(wx.BOTH)

    def __del__(self):
        pass

    def loginFunction(self, event):
        self.account = self.textCtrl_username.GetValue()
        self.password = self.textCtrl_password.GetValue()
        if self.validate():
            params = {"account": self.account}
            self.Destroy()
            self.UpdateUI(1, params)  # 更新UI-Frame

    def cancleEvent(self, event):
        wx.Exit()

    # 登录验证
    def validate(self):
        record = Sql.selectSql((self.account,), Sql.loginSql)
        if record == []:
            self.label_wrong_info.Show(True)
            # dlg = wx.MessageDialog(None, u"此用户不存在", u"登录失败", wx.OK | wx.ICON_EXCLAMATION)
            # dlg.ShowModal()
            return False
        if record[0][1] != self.password:
            self.label_wrong_info.Show(True)
            # dlg = wx.MessageDialog(None, u"密码错误", u"登录失败", wx.OK | wx.ICON_EXCLAMATION)
            # dlg.ShowModal()
            return False
        return True

'''
#登录界面
class LoginFrame(wx.Frame):
    def __init__(self, parent=None, id=-1, UpdateUI=None):
        px = wx.DisplaySize()
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title='登录界面', size=(320, 200), 
                          pos=(px[0]/3, px[1]/3))
        self.UpdateUI = UpdateUI
        self.InitUI() # 绘制UI界面

    def InitUI(self):
        panel = wx.Panel(self)
        
        font = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL, True)

        accountLabel = wx.StaticText(panel, -1, '账号', pos=(20, 25))
        accountLabel.SetForegroundColour('#0a74f7')
        accountLabel.SetFont(font)
        self.accountInput = wx.TextCtrl(panel, -1, u'', pos=(80, 25), size=(180, -1))
        self.accountInput.SetForegroundColour('gray')
        self.accountInput.SetFont(font)

        
        passwordLabel = wx.StaticText(panel, -1, '密码', pos=(20, 70))
        passwordLabel.SetForegroundColour('#0a74f7')
        passwordLabel.SetFont(font)
        self.passwordInput = wx.TextCtrl(panel, -1, u'', pos=(80, 70), size=(180, -1), style=wx.TE_PASSWORD)
        self.passwordInput.SetFont(font)

        sureButton = wx.Button(panel, -1, u'登录', pos=(20, 110), size=(120, 40))
        sureButton.SetBackgroundColour('#0a74f7')
        sureButton.SetForegroundColour('white')
        self.Bind(wx.EVT_BUTTON, self.loginFunction, sureButton) # 为【确定Button】绑定事件

        cancleButton = wx.Button(panel, -1, u'取消', pos=(160, 110), size=(120, 40))
        cancleButton.SetBackgroundColour('black')
        cancleButton.SetForegroundColour('#ffffff')
        self.Bind(wx.EVT_BUTTON, self.cancleEvent, cancleButton)

'''