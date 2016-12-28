#coding:utf8
from gfirefly.utils.singleton import Singleton;
import util;
import json;

class Config:
	'''配置管理类
	'''
	
	__metaclass__ = Singleton;
	
	def __init__(self):
		self._json_obj = None;
		self._output = None;
	
	def get_json_obj(self, file=None):
		'''
		获取配置json对象
		'''
		if None == file:
			file = "config.json";
		if None == self._json_obj:
			self._json_obj = util.unicode_to_str(json.load(open(file,'r')))
		return self._json_obj;

	def get_path_output(self):
		'''
		获取输出路径
		'''
		if None == self._rech_port:
			config = self.get_json_obj();
			sersconf = config.get('servers',{});
			rechconf = sersconf.get('recharge', {});
			self._rech_port = str(rechconf.get('webport'));
		return self._rech_port;