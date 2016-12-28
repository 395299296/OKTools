#coding:utf8
'''
Created on 2016年10月30日

@author: zhangjianbin
'''
from app.format import FormatConvert;
from app.common import util;
import sys, os, codecs;

sys=sys;
code=sys.getdefaultencoding();
if code != "utf-8":
    reload(sys);
    sys.setdefaultencoding("utf-8");

if __name__ == '__main__':
    config = os.path.abspath('.') + '/conf/config.conf';
    try:
        src = util.parser_config(config, 'path', 'srcFolder');
        dest = util.parser_config(config, 'path', 'destFolder');
        src = os.path.abspath('.') + '/' + src;
        dest = os.path.abspath('.') + '/' + dest;
        checkIn = util.parser_config(config, 'path', 'checkIn');
        lunchHour = util.parser_config(config, 'path', 'lunchHour');
        afternoon = util.parser_config(config, 'path', 'afternoon');
        checkOut = util.parser_config(config, 'path', 'checkOut');
        overtime = util.parser_config(config, 'path', 'overtime');
        dutyCheckIn = util.parser_config(config, 'path', 'dutyCheckIn');
        dutyTime = util.parser_config(config, 'path', 'dutyTime'); 
        startDate = util.parser_config(config, 'path', 'startDate');
        endDate = util.parser_config(config, 'path', 'endDate');
        holidays = util.parser_config(config, 'path', 'holidays');
        weekend = util.parser_config(config, 'path', 'weekend');

        formatConvert = FormatConvert(src, dest, None);
        formatConvert.excel_dy(startDate, endDate, checkIn, lunchHour, afternoon, checkOut, overtime, dutyCheckIn, dutyTime, holidays, weekend);
        
    except Exception, e:
        util.log("Error, %s, config: %s" % (e, config), console=None);