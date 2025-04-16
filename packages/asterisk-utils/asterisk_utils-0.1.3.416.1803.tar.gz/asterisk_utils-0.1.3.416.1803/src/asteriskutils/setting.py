import json
import os
from asteriskutils.tools import wprint,error_print

if  __name__ == "__main__":
    import sys
    error_print('本段代码必须从应用主入口导入执行。退出！')
    sys.exit(1)

'''
AppConfig的默认配置，当AppConfig.json文件缺失时使用

'''
AppConfig = {
    "version":"0.1.0",
    "author":"Asterisk Dev Team",
    "email":"geoshan@163.com",
    "debug": 1,
    "prompt":"Asterisk-utils > ",
    "log":{
        "log_level":"DEBUG",
        "log_path":"{App}/log",
        "log_file_name":"%Y-%m-%d",
        "log_format":"%(asctime)s - %(levelname)s - %(message)s"
    },
    "logo_text_file":"logo.attpl",
    "title_text_file":"title.attpl",
    "errors":{
        "404":"服务器接口不存在 ，请请确认服务器配置后再试。",
        "500":"服务器接口不存在 ，或者http api的方法不支持",
        "504":"ConnectTimeout -- 请稍后再试",
        "501":"服务器可能未启动 ，请稍后再试。",
        "502":"无法连接服务器 ，请稍后再试。",
        "503":"ChunkedEncodingError -- 请稍后再试",
        "509":"Unfortunately -- 请稍后再试"
    }
}
# 读取系统默认参数，主要为：version、debug、log等
try:
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'asterisk.json'),'r',encoding='utf8') as fp:
        AppConfig = json.load(fp)
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'title.attpl'),"r",encoding='utf8') as fp:
        AppConfig['title_text'] = fp.read()
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logo.attpl'),"r",encoding='utf8') as fp:
        AppConfig['logo_text'] = fp.read()
    
except FileNotFoundError:
    wprint('当前目录下的配置文件asterisk.json不存在，启用默认配置。')

