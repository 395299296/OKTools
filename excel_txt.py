#coding:utf8
'''
Created on 2014年12月27日

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
        filter = util.parser_config(config, 'path', 'filter');
        cleardir = util.parser_config(config, 'path', 'cleardir');
        if int(cleardir) == 1:
            util.remove_some_files(dest, '.txt', ['files.txt']);
        formatConvert = FormatConvert(src, dest, None);
        filelist = [];
        formatConvert.excel_to_txt(pre, post, among, filter, filelist);
        filelist.sort();
        fp = codecs.open(dest + '/files.txt', 'w', "utf-8");
        fp.write(util.join('\n', filelist).encode('utf-8'));
        fp.close();
    except Exception, e:
        util.log("Error, %s, config: %s" % (e, config), console=None);