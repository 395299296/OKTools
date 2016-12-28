#coding:utf8

import os, json;
import xdrlib,sys;
import xlrd;
import types;
import time;
import datetime;
from app.common import util;

class FormatConvert(object):
	'''
	格式转换类
	'''
	
	def __init__(self, src, dest, console):
		self._src = src; #源文件夹
		self._dest = dest; #目标文件夹
		self._console = console; #控制台控件
		self.init();
	
	def init(self):
		'''
		初始化
		'''
		#util.remove_files(self._dest);
	
	def txt_to_json(self, _type=True):
		'''
		txt转换为json文件
		'''
		self.files = util.get_files(self._src, '.txt');
		for item in self.files:
			f = open(item, 'r');
			lines = f.readlines();
			head_arr = [];
			type_arr = [];
			res_arr = [];
			for i, line in enumerate(lines):
				line = line.strip('\n');
				if 0 == i: #表头
					head_arr = line.replace('\xef\xbb\xbf', '').split('\t');
					continue;
				if 1 == i and _type:
					type_arr = line.split('\t');
					continue;
				tmp_arr = [];
				sub_arr = line.split('\t');
				for j, _str in enumerate(sub_arr):
					if j >= len(head_arr): continue;
					value = _str.decode('utf8');
					if j < len(type_arr):
						value = str(self.str_to_type(value, type_arr[j]));
					tmp_arr.append('"%s": %s'%(head_arr[j], value)); 
				res_arr.append('{%s}'%util.join(', ', tmp_arr));
			f.close();
			self.write_data(item, '[\n%s\n]'%util.join(',\n', res_arr), '.json');
			
		return 'ok';
			
	def str_to_type(self, value, _type):
		'''
		将字符串自动转换成对应的类型
		'''
		if 'int' == _type: return int(value);
		if 'float' == _type: return float(value);
		if 'string' == _type: return '"%s"'%str(value);
		return value;
	
	def open_excel(self, _file):
		'''
		读取Excel文件
		'''
		try:
			data = xlrd.open_workbook(_file);
			return data;
		except Exception, e:
			util.log('Error, %s, open excel "%s"'%(e, _file), console=self._console);
		
	def excel_table_byindex(self, _file, header=[], colnameindex=0, by_index=0):
		'''
		根据索引获取Excel表格中的数据
		@param _file：Excel文件路径
		@param header:表头字段名
		@param colnameindex：表头列名所在行的索引
		@param by_index：表的索引
		'''
		data = self.open_excel(_file);
		if None == data: return;
		
		table = data.sheets()[by_index];
		nrows = table.nrows; #行数
		ncols = table.ncols; #列数
		colnames = table.row_values(colnameindex); #某一行数据
		for i in range(len(colnames)): #遍历表头
			header.append(colnames[i]);
		res_arr = [];
		for rownum in range(1, nrows): #遍历每一行
			row = table.row_values(rownum);
			if row:
				app = {};
				for i in range(len(colnames)): #遍历每一列
					app[colnames[i]] = row[i];
				res_arr.append(app);
		return res_arr;
	
	def excel_table_byname(self, _file, colnameindex=0, by_name=u'Sheet1'):
		'''
		根据名称获取Excel表格中的数据 
		@param _file：Excel文件路径
		@param colnameindex：表头列名所在行的索引
		@param by_name：Sheet1名称
		'''
		data = self.open_excel(_file);
		if None == data: return;
		
		table = data.sheet_by_name(by_name);
		nrows = table.nrows; #行数 
		colnames = table.row_values(colnameindex); #某一行数据 
		res_arr = [];
		for rownum in range(1, nrows): #遍历每一行
			row = table.row_values(rownum);
			if row:
				app = {};
				for i in range(len(colnames)): #遍历每一列
					app[colnames[i]] = row[i];
				res_arr.append(app);
		return res_arr;
	
	def excel_to_txt(self, _pre=None, _post=None, _among=None, _filter=None, filelist=None):
		'''
		excel转换为txt文件
		'''
		self.files = util.get_files(self._src, '.xlsx');
		self.files.extend(util.get_files(self._src, '.xls'));
		for item in self.files:
			filename = os.path.basename(item);
			basename = util.get_basename(filename);
			if filelist != None:
				filelist.append(util.get_basename(filename));
			if '' != _pre:
				if basename.find(_pre) != 0:
					continue;
			if '' != _post:
				if basename.rfind(_post) != len(basename) - len(_post):
					continue;
			if '' != _among:
				if basename.find(_among) == -1:
					continue;
			if '' != _filter:
				if item.find(_filter) != -1:
					continue;
			header = [];
			res_arr = [];
			tables = self.excel_table_byindex(item, header);
			if None == tables: continue;
			real_header = [];
			for key in header:
				if '' != key and '#' != key[0]:
					real_header.append(key);
			res_arr.append(util.join('\t', real_header));
			for row in tables:
				row_arr = [];
				for key in real_header:
					if row.has_key(key):
						if type(row[key]) is types.FloatType and row[key] == int(row[key]):
							row[key] = int(row[key]);
						if type(row[key]) is types.IntType or type(row[key]) is types.FloatType:
							row[key] = unicode(row[key]);
						row_arr.append(row[key]);
				res_arr.append(util.join('\t', row_arr));
			self.write_data(item, util.join('\n', res_arr), '.txt');
			
		return 'ok';
	
	def excel_to_csv(self):
		'''
		excel转换为csv文件
		'''
		self.files = util.get_files(self._src, '.xlsx');
		for item in self.files:
			header = [];
			res_arr = [];
			tables = self.excel_table_byindex(item, header);
			if None == tables: continue;
			res_arr.append(util.join(',', header));
			for row in tables:
				row_arr = [];
				for key in header:
					if row.has_key(key):
						if type(row[key]) is types.FloatType and row[key] == int(row[key]):
							row[key] = int(row[key]);
						if type(row[key]) is types.IntType or type(row[key]) is types.FloatType:
							row[key] = unicode(row[key]);
						row_arr.append(row[key]);
				res_arr.append(util.join(',', row_arr));
			self.write_data(item, util.join('\n', res_arr), '.csv');
			
		return 'ok';
	
	def excel_to_json(self):
		'''
		excel转换为json文件
		'''
		self.files = util.get_files(self._src, '.xlsx');
		self.files.extend(util.get_files(self._src, '.xls'));
		for item in self.files:
			basename = os.path.basename(item);
			header = [];
			res_arr = [];
			tables = self.excel_table_byindex(item, header);
			if None == tables: continue;
			real_header = [];
			for key in header:
				if '' != key and '#' != key[0]:
					real_header.append(key);
			for row in tables:
				row_arr = [];
				for key in real_header:
					if row.has_key(key):
						if type(row[key]) is types.FloatType and row[key] == int(row[key]):
							row[key] = int(row[key]);
						if type(row[key]) is types.IntType or type(row[key]) is types.FloatType:
							row[key] = unicode(row[key]);
						else:
							row[key] = '"%s"'%unicode(row[key]);
						row_arr.append('"%s": %s'%(key, row[key]));
				res_arr.append('{%s}'%util.join(', ', row_arr));
			self.write_data(item, '[\n%s\n]'%util.join(',\n', res_arr), '.json', True);
			
		return 'ok';
	
	def excel_to_lua(self, _pre=None, _post=None, _among=None, _filter=None, filelist=None):
		'''
		excel转换为lua文件
		'''
		self.files = util.get_files(self._src, '.xlsx');
		self.files.extend(util.get_files(self._src, '.xls'));
		for item in self.files:
			filename = os.path.basename(item);
			basename = util.get_basename(filename);
			if filelist != None:
				filelist.append(util.get_basename(filename));
			if '' != _pre:
				if basename.find(_pre) != 0:
					continue;
			if '' != _post:
				if basename.rfind(_post) != len(basename) - len(_post):
					continue;
			if '' != _among:
				if basename.find(_among) == -1:
					continue;
			if None != _filter:
				if util.indexOf(_filter, basename) != -1:
					continue;
			header = [];
			res_arr = [];
			tables = self.excel_table_byindex(item, header);
			if None == tables: continue;
			real_header = [];
			type_map = {};
			for key in header:
				if '' != key and '#' != key[0]:
					real_header.append(key);
					type_map[key] = tables[0][key];
			res_arr.append('cc.exports.' + basename + 'ConfigData = {');
			for i in range(1, len(tables)):
				row_arr = [];
				row_arr.append('\t{');
				row = tables[i];
				for key in real_header:
					if row.has_key(key):
						row[key] = unicode(str(self.str_to_type(row[key], type_map[key])));
						row_arr.append('\t\t' + key + ' = ' + row[key] + ',');
				row_arr.append('\t},');
				res_arr.append(util.join('\n', row_arr));
			res_arr.append('}');
			self.write_data(item, util.join('\n', res_arr), 'ConfigData.lua', True);
			
		return 'ok';
		
	def excel_to_xml(self, _pre=None, _post=None, _among=None, _filter=None, filelist=None):
		'''
		excel转换为xml文件
		'''
		self.files = util.get_files(self._src, '.xlsx');
		self.files.extend(util.get_files(self._src, '.xls'));
		for item in self.files:
			filename = os.path.basename(item);
			basename = util.get_basename(filename);
			if filelist != None:
				filelist.append(util.get_basename(filename));
			if '' != _pre:
				if basename.find(_pre) != 0:
					continue;
			if '' != _post:
				if basename.rfind(_post) != len(basename) - len(_post):
					continue;
			if '' != _among:
				if basename.find(_among) == -1:
					continue;
			if '' != _filter:
				if item.find(_filter) != -1:
					continue;
			header = [];
			res_arr = [];
			tables = self.excel_table_byindex(item, header);
			if None == tables: continue;
			real_header = [];
			type_map = {};
			for key in header:
				if '' != key and '#' != key[0]:
					real_header.append(key);
					type_map[key] = tables[0][key];
			res_arr.append('<?xml version="1.0" encoding="utf8"?>');
			res_arr.append('<config>');
			for i in range(1, len(tables)):
				row_arr = [];
				row = tables[i];
				for key in real_header:
					if row.has_key(key):
						if type(row[key]) is types.FloatType and row[key] == int(row[key]):
							row[key] = int(row[key]);
						if type(row[key]) is types.IntType or type(row[key]) is types.FloatType:
							row[key] = unicode(row[key]);
						row_arr.append(key + '="' + row[key] + '"');
				res_arr.append('\t<' + basename + ' ' + util.join(' ', row_arr) + ' />');
			res_arr.append('</config>');
			self.write_data(item, util.join('\n', res_arr), '.xml');
			
		return 'ok';

	def excel_dy(self, _startDate, _endDate, _checkIn, _lunchHour, _afternoon, _checkOut, _overtime, _dutyCheckIn, _dutyTime, _holidays, _weekend):
		'''
		excel考勤表处理
		'''
		self.files = util.get_files(self._src, '.xlsx');
		self.files.extend(util.get_files(self._src, '.xls'));
		out_header = ['人员编号', '姓名', '迟到次数', '迟到日期', '早退次数', '早退日期', '加班次数', '加班日期', '周末加班次数', '周末加班日期', '值班次数', '值班日期', '上班未打卡次数', '上班未打卡日期', '下班未打卡次数', '下班未打卡日期', '旷工次数', '旷工日期'];
		holidays = _holidays.split(',');
		weekend = _weekend.split(',');
		for item in self.files:
			filename = os.path.basename(item);
			basename = util.get_basename(filename);
			header = [];
			tables = self.excel_table_byindex(item, header);
			if None == tables: continue;
			res_arr = [];
			res_arr.append(util.join(',', out_header));
			staff_dict = {};
			for row in tables:
				uid = str(row[unicode('人员编号')]);
				if not staff_dict.has_key(uid):
					staff_dict[uid] = [];
				staff_dict[uid].append(row);
			attendance_info = [];
			d1 = datetime.datetime.strptime(_startDate, '%Y-%m-%d');
			d2 = datetime.datetime.strptime(_endDate, '%Y-%m-%d');
			delta = d2 - d1;
			keys = staff_dict.keys();
			keys.sort();
			for x in xrange(0, len(keys)):
				value = staff_dict[keys[x]];
				#if value[0][unicode('姓名')] != unicode('张建斌1'): continue
				uncheckInTimes = [];
				uncheckOutTimes = [];
				lateTimes = [];
				earlyTimes = [];
				overTimes = [];
				dutyTimes = [];
				weekendTimes = [];
				absentTimes = [];
				for i in range(0, delta.days):
					date = d1 + datetime.timedelta(days=i);
					date = date.strftime('%Y-%m-%d');
					checkIn = self.early_datetime(date, value);
					checkOut = self.last_datetime(date, value);
					if util.indexOf(holidays, date) != -1:
						if checkIn != None:
							dutyTimes.append(date);
						continue;
					if util.indexOf(weekend, date) != -1:
						if checkIn != None and checkOut != None:
							t1 = datetime.datetime.strptime(checkIn, '%H:%M');
							t2 = t1 + datetime.timedelta(hours=int(_dutyTime));
							if t2.strftime('%H:%M') <= checkOut:
								weekendTimes.append(date);
						continue;
					if checkIn != None and checkIn > _checkIn and checkIn < _lunchHour:
						lateTimes.append(date);
					if checkOut != None and checkOut < _checkOut and checkOut >= _afternoon:
						earlyTimes.append(date);
					elif checkOut != None and checkOut >= _overtime:
						overTimes.append(date);
					if checkIn == None and checkOut == None:
						absentTimes.append(date);
					elif checkIn == None or checkIn >= _lunchHour:
						uncheckInTimes.append(date);
					elif checkOut == None or checkOut < _afternoon:
						uncheckOutTimes.append(date);

				row_arr = [];
				row_arr.append(keys[x]);
				row_arr.append(value[0][unicode('姓名')]);
				row_arr.append(len(lateTimes));
				row_arr.append('|'.join(lateTimes));
				row_arr.append(len(earlyTimes));
				row_arr.append('|'.join(earlyTimes));
				row_arr.append(len(overTimes));
				row_arr.append('|'.join(overTimes));
				row_arr.append(len(weekendTimes));
				row_arr.append('|'.join(weekendTimes));
				row_arr.append(len(dutyTimes));
				row_arr.append('|'.join(dutyTimes));
				row_arr.append(len(uncheckInTimes));
				row_arr.append('|'.join(uncheckInTimes));
				row_arr.append(len(uncheckOutTimes));
				row_arr.append('|'.join(uncheckOutTimes));
				row_arr.append(len(absentTimes));
				row_arr.append('|'.join(absentTimes));

				res_arr.append(util.join(',', row_arr));

			self.write_data(item, util.join('\n', res_arr), '.csv');
			
		return 'ok';

	def early_datetime(self, _date, _list):
		'''
		最早打卡时间
		'''
		result = None;
		for item in _list:
			if item[unicode('刷卡日期')] == _date:
				if result == None or item[unicode('刷卡时间')] < result:
					result = item[unicode('刷卡时间')];
		return result;

	def last_datetime(self, _date, _list):
		'''
		最晚打卡时间
		'''
		result = None;
		for item in _list:
			if item[unicode('刷卡日期')] == _date:
				if result == None or item[unicode('刷卡时间')] > result:
					result = item[unicode('刷卡时间')];
		return result;

	def checkInOnTime(self, _checkTime, _limitTime):
		'''
		是否按时上班
		'''
		if _checkTime != None and _checkTime <= _limitTime:
			return True;

		return False;

	def checkOutOnTime(self, _checkTime, _limitTime):
		'''
		是否按时下班
		'''
		if _checkTime != None and _checkTime >= _limitTime:
			return True;

		return False;
	
	def merge_json(self, _match, _filter, _id, _outfile):
		'''
		合并所给的所有json文件为一个json文件
		'''
		self.files = util.get_files(self._src, '.json');
		values = [];
		for item in self.files:
			if item.find(_match) == -1 or item.find(_filter) != -1:
				continue;
			try:
				f = open(item, 'r');
				data_string = f.read();
				f.close();
				decoded = json.loads(data_string);
			except Exception, e:
				util.log("Error, %s, read file: %s" % (e, item), console=None);
				continue;
			for each in decoded:
				if not each.has_key(_id):
					continue;
				values.append(each);
		self.write_data(_outfile, json.dumps(values), '.json');
			
		return 'ok';
	
	def copy_files(self, _pre, _post, _among, _filter, _keepdir, _ext):
		'''
		拷贝将满足条件的文件
		'''
		self.files = util.get_files(self._src, _ext);
		for item in self.files:
			filename = os.path.basename(item);
			basename = util.get_basename(filename);
			if '' != _pre:
				if basename.find(_pre) != 0:
					continue;
			if '' != _post:
				if basename.rfind(_post) != len(basename) - len(_post):
					continue;
			if '' != _among:
				if basename.find(_among) == -1:
					continue;
			if '' != _filter:
				if item.find(_filter) != -1:
					continue;
			if int(_keepdir) == 0:
				outfile = self._dest + '/' + filename;
			else:
				outfile = item.replace(self._src, self._dest);
			
			outfile = os.path.normpath(util.format_path(outfile));
			util.mkdir(os.path.dirname(outfile));
			util.copy_file(item, outfile);
			util.log('File successfully copied : ' + outfile, console=self._console);
			
		return 'ok';
	
	def write_data(self, filename, strs, extname, nobom=False):
		'''
		将数据写入到目标文件
		'''
		util.mkdir(self._dest);
		basename = os.path.basename(filename);
		file_out = os.path.normpath(os.path.join(self._dest, util.get_basename(basename) + extname));
		fp = open(file_out, 'w');
		if not nobom:
			strs = '\xef\xbb\xbf' + strs;
		fp.write(strs);
		fp.close();
		util.log('File successfully converted : ' + file_out, console=self._console);

	def write_xls(self, filename, header, data):
		'''
		将数据写入xls
		'''
		util.mkdir(self._dest);
		file_out = os.path.normpath(os.path.join(self._dest, filename));
		book = xlwt.Workbook(encoding='utf-8',style_compression=0);
		sheet = book.add_sheet('data', cell_overwrite_ok=True);
		for x in xrange(0,len(header)):
			sheet.write(0, x, header[x].decode('gbk'));
		for i in xrange(0, len(data)):
			for j in xrange(0,len(header)):
				sheet.write(i, j, data[i][header[j]].decode('gbk'));
		book.save(file_out);