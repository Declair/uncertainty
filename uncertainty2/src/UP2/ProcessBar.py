# -*- coding: utf-8 -*-
import time
import wx

class ProcessBar(wx.Frame):
    def __init__(self, parent, title, range):
        super(ProcessBar, self).__init__(parent, title=title, size=(300, 200))
        self.range = range
        self.InitUI()

    def InitUI(self):
        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)

        self.gauge = wx.Gauge(pnl, range=self.range, size=(250, 25), style=wx.GA_HORIZONTAL)

        hbox1.Add(self.gauge, proportion=1, flag=wx.ALIGN_CENTRE)

        vbox.Add((0, 30))
        vbox.Add(hbox1, flag=wx.ALIGN_CENTRE)
        vbox.Add((0, 20))
        pnl.SetSizer(vbox)

        self.SetSize((300, 200))
        self.Centre()
        self.Show(True)

    def SetProcess(self,count,end = 0):
        if(end == 1): # 快速结束进度条
            while True:
                time.sleep(0.001)
                count += 1
                self.gauge.SetValue(count)

                if count >= self.range:
                    return
        else: # 按count 设置进度条
            self.gauge.SetValue(count)

# xx = wx.App()
# x = ProcessBar(None, '打开程序中', 100)
# x.SetProcess(6,1)
# return