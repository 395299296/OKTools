#coding=utf8

'''
工具类
'''
import time;
import datetime;
import math;
import os;
import re;
import hashlib;
import hmac;
import sys;
import struct;
import wx;
import ConfigParser;

_DELTA = 0x9E3779B9;

def mkdir(path):  
	'''
	创建路径
	''' 
	path = path.strip();
	path = path.rstrip('/');
	if not os.path.exists(path):  
		os.makedirs(path);
	
def	remove_files(path, sub=None, remain=True):
	'''
	删除所有文件
	'''
	sub = sub if sub else path;
	if not os.path.exists(sub): return;
	
	if os.path.isdir(sub):
		files = os.listdir(sub);
		for item in files:
			curr = os.path.join(sub, item);
			if item.find('.svn') != -1:
				if remain: continue;
				os.chmod(curr, '777');
			if os.path.isdir(sub):
				remove_files(path, curr);
			else:
				os.remove(curr);
		if path == sub and remain: return;
		
		files = os.listdir(sub);
		if 0 < len(files):
			time.sleep(1);
		os.rmdir(sub);
	else:
		os.remove(sub);
		
def	remove_some_files(path, extname, filters=None):
	'''
	删除某一类型的文件，不遍历子目录
	'''
	if not check_path(path): return;
	
	files = os.listdir(path);
	for item in files:
		curr = os.path.join(path, item);
		if not os.path.exists(curr): continue;
		if os.path.isdir(curr): continue;
		if filters and filters.count(item) != 0: continue;
		if get_extname(item) == extname:
			os.remove(curr);
	
def	remove_some_folders(path, match):
	'''
	删除目录下指定的文件夹
	'''
	if not check_path(path): return;
	
	files = os.listdir(path);
	for item in files:
		curr = os.path.join(path, item);
		if not os.path.exists(curr): continue;
		if not os.path.isdir(curr): continue;
		if match and item.find(match) == -1: continue;
		remove_files(curr, curr);
		if not os.path.exists(curr): continue;
		os.rmdir(curr);
	
def	get_one_foldern(path, match):
	'''
	获取目录下指定的文件夹
	'''
	if not check_path(path): return;
	
	files = os.listdir(path);
	for item in files:
		curr = os.path.join(path, item);
		if not os.path.exists(curr): continue;
		if not os.path.isdir(curr):continue;
		if item.find(match) != -1: return curr;

def get_basename(filename):
	'''
	获取文件扩展名
	'''
	sufix = os.path.splitext(filename);
	return sufix[0];

def get_extname(filename):
	'''
	获取文件扩展名
	'''
	sufix = os.path.splitext(filename);
	return sufix[1];

def	get_files(root, extname=None):
	'''
	获取路径下的所有文件
	'''
	res = [];
	if not os.path.exists(root):
		print('Warning: ENOENT, no such file or directory "%s"\n'%root);
	else:
		files = os.listdir(root);
		for item in files:
			if '.svn' == item or 'Thumbs.db' == item or item.startswith('~'): continue;
			path = os.path.join(root, item)
			if not os.path.isdir(path):
				if extname and get_extname(item) != extname: continue;
				res.append(path);
			else:
				res.extend(get_files(path, extname));
	
	return res;

def copy_file(src, dest):
	if src.find(".svn") > 0:
		return;
	if not os.path.exists(src):
		return;
	if not os.path.isfile(src):
		return;

	f = open(src, 'rb');
	data = f.read();
	f.close();
	fp = open(dest, 'wb');
	fp.write(data);
	fp.close();

def log(*args, **kw):
	'''
	在控制台跟客户端输出日志
	'''
	strs = join(', ', args);
	timestamp = time.time();
	timearray = str(timestamp).split('.');
	head = '[%s+%s]'%(from_unixtime(int(timestamp)), str('000' + timearray[1])[-3:]);
	log_info = '%s %s'%(head, strs);
	if kw.has_key('console'):
		print(unicode(log_info));
		log_info += '\n';
		if None != kw['console']:
			kw['console'].AppendText(log_info.decode('utf8'));
		else:
			fp = open("log.log", 'a+');
			fp.write('\xef\xbb\xbf' + log_info);
			fp.close();
	else:
		flag = kw['flag'] if kw.has_key('flag') else wx.OK|wx.ICON_WARNING;
		dlg = wx.MessageDialog(None, strs.decode('utf8'), "MessageDialog", flag);
		result = dlg.ShowModal();
		dlg.Destroy();
		
def check_path(path):
	'''
	检查路径
	'''
	if not os.path.exists(path): return False;
	if not os.path.isdir(path): return False;
	
	return True;

def format_path(path):
	'''
	格式化路径
	'''
	return path.replace('/', '\\');
	
def trim(strs):
	'''
	去除所有空格
	'''
	if not isinstance(strs, str): return "";
	return join("", str(strs).split());

def from_unixtime(timestamp=time.time(), _format="%Y-%m-%d %H:%M:%S"):
	'''
	将时间戳转换为日期
	'''
	timearray = time.localtime(timestamp);
	datetime = time.strftime(_format, timearray);
	return datetime;

def unixtime_stamp(*args):
	'''
	将日期转换为时间戳
	'''
	args = list(args);
	for i in range(9-len(args)):
		args.append(0);
	timestamp = time.mktime(args);
	return timestamp;

def date_to_time(dt, _format="%Y-%m-%d %H:%M:%S"):
	'''
	将日期转换为时间戳
	'''
	time_arr = time.strptime(dt, _format);
	timestamp = int(time.mktime(time_arr));
	return timestamp;

def unicode_to_str(data):
	'''
	转换编码格式
	'''
	if isinstance(data, list):
		for x in range(len(data)):
			data[x] = unicode_to_str(data[x]);
	elif isinstance(data, tuple):
		new_data = [];
		for x in range(len(data)):
			new_data.append(unicode_to_str(data[x]));
		data = tuple(new_data);
	elif isinstance(data, dict):
		new_data = {};
		for key in data:
			new_data[unicode_to_str(key)] = unicode_to_str(data[key]);
		data = new_data;
	elif isinstance(data, unicode):
		data = data.encode('utf-8');
		
	return data;

def gbk_to_utf8(_str):
	'''
	中文编码转换
	'''
	try:
		return _str.decode('gbk').encode('utf8');
	except Exception, e:
		log("Error, %s, gbk to utf8... ..."%e, _str);
		return _str;
	
def str_to_int(value):
	'''
	转换字符串为整数
	'''
	if isinstance(value, unicode):
		value = value.encode('utf-8');
	if isinstance(value, str):
		value = int(value);
	elif isinstance(value, list):
		for i, item in enumerate(value):
			value[i] = str_to_int(item);
	
	return value;

def join(sep, args):
	'''
	连接字符串
	'''
	args_list = [];
	for item in args:
		if isinstance(item, str):
			args_list.append("%s"%item);
		elif isinstance(item, unicode):
			args_list.append("%s"%item.encode('utf-8'));
		else:
			args_list.append("%s"%str(item));
			
	return sep.join(args_list);

def indexOf(_list, item):
	'''
	查找元素在列表中位置
	'''
	for i, v in enumerate(_list):
		if item == v:
			return i;
	return -1;

def lastIndexOf(_list, item):
	'''
	逆向查找元素在列表中位置
	'''
	for i in range(len(_list)-1, -1, -1):
		if item == _list[i]:
			return i;
	return -1;

def md5(_str):
	'''
	获取md5校验
	'''
	result = hashlib.md5(str(_str)).hexdigest();
	return result;

def hmac_md5(_str, key):
	'''
	获取hmac-md5校验
	'''
	result = hmac.new(key);
	result.update(_str);
	result = result.hexdigest();
	return result;

def _long2str(v, w):
	n = (len(v) - 1) << 2;
	if w:
		m = v[-1];
		if (m < n - 3) or (m > n): return '';
		n = m;
	s = struct.pack('<%iL' % len(v), *v);
	return s[0:n] if w else s;

def _str2long(s, w):
	n = len(s);
	m = (4 - (n & 3) & 3) + n;
	s = s.ljust(m, "\0");
	v = list(struct.unpack('<%iL' % (m >> 2), s));
	if w: v.append(n);
	return v;

def _long2int(v):
	'''
	将长整型截取为32位整型
	'''
	return v % sys.maxint;

def _str2bytes(_str):
	r = [];
	for i in range(len(_str)):
		r.extend(_str2long(_str[i], False));
	return r;

def encrypt(_str, key):
	'''
	XXTEA加密
	'''
	if _str == '': return _str;
	v = _str2long(_str, True);
	k = _str2long(key.ljust(16, "\0"), False);
	n = len(v) - 1;
	z = v[n];
	y = v[0];
	_sum = 0;
	q = 6 + 52 // (n + 1);
	while q > 0:
		_sum = (_sum + _DELTA) & 0xffffffff;
		e = _sum >> 2 & 3;
		for p in xrange(n):
			y = v[p + 1];
			v[p] = (v[p] + ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4) ^ (_sum ^ y) + (k[p & 3 ^ e] ^ z))) & 0xffffffff;
			z = v[p];
		y = v[0];
		v[n] = (v[n] + ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4) ^ (_sum ^ y) + (k[n & 3 ^ e] ^ z))) & 0xffffffff;
		z = v[n];
		q -= 1;
	return _long2str(v, False);

def decrypt(_str, key):
	'''
	XXTEA解密
	'''
	if _str == '': return _str;
	v = _str2long(_str, False);
	k = _str2long(key.ljust(16, "\0"), False);
	n = len(v) - 1;
	z = v[n];
	y = v[0];
	q = 6 + 52 // (n + 1);
	_sum = (q * _DELTA) & 0xffffffff;
	while (_sum != 0):
		e = _sum >> 2 & 3;
		for p in xrange(n, 0, -1):
			z = v[p - 1];
			v[p] = (v[p] - ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4) ^ (_sum ^ y) + (k[p & 3 ^ e] ^ z))) & 0xffffffff;
			y = v[p];
		z = v[n];
		v[0] = (v[0] - ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4) ^ (_sum ^ y) + (k[0 & 3 ^ e] ^ z))) & 0xffffffff;
		y = v[0];
		_sum = (_sum - _DELTA) & 0xffffffff;
	return _long2str(v, True);

def parser_config(filename, section, key):
	cf = ConfigParser.ConfigParser();
	cf.read(filename);
	return unicode(cf.get(section, key));
