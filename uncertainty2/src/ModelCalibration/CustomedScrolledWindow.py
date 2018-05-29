import wx
class CustomedScrolledWindow(wx.ScrolledWindow):
    def __init__(self, parent):
        wx.ScrolledWindow.__init__(self, parent=parent)
        self.static_text = wx.StaticText(self, label="this is a test \n 1 \n 2 \n 3 \n 4")
