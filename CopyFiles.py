#coding:utf8
'''
Created on 2015年4月16日

@author: zhangjianbin
'''
from app.format import FormatConvert;
from app.common import util;
import sys, os;

sys=sys;
code=sys.getdefaultencoding();
if code != "utf-8":
    reload(sys);
    sys.setdefaultencoding("utf-8");

if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        config = os.path.abspath('.') + '/conf/config.conf';
    else:
        config = os.path.abspath('.') + '/' + args[1];
    try:
        src = util.parser_config(config, 'path', 'srcFolder');
        dest = util.parser_config(config, 'path', 'destFolder');
        if len(args) > 2:
            if args[2] == 'trunk':
                src = src.replace('{0}', 'trunk');
                dest = dest.replace('{0}', 'trunk');
            else:
                src = src.replace('{0}', 'branches/' + args[2]);
                dest = dest.replace('{0}', 'branches/' + args[2]);
        ext = util.parser_config(config, 'path', 'extname');
        pre = util.parser_config(config, 'path', 'prefix');
        post = util.parser_config(config, 'path', 'postfix');
        among = util.parser_config(config, 'path', 'among');
        filter = util.parser_config(config, 'path', 'filter');
        keepdir = util.parser_config(config, 'path', 'keepdir');
    except Exception, e:
        util.log("Error, %s, config: %s" % (e, config), console=None);
        os._exit();
        
    src = util.format_path(os.path.abspath('.') + '/' + src);
    dest = util.format_path(os.path.abspath('.') + '/' + dest);
    formatConvert = FormatConvert(src, dest, None);
    formatConvert.copy_files(pre, post, among, filter, keepdir, ext);
    