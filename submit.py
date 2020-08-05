#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import json
import requests
import re
import sys
import os

if os.path.exists("NOSUBMIT"):
    exit()

data = {}

with open("./data.json","r") as fd:
    data=json.load(fd)
    
conn = requests.Session()

# Login
result = conn.post('https://xxcapp.xidian.edu.cn/uc/wap/login/check',data={'username':data['_u'],'password':data['_p']})
if result.status_code != 200:
    print('认证大失败')
    exit()

# Submit
result = conn.get('https://xxcapp.xidian.edu.cn/ncov/wap/default/index')
if result.status_code != 200:
    print('获取页面大失败')
    exit()

if os.path.exists("last_get.html"):
    os.rename("last_get.html","last_get.html.1")

with open("last_get.html","w") as fd:
    fd.write(result.text)

# TODO: diff those two files to determine whether submission form has been updated, then delay the submission when necessary

predef = json.loads(re.search('var def = ({.*});',result.text).group(1))

if "dump_geo" in sys.argv:
    print(predef['geo_api_info'])
    exit()

try:
    del predef['jrdqtlqk']
    del predef['jrdqjcqk']
except:
    pass
del data['_u']
del data['_p']
predef.update(data)

result = conn.post('https://xxcapp.xidian.edu.cn/ncov/wap/default/save',data=predef)
print(result.text)
