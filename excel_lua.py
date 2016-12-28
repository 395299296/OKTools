#coding:utf8
'''
Created on 2016年7月6日

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
        args = sys.argv;
        if len(args) >= 2:
            if args[1] == 'trunk':
                src = src.replace('{0}', 'trunk');
                dest = dest.replace('{0}', 'trunk');
            else:
                src = src.replace('{0}', 'branches/' + args[1]);
                dest = dest.replace('{0}', 'branches/' + args[1]);
        pre = util.parser_config(config, 'path', 'prefix');
        post = util.parser_config(config, 'path', 'postfix');
        among = util.parser_config(config, 'path', 'among');
        filters = util.parser_config(config, 'path', 'filter');
        filters = filters.split(',');
        cleardir = util.parser_config(config, 'path', 'cleardir');
        if int(cleardir) == 1:
            util.remove_some_files(dest, '.lua');
        formatConvert = FormatConvert(src, dest, None);
        formatConvert.excel_to_lua(pre, post, among, filters);
        
    except Exception, e:
        util.log("Error, %s, config: %s" % (e, config), console=None);