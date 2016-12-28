#coding:utf8
import wx;
import os;
from app.format import FormatConvert;
from app.common import util;

class MainFrame(wx.Frame):
	def __init__(self):
		self.width = 600;
		self.height = 400;
		self.grid_span = 20;
		self.main_sizer = None;
		self.sizers = {};
		self.controls = {};
		self.pages = {};
		self.curr_page = [];
		self.OnShow();
		
	def OnShow(self):
		'''
		显示主界面
		'''
		wx.Frame.__init__(self, None, -1, 'OKTools', size=(self.width, self.height));
		self.panel = wx.Panel(self, -1);
		#菜单栏
		menubar = wx.MenuBar();
		menu1 = wx.Menu();
		menubar.Append(menu1, u'文件');
		menu1.Append(1001, u'打开文件');
		menu1.Append(1002, u'打开目录');
		menu2 = wx.Menu();
		menubar.Append(menu2, u'配置');
		menu2.Append(2001, u'参数配置');
		self.SetMenuBar(menubar);
		#工具栏
		toolbar = self.CreateToolBar(wx.TB_HORIZONTAL|wx.TB_TEXT);
		main = wx.Image('app/icons/main.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap();
		back = wx.Image('app/icons/back.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap();
		do = wx.Image('app/icons/do.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap();
		toolbar.AddSimpleTool(100, main, u'主界面');
		toolbar.AddSimpleTool(200, back, u'返回上一级');
		toolbar.AddSimpleTool(300, do, u'执行');
		toolbar.Realize();
		self.Bind(wx.EVT_TOOL, self.OnTMain, id=100);
		self.Bind(wx.EVT_TOOL, self.OnTBack, id=200);
		self.Bind(wx.EVT_TOOL, self.OnTDo, id=300);
		#布局层
		self.sizers['main'] = wx.BoxSizer(wx.VERTICAL);
		labels = [{'format':u'格式转换'}, {'package':u'版本打包'}, {'log':u'解析日志'}];
		for item in labels:
			button = wx.Button(self.panel, -1, item.items()[0][1]);
			self.controls[button.GetId()] = item.items()[0][0];
			self.Bind(wx.EVT_BUTTON, self.OnClick, button);
			self.sizers['main'].Add(button, 0, wx.ALIGN_CENTER|wx.ALL, self.grid_span);
		self.main_sizer = wx.BoxSizer(wx.HORIZONTAL);
		self.main_sizer.Add(self.sizers['main'], 1, wx.ALIGN_CENTER|wx.ALL);
		self.curr_page.append('main');
		self.SetClientSize((self.width, self.height));
		self.panel.SetSizerAndFit(self.main_sizer);
		self.main_sizer.SetSizeHints(self.panel);
		self.Centre();
	
	def OnClick(self, event):
		'''
		txt转换json
		'''
		logic_type = self.controls.get(event.GetId());
		last_index = len(self.curr_page) - 1;
		if 0 > last_index: return;
		
		curr_sizer = self.sizers[self.curr_page[last_index]];
		self.main_sizer.Hide(curr_sizer);
		self.curr_page.append(logic_type);
		if not self.sizers.has_key(logic_type):
			if 'format' == logic_type:
				self.CreateFormatSizer(logic_type);
			elif 'package' == logic_type:
				return;
			elif 'log' == logic_type:
				return;
			elif 'excel_txt' == logic_type or 'excel_txt' == logic_type or 'txt_json' == logic_type or 'excel_json' == logic_type or 'excel_lua' == logic_type: 
				self.CreateConvertSizer(logic_type);
		else:
			self.main_sizer.Show(self.sizers[logic_type]);
		self.main_sizer.Layout();
		
	def OnTMain(self, event):
		'''
		主界面
		'''
		last_index = len(self.curr_page) - 1;
		if 0 >= last_index: return;
		
		self.main_sizer.Hide(self.sizers[self.curr_page[last_index]]);
		self.main_sizer.Show(self.sizers[self.curr_page[0]]);
		self.curr_page = ['main'];
		self.main_sizer.Layout();
		
	def OnTBack(self, event):
		'''
		返回上一级
		'''
		last_index = len(self.curr_page) - 1;
		if 0 >= last_index: return;
		
		self.main_sizer.Hide(self.sizers[self.curr_page[last_index]]);
		self.main_sizer.Show(self.sizers[self.curr_page[last_index - 1]]);
		self.main_sizer.Layout();
		self.curr_page.pop();
		
	def OnTDo(self, event):
		'''
		执行
		'''
		last_index = len(self.curr_page) - 1;
		if 0 > last_index: return;
		
		logic_type = self.curr_page[last_index];
		parent_page = self.curr_page[last_index - 1] if 1 <= last_index else '';
		if 'format' == parent_page:
			text_input = self.pages[logic_type].get('src');
			text_output = self.pages[logic_type].get('dest');
			src = text_input.GetValue();
			dest = text_output.GetValue();
			if not util.check_path(src):
				util.log(u"请选择正确的源文件夹路径！");
				return;
			if not util.check_path(dest):
				util.log(u"请选择正确的目标文件夹路径！");
				return;
			self.pages[logic_type]['console'].SetValue('');
			formatConvert = FormatConvert(src, dest, self.pages[logic_type].get('console'));
			result = '';
			if 'excel_txt' == logic_type:
				result = formatConvert.excel_to_txt();
			elif 'excel_txt' == logic_type:
				result = formatConvert.excel_to_csv();
			elif 'txt_json' == logic_type:
				result = formatConvert.txt_to_json();
			elif 'excel_json' == logic_type:
				result = formatConvert.excel_to_json();
			elif 'excel_lua' == logic_type:
				result = formatConvert.excel_to_lua(False);
			if 'ok' == result:
				util.log(u"执行完毕！", flag=wx.OK|wx.ICON_INFORMATION);
		
	def OnPath(self, event):
		'''
		打开路径
		'''
		relate_ctr = self.controls.get(event.GetId());
		filterFile = " All files (*.*) |*.*";
		opendialog = wx.FileDialog(self, u"选择文件", os.getcwd(), "", filterFile, wx.OPEN);
		if opendialog.ShowModal() == wx.ID_OK:
			path = opendialog.GetPath();
			relate_ctr.AppendText(os.path.dirname(path));
		opendialog.Destroy();
		
	def CreateFormatSizer(self, logic_type):
		'''
		创建格式转换布局
		'''
		self.sizers[logic_type] = wx.BoxSizer(wx.VERTICAL);
		labels = [{'excel_txt':u'Excel转换Txt'}, {'excel_txt':u'Excel转换Csv'}, {'txt_json':u'Txt转换Json'}, {'excel_json':u'Excel转换Json'}, {'excel_lua':u'Excel转换Lua'}];
		for item in labels:
			button = wx.Button(self.panel, -1, item.items()[0][1]);
			self.controls[button.GetId()] = item.items()[0][0];
			self.Bind(wx.EVT_BUTTON, self.OnClick, button);
			self.sizers[logic_type].Add(button, 0, wx.ALIGN_CENTER|wx.ALL, self.grid_span);
		self.main_sizer.Add(self.sizers[logic_type], 1, wx.ALIGN_CENTER|wx.ALL);
	
	def CreateConvertSizer(self, logic_type):
		'''
		创建Txt转Json布局
		'''
		self.sizers[logic_type] = wx.GridBagSizer(hgap=0, vgap=10);
		label1 = wx.StaticText(self.panel, -1, label=u'源文件夹：');
		label2 = wx.StaticText(self.panel, -1, label=u'目标文件夹：');
		text_input = wx.TextCtrl(self.panel,-1, size=(300,10));
		text_output = wx.TextCtrl(self.panel,-1, size=(300,10));
		bmp_open = wx.Image('app/icons/open.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap();
		btn_input = wx.BitmapButton(self.panel, -1, bmp_open);
		btn_output = wx.BitmapButton(self.panel, -1, bmp_open);
		text_console = wx.TextCtrl(self.panel, -1, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.TE_LEFT|wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_PROCESS_ENTER);
		text_console.SetMaxLength(0);
		self.sizers[logic_type].Add(label1, pos=(0,0), span=(1,1), flag=wx.LEFT|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, border=self.grid_span);
		self.sizers[logic_type].Add(text_input, pos=(0,1), span=(1,1), flag=wx.EXPAND|wx.ALL);
		self.sizers[logic_type].Add(btn_input, pos=(0,2), span=(1,1), flag=wx.RIGHT, border=self.grid_span);
		self.sizers[logic_type].Add(label2, pos=(1,0), span=(1,1), flag=wx.LEFT|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, border=self.grid_span);
		self.sizers[logic_type].Add(text_output, pos=(1,1), span=(1,1), flag=wx.EXPAND|wx.ALL);
		self.sizers[logic_type].Add(btn_output, pos=(1,2), span=(1,1), flag=wx.RIGHT, border=self.grid_span);
		self.sizers[logic_type].Add(text_console, pos=(2,0), span=(8,3), flag=wx.EXPAND|wx.ALL, border=self.grid_span);
		self.sizers[logic_type].AddGrowableRow(2);
		self.sizers[logic_type].AddGrowableCol(1);
		self.main_sizer.Add(self.sizers[logic_type], 1, wx.TOP|wx.EXPAND);
		#关联控件id
		self.controls[btn_input.GetId()] = text_input;
		self.controls[btn_output.GetId()] = text_output;
		self.Bind(wx.EVT_BUTTON, self.OnPath, btn_input);
		self.Bind(wx.EVT_BUTTON, self.OnPath, btn_output);
		self.pages[logic_type] = {};
		self.pages[logic_type]['src'] = text_input;
		self.pages[logic_type]['dest'] = text_output;
		self.pages[logic_type]['console'] = text_console;
