# -*- coding: utf-8 -*-
import wx

class ProcessBar(wx.Frame):
    range = 20
    def __init__(self, parent, title, range):
        super(ProcessBar, self).__init__(parent, title=title, size=(300, 200))
        self.InitUI()
        self.range = range

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

    # def SetProcess(self, e):
    #     while True:
    #         time.sleep(1)
    #         self.count = self.count + 1
    #         self.gauge.SetValue(self.count)
    #
    #         if self.count >= 20:
    #             print "end"
    #             return


# ex = wx.App()
# ProcessBar(None, '实现方案生成中')
# ex.MainLoop()