#coding:utf8
import wx, sys;
from app.dialog.main import MainFrame;
sys=sys;
code=sys.getdefaultencoding();
if code != "utf-8":
	reload(sys);
	sys.setdefaultencoding("utf-8");
	
if __name__ == '__main__':
	app = wx.App();
	mainFrame = MainFrame();
	mainFrame.Show()
	app.MainLoop()
